# RFID system audit — plastic (Reader 2 write + optional Reader 5)

**Symptom you see:** `Status_Code = 10`, `Error = TRUE`, `RFID_Bereit = FALSE`  
**Meaning:** Timeout — Factory I/O **Command ID** did not change within 2 s. Fault stays latched until **Reset**.

---

## 1) Clear the latch first

| Action | Tag (your TIA) | Address |
|---|---|---|
| Pulse Reset | `2b_HMI_RFID_Reset` | `%M30.5` |

Must become: `Error = FALSE`, `Status_Code = 0`, `RFID_Bereit = TRUE`.

Until then **no** Write/Read starts on older FB versions.  
**v1.4+:** a new Write/Read/Lesen rising edge clears Error and starts the job (automatic retry).

---

## 2) Factory I/O — Reader 2 (WRITE at 4b) — must match exactly

| Signal | TIA tag | Address |
|---|---|---|
| Status | `4b_RFID Reader 2 Status` | `%ED130` / `%ID130` |
| Read Data | `4b_RFID Reader 2 Read Data` | `%ED134` / `%ID134` |
| **Command ID** | `4b_RFID Reader 2 Command ID` | `%ED138` / `%ID138` |
| **Execute** | `4b_RFID Reader 2 Execute Command` | `%A11.1` / `%Q11.1` |
| Command | `4b_RFID Reader 2 Command` | `%AD104` / `%QD104` |
| Write Data | `4b_RFID Reader 2 Write Data` | `%AD108` / `%QD108` |
| Memory Index | `4b_RFID Reader 2 Memory Index` | `%AD112` / `%QD112` |

**Online test after Reset:**

1. Pulse CHECK or WRITE  
2. Watch `Execute` pulse TRUE one cycle  
3. **`Command ID` must increment** (0→1→2…)  

If CmdID stays **0** → FIO not connected, wrong driver map, or wrong reader selected in Factory I/O.  
This is the **root cause** of Status 10.

---

## 3) Critical parameter conflicts (your TIA vs old repo)

From your export `PLCTags_from TIA.xlsx` — use **these**, not the old `%M20.4` / `%M21` map alone:

### HMI / Vision handshake (WRITE path)

| Role | Correct TIA tag | Address | Wrong if… |
|---|---|---|---|
| Write pulse (Vision → RFID) | `2b_HMI_RFID_Write` | `%M20.0` | Using `%M20.1` only as Write |
| Write_Req alias | `2a_VisionData_Write_Req` | `%M20.1` | Must be **same pulse** as HMI_Write or wire both to same bit |
| Reset | `2b_HMI_RFID_Reset` | `%M30.5` | Using `%M20.4` while HMI/Reset is on M30.5 |
| RFID Busy (to Vision) | Prefer `RFID_Busy` **or** `2b_HMI_RFID_Busy` | `%M21.0` vs `%M30.1` | Vision and RFID FB must use the **same** Busy/Done/Bereit tags |
| RFID Done (to Vision) | Prefer `RFID_Done` **or** `2b_HMI_RFID_Done` | `%M21.1` vs `%M30.4` | Mismatch = Write_Pulse never completes |
| RFID Bereit (to Vision) | Prefer `RFID_Bereit` **or** `2b_HMI_RFID_Bereit` | `%M22.0` vs `%M30.0` | Mismatch = Allow_Write never fires Write_Req |

**Rule:** On Vision FB and `RFID_Read_Write_DB_1`, these four must be the **identical** tags:

`RFID_Bereit`, `RFID_Busy`, `RFID_Done`, `HMI_Reset` / `Reset`

Pick **one** set (recommended = RFID FB outputs at `%M21`/`%M22` + Reset `%M30.5` if that is your HMI button) and wire Vision to those same tags.

### Start write

| Pin | Tag | Address |
|---|---|---|
| Vision `Allow_Write` | `4b_Done(1)` | `%M10.0` |

### Product data into RFID FB

| RFID pin | Tag | Address |
|---|---|---|
| `RFID_Code_In` | `2b_VisionData_RFID_CODE` | `%MD42` |
| `Artikelnummer_In` | `2b_VisionData_Artikelnummer` | `%MW28` |
| `Materialart_In` | `2b_VisionData_Materialart` | `%MB46` |
| `ProductTyp_In` | `2b_VisionData_ProductType` | `%MW38` |

---

## 4) `RFID_Read_Write_DB_1` call checklist

| Pin | Must be |
|---|---|
| `HMI_Write` | `2b_HMI_RFID_Write` (`%M20.0`) — rising edge |
| `HMI_Reset` | `2b_HMI_RFID_Reset` (`%M30.5`) |
| `RFID_Lesen` | `FALSE` on write instance |
| `Op_Mode` | `10` is OK (unused when `HMI_Write` forces Job **11**) |
| `Command_ID` / `Status` / `Read_Data` | Reader **2** `%ED138/130/134` |
| `Execute_Command` … | Reader **2** `%A11.1`, `%AD104/108/112` |
| `Timeout` | `T#2S` (or `T#5S` while debugging FIO) |
| Product `*_In` | Vision tags above |
| `Busy`/`Done`/`Error`/`Bereit` | Shared with Vision |

Do **not** leave `Tag_Present` / lamps forced to constant `false` on outputs.

---

## 5) Two readers — do not mix

| Instance | Hardware | Job |
|---|---|---|
| `RFID_Read_Write_DB_1` | **4b Reader 2** | WRITE after `4b_Done` |
| `RFID_Read_Write_DB_2` | **5b Reader 5** | READ at warehouse State 10 |

Wrong pairing (Execute on Reader 2, CmdID from Reader 5) → always Status **10**.

Reader 5 map:

| Signal | Address |
|---|---|
| Status / Read / CmdID | `%ED150` / `%ED154` / `%ED158` |
| Execute | `%A13.7` |
| Command / Write / Index | `%AD124` / `%AD128` / `%AD132` |

Also: move `5b_RFID_Lesen` off `%M0.0` → `%M65.0`.

---

## 6) Process order (when handshake works)

```
Vision Both_Ready (data stamped)
        ↓
4b_Done(1) = TRUE  →  Allow_Write
        ↓
Write_Req / 2b_HMI_RFID_Write pulse
        ↓
RFID Job 11 → Cmd 0 (tag present) → Cmd 3×4 (write indexes 0..3)
        ↓
Command ID increments each step
        ↓
Pallet_Tagged / Combo_Done
```

If `4b_Done` is TRUE but Vision never got Both_Ready → no Write_Req (normal).  
If Error latched → no Write_Req even with Done (Status 10).

---

## 7) Status codes quick reference

| Code | Meaning |
|---|---|
| 0 | OK |
| 1 | No tag in field (FIO) |
| 2 | Too many tags |
| 3 | Bad memory index |
| 4 | Bad command |
| **10** | **PLC timeout — CmdID never changed** |
| 11 | Bad Op_Mode / Job |

---

## 8) Fix order (do in sequence)

1. ☐ Pulse `2b_HMI_RFID_Reset` — clear Error  
2. ☐ Unify Vision ↔ RFID Busy/Done/Bereit/Reset tags (one set)  
3. ☐ Confirm Reader 2 FIO addresses (table §2)  
4. ☐ FIO running + PLC connected; tag under Reader 2  
5. ☐ Manual CHECK → CmdID increments  
6. ☐ Vision Both_Ready + `4b_Done(1)` → Write → CmdID moves → Gueltig/Pallet_Tagged  
7. ☐ Only then warehouse Reader 5 read path  

---

## 9) Recommended shared Merker set (plastic write)

Use this consistently on Vision + `RFID_Read_Write_DB_1`:

| Signal | Tag | Address |
|---|---|---|
| Write | `2b_HMI_RFID_Write` | `%M20.0` |
| Reset | `2b_HMI_RFID_Reset` | `%M30.5` |
| Busy | `RFID_Busy` | `%M21.0` |
| Done | `RFID_Done` | `%M21.1` |
| Error | `RFID_Error` | `%M21.2` |
| Bereit | `RFID_Bereit` | `%M22.0` |
| Gueltig | `RFID_Gueltig` | `%M22.1` |
| Fehler | `RFID_Fehler` | `%M22.2` |
| Status_Code | `RFID_Status_Code` | `%MW44` |
| Allow_Write | `4b_Done(1)` | `%M10.0` |

If HMI still shows `2b_HMI_RFID_Busy/Done/Bereit` on `%M30.x`, either retarget HMI to `%M21`/`%M22` **or** wire Vision/RFID FB to the `%M30` tags — but not mixed.
