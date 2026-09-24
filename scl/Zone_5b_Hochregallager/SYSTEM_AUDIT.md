# Warehouse system audit — inconsistencies (30.08.2026)

Scope: Zone 5b (Warehouse_1) + glue to Vision / 4b RFID write.  
Sources: TIA screenshots + repo SCL/tags/docs.

---

## Critical (blocks Auto Einlagern)

### C1 — Gate `RFID_Pallet_Tagged` forced `false`

| Where | Your TIA | Required |
|---|---|---|
| `5b_Warehouse_Gate` | constant `false` | `2b_HMI_RFID_Pallet_Tagged` **`%M40.2`** |

Without this (and with `%M40.0` Combo_Done also FALSE), **`Paket_Fuer_Hochregal` `%M62.1` stays FALSE** → Auto never starts.

### C2 — Automatik `RFID_Lesen` out forced `false`

| Where | Your TIA | Required |
|---|---|---|
| `Hochregal_Automatik_Betrieb` out | constant `false` | `5b_RFID_Lesen` **`%M65.0`** |

DB_2 never receives a read request → State 10 hangs.

### C3 — Automatik missing **`RFID_Busy`** input (often not on FB yet)

V1.4 State 10 uses `#RFID_Busy`, but many TIA projects never created the pin.

**Add in TIA** (open `Hochregal_Automatik_Betrieb` → Interface → Input):

| Name | Type | Default | Then wire in OB1 |
|---|---|---|---|
| **`RFID_Busy`** | Bool | FALSE | **`RFID_5b_Busy` `%M65.1`** |

```
RFID_Lesen := TRUE
IF RFID_Busy THEN RFID_Read_Armed := TRUE
IF RFID_Read_Armed AND RFID_Gueltig THEN → State 20
```

Without the pin (or if FALSE forever), Gueltig alone never advances → stuck in State **10**.

### C4 — DB_1 `Pallet_Tagged` vs `Tag_Present`

| Wrong | Correct |
|---|---|
| `Tag_Present` → `%M40.2` | **`Pallet_Tagged` → `%M40.2`** |

Gate needs write-OK, not “tag in field”.

---

## High (wrong Auto / wrong data)

### H1 — OB1 call order inconsistent in docs vs glue file

**Correct order (same-scan RFID + Soll override):**

```
1 Vision
2 DB_1 write (Reader 2)
3 Gate
4 Datenverwaltung
5 Automatik          ← sets %M65.0, Soll when Busy
6 Manual Soll        ← overrides Soll only in Einricht
7 Stacker IO         ← Soll → FIO; writes Ist_*
8 DB_2 read          ← reads %M65.0
```

| Doc / file | Problem |
|---|---|
| `WAREHOUSE_1_SETUP.md` §3 | Old order: Stacker → DB_2 → Automatik (RFID_Lesen one scan late) |
| **§3 NW 9** | `FB_Warehouse_Actuators` — Warning Light + Alarm Siren |

### H2 — Tag name fork: `RFID_Pallet_Tagged` vs `2b_HMI_RFID_Pallet_Tagged`

| Source | Tag | Address |
|---|---|---|
| Live / COMMISSIONING | `2b_HMI_RFID_Pallet_Tagged` | **`%M40.2`** |
| Old CSV / Plastic OB1 | `RFID_Pallet_Tagged` | `%M22.5` |

**Use `%M40.2` only.** Gate + DB_1 must share that bit. Do not leave `%M22.5` as a second write-OK flag.

### H3 — `OB1_Plastic_Warehouse.scl` is stale for Warehouse_1

Uses:
- `RFID_Busy` / `RFID_Gueltig` from **4b DB_1** (not `RFID_5b_*`)
- `RFID_Lesen` → `"RFID_Lesen"` (not `5b_RFID_Lesen`)
- `Pallet_Tagged` → `"RFID_Pallet_Tagged"` (not `%M40.2`)

Prefer separate Warehouse_1 FBs + [`WAREHOUSE_1_SETUP.md`](WAREHOUSE_1_SETUP.md) §3. Old OB1 paste files: [`legacy/`](legacy/) only.

### H4 — Manual Soll call (your screenshot) incomplete

| Pin | Must be |
|---|---|
| `Enable` | **TRUE** (was `false` → FB dead) |
| `Automatik_Busy` | `HRL_Busy` `%M64.0` |
| `Not_Aus` | `Not_Aus` `%M60.3` |
| `Ist_X/Z` | `%MD96` / `%MD100` |
| `Soll_X/Z` | `%MD104` / `%MD108` (IN_OUT) |
| `HMI_Soll_X/Z` | `%MD152` / `%MD156` (IN_OUT) |
| `Copy_Ist_to_Soll` | `%M61.7` |
| Step pins (v1.1) | `%M65.7`, `%M66.0–2`, `Jog_Step` `%MD160` |

Place **after Automatik, before Stacker**.

---

## Medium (docs / optional / commissioning)

### M1 — Mode HMI: latch vs momentary

`Mode_Einricht` / `Mode_Auto` / `Mode_Hand` must be **radio / latched**.  
Command buttons = Setze Bit + Rücksetze Bit.

### M2 — Automatik `Paket_Vor_Regal` pin

Must use **gated** `Paket_Fuer_Hochregal` `%M62.1` for Auto (not raw `%M62.0` / `%E14.3`).  
Your earlier screenshot used `%M62.1` — OK.

### M3 — `5b_RFID_Lesen` address

TIA export snapshot still had **`%M0.0`**. Live must be **`%M65.0`**.

### M4 — Datenverwaltung `Einricht_Mode`

Must be **`Mode_Einricht` `%M60.0`**, not `HRL_Mode_Einricht` `%M64.5` (status out).

### M5 — Automatik constants

| Pin | Value |
|---|---|
| `Offset_Z` | `0.01` |
| `Foerderband_Seite` | `1` |
| `Ziel_Fachnummer_Out` | `%MW130` (not `%MW80`) |

### M6 — DB_2 timers

`Execute_Hold` = `T#100MS`, `Tag_Wait_Time` ≥ `T#30S`, `Timeout` prefer `T#15S`.

### M7 — Palette feedback (Factory I/O)

No load sensor — `Palette_Aufgenommen` / `Abgelegt` are derived. If State 30 sticks, check derivation + `%E14.3` behaviour when fork picks.

### M8 — README lists Manual Soll missing

`FB_Warehouse_Manual_Soll.scl` not yet in README baustein table.

---

## Address map — no hard conflict (verified)

| Range | Use |
|---|---|
| M60–M64 | Modes / HMI / process / cmds / status |
| M65.0–6 | RFID_5b handshake |
| M65.7, M66.0–2 | Manual Soll jog pulses |
| MD96–MD124 | Ist / Soll / Home / Ausgabe |
| MD140–MW148 | RFID_5b product outs |
| MD152–MD160 | HMI_Soll + Jog_Step |

---

## TIA fix checklist (do in order)

| # | Action | Done |
|---|---|---|
| 1 | Gate: `RFID_Pallet_Tagged` → `%M40.2` | ☐ |
| 2 | DB_1: `Pallet_Tagged` → `%M40.2` (not Tag_Present) | ☐ |
| 3 | Automatik: `RFID_Lesen` → `%M65.0` | ☐ |
| 4 | Automatik: `RFID_Busy` → `%M65.1` | ☐ |
| 5 | Automatik: RFID status/product from `RFID_5b_*` only | ☐ |
| 6 | Automatik: `Paket_Vor_Regal` ← `%M62.1` | ☐ |
| 7 | Manual Soll: Enable TRUE + all pins (see H4) | ☐ |
| 8 | OB1 order: … Automatik → Manual → Stacker → DB_2 | ☐ |
| 9 | Mode radios latched; `Mode_Auto` stays TRUE | ☐ |
| 10 | Raster taught; Home_X/Z set | ☐ |

---

## Smoke tests after fixes

**A — Gate**  
Pallet at rack + `%M40.2` TRUE → `%M62.1` TRUE.

**B — Hand Einlagern**  
`RFID_CODE` ≠ 0 on Fachaktuell → Mode Hand → Start → States 20→300 → Belegt +1.

**C — Auto**  
Mode Auto + `%M62.1` TRUE → State 10 → `%M65.0` TRUE → `%ED158` steps → Gueltig → State 20→300.

**D — Manual Soll**  
Mode Einricht, Busy FALSE → type Soll X → `%MD104` follows → crane moves.
