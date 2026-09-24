# Zone 5 — Bänder zu den Hochregalen

| NW | TIA-Titel | Ziel | Tags |
|---:|---|---|---|
| **26** | `Zone_5a_Conveyor_Belts_to_Plastic_Components_Warehouse` | Plastic W1 (NW 29) | `5a_*` `%E12` / `%A12` |
| **27** | `Zone_5b_Conveyor_Belts_to_Metal_Components_Warehouse` | Metal W2 (NW 28) | `5b_*` `%E13` / `%A13` |

**NW 27 SCL:** [`OB1_NW27_Belts_to_Metal_Warehouse.scl`](OB1_NW27_Belts_to_Metal_Warehouse.scl)  
**Warehouse_2:** [`../Zone_5a_Metall_Hochregallager/`](../Zone_5a_Metall_Hochregallager/) (NW **28**)

## NW 27 — paste into OB1

Stop all 5b belts when `Not_Aus_W2` **or** pallet at metal crane (`5a_Metal_Pallet_vor_Regal` `%E15.0`).

| Motor | Address |
|---|---|
| `5b_Roller Conveyor (4m) 0` | `%A13.0` |
| `5b_Curved Roller Conveyor 2 CCW` | `%A13.1` |
| `5b_Roller Conveyor (2m) 1` | `%A13.2` |
| `5b_Curved Roller Conveyor 4` | `%A13.3` |
| `5b_Roller Conveyor (6m) 0` | `%A13.4` |
| `5b_Curved Roller Conveyor 3 CCW` | `%A13.5` |

| Sensor (monitor) | Address |
|---|---|
| `5b_1_to_Warehouse` | `%E13.0` |
| `5b_2_to_Warehouse` | `%E13.1` |
| `5b_3_to_Warehouse` | `%E13.2` |
| `5b_Diffuse Sensor 48` | `%E13.4` |
| `5a_Metal_Pallet_vor_Regal` | `%E15.0` |

Leave `5b_Loading Conveyor 1` `%A14.3` to Warehouse_1 (plastic).
