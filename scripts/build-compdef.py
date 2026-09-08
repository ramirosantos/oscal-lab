#!/usr/bin/env python3
"""Erzeugt die Component Definition aus der Rule-Matrix."""
import json, datetime

now = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
NS  = "https://oscal-compass.github.io/compliance-trestle/schemas/oscal/cd"
DH  = "docker.io/labuser"          # <-- Ihren Docker-Hub-Benutzer eintragen

def rule(rid, rdesc, cid, cdesc, tag):
    """Vier Properties, ueber 'remarks' zu einem Regelsatz gruppiert."""
    return [{"name": n, "ns": NS, "value": v, "remarks": tag} for n, v in
            [("Rule_Id", rid), ("Rule_Description", rdesc),
             ("Check_Id", cid), ("Check_Description", cdesc)]]

KYVERNO = [
 ("kyv-require-non-root","Container muessen als nicht-privilegierter User ohne Privilege-Escalation laufen","require-non-root","Kyverno PolicyReport-Ergebnis der ValidatingPolicy require-non-root","rule_set_01"),
 ("kyv-drop-all-caps","Alle Linux-Capabilities werden gedroppt, seccompProfile=RuntimeDefault","drop-all-capabilities","Kyverno PolicyReport-Ergebnis der ValidatingPolicy drop-all-capabilities","rule_set_02"),
 ("kyv-readonly-rootfs","Root-Dateisystem der Container ist read-only","require-ro-rootfs","Kyverno PolicyReport-Ergebnis der ValidatingPolicy require-ro-rootfs","rule_set_03"),
 ("kyv-signed-images","Nur signierte Images aus " + DH + " sind zugelassen","verify-image-signature","Kyverno ImageValidatingPolicy verify-image-signature","rule_set_04"),
 ("kyv-resource-limits","CPU- und Memory-Limits sind gesetzt","require-resource-limits","Kyverno ValidatingPolicy require-resource-limits","rule_set_05"),
 ("kyv-no-hostpath","hostPath-Volumes, hostNetwork, hostPID und hostIPC sind verboten","disallow-host-namespaces","Kyverno ValidatingPolicy disallow-host-namespaces","rule_set_06"),
]
PSA = [("psa-restricted-enforce","Namespace erzwingt Pod Security Standard 'restricted'","psa-restricted-label","kubectl-Pruefung des Labels pod-security.kubernetes.io/enforce=restricted","rule_set_07")]
CALICO = [
 ("net-default-deny","Default-Deny NetworkPolicy fuer Ingress und Egress je Workload-Namespace","default-deny-netpol","Ergebnis der Kyverno ValidatingPolicy default-deny-netpol im ClusterPolicyReport","rule_set_08"),
 ("net-mtls","Ost-West-Verkehr ist per WireGuard verschluesselt","calico-wireguard","FelixConfiguration.spec.wireguardEnabled=true und Annotation projectcalico.org/WireguardPublicKey auf allen k8s-Nodes","rule_set_09"),
]
API = [
 ("api-audit-policy","API-Server Audit-Policy erzeugt Metadata- und Request-Level Events","apiserver-audit-policy","Pruefung der kube-apiserver Flags --audit-policy-file und --audit-log-path","rule_set_10"),
 ("api-etcd-encryption","Secrets werden at-rest mit AES-256-GCM verschluesselt","apiserver-encryption-config","Pruefung EncryptionConfiguration und etcdctl-Stichprobe","rule_set_11"),
 ("api-anonymous-off","Anonymer Zugriff ist auf die Health-Endpunkte /healthz, /livez und /readyz beschraenkt","apiserver-anonymous-auth","AuthenticationConfiguration mit anonymous.conditions, referenziert ueber --authentication-config","rule_set_12"),
]

def ir(uid, cid, desc, rules):
    return {"uuid": uid, "control-id": cid, "description": desc,
            "props": [{"name": "Rule_Id", "ns": NS, "value": r} for r in rules]}

WL = "trestle://profiles/k8s-workload-restricted/profile.json"
PL = "trestle://profiles/k8s-platform-baseline/profile.json"

def comp(uid, name, ctype, desc, rules, ci_uuid, src, ci_desc, irs):
    props = [p for r in rules for p in rule(*r)]
    return {"uuid": uid, "type": ctype, "title": name, "description": desc, "props": props,
            "control-implementations": [{"uuid": ci_uuid, "source": src,
                                         "description": ci_desc, "implemented-requirements": irs}]}

cd = {"component-definition": {
 "uuid": "9f2c7a10-0000-4000-8000-00000000cd01",
 "metadata": {"title": "Kubernetes Security Stack (minikube Lab) - Component Definition",
              "last-modified": now, "version": "1.0.0", "oscal-version": "1.2.2"},
 "components": [
  comp("c0000001-0000-4000-8000-000000000001","Kyverno Admission Controller","software",
       "Kyverno 1.18 ValidatingPolicy und ImageValidatingPolicy als Admission- und Background-Enforcement.",
       KYVERNO,"e0000001-0000-4000-8000-000000000001",WL,"Enforcement der Workload-Controls durch Kyverno.",[
    ir("f0000001-0000-4000-8000-000000000001","ac-6","Least Privilege wird durch Verbot von privileged, allowPrivilegeEscalation und root-UID durchgesetzt.",["kyv-require-non-root","kyv-drop-all-caps"]),
    ir("f0000001-0000-4000-8000-000000000002","cm-7","Least Functionality: hostPath, hostNetwork, hostPID/IPC und nicht benoetigte Capabilities sind blockiert.",["kyv-no-hostpath","kyv-drop-all-caps"]),
    ir("f0000001-0000-4000-8000-000000000003","cm-7.5","Allow-by-exception: nur signierte Images aus der eigenen Docker-Hub-Organisation.",["kyv-signed-images"]),
    ir("f0000001-0000-4000-8000-000000000004","cm-14","Signed Components: Cosign-Signaturpruefung im Admission-Pfad.",["kyv-signed-images"]),
    ir("f0000001-0000-4000-8000-000000000005","si-7","Software-Integritaet ueber Image-Signatur und read-only Root-Dateisystem.",["kyv-signed-images","kyv-readonly-rootfs"]),
    ir("f0000001-0000-4000-8000-000000000006","sc-39","Prozessisolation ueber seccomp, Capability-Drop und Non-Root-Ausfuehrung.",["kyv-require-non-root","kyv-drop-all-caps"]),
    ir("f0000001-0000-4000-8000-000000000007","si-3","Ressourcenlimits begrenzen die Wirkung von Cryptominern und DoS durch Schadcode.",["kyv-resource-limits"]),
   ]),
  comp("c0000002-0000-4000-8000-000000000002","Pod Security Admission","software",
       "In-Tree PodSecurity Admission Plugin mit Namespace-Labels.",
       PSA,"e0000002-0000-4000-8000-000000000002",WL,"Zweite Verteidigungslinie unabhaengig von Kyverno.",[
    ir("f0000002-0000-4000-8000-000000000001","ac-3","Access Enforcement auf Pod-Spezifikationsebene durch PSS restricted.",["psa-restricted-enforce"]),
    ir("f0000002-0000-4000-8000-000000000002","ac-6.10","Nicht-privilegierte Workloads koennen keine privilegierten Funktionen ausfuehren.",["psa-restricted-enforce"]),
    ir("f0000002-0000-4000-8000-000000000003","cm-6","Configuration Settings entsprechen dem Pod Security Standard restricted.",["psa-restricted-enforce"]),
   ]),
  comp("c0000003-0000-4000-8000-000000000003","Calico CNI","software",
       "Calico als CNI mit NetworkPolicy-Enforcement und WireGuard-Transportverschluesselung.",
       CALICO,"e0000003-0000-4000-8000-000000000003",WL,"Netzwerksegmentierung und Transportverschluesselung.",[
    ir("f0000003-0000-4000-8000-000000000001","sc-7","Boundary Protection durch Namespace-bezogene NetworkPolicies.",["net-default-deny"]),
    ir("f0000003-0000-4000-8000-000000000002","sc-7.5","Deny-by-default fuer Ingress und Egress.",["net-default-deny"]),
    ir("f0000003-0000-4000-8000-000000000003","sc-8","Transmission Confidentiality im Cluster-Netz.",["net-mtls"]),
    ir("f0000003-0000-4000-8000-000000000004","sc-8.1","Kryptographischer Schutz des Ost-West-Verkehrs (WireGuard).",["net-mtls"]),
   ]),
  comp("c0000004-0000-4000-8000-000000000004","Kubernetes Control Plane","service",
       "kube-apiserver, etcd und Auditing der minikube-Control-Plane.",
       API,"e0000004-0000-4000-8000-000000000004",PL,"Plattformseitige Umsetzung von Audit-, Krypto- und Zugriffs-Controls.",[
    ir("f0000004-0000-4000-8000-000000000001","au-2","Event Logging ueber die kube-apiserver Audit-Policy.",["api-audit-policy"]),
    ir("f0000004-0000-4000-8000-000000000002","au-12","Audit Record Generation auf dem API-Server.",["api-audit-policy"]),
    ir("f0000004-0000-4000-8000-000000000003","au-3","Audit-Records enthalten Subjekt, Verb, Ressource, Quelle und Ergebnis.",["api-audit-policy"]),
    ir("f0000004-0000-4000-8000-000000000004","sc-28","Protection of Information at Rest fuer etcd-Inhalte.",["api-etcd-encryption"]),
    ir("f0000004-0000-4000-8000-000000000005","sc-28.1","Kryptographischer Schutz at-rest mit AES-256-GCM.",["api-etcd-encryption"]),
    ir("f0000004-0000-4000-8000-000000000006","ia-2","Anonymer Zugriff ist auf drei Health-Endpunkte beschraenkt; jeder andere Zugriff erfordert Authentifizierung.",["api-anonymous-off"]),
    ir("f0000004-0000-4000-8000-000000000007","ac-3","Access Enforcement durch RBAC am API-Server.",["api-anonymous-off"]),
   ]),
 ]}}

with open("component-definitions/k8s-security-stack/component-definition.json", "w") as fh:
    json.dump(cd, fh, indent=2, ensure_ascii=False)
print("Component Definition geschrieben: 4 Komponenten, 12 Rules")
