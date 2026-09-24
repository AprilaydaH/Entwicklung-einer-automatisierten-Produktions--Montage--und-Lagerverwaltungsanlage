# Zone 2B — Vision + Transportband Kunststoff

**TIA:**
- NW **7** `Zone_2b_VisionData_Sensors`
- NW **8** `Zone_2b_(Plastic)_Conveyor_Belts_after_Robot_(CNC)_station`

**Hardware:** Vision cameras at **Zone 3B 2-axis Pick & Place** (lid/base **before** assembly).

**Code:** [`scl/Zone_2b_Vision_Foerderbaender/`](../../../scl/Zone_2b_Vision_Foerderbaender/)

| Schritt | Baustein |
|---|---|
| Vision Lid + Base at 3B P&P | `FB_VisionReader` **v2.10** (TIA `%FB17 VisionSensorData`) |
| Encode | Materialart=1, Color_Code, Artikelnummer, ProductTyp, RFID_CODE |
| Combo | **`2b_VisionData_Combo_Done`** `%M40.0` → Warehouse_1 Gate (NW 29) |
| Write trigger | `Allow_Write` := `4b_Done(1)` → one `Write_Req` pulse |
| RFID Write | Zone **4B** DB_1 Reader 2 — [`Zone_4b`](../Zone_4b_Kunststoff_Palletizer_RFID/) |
| RFID Read / Gate / Auto | Zone **5B** — [`SYSTEM_AUDIT.md`](../../../scl/Zone_5b_Hochregallager/SYSTEM_AUDIT.md) |

Tags: [`TAGS_VisionSensorData.md`](../../../scl/Zone_2b_Vision_Foerderbaender/TAGS_VisionSensorData.md)  
Flow: [`RFID_AUTOMATIC.md`](../../../scl/Zone_4b_Kunststoff_Palletizer_RFID/RFID_AUTOMATIC.md)

**Metal Vision** is separate: [Zone 2A NW 5](../Zone_2a_Foerderbaender/)

Zurück: [04_Anlagenbereiche](../README.md)
