#!/usr/bin/env python3
"""
evidence_to_oscal_ar.py
Wandelt Kyverno PolicyReports und manuelle/skriptbasierte Checks in ein
OSCAL Assessment-Results-Dokument (OSCAL 1.2.x) um.

Aufruf:
  ./evidence_to_oscal_ar.py \
      --compdef component-definitions/k8s-security-stack/component-definition.json \
      --ssp     system-security-plans/ssp-workload/system-security-plan.json \
      --ssp-href trestle://system-security-plans/ssp-workload/system-security-plan.json \
      --polr    evidence/policyreports.json \
      --cpolr   evidence/clusterpolicyreports.json \
      --checks  evidence/manual-checks.json \
      --out     assessment-results/k8s-ar/assessment-results.json
"""
import argparse, json, uuid, datetime, sys, os

TRESTLE_NS = "https://oscal-compass.github.io/compliance-trestle/schemas/oscal/cd"
LAB_NS = "https://cyberlab.local/ns/oscal"


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def det_uuid(*parts):
    """Deterministische UUIDs -> stabile Diffs zwischen zwei Assessment-Laeufen."""
    return str(uuid.uuid5(uuid.NAMESPACE_URL, "oscal-lab:" + "|".join(str(p) for p in parts)))


def load_compdef(path):
    """Liefert rules{rule_id->info}, check2rule{check_id->rule_id}, ctrl2rules{(comp,ctrl)->[rule]}"""
    cd = json.load(open(path))["component-definition"]
    rules, check2rule, ctrl2rules, comps = {}, {}, {}, {}
    for c in cd["components"]:
        comps[c["title"]] = {"uuid": c["uuid"], "type": c["type"], "title": c["title"]}
        cur = {}
        for p in c.get("props", []):
            rem = p.get("remarks")
            cur.setdefault(rem, {})[p["name"]] = p["value"]
        for _, r in cur.items():
            rid = r.get("Rule_Id")
            if not rid:
                continue
            rules[rid] = {"component": c["title"], "desc": r.get("Rule_Description", ""),
                          "check": r.get("Check_Id"), "check_desc": r.get("Check_Description", "")}
            if r.get("Check_Id"):
                check2rule[r["Check_Id"]] = rid
        for ci in c.get("control-implementations", []):
            for ir in ci.get("implemented-requirements", []):
                rs = [p["value"] for p in ir.get("props", []) if p["name"] == "Rule_Id"]
                ctrl2rules.setdefault((c["title"], ir["control-id"]), []).extend(rs)
    return rules, check2rule, ctrl2rules, comps


def norm_polr(polr_files):
    """kubectl get polr/cpolr -o json -> flache Check-Ergebnisse."""
    out = []
    for f in polr_files:
        if not f or not os.path.exists(f):
            continue
        origin = f
        doc = json.load(open(f))
        for item in doc.get("items", [doc]):
            ns = item.get("metadata", {}).get("namespace", "")
            for res in item.get("results", []):
                for sub in res.get("resources", [{}]) or [{}]:
                    out.append({
                        "check_id": res.get("policy"),
                        "rule": res.get("rule"),
                        "result": res.get("result"),          # pass | fail | warn | error | skip
                        "message": res.get("message", ""),
                        "subject": "/".join(x for x in [ns, sub.get("kind", ""), sub.get("name", "")] if x),
                        "subject_uid": sub.get("uid", ""),
                        "source": item.get("metadata", {}).get("name", "policyreport"),
                        "origin": origin,
                        "timestamp": res.get("timestamp") or now(),
                        "method": "TEST",
                    })
    return out


def norm_checks(path):
    """Eigenes, schlankes Evidenzformat fuer Nicht-Kyverno-Checks."""
    if not path or not os.path.exists(path):
        return []
    out = []
    for c in json.load(open(path)):
        c.setdefault("method", "EXAMINE")
        c.setdefault("timestamp", now())
        c["origin"] = path
        out.append(c)
    return out


def to_ts(v):
    """Kyverno-Timestamps koennen {seconds,nanos} sein."""
    if isinstance(v, dict) and "seconds" in v:
        return datetime.datetime.fromtimestamp(int(v["seconds"]), datetime.timezone.utc)\
                .isoformat(timespec="seconds").replace("+00:00", "Z")
    return v


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--compdef", required=True)
    ap.add_argument("--ssp", required=True)
    ap.add_argument("--ssp-href", required=True)
    ap.add_argument("--polr"); ap.add_argument("--cpolr"); ap.add_argument("--checks")
    ap.add_argument("--title", default="Assessment Results - Kubernetes Workload Baseline (EVE-NG Lab)")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    rules, check2rule, ctrl2rules, comps = load_compdef(a.compdef)
    ssp = json.load(open(a.ssp))["system-security-plan"]
    ssp_controls = [ir["control-id"] for ir in ssp["control-implementation"]["implemented-requirements"]]

    evidence = norm_polr([a.polr, a.cpolr]) + norm_checks(a.checks)

    observations, rule_state = [], {}
    seen_evidence = {}
    dup_count = 0
    for e in evidence:
        rid = check2rule.get(e["check_id"])
        if rid is None:
            print(f"WARN: check '{e['check_id']}' ist keiner Rule_Id zugeordnet - uebersprungen", file=sys.stderr)
            continue
        ts = to_ts(e["timestamp"])
        # Ohne Cluster-Cleanup zwischen Testlaeufen meldet Kyverno dieselbe Regel/Resource
        # oft mehrfach identisch (Admission- + Background-Scan, oder Reste alter
        # PolicyReport-Objekte aus frueheren rollout restarts). Das ist keine zusaetzliche
        # Evidenz, sondern dieselbe Tatsache erneut gemeldet - inhaltlich identische
        # Eintraege werden zu einer Observation zusammengefasst statt dupliziert.
        dedup_key = (rid, e["subject"], ts, e["result"], e["message"])
        if dedup_key in seen_evidence:
            dup_count += 1
            continue
        seen_evidence[dedup_key] = True
        # Hash schliesst result/message mit ein: selbst wenn zwei wirklich
        # unterschiedliche Befunde zufaellig dieselbe (rid, subject, ts) haben,
        # duerfen sie nie dieselbe Observation-UUID bekommen (trestle: Duplicate detected).
        obs_uuid = det_uuid("obs", rid, e["subject"], ts, e["result"], e["message"])
        observations.append({
            "uuid": obs_uuid,
            "title": f"{rid} :: {e['subject'] or 'cluster'}",
            "description": rules[rid]["check_desc"] or rules[rid]["desc"],
            "props": [
                {"name": "Rule_Id", "ns": TRESTLE_NS, "value": rid},
                {"name": "Check_Id", "ns": TRESTLE_NS, "value": e["check_id"]},
                {"name": "result", "ns": LAB_NS, "value": e["result"]},
                {"name": "assessment-source", "ns": LAB_NS, "value": e["source"]},
            ],
            "methods": [e["method"]],
            "types": ["control-objective"],
            # subject-uuid wird pro Observation neu abgeleitet (nicht nur aus dem
            # Subject-Text): mehrere Policies pruefen oft denselben Pod, und eine
            # wiederverwendete UUID gilt trestle als Duplikat, nicht als Verweis.
            "subjects": [{"subject-uuid": det_uuid("subj", obs_uuid), "type": "component",
                          "title": e["subject"] or "cluster",
                          "props": [{"name": "resource", "ns": LAB_NS, "value": e["subject"] or "cluster"}]}],
            "relevant-evidence": [{"href": "file://" + os.path.abspath(e["origin"]),
                                   "description": e["message"] or "Rohdaten des Checks"}],
            "collected": ts,
        })
        st = rule_state.setdefault(rid, {"pass": 0, "fail": 0, "obs": [], "msgs": []})
        st["obs"].append(obs_uuid)
        if e["result"] in ("fail", "error"):
            st["fail"] += 1
            if e["message"]:
                st["msgs"].append(f"{e['subject']}: {e['message']}")
        elif e["result"] == "pass":
            st["pass"] += 1

    if dup_count:
        print(f"INFO: {dup_count} inhaltlich identische Evidenz-Eintraege zusammengefasst "
              f"(vermutlich kein Cluster-Cleanup zwischen Testlaeufen)", file=sys.stderr)

    findings, risks = [], []
    for (comp_title, ctrl), rlist in sorted(ctrl2rules.items()):
        if ctrl not in ssp_controls:
            continue
        rlist = sorted(set(rlist))
        covered = [r for r in rlist if r in rule_state]
        if not covered:
            state, txt = "not-satisfied", "Keine Evidenz erhoben (Control nicht abgedeckt)."
        else:
            failed = [r for r in covered if rule_state[r]["fail"] > 0]
            state = "not-satisfied" if failed else "satisfied"
            txt = ("Fehlgeschlagene Rules: " + ", ".join(failed)) if failed else \
                  ("Alle Rules bestanden: " + ", ".join(covered))
        f_uuid = det_uuid("finding", comp_title, ctrl)
        obs_ids = [o for r in covered for o in rule_state[r]["obs"]]
        finding = {
            "uuid": f_uuid,
            "title": f"{ctrl} :: {comp_title}",
            "description": txt,
            "props": [{"name": "assessed-component", "ns": LAB_NS, "value": comp_title}],
            "target": {"type": "objective-id", "target-id": f"{ctrl}_obj",
                       "description": f"Assessment Objective zu {ctrl.upper()}",
                       "props": [{"name": "control-id", "ns": LAB_NS, "value": ctrl}],
                       "status": {"state": state}},
        }
        # OSCAL erlaubt related-observations nur mit mindestens 1 Eintrag - eine
        # leere Liste (Control ganz ohne Evidenz) ist ein Schemafehler, das Feld
        # muss dann komplett entfallen statt leer mitgeschickt zu werden.
        if obs_ids:
            finding["related-observations"] = [{"observation-uuid": o} for o in obs_ids]
        if state == "not-satisfied":
            r_uuid = det_uuid("risk", comp_title, ctrl)
            finding["related-risks"] = [{"risk-uuid": r_uuid}]
            detail = "; ".join(m for r in covered for m in rule_state[r]["msgs"][:3]) or txt
            risk = {
                "uuid": r_uuid,
                "title": f"Control {ctrl.upper()} nicht erfuellt ({comp_title})",
                "description": detail,
                "statement": f"Die Umsetzung von {ctrl.upper()} durch {comp_title} wurde als nicht wirksam bewertet.",
                "props": [{"name": "severity", "ns": LAB_NS, "value": "high" if ctrl in ("ac-6", "cm-14", "sc-39", "si-7") else "moderate"}],
                "status": "open",
            }
            if obs_ids:
                risk["related-observations"] = [{"observation-uuid": o} for o in obs_ids]
            risks.append(risk)
        findings.append(finding)

    total = len(findings)
    ok = sum(1 for f in findings if f["target"]["status"]["state"] == "satisfied")
    ar = {"assessment-results": {
        "uuid": det_uuid("ar", a.ssp_href, now()),          # je Lauf eindeutig
        "metadata": {"title": a.title, "last-modified": now(), "version": now(),
                     "oscal-version": "1.2.2",
                     "roles": [{"id": "assessor", "title": "Automated Assessor (CI)"}],
                     "parties": [{"uuid": det_uuid("party", "lab-audit"), "type": "organization",
                                  "name": "Lab Audit Team"}],
                     "responsible-parties": [{"role-id": "assessor",
                                              "party-uuids": [det_uuid("party", "lab-audit")]}]},
        "import-ap": {"href": "trestle://assessment-plans/k8s-ap/assessment-plan.json"},
        "results": [{
            "uuid": det_uuid("result", now()),
            "title": "Automatisierter Compliance-Lauf",
            "description": f"{ok} von {total} bewerteten Control/Komponenten-Paaren erfuellt.",
            "start": now(),
            "end": now(),
            "reviewed-controls": {"control-selections": [
                {"description": "Controls des SSP ssp-workload.",
                 "include-controls": [{"control-id": c} for c in ssp_controls]}]},
            "observations": observations,
            "risks": risks,
            "findings": findings,
        }]}}
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    json.dump(ar, open(a.out, "w"), indent=2, ensure_ascii=False)
    print(f"OSCAL Assessment Results geschrieben: {a.out}")
    print(f"  Observations : {len(observations)}")
    print(f"  Findings     : {total} (satisfied {ok} / not-satisfied {total-ok})")
    print(f"  Risks        : {len(risks)}")


if __name__ == "__main__":
    main()
