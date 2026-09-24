# Put the first pallet in the warehouse

Do **Phase 0 → 1 → 2** in order. Phase 1 proves the crane without Vision. Phase 2 is full automatic.

---

## Phase 0 — Wire fixes (5 min, online)

Your screenshots showed these still broken:

| # | Block | Pin | Set to |
|---|-------|-----|--------|
| 1 | `5b_Warehouse_Gate` | `RFID_Pallet_Tagged` | `2b_HMI_RFID_Pallet_Tagged` `%M40.2` |
| 2 | `Hochregal_Automatik_Betrieb` | `RFID_Lesen` **out** | `5b_RFID_Lesen` `%M65.0` |
| 3 | DB_1 (4b) | `Pallet_Tagged` **out** | `%M40.2` (not `Tag_Present`) |
| 4 | Automatik | `Paket_Vor_Regal` **in** | `Paket_Fuer_Hochregal` `%M62.1` |
| 5 | Automatik | `Foerderband_Seite` | **`1`** |
| 6 | Automatik | `Offset_Z` | **`0.2`** |
| 7 | Automatik | `Ziel_Fachnummer_Out` | `%MW130` (not `%MW80`) |

Download → online.

---

## Phase 1 — Teach raster + Hand Einlagern (crane only)

**Goal:** One pallet stored in Fach 1 without Vision/RFID.

### 1.1 Factory I/O

- PLC connected, scene running
- Stacker crane driver: `%ED162/166`, `%AD136/140`, `%E13.6–14.2`, `%A14.0/1`

### 1.2 Teach positions (Mode **Einricht** `%M60.0`)

1. Jog crane to **loading position** (fork picks at `%E14.3`)
2. Set `HMI_Fachnummer` = **1** → pulse **`HMI_Pos_Speichern`** `%M60.6`
3. Jog to **Fach 2** (one bay right) → Pos speichern → note `Pitch_X` on HMI
4. Jog to **Fach 7** (one level up, if Spalten=6) → Pos speichern → note `Pitch_Z`
5. Pulse **`HMI_Raster_Berechnen`** `%M60.7` → Info_Code **17**, `HRL_Anzahl_Frei` = **54**
6. Teach **`Home_X/Z`** `%MD112/116` at crane home (where State 300 returns)

### 1.3 Hand store (skip RFID)

1. Mode **Hand** `%M60.2` ON (Einricht/Auto OFF)
2. On HMI fill `gldb_AktuellerFach_HMI.Auswahl.Fachaktuell`:
   - `RFID_CODE` ≠ 0 (any test value)
   - `Materialart` = **1** (plastic)
   - `Artikelnummer`, `ProductTyp`, `Color_Code` as needed
3. Place pallet at rack → `%E14.3` TRUE
4. Pulse **`HMI_Start_Einlagern`** `%M61.3`

### 1.4 Watch success

| State | Meaning |
|-------|---------|
| **0** | Wait at Home for pallet (`%E14.3`) |
| **10** | Read RFID (armed handshake) |
| **20** | Find free slot |
| **30→60** | Band: move → extend → pick → lift Z0.4 + retract |
| **70→90** | Rack: move → extend+lower → place+lift+retract |
| **100** | Write slot DB (from `Akt_*` vars) |
| **110** | Return home |

| Tag | After success |
|-----|----------------|
| `HRL_Done` | pulse TRUE |
| `HMI_Ziel_Fach` | slot number |
| `HRL_Anzahl_Belegt` | **1** |
| `gldb_LagerverwaltungData.Fach[n].Belegt` | TRUE |

**Stuck?**

| Symptom | Fix |
|---------|-----|
| State 50 forever | Pick feedback — check `%M63.1`, `%M62.2`, `FB_Warehouse_Stacker_IO` |
| State 50 forever | `Position_Erreicht` — check `%AD136/140` move in FIO |
| State 912 | No free slot / raster not calculated |
| Error 900 | Note `HMI_State`, `Fehlercode` on HMI |

---

## Phase 2 — Full automatic (Vision → 4b write → 5b store)

**Goal:** Pallet tagged at 4b, conveyed to warehouse, stored without button.

### 2.1 Upstream (4b) must work first

See [`../Zone_4b_Kunststoff_Palletizer_RFID/COMMISSIONING.md`](../Zone_4b_Kunststoff_Palletizer_RFID/COMMISSIONING.md).

Before conveying to warehouse, online must show:

| Tag | Value |
|-----|-------|
| `%M40.1` Both_Ready | TRUE (at P&P) |
| `%M40.2` Pallet_Tagged | TRUE (after 4b write) |
| `%ED138` Command ID | stepped 0→~23 during write |

OB1 order: **Vision → DB_1 → Gate → … → Automatik → DB_2**

### 2.2 Convey to warehouse

1. Run conveyors until **`5b_Pallet_vor_Regal`** `%E14.3` = TRUE
2. Confirm gate:
   - `%M62.0` TRUE
   - **`%M62.1` TRUE** ← needs `%M40.0` OR `%M40.2`

### 2.3 Auto mode

1. Mode **Auto** `%M60.1` ON (Hand/Einricht OFF)
2. **Not_Aus** OFF
3. **Do not** press Start Einlagern — Auto starts alone

Within 1–2 scans:

| Tag | Value |
|-----|-------|
| `HRL_Busy` | TRUE |
| `HMI_State` | **10** |
| `%M65.0` | TRUE |
| `%ED158` | Command ID steps |
| `RFID_5b_Gueltig` | TRUE |
| `HMI_State` | **20** → motion |

Product copied from tag → `gldb_AktuellerFach_HMI.Fachaktuell`.

### 2.4 After first auto pallet

| Check | Expected |
|-------|----------|
| `HRL_Anzahl_Belegt` | +1 |
| `Fach[n].RFID_CODE` | matches `%MD140` read |
| `Fach[n].Materialart` | 1 |
| Crane | State **300** home |

### 2.5 Second pallet

1. Reset `%M40.2` / new cycle: Vision latches new product, 4b writes new tag
2. `Paket_Uebernommen` clears when pallet leaves `%E14.3`
3. New pallet at rack + `%M62.1` TRUE → Auto starts again

---

## Quick reference — state map

| HMI_State | Phase |
|-----------|-------|
| 0 | Idle |
| 10 | RFID read (Reader 5) |
| 20 | Find free Fach |
| 22–32 | Pick at loading |
| 40–72 | Travel + place in rack |
| 90 | DB Einlagern |
| 300 | Home |
| 900 | Error |

---

## Minimum online trace (add to chart)

`%M40.2`, `%M62.1`, `HMI_State`, `%M65.0`, `RFID_5b_Gueltig`, `HRL_Busy`, `Position_Erreicht`, `%ED158`
