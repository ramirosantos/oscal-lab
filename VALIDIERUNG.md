# Regel bei widersprüchlichen Validierungsergebnissen

1. `oscal-cli-ms` ist normativ. Es prüft direkt gegen das NIST-Metaschema.
2. Kompatibilitätswarnungen von trestle (z. B. zur oscal-version) sind zulässig.
   Sie werden im Pull Request dokumentiert, blockieren aber nicht.
3. Ein Schema-Fehler bei einem der beiden Werkzeuge blockiert den Merge.
4. Sagt trestle "invalid" und oscal-cli-ms "valid", wird der Fall untersucht,
   bevor gemerged wird — trestle findet Fehler, die das Schema nicht abdeckt.
