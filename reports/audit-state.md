# Audit State - Kubernetes Workload Baseline (minikube Lab)

- Bewertete Control/Komponenten-Paare: **18**
- Erfuellt (satisfied): **9**
- Nicht erfuellt (not-satisfied): **9**
- Compliance-Score: **50 %**
- Observations: **20**, Risks: **9**

## Ergebnis je Control-Familie

| Familie | Erfuellt | Gesamt | Quote |
|---|---:|---:|---:|
| AC | 1 | 4 | 25 % |
| AU | 2 | 2 | 100 % |
| CM | 1 | 4 | 25 % |
| SC | 4 | 6 | 66 % |
| SI | 1 | 2 | 50 % |

## Detailergebnisse

| Control | Komponente | Status | Begruendung |
|---|---|---|---|
| AC-3 | Kubernetes Control Plane | FAIL | Fehlgeschlagene Rules: api-anonymous-off |
| AC-3 | Pod Security Admission | FAIL | Fehlgeschlagene Rules: psa-restricted-enforce |
| AC-6 | Kyverno Admission Controller | PASS | Alle Rules bestanden: kyv-drop-all-caps, kyv-require-non-root |
| AC-6.10 | Pod Security Admission | FAIL | Fehlgeschlagene Rules: psa-restricted-enforce |
| AU-12 | Kubernetes Control Plane | PASS | Alle Rules bestanden: api-audit-policy |
| AU-2 | Kubernetes Control Plane | PASS | Alle Rules bestanden: api-audit-policy |
| CM-14 | Kyverno Admission Controller | FAIL | Fehlgeschlagene Rules: kyv-signed-images |
| CM-6 | Pod Security Admission | FAIL | Fehlgeschlagene Rules: psa-restricted-enforce |
| CM-7 | Kyverno Admission Controller | PASS | Alle Rules bestanden: kyv-drop-all-caps, kyv-no-hostpath |
| CM-7.5 | Kyverno Admission Controller | FAIL | Fehlgeschlagene Rules: kyv-signed-images |
| SC-28 | Kubernetes Control Plane | PASS | Alle Rules bestanden: api-etcd-encryption |
| SC-39 | Kyverno Admission Controller | PASS | Alle Rules bestanden: kyv-drop-all-caps, kyv-require-non-root |
| SC-7 | Calico CNI | FAIL | Fehlgeschlagene Rules: net-default-deny |
| SC-7.5 | Calico CNI | FAIL | Fehlgeschlagene Rules: net-default-deny |
| SC-8 | Calico CNI | PASS | Alle Rules bestanden: net-mtls |
| SC-8.1 | Calico CNI | PASS | Alle Rules bestanden: net-mtls |
| SI-3 | Kyverno Admission Controller | PASS | Alle Rules bestanden: kyv-resource-limits |
| SI-7 | Kyverno Admission Controller | FAIL | Fehlgeschlagene Rules: kyv-signed-images |
