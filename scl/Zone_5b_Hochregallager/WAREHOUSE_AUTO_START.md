# Warehouse — automatic Einlagern (no Start button)

**Goal:** Pallet arrives tagged at the rack → crane reads RFID → stores pallet → home.  
**No** `HMI_Start_Einlagern` in Auto mode — Automatik V1.4 starts alone when the gate opens.

---

## How Auto start works (V4.0)

**State 0** waits at Home. When pallet arrives at the band:

| Condition | Tag | Must be |
|-----------|-----|---------|
| Auto mode | `Mode_Auto` | `%M60.1` **TRUE** |
| Pallet at band | `Paket_Vor_Regal` / `Paket_Fuer_Hochregal` | **TRUE** |
| Not already stored this cycle | `Paket_Uebernommen` (STAT) | **FALSE** |
| No fault | `Not_Aus`, `HRL_Error`, `Mode_Einricht` | **FALSE** |

→ **`State := 10`** (read RFID). **`RFID_Bereit` is NOT checked in state 0** — state 10 waits for the reader.

You do **not** press Start Einlagern in Auto (Hand only).

---

## Two TIA fixes (from your online screenshots)

### 1 — Gate `%FB31` `5b_Warehouse_Gate`

| Pin | Wrong now | Fix |
|-----|-----------|-----|
| `RFID_Pallet_Tagged` | constant `false` | **`2b_HMI_RFID_Pallet_Tagged`** `%M40.2` |

Also confirm **4b DB_1** output pin **`Pallet_Tagged`** (not `Tag_Present`) drives `%M40.2`.

### 2 — Automatik `%FB21` output

| Pin | Wrong now | Fix |
|-----|-----------|-----|
| `RFID_Lesen` **out** | constant `false` | **`5b_RFID_Lesen`** `%M65.0` |

DB_2 `RFID_Lesen` **in** must use the **same** tag `%M65.0`.

---

## Full automatic chain

```
Vision (3B) → latch product
     ↓
4b_Done %M10.0 → Vision Write_Req → %M20.0 → DB_1 WRITE (Reader 2)
     ↓
Pallet_Tagged %M40.2  (+ optional Combo_Done %M40.0)
     ↓
Gate: Paket_Fuer_Hochregal %M62.1 = sensor AND (Combo_Done OR Pallet_Tagged)
     ↓
Mode_Auto %M60.1 → Automatik State 10 (auto, no button)
     ↓
RFID_Lesen %M65.0 → DB_2 READ (Reader 5)
     ↓
RFID_5b_Gueltig → copy product → State 20 → free slot → Einlagern → Home
```

---

## OB1 call order (Main OB1)

Run networks in this order:

| # | Network | Why |
|---|---------|-----|
| 1 | Vision `%FB17` | Outputs `%M20.0` |
| 2 | DB_1 `%DB76` | Same-scan write pulse |
| 3 | Gate `%DB97` | `%M62.1` |
| 4 | Stacker `%DB98` | Crane I/O |
| 5 | Datenverwaltung `%DB92` | Slot DB |
| 6 | **Automatik `%DB93`** | Sets `%M65.0` in State 10 |
| 7 | **DB_2 `%DB96`** | Reads `%M65.0` (best: **after** Automatik) |

If DB_2 runs **before** Automatik, read starts **one scan later** — usually OK while State 10 is held.

Reference glue: [`OB1_Warehouse_1_IO.scl`](OB1_Warehouse_1_IO.scl) + Automatik pins in [`WAREHOUSE_1_SETUP.md`](WAREHOUSE_1_SETUP.md) §4.

---

## Automatik inputs (confirm)

| Pin | Wire to |
|-----|---------|
| `Paket_Vor_Regal` | **`Paket_Fuer_Hochregal`** `%M62.1` (gated — not raw `%M62.0`) |
| `RFID_Bereit` | `RFID_5b_Bereit` `%M65.4` |
| `RFID_Gueltig` | `RFID_5b_Gueltig` `%M65.5` |
| `RFID_Fehler` | `RFID_5b_Fehler` `%M65.6` |
| `RFID_Code` … | `RFID_5b_Code_Out` `%MD140` … |

---

## HMI / mode (one-time)

1. Teach raster: Mode **Einricht** → Fach 1 + pitch → **Raster berechnen** ([`RASTER_TEACH.md`](RASTER_TEACH.md))
2. Set **Mode Auto** `%M60.1` ON (Hand/Einricht OFF)
3. **Not_Aus** OFF `%M60.3`
4. Disable HMI **WRITE** on `%M20.0` during auto test (extra pulses break DB_1)

---

## Watch online — success sequence

| Step | Tags |
|------|------|
| Pallet at rack | `%E14.3` TRUE, `%M62.0` TRUE |
| Tagged + gate | `%M40.2` TRUE → **`%M62.1` TRUE** |
| Auto picks up | `Mode_Auto` TRUE → `HMI_State` **10**, `HRL_Busy` TRUE, Meldecode **100** |
| RFID read | `%M65.0` TRUE → `%ED158` Command ID steps → `RFID_5b_Gueltig` TRUE |
| Store | State **20** → 22…90 → `HRL_Anzahl_Belegt` +1 |
| Done | State **300** home, `HRL_Done` pulse |

---

## If `%M62.1` stays FALSE

| Check | Fix |
|-------|-----|
| `%M40.2` FALSE | Fix DB_1 `Pallet_Tagged`; complete 4b write first |
| `%M40.0` FALSE | OK if `%M40.2` TRUE; wire gate `RFID_Pallet_Tagged` |
| Gate input forced false | Wire `%M40.2` on gate |

## If Auto never leaves State 0

| Check | Fix |
|-------|-----|
| `Mode_Auto` FALSE | Turn Auto ON on HMI |
| `%M62.1` FALSE | Gate / upstream write |
| `RFID_5b_Bereit` FALSE | DB_2 / FIO Reader 5 |
| `HRL_Busy` stuck TRUE | Reset `%M61.5` |
| `Paket_Uebernommen` TRUE | Pallet left rack or reset cycle |

## If State 10 but no read

| Check | Fix |
|-------|-----|
| `%M65.0` never TRUE | Wire Automatik `RFID_Lesen` **out** → `%M65.0` |
| Command ID stuck | DB_2 `Execute_Hold` = `T#100MS`, matching Reader 5 FIO |

---

## Minimum test (after wiring fixes)

1. Run full line until `%M40.2` = TRUE at palletizer  
2. Convey pallet to warehouse (`%E14.3` TRUE)  
3. Confirm **`%M62.1` TRUE**  
4. Set **`Mode_Auto` TRUE** only — do not press Start Einlagern  
5. Within 1–2 scans: `HMI_State` = **10**, then crane moves
