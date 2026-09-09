#!/usr/bin/env python3
"""ar_to_poam.py - erzeugt aus OSCAL Assessment Results ein OSCAL POA&M."""
import argparse, json, uuid, datetime, os

LAB_NS = "https://cyberlab.local/ns/oscal"
SLA = {"high": 14, "moderate": 45, "low": 90}      # Tage bis Faelligkeit

def det_uuid(*p):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, "oscal-lab:" + "|".join(map(str, p))))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ar", required=True)
    ap.add_argument("--ssp-href", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    now  = datetime.datetime.now(datetime.timezone.utc)
    nowz = now.isoformat(timespec="seconds").replace("+00:00", "Z")
    res  = json.load(open(a.ar))["assessment-results"]["results"][0]
    risk_by_uuid = {r["uuid"]: r for r in res.get("risks", [])}

    items, observations, risks = [], [], []
    for f in res["findings"]:
        if f["target"]["status"]["state"] == "satisfied":
            continue
        ctrl = f["target"]["props"][0]["value"]
        comp = f["props"][0]["value"]
        rk   = [risk_by_uuid[r["risk-uuid"]] for r in f.get("related-risks", [])
                if r["risk-uuid"] in risk_by_uuid]
        sev  = next((p["value"] for r in rk for p in r.get("props", [])
                     if p["name"] == "severity"), "moderate")
        due  = (now + datetime.timedelta(days=SLA[sev])).date().isoformat()
        items.append({
            "uuid": det_uuid("poam-item", ctrl, comp),
            "title": "POA&M " + ctrl.upper() + " - " + comp,
            "description": f.get("description", ""),
            "props": [{"name": "severity", "ns": LAB_NS, "value": sev},
                      {"name": "scheduled-completion-date", "ns": LAB_NS, "value": due},
                      {"name": "control-id", "ns": LAB_NS, "value": ctrl}],
            "related-findings":     [{"finding-uuid": f["uuid"]}],
            "related-observations": f.get("related-observations", []),
            "related-risks":        f.get("related-risks", []),
            "remarks": "Remediation bis " + due + " (SLA " + sev + " = " + str(SLA[sev]) + " Tage).",
        })
        observations += [o["observation-uuid"] for o in f.get("related-observations", [])]
        risks += rk

    obs_full = [o for o in res["observations"] if o["uuid"] in set(observations)]
    poam = {"plan-of-action-and-milestones": {
        "uuid": det_uuid("poam", nowz[:10]),
        "metadata": {"title": "POA&M - Kubernetes Workload Baseline (minikube Lab)",
                     "last-modified": nowz, "version": nowz, "oscal-version": "1.2.2"},
        "import-ssp": {"href": a.ssp_href},
        "observations": obs_full,
        "risks": list({r["uuid"]: r for r in risks}.values()),
        "poam-items": items}}
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    json.dump(poam, open(a.out, "w"), indent=2, ensure_ascii=False)
    print("POA&M geschrieben: " + a.out + " (" + str(len(items)) + " Items)")

if __name__ == "__main__":
    main()
