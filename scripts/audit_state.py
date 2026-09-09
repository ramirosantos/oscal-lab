#!/usr/bin/env python3
"""audit_state.py - rendert aus OSCAL Assessment Results eine Uebersicht (Markdown)."""
import argparse, json, collections

SYM = {"satisfied": "PASS", "not-satisfied": "FAIL"}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ar", required=True)
    ap.add_argument("--out", default="-")
    a = ap.parse_args()

    res = json.load(open(a.ar))["assessment-results"]["results"][0]
    rows = []
    for f in res["findings"]:
        ctrl = next(p["value"] for p in f["target"]["props"] if p["name"] == "control-id")
        comp = next(p["value"] for p in f["props"]           if p["name"] == "assessed-component")
        rows.append((ctrl, comp, f["target"]["status"]["state"], f["description"]))
    rows.sort()

    ok  = sum(1 for r in rows if r[2] == "satisfied")
    fam, fam_ok = collections.Counter(), collections.Counter()
    for c, _, s, _ in rows:
        k = c.split("-")[0].upper()
        fam[k] += 1
        fam_ok[k] += (s == "satisfied")

    L = ["# Audit State - Kubernetes Workload Baseline (minikube Lab)\n",
         "- Bewertete Control/Komponenten-Paare: **" + str(len(rows)) + "**",
         "- Erfuellt (satisfied): **" + str(ok) + "**",
         "- Nicht erfuellt (not-satisfied): **" + str(len(rows) - ok) + "**",
         "- Compliance-Score: **" + str(ok * 100 // max(len(rows), 1)) + " %**",
         "- Observations: **" + str(len(res["observations"])) + "**, Risks: **"
         + str(len(res.get("risks", []))) + "**\n",
         "## Ergebnis je Control-Familie\n",
         "| Familie | Erfuellt | Gesamt | Quote |", "|---|---:|---:|---:|"]
    for k in sorted(fam):
        L.append("| " + k + " | " + str(fam_ok[k]) + " | " + str(fam[k]) + " | "
                 + str(fam_ok[k] * 100 // fam[k]) + " % |")
    L += ["\n## Detailergebnisse\n",
          "| Control | Komponente | Status | Begruendung |", "|---|---|---|---|"]
    for c, comp, s, d in rows:
        L.append("| " + c.upper() + " | " + comp + " | " + SYM[s] + " | " + d + " |")

    out = "\n".join(L) + "\n"
    if a.out == "-":
        print(out)
    else:
        open(a.out, "w").write(out)
        print("geschrieben: " + a.out)

if __name__ == "__main__":
    main()
