#!/usr/bin/env bash
# Sammelt maschinenlesbare Evidenz aus dem Cluster
set -euo pipefail
OUT="${1:-evidence}"
TS="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
mkdir -p "$OUT"

echo "== [1/4] Kyverno Policy Reports ==============================="
kubectl get policyreport -A -o json     > "$OUT/policyreports.json"
kubectl get clusterpolicyreport -o json > "$OUT/clusterpolicyreports.json"

echo "== [2/4] Cluster-Konfigurationschecks ========================="
CHECKS="$OUT/manual-checks.json"; echo "[" > "$CHECKS"; FIRST=1
emit() {   # emit <check_id> <result> <subject> <message> <source> <method>
  [[ $FIRST -eq 0 ]] && echo "," >> "$CHECKS"; FIRST=0
  jq -nc --arg c "$1" --arg r "$2" --arg s "$3" --arg m "$4" \
         --arg src "$5" --arg me "$6" --arg t "$TS" \
     '{check_id:$c,result:$r,subject:$s,message:$m,source:$src,method:$me,timestamp:$t}' >> "$CHECKS"
}

# --- PSA-Label je Workload-Namespace ---
for ns in $(kubectl get ns -l oscal.cyberlab.local/scope=workload -o jsonpath='{.items[*].metadata.name}'); do
  LVL=$(kubectl get ns "$ns" -o jsonpath='{.metadata.labels.pod-security\.kubernetes\.io/enforce}')
  if [[ "$LVL" == "restricted" ]]; then
    emit psa-restricted-label pass "$ns/Namespace" "pod-security.kubernetes.io/enforce=restricted gesetzt" kubectl-checks EXAMINE
  else
    emit psa-restricted-label fail "$ns/Namespace" "pod-security.kubernetes.io/enforce=${LVL:-<nicht gesetzt>} statt restricted" kubectl-checks EXAMINE
  fi
done

# --- Calico WireGuard ---
# ACHTUNG: In minikube laeuft Calico im Kubernetes-Datastore-Modus (KDD). Calicos
# Node-Ressource ist dort KEIN CRD; "kubectl get nodes.crd.projectcalico.org"
# scheitert immer. Der Public Key steht als Annotation auf dem k8s-Node.
WGEN=$(kubectl get felixconfiguration default \
         -o jsonpath='{.spec.wireguardEnabled}' 2>/dev/null || true)
NODES_TOTAL=$(kubectl get nodes -o jsonpath='{.items[*].metadata.name}' 2>/dev/null \
                | wc -w | tr -d ' ')
NODES_WG=$(kubectl get nodes -o jsonpath=\
'{range .items[*]}{.metadata.annotations.projectcalico\.org/WireguardPublicKey}{"\n"}{end}' \
             2>/dev/null | grep -c . || true)
NODES_WG="${NODES_WG:-0}"
if [[ "$WGEN" == "true" && "$NODES_TOTAL" -gt 0 && "$NODES_WG" -eq "$NODES_TOTAL" ]]; then
  emit calico-wireguard pass "cluster/Calico" \
    "wireguardEnabled=true, Annotation projectcalico.org/WireguardPublicKey auf ${NODES_WG}/${NODES_TOTAL} Nodes" \
    node-annotations TEST
else
  emit calico-wireguard fail "cluster/Calico" \
    "wireguardEnabled=${WGEN:-<nicht gesetzt>}, Schluessel auf ${NODES_WG}/${NODES_TOTAL} Nodes" \
    node-annotations TEST
fi

# --- Image-Signaturpruefung (bewusst deaktiviert, siehe POA&M) ---
# Check_Id muss "verify-image-signature" sein (nicht die Rule_Id "kyv-signed-images"),
# so wie es Check_Id im Component Definition (Teil 17) definiert.
emit verify-image-signature fail "cluster/Kyverno" \
  "Policy verify-image-signature nicht aktiv - Docker-Hub-Registry-Authentifizierung ungeloest (POA&M)" \
  manual-check EXAMINE

# --- API-Server-Startparameter ---
APISERVER=$(kubectl -n kube-system get pod -l component=kube-apiserver \
             -o jsonpath='{.items[0].metadata.name}')
FLAGS=$(kubectl -n kube-system get pod "$APISERVER" \
          -o jsonpath='{.spec.containers[0].command}')
check_flag() {  # check_flag <check_id> <suchmuster> <beschreibung>
  if grep -q -- "$2" <<<"$FLAGS"; then
    emit "$1" pass "minikube/kube-apiserver" "$3" kubectl-apiserver-flags EXAMINE
  else
    emit "$1" fail "minikube/kube-apiserver" "Flag fehlt: $2" kubectl-apiserver-flags EXAMINE
  fi
}
check_flag apiserver-audit-policy      "--audit-policy-file"          "--audit-policy-file und --audit-log-path gesetzt"
check_flag apiserver-encryption-config "--encryption-provider-config" "--encryption-provider-config gesetzt"

# --- Anonymer Zugriff: nicht das Flag pruefen, sondern die Positivliste ---
AUTHNFILE=$(grep -o -- '--authentication-config=[^"]*' <<<"$FLAGS" | cut -d= -f2 || true)
if [[ -n "$AUTHNFILE" ]]; then
  # grep -c gibt bei 0 Treffern selbst schon "0" aus, aber mit Exit-Code 1 (kein
  # Fehler). "|| echo 0" wuerde die "0" doppelt anhaengen ("0\n0") und die
  # spaetere Zahlenpruefung sprengen - deshalb hier nur "|| true".
  PATHS=$(kubectl -n kube-system exec "$APISERVER" -- \
            cat "$AUTHNFILE" 2>/dev/null | grep -c 'path:' || true)
  PATHS="${PATHS:-0}"
  if [[ "$PATHS" -ge 1 ]] && ! grep -q -- '--anonymous-auth=true' <<<"$FLAGS"; then
    emit apiserver-anonymous-auth pass "minikube/kube-apiserver" \
      "AuthenticationConfiguration aktiv, anonymer Zugriff auf $PATHS Health-Pfade beschraenkt" \
      kubectl-apiserver-flags EXAMINE
  else
    emit apiserver-anonymous-auth fail "minikube/kube-apiserver" \
      "AuthenticationConfiguration ohne Pfad-Bedingungen - anonymer Zugriff unbeschraenkt" \
      kubectl-apiserver-flags EXAMINE
  fi
else
  emit apiserver-anonymous-auth fail "minikube/kube-apiserver" \
    "weder --authentication-config noch Einschraenkung des anonymen Zugriffs" \
    kubectl-apiserver-flags EXAMINE
fi

echo "]" >> "$CHECKS"
jq -e . "$CHECKS" > /dev/null && echo "manual-checks.json ist gueltiges JSON"

echo "== [3/4] Audit-Log-Auszug ====================================="
kubectl -n kube-system logs "$APISERVER" --tail=2000 \
  | grep '"kind":"Event"' > "$OUT/audit-excerpt.json" || true

echo "== [4/4] Live-Inventar ========================================"
kubectl get pods -A -o json | jq '{items: [.items[] | {ns:.metadata.namespace, name:.metadata.name,
  images:[.spec.containers[].image], sc:.spec.securityContext}]}' > "$OUT/inventory.json"

echo "Evidenz in $OUT/ ($(du -sh "$OUT" | cut -f1))"
