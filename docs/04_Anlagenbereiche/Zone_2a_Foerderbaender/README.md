# Zone 2A — Metall Band + Vision

**TIA:**
- NW **3** `Zone_2a_Metal_Conveyor_Belts_after_Robot_(CNC)_station`
- NW **5** `Zone_2a_VisionData_Sensors` ← metal Vision

**Code:** [`scl/Zone_2a_Foerderbaender/`](../../../scl/Zone_2a_Foerderbaender/)

## NW 5 — Vision Data Sensors (Metall)

| | |
|---|---|
| Instance | `2a_VisionSensorData_DB` (`%DB102`) |
| FB | Metal body (`FB_VisionReader_Metal` / copy of FB17) — **not** plastic FB17 body |
| Cameras | `2a_Vision Sensor 2 (Value)` `%ED170` · `2a_Vision Sensor 3 (Value)` `%ED174` |
| Codes | Lid=**8**, Base=**9** (Factory I/O All Numerical) |
| Product | `Materialart=2` (Metall), sequential `Artikelnummer`, `RFID_Code=YYMMDD` — **no color** |
| Combo | **`2a_VisionData_Combo_Done`** `%M56.0` → Warehouse_2 Gate (NW 28) |
| Allow_Write | `4a_Done` `%M10.6` (RFID write later) |

| File | Role |
|---|---|
| [`FB_VisionReader_Metal.scl`](../../../scl/Zone_2a_Foerderbaender/FB_VisionReader_Metal.scl) | Metal latch + stamp |
| [`OB1_NW5_Metal_Vision.scl`](../../../scl/Zone_2a_Foerderbaender/OB1_NW5_Metal_Vision.scl) | Paste into NW 5 |
| [`PLC_Tags_Metal_Vision.csv`](../../../scl/Zone_2a_Foerderbaender/PLC_Tags_Metal_Vision.csv) | Tags |

**Do not** share cameras with plastic (`2b_*` `%ED142`/`%ED146` on NW 7).

## NW 3 — Conveyors

Metal belts after CNC (SCL as wired in TIA).

## Downstream

3A P&P → 4A Palettierer → Band NW 27 → [Zone 5A Warehouse_2](../Zone_5a_Metall_Hochregallager/)

Zurück: [04_Anlagenbereiche](../README.md)
