# Get Vision → RFID write working (commissioning)

Do these **in order**. Do not skip. One step fails → stop and fix it.

---

## A) Factory I/O — Vision hardware (most common fail)

1. Both cameras: Operating mode = **Detects All (Numerical)** (not Blue Bases)  
2. Drivers map:
   - Lid Value → `%ID142` / `%ED142`
   - Base Value → `%ID146` / `%ED146`
3. Place cameras on **3B 2-axis P&P** lid + base infeeds  
4. Scene running + PLC connected  

**Proof:** Watch table online — put parts under cameras:

| Tag | Must show |
|---|---|
| `%ED142` | **1…6** |
| `%ED146` | **1…6** |
| `%M40.1` Both_Ready | **TRUE** |
| `%MD42` RFID_CODE | ≠ 0 |
| Vision State `%MW48` | **4** (waiting for write) or **2** |

If still 0 → hardware/mode/map. **SCL cannot fix this.**

---

## B) Force one write (prove DB_1 + Reader 2)

Temporary on Vision call:

`Allow_Write := TRUE`   ← remove `4b_Done` for this test only

Also on **DB_1** (Reader 2 writer):

| Pin | Value |
|---|---|
| `HMI_Write` | `%M20.0` |
| `Execute_Hold` | **`T#100MS`** (not 0) |
| `Timeout` | `T#15S` |
| `Tag_Wait_Time` | `T#30S` |
| `Pallet_Tagged` | `%M40.2` (**not** Tag_Present) |
| Busy/Done/Bereit | `%M30.1/4/0` |

**Proof:**

| Tag | Must show |
|---|---|
| `%M20.0` | pulses / stays until Busy |
| `%A11.1` Execute | pulses ~100 ms |
| `%ED138` Command ID | **0→1→2…** |
| `%M40.2` Pallet_Tagged | **TRUE** |
| Vision State | **3** |

If Command ID stays **0** → Factory I/O Reader 2 driver map / tag in range. Not Vision.

---

## C) Put the real gate back

After B works:

`Allow_Write := "4b_Done(1)"` `%M10.0`

**Proof:** Both_Ready → State 4 → when `%M10.0` TRUE → write → Pallet_Tagged.

If State 4 forever → palletizer Done never comes (4b), not RFID.

---

## D) DB_2 (warehouse) — only after pallet is tagged

DB_2 does **not** write. Fix timers anyway:

| Pin | Value |
|---|---|
| `Execute_Hold` | `T#100MS` |
| `Tag_Wait_Time` | `T#30S` |
| `Timeout` | `T#15S` |
| `RFID_Lesen` | `%M65.0` |

Needs `Paket_Fuer_Hochregal` + Automatik State 10.

---

## Paste versions (if not already)

| FB | Version |
|---|---|
| `FB_VisionReader` | **2.8** |
| `FB_RFID_ReadWrite` | **1.6** |

Compile → download → retest A→B→C.

---

## Who writes what

```
Vision + DB_1 (Reader 2)  =  WRITE pallet   ← fix this first (%M20.0)
DB_2 (Reader 5)           =  READ at warehouse later
```
