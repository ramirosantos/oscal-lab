#!/usr/bin/env python3
"""Traegt Implementierungsprosa in generierte SSP-Markdowns ein."""
import argparse, glob, os, yaml

ap = argparse.ArgumentParser()
ap.add_argument("--dir", required=True)
ap.add_argument("--prose", required=True)
ap.add_argument("--status", default="implemented",
                choices=["implemented", "partial", "planned", "alternative", "not-applicable"])
a = ap.parse_args()

prose = yaml.safe_load(open(a.prose))
n = 0
for f in glob.glob(os.path.join(a.dir, "*", "*.md")):
    cid = os.path.basename(f)[:-3]
    if cid not in prose:
        continue
    t = open(f).read()
    t2 = t.replace(
        "<!-- Add implementation prose for the main This System component for control: "
        + cid + " -->", prose[cid].strip())
    t2 = t2.replace("#### Implementation Status: planned",
                    "#### Implementation Status: " + a.status)
    if t2 != t:
        open(f, "w").write(t2)
        n += 1
print("patched " + str(n))
