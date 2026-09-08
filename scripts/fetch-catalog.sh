#!/usr/bin/env bash
# Reproduzierbarer Abruf des NIST OSCAL-Katalogs
set -euo pipefail

RELEASE="${OSCAL_CONTENT_RELEASE:-v1.5.0}"     # Git-Tag, nicht main!
BASE="https://raw.githubusercontent.com/usnistgov/oscal-content/${RELEASE}/nist.gov/SP800-53/rev5/json"
DEST="${1:-upstream}"
mkdir -p "$DEST"

FILES=(
  "NIST_SP-800-53_rev5_catalog-min.json"
  "NIST_SP-800-53_rev5_LOW-baseline_profile.json"
  "NIST_SP-800-53_rev5_MODERATE-baseline_profile.json"
  "NIST_SP-800-53_rev5_HIGH-baseline_profile.json"
)

echo "== Abruf oscal-content ${RELEASE} =========================="
for f in "${FILES[@]}"; do
  echo "-> $f"
  curl -fsSL --retry 3 --retry-delay 2 -o "${DEST}/${f}" "${BASE}/${f}"
done

cd "$DEST"
if [[ -f SHA256SUMS ]]; then
  echo "== Pruefe Checksummen ======================================"
  sha256sum -c SHA256SUMS
else
  echo "== Erstinitialisierung: SHA256SUMS wird angelegt ==========="
  sha256sum "${FILES[@]}" > SHA256SUMS
  echo "!! SHA256SUMS ins Git aufnehmen und im Review pruefen !!"
fi

echo "== Katalog-Metadaten ======================================="
jq -r '.catalog | "UUID          : \(.uuid)
Titel         : \(.metadata.title)
Version       : \(.metadata.version)
OSCAL-Version : \(.metadata."oscal-version")
Stand         : \(.metadata."last-modified")
Gruppen       : \(.groups | length)
Controls      : \([.groups[].controls[]?] | length) Basis, \([.groups[].controls[]? | recurse(.controls[]?)] | length) mit Erweiterungen"' \
  NIST_SP-800-53_rev5_catalog-min.json
