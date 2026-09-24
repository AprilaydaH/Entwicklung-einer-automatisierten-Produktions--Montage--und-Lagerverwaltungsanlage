# Zone 4A — 3-axis Pick and Place + Palettierer + RFID Metall

**TIA:** NW 13–14 Bänder · NW **15** Palettierer (**3-axis**) · NW **16** / **21** RFID  
**Maschine:** Factory I/O **3-axis Pick and Place** (X/Y/Z analog + C + Grab)

**Code:** [`scl/Zone_4a_Metall_Palletizer_RFID/`](../../../scl/Zone_4a_Metall_Palletizer_RFID/)

| File | Inhalt |
|---|---|
| `FB_GantryPickPlace.scl` | Sequencer 3-axis P&P |
| `OB1_GantryPickPlace.scl` | Isolierter Test |
| `OB1_RFID_Metal.scl` | RFID Metall — later |
| `PLC_Tags_GantryPickPlace.csv` | Tags (`Done` `%M10.6` = `4a_Done`) |

**Upstream Vision:** [Zone 2A NW 5](../Zone_2a_Foerderbaender/) — `Allow_Write` ← `4a_Done`  
**Downstream:** Band NW 27 → [Warehouse_2 NW 28](../Zone_5a_Metall_Hochregallager/)

Zurück: [04_Anlagenbereiche](../README.md)
