# Warehouse_2 (Metal) — setup

**Plastic twin:** [`../Zone_5b_Hochregallager/WAREHOUSE_1_SETUP.md`](../Zone_5b_Hochregallager/WAREHOUSE_1_SETUP.md)  
**Tags:** [`PLC_Tags_Warehouse_2.csv`](PLC_Tags_Warehouse_2.csv) · [`PLC_Tags_Warehouse_2_FIO.csv`](PLC_Tags_Warehouse_2_FIO.csv)

**TIA target:** `Warehouse_Management / Warehouse_2` = Metal · **Zone 5A** · **NW 28** (`Zone_5a__Metal_Components_Warehouse`)

Call FBs separately in OB1 (same pattern as W1 — no wrapper).

---

## 1) Tag ranges (no overlap with W1)

| Area | W2 address |
|---|---|
| Modes / HMI cmds | `%M70`–`%M76` |
| Process | `%M72` / `%M73` / `%M74` |
| Fach / Pitch | `%MW180`, `%MD184`… |
| Ist / Soll / Band | `%MD196`–`%MD272` |
| Status | `%MW228`–`%MW234` (`HRL2_*`) |

Import FIO tags → bind Stacker **Crane 1** in Factory I/O. Digital `E15`/`A15` vacant; analogs **`%ED178`/`%ED182`** / `%AD144`/`%AD148` (Vision 2/3 already occupy `%ED170`/`%ED174`).

**RFID Reader 0:** import [`PLC_Tags_RFID_5a.csv`](PLC_Tags_RFID_5a.csv) — FIO `%ED114/118/122`, `%A15.4`, `%AD88/92/96`. Product outs at **`%MD280+`** (never `%MD78`).

**Mode_Select:** wire `Mode_*_W2` as **IN_OUT** (`⇌`). Output-only pins clear `%M70.0–.2` every scan.

### Stacker Crane 1 (Factory I/O scene offsets)

| Signal | FIO offset | PLC tag (import) |
|---|---|---|
| Moving-X / Z | 73 / 74 | `5b_Metal_Stacker Crane 1 Moving-*` |
| Left / Mid / Right limit | 75 / 76 / 77 | `… Left/Middle/Right Limit` |
| Fork Left / Right | 93 / 94 | `… (Left)` / `(Right)` |
| X/Z Position (V) | AI | `%ED178` / `%ED182` (after Vision `%ED170`/`%ED174`) |
| X/Z Set Point (V) | AO | `%AD144` / `%AD148` (vacant after Crane0 AD140) |

---

## 2) Main OB1 — network order (**NW 28** Metal warehouse)

**Paste:** [`OB1_NW28_Metal_Warehouse.scl`](OB1_NW28_Metal_Warehouse.scl) into **Netzwerk 28** (keep this call order; split into sub-networks if you want):

| NW | FB | Notes |
|---:|---|---|
| 0 | `FB_Warehouse_Mode_Select_W2` | `Mode_*_W2` `%M70.0–.2` |
| 1 | `FB_Warehouse_Gate_W2` | Sensor → `Paket_*_W2` |
| 2 | `FB_Datenverwaltung_Lager_W2` | + OUT → `HRL2_Anzahl_*` |
| 2b | `instLoeschen` / `instSuchen` / `instFreiesFach` | Data cmds |
| 3 | `Hochregal_Automatik_Betrieb_W2` | Sequencer |
| 4 | `FB_Warehouse_Manual_Soll_W2` | After Automatik |
| 5 | `FB_Warehouse_Stacker_IO_W2` | Soll → FIO Crane 1 |
| 6 | `FB_Warehouse_Actuators_W2` | Light / siren |
| 7 | `FB_Meldung_W2` | After Lager FBs |

### Gate

| Pin | Tag |
|---|---|
| `Sensor_Pallet_Vor_Regal` | `5a_Metal_Pallet_vor_Regal` `%E15.0` |
| `Vision_Combo_Done` | **`2a_VisionData_Combo_Done`** `%M56.0` (Zone 2A) |
| `RFID_Pallet_Tagged` | **`4a_RFID_Done`** `%M21.1` (4a write OK) |

| OUT `Paket_Vor_Regal` | `Paket_Vor_Regal_W2` |
| OUT `Paket_Fuer_Hochregal` | `Paket_Fuer_Hochregal_W2` = sensor **AND** (Combo_Done OR Tagged) |

### Automatik constants

| Pin | Value |
|---|---|
| `Offset_Z` | **0.2** |
| `Foerderband_Seite` | **1** (pick Right) |
| `Band_Z_Lift` | teach e.g. **0.5** → `%MD272` |
| `Paket_Vor_Regal` | `Paket_Fuer_Hochregal_W2` (Auto) |
| IN_OUT `Soll_X` / `Soll_Z` | `Soll_X_W2` / `Soll_Z_W2` |
| `State_Out` | `HMI_State_W2` `%MW228` |
| `Ziel_Fachnummer_Out` | `HMI_Ziel_Fach_W2` `%MW230` |
| Busy / Done / Error | `HRL2_Busy` / `Done` / `Error` |

Multi-instances in Automatik DB: `instEinlagern` (`FB_Einlagern_W2`), `instLagerstatus` (`FB_Lagerstatus_W2`).

End-of-scan publish (in body): `"Soll_X_W2"`, `"Gabel_*_Cmd_W2"`, `"Palette_*_Cmd_W2"`.

### Stacker_IO_W2

| Pin | Tag |
|---|---|
| FIO Ist / Moving / Limits | Crane 1 tags |
| `Soll_X` / `Soll_Z` | `Soll_X_W2` / `Soll_Z_W2` |
| `Gabel_*_Cmd` / `Palette_*_Cmd` | `%M73.1–.4` |
| OUT Ist / Position / Gabel / Palette | `*_W2` process tags |
| OUT FIO Soll + fork | Crane 1 setpoints / drives |

---

## 3) State map (same as W1 V5.6)

`0 → 10? → 20 → 30–42 (band) → 50–58 (rack) → 60 (DB) → 70 (home) → 80 → 0`

RFID State **10** skipped when `Fachaktuell.RFID_CODE <> 0` **or** `4a_RFID_Code_Out <> 0`.

NW 28 copies `4a_RFID_Code_Out` → `Fachaktuell` **after** Datenverwaltung (that FB would otherwise overwrite RFID with empty `Fach[n]`).


---

## 4) Watch online

| Tag | Meaning |
|---|---|
| `HMI_State_W2` | Sequencer |
| `Soll_Z_W2` / `Ist_Z_W2` | Motion |
| `HRL2_Busy` / `Done` / `Error` | Status |
| `HMI_Ziel_Fach_W2` | Booked slot |
| `gldb_LagerverwaltungData_W2.Fach[n].Belegt` | DB result |
