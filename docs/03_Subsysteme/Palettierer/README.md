# Subsystem — Palettierer (Zone 4)

**Sicherheitszone:** 4 — Palettierung  
**Repository:** `PickPlace-2Axis-SCL` (dieses Repo)  
**Factory-Rolle:** Fertige Produkte palettieren / in stapelbare Boxen ablegen

## Code

| Datei | Beschreibung |
|---|---|
| [`scl/FB_Palletizer.scl`](../../../scl/FB_Palletizer.scl) | Sequenz + HMI Auto/Manual |
| [`scl/UDT_Palletizer.scl`](../../../scl/UDT_Palletizer.scl) | optionale Variablenstruktur |
| [`scl/PLC_Tags_Palletizer.csv`](../../../scl/PLC_Tags_Palletizer.csv) / `.xlsx` | PLC-Tags |

## Dokumentation

| Dokument | Inhalt |
|---|---|
| [Palletizer_Dokumentation.md](../../Palletizer_Dokumentation.md) | Sequenz, I/O, Commissioning |
| [HMI_Palletizer_Organization.md](../../HMI_Palletizer_Organization.md) | HMI-Screens, Tag-Gruppen |

## Schnittstellen in der Factory (konzeptionell)

| Von / Nach | Signal / Material |
|---|---|
| ← Montage / Fördertechnik | Assembled parts |
| ← Emitter / Box-Pfad | Stackable boxes |
| → Hochregallager | palettierte / beladene Einheiten (Prozesskette) |

## Sicherheit (Zone 4) — Stub

Gefahren: Stapel, Lasten. Schutz: Lichtgitter, Not-Halt (Details in `01_Sicherheit/`).
