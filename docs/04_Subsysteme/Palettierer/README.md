# Subsystem — Palettierer (Zone 4)

**Maschinenlogik:** Function Block **`FB_Palletizer`** (Instanz-DB, z. B. `FB_Palletizer_DB`)  
**OB1:** ruft nur den FB auf — keine Sequenz im OB  
**Sicherheitszone:** 4 — Palettierung  
**Repository:** `PickPlace-2Axis-SCL`  
**Factory-Rolle:** Fertige Produkte palettieren

## Dokumentation

| Dokument | Inhalt |
|---|---|
| [Palletizer_Dokumentation.md](Palletizer_Dokumentation.md) | Sequenz, I/O, Commissioning |
| [HMI_Organisation.md](HMI_Organisation.md) | HMI-Screens, Tag-Gruppen |
| [Test_und_Inbetriebnahme.md](Test_und_Inbetriebnahme.md) | TIA-Import + Factory-I/O-Tests |

## Code

| Datei | Beschreibung |
|---|---|
| [`scl/FB_Palletizer.scl`](../../../scl/FB_Palletizer.scl) | Sequenz + HMI Auto/Manual |
| [`scl/OB1_Palletizer.scl`](../../../scl/OB1_Palletizer.scl) | OB1-Aufruf → PLC-Tags |
| [`scl/UDT_Palletizer.scl`](../../../scl/UDT_Palletizer.scl) | optionale UDT |
| [`scl/PLC_Tags_Palletizer.csv`](../../../scl/PLC_Tags_Palletizer.csv) / `.xlsx` | PLC-Tags |

## Schnittstellen

| Von / Nach | Material |
|---|---|
| ← Montage / Fördertechnik | Assembled parts |
| ← Box-Pfad | Stackable boxes |
| → Hochregallager | beladene Einheiten |

Zurück: [04_Subsysteme](../README.md) · [docs](../../README.md)
