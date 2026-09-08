#!/usr/bin/env bash
#
# oscal-lab.sh — startet und stoppt das OSCAL-Compliance-Lab
#
# Aufruf:  ./oscal-lab.sh start | stop | status
#
# Ablage:  ~/bin/oscal-lab.sh  oder  /usr/local/bin/oscal-lab
# Rechte:  chmod +x oscal-lab.sh
#
# Nicht als root ausfuehren: das minikube-Profil gehoert dem Lab-Benutzer.

set -euo pipefail

# ------------------------------------------------------------------ Einstellungen
# Alle Werte lassen sich per Umgebungsvariable ueberschreiben, z. B.
#   APISERVER_IP=192.168.99.140 ./oscal-lab.sh start
PROFILE="${PROFILE:-oscal-lab}"
NODES="${NODES:-2}"
CPUS="${CPUS:-3}"
MEMORY="${MEMORY:-6g}"
DISK="${DISK:-40g}"
K8S_VERSION="${K8S_VERSION:-v1.35.1}"
APISERVER_IP="${APISERVER_IP:-192.168.99.135}"
APISERVER_NAME="${APISERVER_NAME:-k8s1.lab.local}"
FORWARDER="${FORWARDER:-apiserver-forward}"

# Konfigurationsdateien, die minikube beim Start in den Knoten kopiert
CONF_DIR="${HOME}/.minikube/files/etc/ssl/certs"
CONF_FILES=(audit-policy.yaml encryption-config.yaml admission-config.yaml authn-config.yaml)

# ------------------------------------------------------------------ Ausgabe
log()  { printf '==> %s\n' "$*"; }
warn() { printf '!!  %s\n' "$*" >&2; }
die()  { printf 'FEHLER: %s\n' "$*" >&2; exit 1; }

usage() {
    cat <<USAGE
Aufruf: $(basename "$0") {start|stop|status}

  start   Cluster hochfahren, danach den API-Server-Weiterleiter aktivieren
  stop    Weiterleiter stoppen, danach den Cluster herunterfahren
  status  Zustand von Cluster, Knoten, Weiterleiter und anonymem Zugriff

Profil: ${PROFILE}   Knoten: ${NODES}   Kubernetes: ${K8S_VERSION}

Hinweis: Geaenderte --extra-config-Parameter wirken erst nach
         "minikube -p ${PROFILE} delete". Ein "stop" genuegt dafuer NICHT,
         weil minikube die alten Werte im Profil behaelt.
USAGE
}

# ------------------------------------------------------------------ Vorabpruefung
preflight() {
    [[ ${EUID} -ne 0 ]] || die "Nicht als root ausfuehren — minikube legt das Profil sonst unter /root/.minikube an."

    command -v minikube >/dev/null 2>&1 || die "minikube nicht im PATH gefunden."
    command -v kubectl  >/dev/null 2>&1 || warn "kubectl nicht gefunden — die Knotenpruefung entfaellt."
    docker info >/dev/null 2>&1 || die "Docker antwortet nicht. Laeuft der Dienst, und sind Sie in der Gruppe 'docker'?"

    local missing=()
    local f
    for f in "${CONF_FILES[@]}"; do
        [[ -f "${CONF_DIR}/${f}" ]] || missing+=("${f}")
    done
    if (( ${#missing[@]} > 0 )); then
        die "Diese Dateien fehlen unter ${CONF_DIR}: ${missing[*]}
        Sie werden nur beim Start in den Knoten kopiert — ohne sie startet der
        API-Server nicht. Anlegen wie in Teil 7 des Runbooks beschrieben."
    fi

    # Haeufiger Fehler: der Pfad fuer den Worker-Beitritt fehlt in der
    # AuthenticationConfiguration. Ohne ihn scheitert jedes "kubeadm join".
    if ! grep -q 'configmaps/cluster-info' "${CONF_DIR}/authn-config.yaml"; then
        die "In authn-config.yaml fehlt der Pfad
        /api/v1/namespaces/kube-public/configmaps/cluster-info
        Ohne ihn kann kein Worker-Knoten dem Cluster beitreten."
    fi
}

# ------------------------------------------------------------------ Weiterleiter
forwarder_exists() {
    systemctl cat "${FORWARDER}.service" >/dev/null 2>&1
}

start_forwarder() {
    if ! forwarder_exists; then
        warn "Dienst ${FORWARDER} ist nicht eingerichtet (Teil 9.3) — Fernzugriff von oscal1 nicht moeglich."
        return 0
    fi
    log "Starte Weiterleiter ${FORWARDER}"
    sudo systemctl start "${FORWARDER}"
    sleep 2
    systemctl is-active --quiet "${FORWARDER}" \
        || warn "${FORWARDER} laeuft nicht. Ursache: sudo journalctl -u ${FORWARDER} -n 30 --no-pager"
}

stop_forwarder() {
    forwarder_exists || return 0
    # Zuerst stoppen, danach den Cluster: der Dienst ist auf Restart=always
    # gestellt und wuerde sonst endlos gegen einen sterbenden Cluster laufen.
    log "Stoppe Weiterleiter ${FORWARDER}"
    sudo systemctl stop "${FORWARDER}" || true
}

# ------------------------------------------------------------------ Aktionen
do_start() {
    preflight

    log "Starte Cluster '${PROFILE}' — ${NODES} Knoten, Kubernetes ${K8S_VERSION}"
    minikube start \
        --profile="${PROFILE}" \
        --driver=docker \
        --nodes="${NODES}" \
        --cpus="${CPUS}" \
        --memory="${MEMORY}" \
        --disk-size="${DISK}" \
        --kubernetes-version="${K8S_VERSION}" \
        --container-runtime=containerd \
        --cni=calico \
        --apiserver-ips="${APISERVER_IP}" \
        --apiserver-names="${APISERVER_NAME}" \
        --extra-config=apiserver.audit-policy-file=/etc/ssl/certs/audit-policy.yaml \
        --extra-config=apiserver.audit-log-path=- \
        --extra-config=apiserver.encryption-provider-config=/etc/ssl/certs/encryption-config.yaml \
        --extra-config=apiserver.admission-control-config-file=/etc/ssl/certs/admission-config.yaml \
        --extra-config=apiserver.authentication-config=/etc/ssl/certs/authn-config.yaml \
        --extra-config=apiserver.profiling=false \
        --extra-config=controller-manager.profiling=false \
        --extra-config=scheduler.profiling=false

    if command -v kubectl >/dev/null 2>&1; then
        log "Warte, bis alle Knoten bereit sind"
        kubectl wait --for=condition=Ready nodes --all --timeout=180s \
            || warn "Nicht alle Knoten sind Ready — 'kubectl get nodes' pruefen."
    fi

    start_forwarder
    do_status
}

do_stop() {
    stop_forwarder
    log "Stoppe Cluster '${PROFILE}'"
    minikube -p "${PROFILE}" stop
}

do_status() {
    echo
    log "Cluster"
    minikube -p "${PROFILE}" status || true

    echo
    log "Knoten"
    if command -v kubectl >/dev/null 2>&1; then
        kubectl get nodes -o wide 2>/dev/null || warn "API-Server nicht erreichbar."
    else
        echo "    kubectl nicht installiert"
    fi

    echo
    log "Weiterleiter auf Port 8443"
    if forwarder_exists; then
        printf '    systemd: %s\n' "$(systemctl is-active "${FORWARDER}" 2>/dev/null || echo inaktiv)"
        ss -lnt 2>/dev/null | awk '$4 ~ /:8443$/ {print "    Listener: " $4}' \
            | grep . || echo "    kein Listener auf 8443"
    else
        echo "    nicht eingerichtet (Teil 9.3)"
    fi

    echo
    log "Anonymer Zugriff — erwartet: 401 gesperrt, 200 erlaubt"
    local probe
    probe() {
        minikube -p "${PROFILE}" ssh -- \
            "curl -sk -o /dev/null -w '%{http_code}' https://localhost:8443$1" 2>/dev/null || echo "---"
    }
    printf '    %-52s %s\n' "/api/v1/namespaces/default/pods (muss 401 sein)"  "$(probe /api/v1/namespaces/default/pods)"
    printf '    %-52s %s\n' "/api/v1/.../configmaps/cluster-info (muss 200 sein)" "$(probe /api/v1/namespaces/kube-public/configmaps/cluster-info)"
    printf '    %-52s %s\n' "/livez (muss 200 sein)" "$(probe /livez)"
    echo
}

# ------------------------------------------------------------------ Einsprung
case "${1:-}" in
    start)              do_start  ;;
    stop)               do_stop   ;;
    status)             do_status ;;
    -h|--help|help)     usage     ;;
    "")                 usage >&2; exit 1 ;;
    *)                  usage >&2; die "Unbekannte Aktion: $1" ;;
esac
