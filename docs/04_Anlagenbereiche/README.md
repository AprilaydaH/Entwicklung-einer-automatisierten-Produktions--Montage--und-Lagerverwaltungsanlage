# 4 — Anlagenbereiche (TIA-Netzwerke)

Zonenordner = OB1-Namen.  
**Netzwerke:** [PLC_Networks.md](../01_Projektgrundlagen/PLC_Networks.md) · **Gesamt:** [Gesamtanlage.md](../01_Projektgrundlagen/Gesamtanlage.md)

| Zone | TIA-NW | Doku | SCL |
|---|---|---|---|
| 1A | 1–2 | [Zone_1a_Metall](Zone_1a_Metall/) | scl/Zone_1a_Metall/ |
| 1B | 4, 6 | [Zone_1b_Kunststoff](Zone_1b_Kunststoff/) | scl/Zone_1b_Kunststoff/ |
| **2A** | **3, 5** | [Zone_2a_Foerderbaender](Zone_2a_Foerderbaender/) — Band NW3 · **Vision NW5** | scl/Zone_2a_Foerderbaender/ |
| 2B | 7–8 | [Zone_2b_Vision_Foerderbaender](Zone_2b_Vision_Foerderbaender/) — Vision NW7 · Band NW8 | scl/Zone_2b_Vision_Foerderbaender/ |
| 3A | 9–12 | [Zone_3a_Metall_PickPlace](Zone_3a_Metall_PickPlace/) | scl/Zone_3a_Metall_PickPlace/ |
| 3B | 17–20 | [Zone_3b_Kunststoff_PickPlace](Zone_3b_Kunststoff_PickPlace/) | scl/Zone_3b_Kunststoff_PickPlace/ |
| 4A | 13–16, 21 | [Zone_4a_Metall_Palletizer_RFID](Zone_4a_Metall_Palletizer_RFID/) | scl/Zone_4a_Metall_Palletizer_RFID/ |
| 4B | 22–25 | [Zone_4b_Kunststoff_Palletizer_RFID](Zone_4b_Kunststoff_Palletizer_RFID/) | scl/Zone_4b_Kunststoff_Palletizer_RFID/ |
| **5A** | 26, **28** | [Zone_5a_Metall_Hochregallager](Zone_5a_Metall_Hochregallager/) (**W2** NW28) · [Zone_5a_Foerderband_Lager](Zone_5a_Foerderband_Lager/) (NW26→plastic WH) | scl/Zone_5a_Metall_Hochregallager/ |
| **5B** | 27, **29** | [Zone_5b_Hochregallager](Zone_5b_Hochregallager/) (**W1** NW29) · Band NW27→metal WH | scl/Zone_5b_Hochregallager/ |

## Kunststoff

```
1B (NW 4, 6) → 2B Vision+Band (NW 7–8) → 3B P&P/Waage (NW 17–20)
    → 4B Palettierer + RFID Write (NW 22–25) → Band NW 26
    → 5B Gate + Reader 5 + Auto-Einlagern (NW 29)
```

## Metall

```
1A (NW 1–2) → 2A Band (NW 3) + Vision (NW 5)
    → 3A P&P/Waage (NW 9–12) → 4A Palettierer + RFID (NW 13–16, 21)
    → Band NW 27 → 5A Metal Warehouse NW 28 (Warehouse_2)
```

**Vision Combo (Metall):** NW 5 → `2a_VisionData_Combo_Done` `%M56.0` → Gate NW 28  
**Vision Combo (Kunststoff):** NW 7 → `2b_VisionData_Combo_Done` `%M40.0` → Gate NW 29  
**RFID am Regal:** W1 Reader **5**. W2 **kein** Reader 0 — Automatik ohne State 10, Produkt von 4A Reader 1.

Audit W1: [SYSTEM_AUDIT.md](../../scl/Zone_5b_Hochregallager/SYSTEM_AUDIT.md) · Setup W2: [WAREHOUSE_2_SETUP.md](../../scl/Zone_5a_Metall_Hochregallager/WAREHOUSE_2_SETUP.md) · Org: [Projektorganisation.md](../01_Projektgrundlagen/Projektorganisation.md) · Web-Suche: [Lagerverwaltung Online](../03_Technik/Lagerverwaltung_Online.md)

Zurück: [docs/README.md](../README.md)
