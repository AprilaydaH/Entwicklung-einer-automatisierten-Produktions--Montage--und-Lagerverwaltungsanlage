# Subsystem — Palettierer (Zone 4)

**Sicherheitszone:** 4 — Palettierung  
**Repository:** `PickPlace-2Axis-SCL`  
**Factory-Rolle:** Fertige Produkte palettieren

## Code

| Datei | Beschreibung |
|---|---|
| [`scl/FB_Palletizer.scl`](../../../scl/FB_Palletizer.scl) | Sequenz + HMI Auto/Manual |
| [`scl/UDT_Palletizer.scl`](../../../scl/UDT_Palletizer.scl) | optionale UDT |
| [`scl/PLC_Tags_Palletizer.csv`](../../../scl/PLC_Tags_Palletizer.csv) / `.xlsx` | PLC-Tags |

## Dokumentation

| Dokument | Inhalt |
|---|---|
| [Palletizer_Dokumentation.md](Palletizer_Dokumentation.md) | Sequenz, I/O, Commissioning |
| [HMI_Organisation.md](HMI_Organisation.md) | HMI-Screens, Tag-Gruppen |

## Schnittstellen

| Von / Nach | Material |
|---|---|
| ← Montage / Fördertechnik | Assembled parts |
| ← Box-Pfad | Stackable boxes |
| → Hochregallager | beladene Einheiten |

Zurück: [04_Subsysteme](../README.md) · [docs](../../README.md)
