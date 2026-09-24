# PLC tag address audit (`PLCTags.xlsx`)

Zwei Bedienstellen (nicht mischen): **Set 1 HMI** `%M58` · **Set 2 Factory I/O** `%E9` / `%A15`.

## Set 1 — HMI (`HMI_Plant_*`)

| Tag | Addr |
|---|---|
| `HMI_Plant_Start` | `%M58.0` (TIA hatte `%M58.5`) |
| `HMI_Plant_Stop` | `%M58.1` (TIA `HMI_Productopn_Stop` auf `%M58.4`) |
| `HMI_Plant_Not_Aus` | `%M58.2` |
| `HMI_Plant_Reset` | `%M58.3` (TIA Name `Main_Reset` war hier — Reset HMI und FIO **trennen**) |
| `Plant_Running` / `Plant_Not_Aus` / `Plant_Enable` / `Plant_Ready` | `%M58.4` … `.7` |

## Set 2 — Factory I/O (physikalisch)

| Tag in TIA now | Wrong addr | Why | Move to |
|---|---|---|---|
| `Production_Start` | `%E18.0` | E16+ = Analogeingang | **`%E9.1`** |
| `Production_Stop` | `%E18.1` | same | **`%E9.2`** |
| `Main_Not_Aus` | `%E18.3` | same | **`%E9.3`** |
| `Main_Reset` | `%M58.3` | das ist HMI-Reset | **`%E9.4`** (eigener DI) |
| `Main_Green_Stack_Light` | `%A18.1` | inside 3A X-Soll `%AD16` | **`%A15.5`** |
| `Main_Red_Light` | `%A18.2` | same | **`%A15.6`** |
| `Main_Start_Button_Light` | `%A18.3` | same | **`%A15.7`** |
| `Production_Freigegeben` | `%M100.0` | inside `Ist_Z` `%MD100` | **`Plant_Enable` `%M58.6`** |

Im FB: `HMI_* OR FIO_*` für Start/Stop/Not-Aus/Reset. Lampen: dieselben Statusbits, zwei Ausgänge (Merker + `%A15`).

## Other overlaps (old, do not retag blindly)

| Bytes | Occupants |
|---|---|
| `%MW12` vs `%M12.3–.6` | `4a_State` vs 4B HMI lamps |
| `%MB20` vs `%M20.0/.1` | `Clock_Byte` vs RFID write bits |
| `%MW30` vs `%M30.0–.6` | `4b_State(1)` vs 2B RFID HMI |
| `%MW34` vs `%M34.0–.2` | `4b_Assembly_Count(1)` vs 4A RFID Metal |
| `%MD42` vs `%MW44` | `2b_VisionData_RFID_CODE` vs Status_Code |
| `%MD152` vs `%MW152/%MW154` | W1 `HMI_Soll_X` vs 4A RFID State |
| `%MD156` vs `%MW156` | W1 `HMI_Soll_Z` vs `4a_RFID_Metal_ProductTyp_Out` |

CSV: [`PLC_Tags_Plant_Start_Stop.csv`](PLC_Tags_Plant_Start_Stop.csv)
