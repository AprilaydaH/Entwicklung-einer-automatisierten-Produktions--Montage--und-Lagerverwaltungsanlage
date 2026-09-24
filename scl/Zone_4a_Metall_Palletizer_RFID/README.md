# Zone 4A — 3-axis Pick and Place + Palettierer + RFID Metall

**TIA:** NW 12–13 Bänder · NW 14 `Zone_4a_Metal_Assembly_Palletizer` (**3-axis**) · NW 15 RFID

| Datei | Rolle |
|---|---|
| `FB_GantryPickPlace.scl` | 3-axis Pick and Place / Palettierer Metall (TIA-Name historisch) |
| `OB1_GantryPickPlace.scl` | Isolierter Test |
| `OB1_RFID_Metal.scl` | NW 15 — `RFID_Read_Write_DB_3` Reader 1 + Vision write |
| `PLC_Tags_RFID_4a.csv` | Live Reader 1 + `4a_RFID_Code_Out` `%MD236` |
| `PLC_Tags_GantryPickPlace.csv` | Tags (`Gantry_*` = Alias bis Umbenennung) |

RFID-FB (gemeinsam): [`../Zone_4b_Kunststoff_Palletizer_RFID/FB_RFID_ReadWrite.scl`](../Zone_4b_Kunststoff_Palletizer_RFID/FB_RFID_ReadWrite.scl)
