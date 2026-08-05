# Subsystem — Two-Axis Pick & Place (Zone 3)

**Sicherheitszone:** 3 — Montage  
**Repository:** `PickPlace-2Axis-SCL` (dieses Repo)  
**Factory-Rolle:** Base und Deckel zusammenführen / montieren (Lid auf Base)

## Code

| Datei | Beschreibung |
|---|---|
| [`scl/PickPlace_DigitalAnalog.scl`](../../../scl/PickPlace_DigitalAnalog.scl) | `FB_PickPlace` v1.3 — Analog X/Z, Positioning Bars |

## Dokumentation

Derzeit in der Palettierer-Gesamtdoku und README des Repos referenziert; eigene Montage-Doku folgt bei Bedarf.

Factory-I/O-Tags (Auszug aus Tagliste): Place X/Z Position, Two-Axis Setpoints — siehe `scl/PLC_Tags_Palletizer.csv`.

## Schnittstellen in der Factory (konzeptionell)

| Von / Nach | Signal / Material |
|---|---|
| ← Bearbeitung Metall/Kunststoff | Base / Deckel |
| ← RFID | Produktidentifikation |
| → Palettierer / Fördertechnik | montiertes Teil |

## Sicherheit (Zone 3) — Stub

Gefahren: Greifer, Kollision. Schutz: Sicherheitszaun, Bereichssicherung, reduzierte Geschwindigkeit (Details in `docs/02_Sicherheit/`).
