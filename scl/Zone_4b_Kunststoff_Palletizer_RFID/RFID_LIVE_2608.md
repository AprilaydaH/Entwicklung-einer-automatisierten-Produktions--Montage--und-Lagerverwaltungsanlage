# RFID live map — from PLCTags26.08.xlsx

Export saved as [`PLC_Tags_from_TIA_2608.csv`](PLC_Tags_from_TIA_2608.csv).

## Root cause of Status_Code 10 + broken handshake

Your project has **no** tags named `RFID_Busy`, `RFID_Done`, `RFID_Bereit`, `RFID_Error`, `RFID_Gueltig`, `RFID_Pallet_Tagged`.

Handshake status lives only here:

| Role | Tag in TIA | Address |
|---|---|---|
| Bereit | `2b_HMI_RFID_Bereit` | `%M30.0` |
| Busy | `2b_HMI_RFID_Busy` | `%M30.1` |
| Done | `2b_HMI_RFID_Done` | `%M30.4` |
| Reset | `2b_HMI_RFID_Reset` | `%M30.5` |

If Vision or `RFID_Read_Write_DB_1` still uses missing `RFID_Busy` / `RFID_Done` / `RFID_Bereit`, the write chain is broken and you get timeouts / stuck Error.

---

## Wire `RFID_Read_Write_DB_1` like this (WRITE / Reader 2)

### Inputs

| Pin | Tag | Address |
|---|---|---|
| HMI_Write | `2b_HMI_RFID_Write` | `%M20.0` |
| HMI_Reset | `2b_HMI_RFID_Reset` | `%M30.5` |
| HMI_Read / Check / Clear | create or FALSE | — |
| RFID_Lesen | FALSE | — |
| Op_Mode | 10 | — |
| Command_ID | `4b_RFID Reader 2 Command ID` | `%ED138` |
| Status | `4b_RFID Reader 2 Status` | `%ED130` |
| Read_Data | `4b_RFID Reader 2 Read Data` | `%ED134` |
| RFID_Code_In | `2b_VisionData_RFID_CODE` | `%MD42` |
| Artikelnummer_In | `2b_VisionData_Artikelnumber` | `%MW28` |
| Materialart_In | `2b_VisionData_Materialart` | `%MB46` |
| ProductTyp_In | `2b_VisionData_ProductType` | `%MW38` |
| Timeout | T#5S (debug) / T#2S | — |

### Outputs

| Pin | Tag | Address |
|---|---|---|
| Execute_Command | `4b_RFID Reader 2 Execute Command` | `%A11.1` |
| Command | `4b_RFID Reader 2 Command` | `%AD104` |
| Write_Data_Out | `4b_RFID Reader 2 Write Data` | `%AD108` |
| Memory_Index_Out | `4b_RFID Reader 2 Memory Index` | `%AD112` |
| Busy | **`2b_HMI_RFID_Busy`** | `%M30.1` |
| Done | **`2b_HMI_RFID_Done`** | `%M30.4` |
| Error | create `RFID_Error` or spare Bool | e.g. `%M30.2` |
| RFID_Bereit | **`2b_HMI_RFID_Bereit`** | `%M30.0` |
| RFID_Gueltig | create `RFID_Gueltig` | e.g. `%M30.3` |
| RFID_Fehler | create `RFID_Fehler` | e.g. `%M30.6` |
| Status_Code | create `RFID_Status_Code` | e.g. `%MW44` |
| Pallet_Tagged | **`2b_HMI_RFID_Pallet_Tagged`** | `%M40.2` — NOT Tag_Present |

---

## Wire Vision FB like this

| Pin | Tag |
|---|---|
| Allow_Write | `4b_Done(1)` `%M10.0` — write after P&P assembly |
| RFID_Bereit | `2b_HMI_RFID_Bereit` |
| RFID_Busy | `2b_HMI_RFID_Busy` |
| RFID_Done | `2b_HMI_RFID_Done` |
| Reset | `2b_HMI_RFID_Reset` |
| Write_Req ⇒ | **`2b_HMI_RFID_Write`** `%M20.0` (same as RFID HMI_Write) |
| RFID_Code ⇒ | `2b_VisionData_RFID_CODE` |
| Artikelnummer ⇒ | `2b_VisionData_Artikelnumber` |
| Materialart ⇒ | `2b_VisionData_Materialart` |
| ProductTyp ⇒ | `2b_VisionData_ProductType` |
| Both_Ready ⇒ | `2b_VisionData_Both_Ready` |
| Combo_Done ⇒ | `2b_VisionData_Combo_Done` |

**Important:** Do **not** use `2a_VisionData_Write_Req` `%M20.1` for RFID `HMI_Write` unless you also copy it to `%M20.0`. One write pulse bit only: **`%M20.0`**.

**Automatic (v2.3 + RFID v1.4):** no new FB. `HMI_Read`/`Check`/`Clear` = FALSE. Write retries while `4b_Done` and RFID not Busy; new Write clears Status 10.

---
## Also OK in this export

| Item | Status |
|---|---|
| Reader 2 FIO map | OK (`ED130/134/138`, `A11.1`, `AD104/108/112`) |
| Reader 5 FIO + `%M65` | OK for warehouse |
| `5b_RFID_Lesen` | Fixed at `%M65.0` |
| `4b_Done(1)` | `%M10.0` — use for Allow_Write |

## Still create if missing

`RFID_Error`, `RFID_Gueltig`, `RFID_Fehler`, `RFID_Status_Code`, `RFID_Pallet_Tagged`, optional Check/Clear/Read HMI bits.

---

## Fix order

1. Pulse `2b_HMI_RFID_Reset`  
2. Re-wire Vision + RFID DB_1 Busy/Done/Bereit → **`2b_HMI_RFID_*` @ M30**  
3. Write_Req and HMI_Write both → **`2b_HMI_RFID_Write` @ M20.0**  
4. Prove `%ED138` Command ID increments  
5. Then test `4b_Done(1)` auto write  
