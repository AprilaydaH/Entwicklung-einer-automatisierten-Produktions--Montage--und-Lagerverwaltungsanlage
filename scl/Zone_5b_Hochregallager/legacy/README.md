# Legacy — do not use for go-live

Superseded **OB1 paste files** — wire Main OB1 in TIA using [`../WAREHOUSE_1_SETUP.md`](../WAREHOUSE_1_SETUP.md) §3 (FB calls only).

| File | Use instead |
|---|---|
| `OB1_Main_LEGACY.scl` | `WAREHOUSE_1_SETUP.md` §3 |
| `OB1_Plastic_Warehouse_LEGACY.scl` | §3 + Vision/RFID networks in your TIA project |
| `OB1_Hochregallager_LEGACY.scl` | Separate FBs (not `FB_Hochregallager` wrapper) |
| `OB1_RFID_Anschluss_LEGACY.scl` | RFID notes only |
| ~~`OB1_Warehouse_1_IO.scl`~~ | **Removed** — use `FB_Warehouse_*` + §3 pin tables |

Logic for warning light / siren / band teach: **`FB_Warehouse_Actuators`**, **`FB_Warehouse_Manual_Soll` V1.2**.
