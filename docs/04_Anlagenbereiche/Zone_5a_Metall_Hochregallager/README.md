# Zone 5A — Metal Components Warehouse (Warehouse_2)

**TIA:** NW **28** `Zone_5a__Metal_Components_Warehouse`  
**Code:** [`scl/Zone_5a_Metall_Hochregallager/`](../../../scl/Zone_5a_Metall_Hochregallager/)  
**Mirror of:** [Plastic Warehouse_1 Zone 5B](../Zone_5b_Hochregallager/) (NW 29)

| | |
|---|---|
| Zone | **5A** Metall-Hochregal |
| Warehouse | Warehouse_2 |
| Crane | Stacker Crane **1** |
| Plastic twin | Zone **5B** / Warehouse_1 / NW 29 |
| Feeder belt | NW **27** → metal WH |
| Vision combo | **`2a_VisionData_Combo_Done`** `%M56.0` from [Zone 2A NW 5](../Zone_2a_Foerderbaender/) |
| RFID at rack | Reader **0** (`5a_RFID`) |

Separate Merker (`%M70+`), DBs (`*_W2`), FB types (`*_W2`).

### Gate

`Paket_Fuer_Hochregal_W2` = pallet sensor `%E15.0` **AND** (`2a_VisionData_Combo_Done` OR RFID tagged)

### Docs / SCL

| Doc | |
|---|---|
| [README](../../../scl/Zone_5a_Metall_Hochregallager/README.md) | Start |
| [WAREHOUSE_2_SETUP](../../../scl/Zone_5a_Metall_Hochregallager/WAREHOUSE_2_SETUP.md) | FIO + OB1 |
| [OB1_NW28_Metal_Warehouse.scl](../../../scl/Zone_5a_Metall_Hochregallager/OB1_NW28_Metal_Warehouse.scl) | Paste NW 28 |
| [WAREHOUSE_FIRST_PALLET](../../../scl/Zone_5a_Metall_Hochregallager/WAREHOUSE_FIRST_PALLET.md) | Hand commission |
| [INFO_CODES](../../../scl/Zone_5a_Metall_Hochregallager/INFO_CODES.md) | Meldung 0–17 |
| [HMI_Warehouse_2](../../../scl/Zone_5a_Metall_Hochregallager/HMI_Warehouse_2.md) | Screens |
| [Lagerverwaltung Online](../../03_Technik/Lagerverwaltung_Online.md) | Web-Suche W1+W2 (Streamlit) |
| [PLC_Tags_Warehouse_2.csv](../../../scl/Zone_5a_Metall_Hochregallager/PLC_Tags_Warehouse_2.csv) | Merker |
| [PLC_Tags_RFID_5a.csv](../../../scl/Zone_5a_Metall_Hochregallager/PLC_Tags_RFID_5a.csv) | Reader 0 |
| [PLC_Tags_Warehouse_2_FIO.csv](../../../scl/Zone_5a_Metall_Hochregallager/PLC_Tags_Warehouse_2_FIO.csv) | Crane 1 |

Zurück: [04_Anlagenbereiche](../README.md)
