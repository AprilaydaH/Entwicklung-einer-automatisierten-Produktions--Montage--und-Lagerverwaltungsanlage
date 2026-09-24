# Warehouse_2 — Metal Components Hochregal (**Zone 5A**)

**TIA:** `Warehouse_Management / Warehouse_2` · **Zone 5A** · **NW 28** `Zone_5a__Metal_Components_Warehouse`  
**Mirror of:** [Warehouse_1 plastic Zone 5B](../Zone_5b_Hochregallager/) (NW 29)  
**Factory I/O:** Stacker Crane **1** (not Crane 0)

Separate Merker (`%M70+`), DBs (`*_W2`), and FB types (`*_W2`) so both warehouses run in one PLC.

## Start here

| | |
|---|---|
| **Setup (FIO + OB1)** | [`WAREHOUSE_2_SETUP.md`](WAREHOUSE_2_SETUP.md) |
| **First pallet** | [`WAREHOUSE_FIRST_PALLET.md`](WAREHOUSE_FIRST_PALLET.md) |
| **HMI** | [`HMI_Warehouse_2.md`](HMI_Warehouse_2.md) · **main page** [`HMI_Overview_Main.md`](HMI_Overview_Main.md) · [`HMI_DATA_MGMT.md`](HMI_DATA_MGMT.md) · [`HMI_Tags_Warehouse_2.csv`](HMI_Tags_Warehouse_2.csv) · occupancy [`HMI_Tags_Rack_W2.csv`](HMI_Tags_Rack_W2.csv) · [`HMI_Regal_Animation.md`](../../docs/03_Technik/HMI_Regal_Animation.md) |
| **Info codes** | [`INFO_CODES.md`](INFO_CODES.md) |
| **UDTs / DBs** | [`UDT_README.md`](UDT_README.md) |
| **Raster teach** | [`RASTER_TEACH.md`](RASTER_TEACH.md) |
| **Tags** | [`PLC_Tags_Warehouse_2.csv`](PLC_Tags_Warehouse_2.csv) · [`PLC_Tags_Warehouse_2_FIO.csv`](PLC_Tags_Warehouse_2_FIO.csv) · [`PLC_Tags_RFID_5a.csv`](PLC_Tags_RFID_5a.csv) |
| **Web-Suche** | [`docs/03_Technik/Lagerverwaltung_Online.md`](../../docs/03_Technik/Lagerverwaltung_Online.md) (Streamlit, SQLite) |

## Memory map (no overlap with W1)

| Area | Address |
|---|---|
| Modes / HMI cmds | `%M70`–`%M76` |
| RFID Reader 0 status | `%M77.0`–`.6` |
| RFID product outs | `%MD280+` (not `%MD78` — conflicts W1 `%MW80`) |
| Fach / Pitch / Ist / Soll | `%MW180`, `%MD184`…`%MD272` |
| Status | `%MW228`–`%MW234` (`HRL2_*`) |
| Crane 1 analog | `%ED178`/`%ED182`, `%AD144`/`%AD148` |
| Pallet / fork dig. | `%E15.0`–`.5`, `%A15.0`–`.1` |

**Positions:** `gldb_LagerverwaltungData_W2.Fach[n].Position_X/Z` + `Raster.*` (remanent DB).

## Bausteine (`*_W2`)

| Baustein | Rolle |
|---|---|
| `FB_Warehouse_Mode_Select_W2` | Exclusive Einricht / Auto / Hand — pins **IN_OUT** |
| `FB_Warehouse_Gate_W2` | Sensor **AND** (`2a_VisionData_Combo_Done` OR RFID tagged) |
| `FB_Datenverwaltung_Lager_W2` | HMI sync, teach, raster, counts |
| `Hochregal_Automatik_Betrieb_W2` | V5.6 sequencer (RFID skip if `RFID_CODE <> 0`) |
| `FB_Warehouse_Manual_Soll_W2` | Einricht jog + Band teach |
| `FB_Warehouse_Stacker_IO_W2` | Crane 1 ↔ Ist/Soll/Gabel/Palette |
| `FB_Warehouse_Actuators_W2` | Warning / siren |
| `FB_Einlagern_W2` … `FB_Meldung_W2` | Data management |
| `RFID_Read_Write` (DB_4) | Reader **0** idle until FIO bound — [`OB1_RFID_5a_DB4.scl`](OB1_RFID_5a_DB4.scl) |

## Global DBs

| DB | Type |
|---|---|
| `gldb_LagerverwaltungData_W2` | `UDT_Lager` / Fach[1..54] |
| `gldb_AktuellerFach_HMI_W2` | `UDT_AktuellerFach_HMI` |
| `gldb_Meldungen_W2` | `UDT_Meldungen` |

## Commissioning defaults

- Gate: `%E15.0` + Vision Combo (`%M56.0`) or RFID tagged
- Skip Automatik State 10 when `Fachaktuell.RFID_CODE <> 0`
- `Materialart` default **2** (Metall)
- `Offset_Z = 0.2`, `Foerderband_Seite = 1`
- Mode radios: HMI SetBit → PLC Merker; Mode_Select must be **IN_OUT**
