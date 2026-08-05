# Lageplan — Factory-Zonen

**Quelle:** [Lageplan.pdf](Lageplan.pdf)

Ein Repository = gesamte Anlage. Alle Zonen werden hier dokumentiert und programmiert.

```
┌─────────────────────────────┬─────────────────────────────┐
│ Zone 1 — METALL             │ Zone 2 — KUNSTSTOFF         │
│ Bearbeitungszentrum Deckel  │ Bearbeitungszentrum Deckel  │
│ Bearbeitungszentrum Base    │ Bearbeitungszentrum Base    │
├──────────────┬──────────────┼──────────────┬──────────────┤
│ Zone 3A      │ Zone 3B      │              │              │
│ Pick&Place 3a│ Pick&Place 3b│              │              │
├──────────────┴──────────────┼──────────────┴──────────────┤
│ Zone 4A                     │ Zone 4B                     │
│ Palletizer Metal Parts      │ Palletizer Plastic Parts    │
├─────────────────────────────┼─────────────────────────────┤
│ Zone 5A                     │ Zone 5B                     │
│ Robot station a · b         │ Robot station c · d         │
└─────────────────────────────┴─────────────────────────────┘
        ↕ Förderbänder (Verbindung) ↕ Hochregallager
```

| Zone | Stationen | Code-Pfad |
|---|---|---|
| **1** | Metall CNC Deckel + Base | `scl/Zone1_Metall/` |
| **2** | Kunststoff CNC Deckel + Base | `scl/Zone2_Kunststoff/` |
| **3A / 3B** | Pick and Place 3a / 3b | `scl/Zone3_PickPlace/` |
| **4A / 4B** | Palletizer Metal / Plastic | `scl/Zone4_Palettierer/` |
| **5A / 5B** | Robot stations a–d | `scl/Zone5_Roboter/` |
| — | Förderbänder | `scl/Foerderbaender/` |
| — | Hochregallager | `scl/Hochregallager/` |

**Ein HMI (TP)** bedient alle Zonen — siehe [HMI_Gesamtanlage.md](../03_Technik/HMI_Gesamtanlage.md).

**Nicht im Scope:** Wasserverbrauch.
