# Zone 2A — Metal Vision + Transportband

**TIA:** NW **5** `Zone_2a_VisionData_Sensors` · NW 3 belts after CNC

**Hardware:** Vision cameras at **Zone 3A 2-axis Pick & Place** infeed (metal lid + base **before** assembly).

| Step | Where | Block |
|---|---|---|
| Sense Lid=8 + Base=9 | 3A 2-axis P&P | `FB_VisionReader_Metal` |
| Product data | — | **Metall**: `Materialart=2`, Artikelnr, `RFID_Code=YYMMDD` |
| **Vision combo** | `%M56.0` | **`2a_VisionData_Combo_Done`** → Warehouse_2 Gate |
| Assemble | 3A 2-axis P&P | Zone 3A |
| Palletize | 4A gantry | `4a_Done` `%M10.6` → `Allow_Write` |
| RFID Write | 4A Reader (later) | optional; Gate also accepts `RFID_Pallet_Tagged` |
| Warehouse | NW 28 W2 | Gate = sensor **AND** Combo_Done |

## Files

| File | Role |
|---|---|
| [`FB_VisionReader_Metal.scl`](FB_VisionReader_Metal.scl) | Metal latch + encode (`Materialart=2`) |
| [`OB1_NW5_Metal_Vision.scl`](OB1_NW5_Metal_Vision.scl) | Paste into NW 5 |
| [`PLC_Tags_Metal_Vision.csv`](PLC_Tags_Metal_Vision.csv) | Tags (vacant Merker) |

## Factory I/O codes

| Value | Part |
|---:|---|
| 8 | Metal Product Lid |
| 9 | Metal Product Base |
| 1..6 | Plastic → `*_Reject_Plastic` |
| 7 | Metal Raw (ignored for assembly) |

## TIA call (your NW 5)

Instance: **`2a_VisionSensorData_DB`** (`%DB102`)

Stock **`VisionSensorData` (%FB17)** is the **plastic** FB (colors, `Materialart=1`, `Lid_Reject_Metal`).  
For metal on the same instance:

1. **Copy** `%FB17` → new FB `VisionSensorData_Metal` (or use repo `FB_VisionReader_Metal`)
2. Paste metal body (lid=8 / base=9, **no color**, `Materialart=2`, `RFID_Code=YYMMDD`, sequential `Artikelnummer`)
3. Set DB102 type to that metal FB
4. Wire per [`OB1_NW5_Metal_Vision.scl`](OB1_NW5_Metal_Vision.scl)

1. Cameras already tagged: `2a_Vision Sensor 2/3 (Value)` → `%ED170` / `%ED174` (`%ID170` / `%ID174`)
2. Wire Sensor **2 → Lid**, Sensor **3 → Base** on `2a_VisionSensorData_DB` (swap if reversed)
3. Metal FB body (no color) + product tags from [`PLC_Tags_Metal_Vision.csv`](PLC_Tags_Metal_Vision.csv)
4. Online: force value 8 / 9 → `Both_Ready`, `Materialart=2`, `RFID_Code=YYMMDD`, Artikelnr++
5. Later: metal RFID + Gate `Combo_Done`

**Conflict note:** Crane 1 must **not** use ED170/174 — use `%ED178`/`%ED182` (see Warehouse_2 FIO CSV).

Plastic Vision stays on NW **7** (`2b_*` at `%ED142`/`%ED146`). Do not share cameras.
