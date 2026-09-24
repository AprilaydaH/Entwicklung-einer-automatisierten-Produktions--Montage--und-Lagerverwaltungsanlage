# Instance check — VisionFID + RFID DB_1 + DB_2

Reviewed from your TIA screenshots (27.08.2026).

## Roles

| Instance | Reader | Job |
|---|---|---|
| `%DB82 VisionFID_DB` | — | Encode lid/base → pulse Write |
| `%DB… RFID_Read_Write_DB_1` | Reader **2** (4b) | **WRITE** product |
| `%DB896 RFID_Read_Write_DB_2` | Reader **5** (5b) | **READ** at warehouse |

---

## VisionFID_DB — OK for automatic write

| Pin | Your wire | Verdict |
|---|---|---|
| Allow_Write | `4b_Done(1)` `%M10.0` | Sense at 3B P&P; write after assembly |
| RFID_Busy/Done/Bereit/Reset | `2b_HMI_RFID_*` `@M30` | OK |
| Write_Req | `2b_HMI_RFID_Write` `%M20.0` | OK |
| RFID_Code / Artikel / Mat / Typ | `2b_VisionData_*` | OK |
| Combo_Done | `%M40.0` | OK |
| Both_Ready | `%M40.1` | OK |

No change needed on Vision if FB is **v2.3**.

---

## RFID_Read_Write_DB_1 (Writer) — one fix required

### OK

| Pin | Your wire |
|---|---|
| HMI_Write | `%M20.0` |
| HMI_Read/Check/Clear/Lesen | `false` |
| HMI_Reset | `%M30.5` |
| FIO Reader 2 | `ED130/134/138`, `A11.1`, `AD104/108/112` |
| Product `*_In` | from Vision `%MD42` / `%MW28` / `%MB46` / `%MW38` |
| Busy/Done/Bereit/Error/Gueltig/Fehler | `%M30.0…6` |
| Status_Code | `%MW44` |
| Timeout | `T#5s` |

`Op_Mode = 0` is fine — Write uses Job **11** from `HMI_Write`, not Op_Mode.

### FIX — wrong output pin

| Wrong now | Correct |
|---|---|
| **`Tag_Present` → `%M40.2` `2b_HMI_RFID_Pallet_Tagged`** | **`Pallet_Tagged` → `%M40.2` `2b_HMI_RFID_Pallet_Tagged`** |

`Tag_Present` = “tag in field” (any check).  
`Pallet_Tagged` = **write Job 11 OK** — this is what the warehouse gate needs.

Also:

- Leave `Tag_Present` on a different tag (e.g. `2b_RFID_Tag_Present`) or unconnected.
- Scroll the call and confirm pin **`Pallet_Tagged`** is the one writing `%M40.2` (not forced `false`).

Optional: set `Op_Mode := 10` for consistency (not required for Write).

---

## RFID_Read_Write_DB_2 (Warehouse reader) — mostly OK

**DB_2 never writes the pallet.** Pallet write = **DB_1** + `%M20.0`.  
DB_2 only reads when Automatik pulses `5b_RFID_Lesen`.

### OK (from your online view)

| Pin | Your wire | Verdict |
|---|---|---|
| HMI_Write/Read/Check/Clear | `false` | OK (read-only) |
| HMI_Reset | `false` | OK |
| RFID_Lesen | `5b_RFID_Lesen` `%M65.0` | OK |
| Op_Mode | `10` | OK |
| Command_ID / Status / Read | Reader 5 `%ED158/150/154` | OK |
| Busy…Fehler / outs | `RFID_5b_*` | OK |
| Pallet_Tagged | `false` | OK |

Idle with `RFID_Bereit = TRUE` and `RFID_Lesen = FALSE` is **correct** until warehouse Auto State 10.

### Fix on DB_2 (your screenshot)

| Pin | Now | Set to |
|---|---|---|
| `Execute_Hold` | **T#0MS** | **`T#100MS`** |
| `Tag_Wait_Time` | **T#0MS** | **`T#30S`** (or `T#2M`) |
| `Tag_Retry_Time` | **T#0MS** | **`T#1S`** |
| `Timeout` | T#2s | **`T#15S`** better |

`T#0MS` on Execute_Hold → FIO often never sees Execute → Status 10 on read later.

### Fix recommended (if still shared)

| Pin | Change to |
|---|---|
| HMI_Reset | keep **`false`** (your shot is good) |

---

## Auto chain after the fix

```
VisionFID  →  Write_Req %M20.0
     ↓
DB_1 Writer (Reader 2)  →  Pallet_Tagged %M40.2  +  Combo_Done %M40.0
     ↓
Warehouse Gate: Paket + (Combo_Done OR Pallet_Tagged)
     ↓
Automatik → 5b_RFID_Lesen %M65.0
     ↓
DB_2 Reader (Reader 5) → RFID_5b_Code_Out → Einlagern
```

## Timeouts (v1.6) — long travel OK

| Pin | Default | Meaning |
|---|---|---|
| `Timeout` | **T#15S** | Only waits for FIO **Command ID** |
| `Tag_Wait_Time` | **T#3M** | Wait for assembly/tag (Status 1 = no error) |
| `Tag_Retry_Time` | T#1S | Re-check present while waiting |
| `Execute_Hold` | T#100MS | Execute pulse width |

While waiting: `Waiting_For_Tag = TRUE`, `State = 140`, `Busy = TRUE`, **no Status 10**.

On DB_1 set `Timeout := T#15S` (or longer). Leave `Tag_Wait_Time` at 3 min or set `T#5M` if convey is slower.
