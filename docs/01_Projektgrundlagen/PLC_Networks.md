# SPS-Netzwerke (OB1) â€” TIA Portal

**Quelle:** TIA Main OB1, **29 Netzwerke** (Stand Screenshot Sep 2026)  
**Beschreibung (engl.):** [Main_Program_Sweep.md](Main_Program_Sweep.md) v1.5  
**Lageplan:** [Lageplan.md](Lageplan.md)

| NW | Zone | Kurz | SCL-Ordner |
|---:|---|---|---|
| 1â€“2 | **1A** | Metal raw + Robot/CNC | `scl/Zone_1a_Metall/` |
| 3 | **2A** | Metal conveyors after CNC | `scl/Zone_2a_Foerderbaender/` |
| 4 | **1B** | Plastic raw input | `scl/Zone_1b_Kunststoff/` |
| 5 | **2A** | VisionData Sensors (metal) | `scl/Zone_2a_Foerderbaender/` |
| 6 | **1B** | Plastic Robot/CNC | `scl/Zone_1b_Kunststoff/` |
| 7â€“8 | **2B** | Vision + plastic conveyors | `scl/Zone_2b_Vision_Foerderbaender/` |
| 9â€“12 | **3A** | Band, **2-axis P&P**, Scale 1 | `scl/Zone_3a_Metall_PickPlace/` |
| 13â€“16 | **4A** | Band, **3-axis P&P**, RFID metal | `scl/Zone_4a_Metall_Palletizer_RFID/` |
| 17â€“20 | **3B** | Band, **2-axis P&P**, Scale 2 | `scl/Zone_3b_Kunststoff_PickPlace/` |
| 21 | **4A** | Metal RFID (additional) | `scl/Zone_4a_Metall_Palletizer_RFID/` |
| 22â€“25 | **4B** | Band, Palettierer, RFID plastic | `scl/Zone_4b_Kunststoff_Palletizer_RFID/` |
| 26 | **5A** | Conveyors to **plastic** warehouse | `scl/Zone_5a_Foerderband_Lager/` |
| 27 | **5B** | Conveyors to **metal** warehouse | `scl/Zone_5a_Foerderband_Lager/` / belt |
| 28 | **5A** | **Metal** Components Warehouse (W2) | `scl/Zone_5a_Metall_Hochregallager/` |
| 29 | **5B** | **Plastic** Components Warehouse (W1) | `scl/Zone_5b_Hochregallager/` |

## TIA-Netzwerktitel (verbindlich)

| NW | TIA-Titel | Zone | Funktion |
|---:|---|---|---|
| 1 | `Zone_1a_Metal_Row Material input` | **1A** | Metal raw-material input |
| 2 | `Zone_1a_Metall_Robot_(CNC)_station` | **1A** | Metal robot / CNC |
| 3 | `Zone_2a_Metal_Conveyor_Belts_after_Robot_(CNC)_station` | **2A** | Metal conveyors after CNC |
| 4 | `Zone_1b_(Plastic)_Row Material input` | **1B** | Plastic raw-material input |
| 5 | `Zone_2a_VisionData_Sensors` | **2A** | Vision data (metal path / shared) |
| 6 | `Zone_1b_(Plastic)_Robot_(CNC)_station` | **1B** | Plastic robot / CNC |
| 7 | `Zone_2b_VisionData_Sensors` | **2B** | Vision data sensors (`FB17` VisionSensorData) |
| 8 | `Zone_2b_(Plastic)_Conveyor_Belts_after_Robot_(CNC)_station` | **2B** | Plastic conveyors after CNC |
| 9 | `Zone_3a_Metal_Conveyor_Belts_before Pick and Place Assembly` | **3A** | Conveyors before metal assembly |
| 10 | `Zone_3a_Metal_Pick_And_Place_1` | **3A** | **2-axis Pick and Place** (metal) |
| 11 | `Zone_3a_Metal_Waage_1` | **3A** | Metal scale 1 |
| 12 | `Zone_3a_Metal_Conveyor_Belts_after_scale_1` | **3A** | Conveyors after scale 1 |
| 13 | `Zone_4a_Conveyor_Belts_before_Palletizer` | **4A** | Conveyors before metal palletizer |
| 14 | `Zone_4a_Roller_Conveyor_Belts_before_Palletizer` | **4A** | Roller conveyors before palletizer |
| 15 | `Zone_4a_Metal_Assembly_Palletizer` | **4A** | **3-axis Pick and Place** / metal palletizer |
| 16 | `Zone_4a_Metal_Components_RFID` | **4A** | Metal components RFID |
| 17 | `Zone_3b_(Plastic)__Conveyor_Belts_before_Pick and Place Assembly` | **3B** | Conveyors before plastic assembly |
| 18 | `Zone_3b_(Plastic)_Pick_and_Place_2` | **3B** | **2-axis Pick and Place** (plastic) |
| 19 | `Zone_3b_(Plastic)_scale_2` | **3B** | Plastic scale 2 |
| 20 | `Zone_3b_(Plastic)_Conveyor_Belts_after_scale_2` | **3B** | Conveyors after scale 2 |
| 21 | `Zone_4a_Metal_RFID` | **4A** | Metal RFID (station / write path) |
| 22 | `Zone_4b_Conveyor_Belts_before_Palletizer` | **4B** | Conveyors before plastic palletizer |
| 23 | `Zone_4b_Roller_Conveyor_Belts_before_Palletizer` | **4B** | Roller conveyors before palletizer |
| 24 | `Zone_4b_Plastic_Assembly_Palletizer` | **4B** | Plastic assembly palletizer |
| 25 | `Zone_4b_Plastic_RFID` | **4B** | Plastic RFID Write/Read |
| 26 | `Zone_5a_Conveyor_Belts_to_Plastic_Components_Warehouse` | **5A** | Conveyors to plastic warehouse |
| 27 | `Zone_5b_Conveyor_Belts_to_Metal_Components_Warehouse` | **5B** | Conveyors to metal warehouse |
| 28 | `Zone_5a__Metal_Components_Warehouse` | **5A** | **Warehouse_2** metal Hochregal |
| 29 | `Zone_5b_Plastic_Components_Warehouse` | **5B** | **Warehouse_1** plastic Hochregal |

## Materialfluss

**Metall:** NW 1â€“3 â†’ 5 â†’ 9â€“12 â†’ 13â€“16 â†’ 21 â†’ **27â€“28**  
**Kunststoff:** NW 4 â†’ 6â€“8 â†’ 17â€“20 â†’ 22â€“25 â†’ **26 + 29**

| Station | NW |
|---|---:|
| 2-axis P&P Metall | 10 |
| 2-axis P&P Kunststoff | 18 |
| 3-axis P&P Metall | 15 |
| Plastic RFID Write | 25 |
| Metal warehouse (W2) | **28** |
| Plastic warehouse (W1) | **29** |

**Vision Kunststoff (NW 7):** `FB17` / `FB_VisionReader` — Farbe, `Combo_Done`, Reject Metal.  
**Vision Metall (NW 5):** `FB_VisionReader_Metal` — `Materialart=2`, Datum/Artikel, `2a_VisionData_Combo_Done` → Gate W2.

**RFID am Regal:** W1 Reader **5** (`5b_RFID`). W2 **kein** Reader 0 — Automatik ohne State 10, Produkt von 4A Reader 1.

**OB100** (Startup): einmalig STOP→RUN — `scl/HMI_Plant/OB100_Startup.scl`. Nicht Teil des zyklischen Sweep.

**Nach NW 29:** `FB_Plant_Start_Stop` (FUP) — Produktion Start/Stop + Not-Aus, Q-Inhibit. Dann `"OB100_Startup_Init" := FALSE`. Rezept: [`scl/HMI_Plant/FB_Plant_Start_Stop.md`](../../scl/HMI_Plant/FB_Plant_Start_Stop.md).
