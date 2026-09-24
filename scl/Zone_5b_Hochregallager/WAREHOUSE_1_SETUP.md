# Warehouse_1 — final connections (from TIA tag export)

**Source:** `PLCTags_from TIA.xlsx` → [`PLC_Tags_from_TIA_export.csv`](PLC_Tags_from_TIA_export.csv)  
**Go-live checklist:** [`PLASTIC_WAREHOUSE_GOLIVE.md`](PLASTIC_WAREHOUSE_GOLIVE.md)

TIA folder: `Warehouse_Management / Warehouse_1`  
Call **Datenverwaltung + Automatik as separate FBs** (do **not** add `FB_Hochregallager` wrapper).

---

## 1) Tag audit — what you already have

| Area | TIA table | Status |
|---|---|---|
| Warehouse modes/HMI/process | `Warehouse` | ✅ M60–M64, MW80, MD84–MD124, MW128–134 |
| Vision + RFID write (4b) | `2b_VisionDataSensors`, `RFID_Reader`, `Forderband` | ✅ |
| Conveyor 5a/5b digital | `Forderband`, `Warehouse` | ✅ partial |
| Stacker crane analog + fork | — | ❌ **import** [`PLC_Tags_Warehouse_1_FIO.csv`](PLC_Tags_Warehouse_1_FIO.csv) |
| RFID Reader 5 (stacker read) | — | ❌ **import** [`PLC_Tags_RFID_5b.csv`](PLC_Tags_RFID_5b.csv) |

### Fix immediately in TIA

| Tag | Current | Action |
|---|---|---|
| `5b_RFID_Lesen` | `%M0.0` | **Move to `%M65.0`** — M0.0 is reserved |
| `Ziel_Fachnummer_Out` on Automatik | `%MW80` (`HMI_Fachnummer`) | **Wire to `%MW130` (`HMI_Ziel_Fach`)** |
| `Einricht_Mode` on Datenverwaltung | `%M64.5` (`HRL_Mode_Einricht`) | **Wire to `%M60.0` (`Mode_Einricht`)** — output ≠ input |
| Automatik `Offset_Z` | `0.0` | Set **`0.2`** |
| Automatik `Foerderband_Seite` | `0` | Set **`1`** (fork extends right at loading side) |
| Automatik `Paket_Vor_Regal` | direct `%E14.3` OK | Or use `%M62.0` via OB1 glue (see below) |

### Vision / warehouse memory — no conflict

Vision uses **M40 / MD42** (`2b_VisionData_*`). Warehouse uses **M60+**. Keep both.

| Vision (TIA name) | Address |
|---|---|
| `2b_VisionData_Combo_Done` | `%M40.0` |
| `2b_VisionData_Both_Ready` | `%M40.1` |
| `2b_VisionData_RFID_CODE` | `%MD42` |
| `RFID_Code_IN` (RFID FB in) | `%MD22` |
| `2b_Vision Sensor Lid (Value)` | `%ED142` |
| `2b_Vision Sensor Base(Value)` | `%ED146` |

---

## 2) Factory I/O ↔ PLC (Warehouse_1 / Zone 5b)

Import missing tags, then bind in Factory I/O driver.

### Stacker crane (analog)

| Factory I/O signal | PLC tag (import) | TIA address | Automatik pin |
|---|---|---|---|
| Stacker Crane 0 X Position (V) | `5b_Stacker Crane 0 X Position (V)` | `%ED162` | → `Ist_X` (`%MD96`) |
| Stacker Crane 0 Z Position (V) | `5b_Stacker Crane 0 Z Position (V)` | `%ED166` | → `Ist_Z` (`%MD100`) |
| Stacker Crane 0 X Set Point (V) | `5b_Stacker Crane 0 X Set Point (V)` | `%AD136` | ← `Soll_X` (`%MD104`) |
| Stacker Crane 0 Z Set Point (V) | `5b_Stacker Crane 0 Z Set Point (V)` | `%AD140` | ← `Soll_Z` (`%MD108`) |

### Stacker crane (digital fork + motion)

| Factory I/O signal | PLC tag | Address | Automatik pin |
|---|---|---|---|
| Stacker Crane 0 Moving-X | `5b_Stacker Crane 0 Moving-X` | `%E13.6` | derive `Position_Erreicht` |
| Stacker Crane 0 Moving-Z | `5b_Stacker Crane 0 Moving-Z` | `%E13.7` | derive `Position_Erreicht` |
| Stacker Crane 0 Left Limit | `5b_Stacker Crane 0 Left Limit` | `%E14.0` | `Gabel_Links_Ausgefahren` |
| Stacker Crane 0 Right Limit | `5b_Stacker Crane 0 Right Limit` | `%E14.1` | `Gabel_Rechts_Ausgefahren` |
| Stacker Crane 0 Middle Limit | `5b_Stacker Crane 0 Middle Limit` | `%E14.2` | `Gabel_Eingefahren` |
| Stacker Crane 0 (Left) | `5b_Stacker Crane 0 (Left)` | `%A14.0` | ← `Gabel_Links_Cmd` |
| Stacker Crane 0 (Right) | `5b_Stacker Crane 0 (Right)` | `%A14.1` | ← `Gabel_Rechts_Cmd` |

`Fahre_Zu_Position` has **no FIO output** — crane follows `Soll_X` / `Soll_Z` setpoints.

### Pallet + conveyors (already in TIA)

| Signal | Address | Use |
|---|---|---|
| `5b_Pallet_vor_Regal` | `%E14.3` | Pallet at warehouse loading → `Paket_Vor_Regal` |
| `5b_1_to_Warehouse` | `%E13.0` | Conveyor interlock (optional) |
| `5b_Loading Conveyor 1` | `%A14.3` | Run while storing (optional) |
| **`5b_Warning Light 5`** | **`%A14.2`** | **ON while `HRL_Busy`** (OB1 §9) — verify FIO driver |
| **`5b_Alarm Siren 2`** | **`%A14.4`** | **ON on `HRL_Error` OR `Not_Aus`** (OB1 §9) — verify FIO driver |

### Automatik Band pose (V3.0 — hardcoded)

V3.0 **ignores** `Band_X` / `Band_Z` on the Automatik FB. Loading side is always:

| Phase | X | Z |
|---|---|---|
| Pick at band | 0.0 | 0.0 |
| Lift after pick | 0.0 | 0.4 |

`Band_X` / `Band_Z` tags (`%MD164` / `%MD168`) remain for Einricht teach / HMI monitor only.

| Tag | Address | Use |
|---|---|---|
| `HMI_Copy_Ist_to_Band` | `%M66.3` | Einricht pulse: copy `Ist_X/Z` → `Band_X/Z` (monitor) |

### RFID Reader 5 — Automatik State 10 read

| Signal | Address | RFID FB pin |
|---|---|---|
| RFID Reader 5 Status | `%ED150` | `Status` |
| RFID Reader 5 Read Data | `%ED154` | `Read_Data` |
| RFID Reader 5 Command ID | `%ED158` | `Command_ID` |
| RFID Reader 5 Execute Command | `%A13.7` | `Execute_Command` |
| RFID Reader 5 Command | `%AD124` | `Command` |
| RFID Reader 5 Write Data | `%AD128` | `Write_Data_Out` |
| RFID Reader 5 Memory Index | `%AD132` | `Memory_Index_Out` |

### RFID Reader 4b — Vision write (already wired)

| Signal | Address |
|---|---|
| Execute | `%A11.1` |
| Status / Read / CmdID | `%ED130` / `%ED134` / `%ED138` |
| Command / Write / Index | `%AD104` / `%AD108` / `%AD112` |

---

## 3) Main OB1 — network order (wire in TIA, no OB paste files)

Build these networks in **Main OB1** in TIA (LAD/FBD/ST calls only). Logic lives in **FBs** — see pin tables below.

**Correct order** (same-scan RFID + Einricht Soll override):

| NW | FB / block | Notes |
|---:|---|---|
| 0 | `FB_Warehouse_Mode_Select` | Exclusive Einricht / Auto / Hand |
| 1 | Vision `FB17` | `2b_VisionData_*` |
| 2 | `RFID_Read_Write_DB_1` | Reader 2 write (4b) |
| 3 | `FB_Warehouse_Gate` | → `Paket_Fuer_Hochregal` |
| 4 | `FB_Datenverwaltung_Lager` | HMI / Raster / teach Fach → `%MW132/134` |
| 4b | `instLoeschen`, `instSuchen`, `instFreiesFach` | Data commands — see [`HMI_DATA_MGMT.md`](HMI_DATA_MGMT.md) |
| 5 | `Hochregal_Automatik_Betrieb` | Sequencer V5.6 — `%M65.0`, Soll when Busy |
| 6 | `FB_Warehouse_Manual_Soll` | Einricht jog + **Band teach** (V1.2) |
| 7 | `FB_Warehouse_Stacker_IO` | Soll → FIO, Palette feedback |
| 8 | `RFID_Read_Write_DB_2` | Reader 5 read (after Automatik) |
| 9 | `FB_Warehouse_Actuators` | Warning Light 5 + Alarm Siren 2 |
| 10 | `FB_Meldung` (`instMeldung`) | `Info_Code` → `Info_Text` — **after** NW4/4b/5 |

### NW 4b — Data management commands

Multi-instances in Datenverwaltung DB (or OB1 temps):

```scl
"instLoeschen"(Execute := "HMI_Loeschen" AND ("Mode_Hand" OR "Mode_Einricht"));

IF "HMI_Suchen" THEN
    "instSuchen"();
END_IF;

"instFreiesFach"(Start := "HMI_FreiesFach");

"instMeldung"();
```

| Button | Tag | Notes |
|---|---|---|
| Löschen | `HMI_Loeschen` `%M61.0` | Hand / Einricht |
| Suchen | `HMI_Suchen` `%M61.1` | Uses `Fachaktuell` search fields |
| Freies Fach | `HMI_FreiesFach` `%M61.2` | Rising edge in `FB_Freies_Fach_Suchen` |

Full HMI guide: [`HMI_DATA_MGMT.md`](HMI_DATA_MGMT.md)

Full inconsistency list: [`SYSTEM_AUDIT.md`](SYSTEM_AUDIT.md)  
Auto start: [`WAREHOUSE_AUTO_START.md`](WAREHOUSE_AUTO_START.md)

### NW 0 — `FB_Warehouse_Mode_Select`

| Pin | Tag |
|---|---|
| `Mode_Einricht` | `Mode_Einricht` `%M60.0` |
| `Mode_Auto` | `Mode_Auto` `%M60.1` |
| `Mode_Hand` | `Mode_Hand` `%M60.2` |

### NW 3 — `FB_Warehouse_Gate`

| Pin | Tag |
|---|---|
| `Sensor_Pallet_Vor_Regal` | `5b_Pallet_vor_Regal` |
| `Vision_Combo_Done` | `2b_VisionData_Combo_Done` |
| `RFID_Pallet_Tagged` | `2b_HMI_RFID_Pallet_Tagged` `%M40.2` |
| OUT `Paket_Vor_Regal` | `Paket_Vor_Regal` |
| OUT `Paket_Fuer_Hochregal` | `Paket_Fuer_Hochregal` |

### NW 6 — `FB_Warehouse_Manual_Soll` (V1.2)

| Pin | Tag |
|---|---|
| `Einricht_Mode` | `Mode_Einricht` |
| `Automatik_Busy` | `HRL_Busy` |
| `Ist_X` / `Ist_Z` | `Ist_X` / `Ist_Z` |
| `Copy_Ist_to_Soll` | `HMI_Copy_Ist_to_Soll` |
| **`Copy_Ist_to_Band`** | **`HMI_Copy_Ist_to_Band`** `%M66.3` |
| IN/OUT `Soll_X` / `Soll_Z` | `Soll_X` / `Soll_Z` |
| IN/OUT `HMI_Soll_X` / `HMI_Soll_Z` | `HMI_Soll_X` / `HMI_Soll_Z` |
| **IN/OUT `Band_X` / `Band_Z`** | **`Band_X` / `Band_Z`** `%MD164` / `%MD168` |

### NW 7 — `FB_Warehouse_Stacker_IO`

| Pin | Tag |
|---|---|
| FIO Ist / Moving / Limits | `5b_Stacker Crane 0 …` (see §2) |
| `Soll_X` / `Soll_Z` | `Soll_X` / `Soll_Z` |
| `Gabel_*_Cmd` | `%M63.3`–`.5` |
| `Palette_Aufnehmen_Cmd` / `Ablegen_Cmd` | `%M63.1` / `%M63.2` |
| OUT → Automatik | `Ist_X/Z`, `Position_Erreicht`, `Gabel_*`, `Palette_Aufgenommen` |
| OUT → FIO | setpoints + fork drives |
| **`Pick_FIO_Fallback_En`** | **`TRUE`** (constant) |

### NW 9 — `FB_Warehouse_Actuators`

| Pin | Tag |
|---|---|
| `HRL_Busy` | `HRL_Busy` `%M64.0` |
| `HRL_Error` | `HRL_Error` `%M64.2` |
| `Not_Aus` | `Not_Aus` `%M60.3` |
| OUT `Warning_Light_5` | **`5b_Warning Light 5`** `%A14.2` (verify FIO) |
| OUT `Alarm_Siren_2` | **`5b_Alarm Siren 2`** `%A14.4` (verify FIO) |

Gate FB: [`FB_Warehouse_Gate.scl`](FB_Warehouse_Gate.scl)  
Stacker FB: [`FB_Warehouse_Stacker_IO.scl`](FB_Warehouse_Stacker_IO.scl)  
Manual Soll: [`FB_Warehouse_Manual_Soll.scl`](FB_Warehouse_Manual_Soll.scl)  
Actuators: [`FB_Warehouse_Actuators.scl`](FB_Warehouse_Actuators.scl)

---

## 4) Automatik_Betrieb_DB_1 — pin wiring

Use **exact TIA tag names** from the `Warehouse` table.

### Inputs — modes & HMI

| Pin | Tag | Address |
|---|---|---|
| Auto_Mode | `Mode_Auto` | `%M60.1` |
| Hand_Mode | `Mode_Hand` | `%M60.2` |
| Einricht_Mode | `Mode_Einricht` | `%M60.0` |
| Not_Aus | `Not_Aus` | `%M60.3` |
| HMI_Start_Einlagern | `HMI_Start_Einlagern` | `%M61.3` |
| HMI_Start_Auslagern | `HMI_Start_Auslagern` | `%M61.4` |
| Reset | `HMI_Reset` | `%M61.5` |
| Stop | `HMI_Stop` | `%M61.6` |

### Inputs — process

| Pin | Tag | Source |
|---|---|---|
| Paket_Vor_Regal | `Paket_Fuer_Hochregal` | Gate (Auto) or `Paket_Vor_Regal` (Hand test) |
| Position_Erreicht | `Position_Erreicht` | OB1: NOT Moving-X AND NOT Moving-Z |
| Palette_Aufgenommen | `Palette_Aufgenommen` | OB1 simulation (no FIO load sensor) |
| Palette_Abgelegt | `Palette_Abgelegt` | OB1 simulation |
| Gabel_Rechts_Ausgefahren | `Gabel_Rechts_Ausgefahren` | `%E14.1` or `%M62.5` |
| Gabel_Links_Ausgefahren | `Gabel_Links_Ausgefahren` | `%E14.0` or `%M62.6` |
| Gabel_Eingefahren | `Gabel_Eingefahren` | `%E14.2` or `%M62.7` |
| Ist_X / Ist_Z | `Ist_X` / `Ist_Z` | `%MD96` / `%MD100` |
| Home_X/Z, Ausgabe_X/Z | teach tags | `%MD112`–`%MD124` |
| Offset_Z | **constant** | `0.2` |
| Foerderband_Seite | **constant** | `1` |

Band pose is **hardcoded in V3.0** (X=0, Z pick 0.0, lift 0.4) — `Band_X`/`Band_Z` tags optional for HMI only.

### Inputs — RFID (Auto State 10)

| Pin | Tag | Source |
|---|---|---|
| **RFID_Busy** | **`RFID_5b_Busy`** | **`%M65.1` — required for V1.4 State 10** |
| RFID_Bereit | `RFID_5b_Bereit` | `%M65.4` |
| RFID_Gueltig | `RFID_5b_Gueltig` | `%M65.5` |
| RFID_Fehler | `RFID_5b_Fehler` | `%M65.6` |
| RFID_Artikelnummer | `RFID_5b_Artikelnummer_Out` | `%MW144` |
| RFID_Materialart | `RFID_5b_Materialart_Out` | `%MB146` |
| RFID_ProduktTyp | `RFID_5b_ProductTyp_Out` | `%MW148` |
| RFID_Code | `RFID_5b_Code_Out` | `%MD140` |

Without **`RFID_Busy`**, State 10 never arms → stuck even if Gueltig is TRUE.

**Hand commissioning:** pre-fill `gldb_AktuellerFach_HMI.Auswahl.Fachaktuell` (RFID_CODE <> 0) → skips State 10.

**Gate:** `RFID_Pallet_Tagged` ← `2b_HMI_RFID_Pallet_Tagged` **`%M40.2`** from DB_1 `Pallet_Tagged` (not Tag_Present, not `%M22.5`).

### Outputs

| Pin | Tag | Address |
|---|---|---|
| Busy / Done / Error | `HRL_Busy` / `HRL_Done` / `HRL_Error` | `%M64.0`–`.2` |
| Fahre_Zu_Position | `Fahre_Zu_Position` | `%M63.0` |
| Soll_X / Soll_Z | `Soll_X` / `Soll_Z` | `%MD104` / `%MD108` |
| Palette_Aufnehmen | `Palette_Aufnehmen_Cmd` | `%M63.1` |
| Palette_Ablegen | `Palette_Ablegen_Cmd` | `%M63.2` |
| Gabel_Rechts_Aus | `Gabel_Rechts_Cmd` | `%M63.3` |
| Gabel_Links_Aus | `Gabel_Links_Cmd` | `%M63.4` |
| Gabel_Einfahren | `Gabel_Mitte_Cmd` | `%M63.5` |
| RFID_Lesen | `5b_RFID_Lesen` | `%M65.0` → `RFID_Read_5b_DB_1.RFID_Lesen` |
| State_Out | `HMI_State` | `%MW128` |
| Ziel_Fachnummer_Out | `HMI_Ziel_Fach` | `%MW130` ← **not** MW80 |

### FB_Datenverwaltung_Lager_DB_1

| Pin | Tag |
|---|---|
| Einricht_Mode | `Mode_Einricht` (`%M60.0`) |
| Initialisieren | `HMI_Initialisieren` |
| HMI_Fachnummer | `HMI_Fachnummer` (`%MW80`) |
| Ist_X / Ist_Z | `Ist_X` / `Ist_Z` |
| HMI_Raster_Berechnen + Pitch | `HMI_Raster_Berechnen`, `HMI_Pitch_X/Z`, … |
| **OUT Anzahl_Belegt** | **`HRL_Anzahl_Belegt` `%MW132`** |
| **OUT Anzahl_Frei** | **`HRL_Anzahl_Frei` `%MW134`** |

### Hochregal_Automatik_Betrieb — V5.6

**Multi-instances** in Automatik DB: `instEinlagern`, `instLagerstatus`

| Data | Source |
|---|---|
| `Position_X` / `Position_Z` | `gldb_LagerverwaltungData.Fach[#Ziel_Fachnummer]` |
| Pallet product (until place) | STAT `Akt_*` |
| State **60** DB book | `Akt_*` → `Fachaktuell` → **`instEinlagern`** → **`instLagerstatus`** |

**Einlagern:** `0` → `10` → `20` → `30`–`42` (band) → `50`–`58` (rack) → **`60`** (DB) → **`70`** (home) → **`80`** (done) → `0`

**Auslagern:** not implemented in V5.6 — defer `HMI_Start_Auslagern`

**STAT:** `RFID_Read_Armed`, `Akt_RFID_CODE`, `Akt_Artikelnummer`, `Akt_Materialart`, `Akt_ProductTyp`, `i`, `TON_Fork`

Pick/place timers: **`FB_Warehouse_Stacker_IO`** only.

---

## 5) Palette feedback (Factory I/O limitation)

Stacker Crane in Factory I/O has **no fork-load sensor**. `FB_Warehouse_Stacker_IO` V1.1 derives:

```
Palette_Aufgenommen :=
  (Aufnehmen_Cmd AND NOT Pallet_vor_Regal AND fork extended)   // real plant
  OR (Aufnehmen_Cmd AND fork extended for 1.5 s while sensor still TRUE)  // FIO fallback
```

Defaults: `Pick_FIO_Fallback_En := TRUE`, `Pick_FIO_Fallback_PT := T#1500ms` — no extra OB1 wiring.

`Palette_Abgelegt := Ablegen_Cmd AND Position_Erreicht AND fork extended` (+ 1.5 s FIO timer in V1.3 — **not** Gabel_Mitte; State 70 keeps fork out)

See §3 NW 7 (`FB_Warehouse_Stacker_IO`) and NW 9 (`FB_Warehouse_Actuators`).

---

## 6) Commissioning order

### A — Crane only (Hand, no Vision)

1. Import FIO tags → compile → Factory I/O connect  
2. Mode **Einricht** → teach Fach 1 + pitch → **Raster berechnen** ([`RASTER_TEACH.md`](RASTER_TEACH.md))  
3. Set `Fachaktuell.RFID_CODE` + product fields on HMI  
4. Mode **Hand** → **Start Einlagern**  
5. Watch `HMI_State` **0→10→20→30→42→50→58→60→70→80**, crane moves, `Fach[n].Belegt = TRUE`, `Info_Code = 1`

### B — Full plastic E2E

1. Vision lid+base → `2b_VisionData_Both_Ready`  
2. Pallet at `%E14.3` → 4b RFID write → `2b_VisionData_Combo_Done`  
3. Mode **Auto** → State 10 read on **Reader 5** → Einlagern  
4. Verify `gldb_LagerverwaltungData.Fach[n]`

---

## 7) Watch online

| Tag | Meaning |
|---|---|
| `HMI_State` | Einlagern V5.6: 0=wait, 10=RFID, 20=slot, 30–42=band, 50–58=rack, **60=DB**, **70=home**, **80=done**, 900=error |
| `HRL_Anzahl_Belegt/Frei` | `%MW132/134` from Datenverwaltung |
| `Info_Text` | After `FB_Meldung` — code 1 = Einlagerung OK |
| `Paket_Fuer_Hochregal` | Auto-start gate |
| `Position_Erreicht` | Crane stopped at setpoint |
| `HRL_Busy` / `HRL_Done` | Sequencer status |
| `HMI_Ziel_Fach` | Target slot (not HMI_Fachnummer) |
