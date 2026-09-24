# HMI — Vision + RFID (Kunststoff / 4b)

**Goal:** Operator screen to Reset → Check → Write → Read before warehouse go-live.  
**Panel:** WinCC Comfort / Unified (same style as Zone 4).  
**PLC:** `VisionFID_DB` + `RFID_Read_Write_DB_1`

Use **your live names** (`2b_…`). Where a tag is missing in TIA, create it with the address below.

---

## 1. Screen layout (one page)

```
┌─────────────────────────────────────────────────────────────────────┐
│  ZONE 5a · Vision + RFID (Plastic)          [Ready][Run][Done][Err] │
├──────────────────────────┬──────────────────────────────────────────┤
│  PRODUCT (from Vision)   │  TAG (from RFID Read)                    │
│  Artikelnummer   ####    │  Serial           ####                   │
│  RFID_CODE       ####    │  RFID_CODE_Out    ####                   │
│  Materialart     #       │  Artikel_Out      ####                   │
│  ProductTyp      ##      │  Material_Out     #                      │
│  Color           #       │  ProductTyp_Out   ##                     │
│  Both_Ready  ○  Combo ○  │  Tag_Present ○  Gueltig ○                │
├──────────────────────────┴──────────────────────────────────────────┤
│  COMMANDS (momentary)                                               │
│  [ Zurücksetzen ]  [ Prüfen ]  [ Schreiben ]  [ Lesen ]  [ Löschen ] │
│                                                                     │
│  Status_Code: ##     State: ##     Busy ○                          │
│  FIO: Cmd ##  CmdID ##  WriteData ##  Execute ○                    │
└─────────────────────────────────────────────────────────────────────┘
```

Header lamps = RFID `HMI_Lamp_*` (Ready / Running / Done / Error).

---

## 2. Create / bind PLC tags (HMI folder)

### 2.1 Commands — HMI → PLC (momentary)

| HMI object | PLC tag | Address | FB pin | Notes |
|---|---|---|---|---|
| **Zurücksetzen** | `2b_HMI_RFID_Reset` | `%M30.5` | `HMI_Reset` + Vision `Reset` | Clears Error / Status 10 |
| **Prüfen** | `2b_HMI_RFID_Check` | `%M20.2` | `HMI_Check` | **Create if missing** |
| **Schreiben** | `2b_HMI_RFID_Write` | `%M20.0` | `HMI_Write` | Shared with Vision `Write_Req` |
| **Lesen** | `2b_HMI_RFID_Read` | `%M20.1` | `HMI_Read` | **Create if missing** |
| **Löschen** | `2b_HMI_RFID_Clear` | `%M20.3` | `HMI_Clear` | Optional |

**WinCC button config (all five):**
- Event **Press** → `SetBit` on tag  
- Event **Release** → `ResetBit` on tag  
- Or: “Set bit while pressed”  
Do **not** use latching switches — FB needs a rising edge.

Wire on RFID call (if still open):
```
HMI_Check := "2b_HMI_RFID_Check"
HMI_Read  := "2b_HMI_RFID_Read"
HMI_Write := "2b_HMI_RFID_Write"
HMI_Clear := "2b_HMI_RFID_Clear"
HMI_Reset := "2b_HMI_RFID_Reset"
```

### 2.2 Product live — Vision → HMI (IO field, read-only)

| Display | PLC tag | Address |
|---|---|---|
| Artikelnummer | `2b_VisionData_Artikelnummer` | `%MW28` |
| RFID_CODE | `2b_VisionData_RFID_CODE` | `%MD42` |
| Materialart | `2b_VisionData_Materialart` | `%MB46` |
| ProductTyp | `2b_VisionData_ProductType` | `%MW38` |
| Color_Code | `2b_VisionData_Color_Code` | `%MB50` *(create if missing)* |
| Both_Ready | `2b_VisionData_Both_Ready` | `%M40.1` |
| Combo_Done | `2b_VisionData_Combo_Done` | `%M40.0` |

### 2.3 Tag readback — RFID → HMI

| Display | PLC tag | Address | Create if missing |
|---|---|---|---|
| Tag_Present | `2b_RFID_Tag_Present` | `%M21.3` | yes |
| Serial_Number | `2b_RFID_Serial_Number` | `%MD48` | yes |
| RFID_CODE_Out | `2b_RFID_Code_Out` | `%MD56` | yes |
| Artikel_Out | `2b_RFID_Artikelnummer_Out` | `%MW60` | yes |
| Material_Out | `2b_RFID_Materialart_Out` | `%MB62` | yes |
| ProductTyp_Out | `2b_RFID_ProductTyp_Out` | `%MW64` | yes |
| Gueltig | `2b_RFID_Gueltig` | `%M22.1` | yes |

Map these from RFID FB outputs (`Tag_Present`, `Serial_Number`, `RFID_Code_Out`, …).

### 2.4 Status / lamps

| Object | PLC tag | Address | Source pin |
|---|---|---|---|
| Lamp Ready | `2b_RFID_Lamp_Ready` | `%M21.4` | `HMI_Lamp_Ready` |
| Lamp Running | `2b_RFID_Lamp_Running` | `%M21.5` | `HMI_Lamp_Running` |
| Lamp Done | `2b_RFID_Lamp_Done` | `%M21.6` | `HMI_Lamp_Done` |
| Lamp Error | `2b_RFID_Lamp_Error` | `%M21.7` | `HMI_Lamp_Error` |
| Status_Code | `2b_RFID_Status_Code` | `%MW44` | `Status_Code` |
| State | `2b_RFID_State` | `%MW42` | `State` |
| Busy | `2b_RFID_Busy` | `%M21.0` | `Busy` |
| Bereit | `2b_RFID_Bereit` | `%M22.0` *(or your `%M30.0`)* | `RFID_Bereit` → also Vision in |

**Status_Code text list (IO field or text list):**

| Code | Text |
|---:|---|
| 0 | OK |
| 1 | No tag |
| 2 | Too many tags |
| 3 | Bad index |
| 4 | Bad command |
| 7 | RFID_CODE missing |
| 10 | **Timeout (FIO handshake)** |
| 11 | Bad Op_Mode |

### 2.5 Diagnostics (optional strip)

| Display | PLC / FIO tag | Address |
|---|---|---|
| Command | `4b_RFID Reader 2 Command` | `%AD104` / `%QD104` |
| Command_ID | `4b_RFID Reader 2 Command ID` | `%ED138` / `%ID138` |
| Write Data | `4b_RFID Reader 2 Write Data` | `%AD108` / `%QD108` |
| Execute | `4b_RFID Reader 2 Execute Command` | `%A11.1` / `%Q11.1` |
| Status (FIO) | `4b_RFID Reader 2 Status` | `%ED130` |

---

## 3. Operator sequence (use this on the screen)

1. **RESET** — wait until Error lamp OFF, Ready ON, Status_Code = 0  
2. Pallet with tag under **4b** reader  
3. **CHECK** — Tag_Present ON; if Status 10 → FIO link broken  
4. Vision: Both_Ready ON, product numbers filled  
5. **WRITE** — Running then Done; Write Data shows values  
6. **READ** — Tag panel shows Artikel / CODE / Material / Typ; Gueltig ON  
7. Combo_Done ON → pallet ready for warehouse sensor  

---

## 4. Colors (simple)

| Lamp | ON color |
|---|---|
| Ready | Green |
| Running | Yellow |
| Done | Blue |
| Error | Red |
| Tag_Present / Gueltig / Combo_Done | Green |
| Both_Ready | Green |

---

## 5. TIA checklist before first test

- [ ] All five command tags exist and are wired on RFID FB  
- [ ] Buttons = momentary (press/release), not toggles  
- [ ] Status lamps wired from RFID outputs (not fixed FALSE)  
- [ ] Product IO fields bound to `%MW28` / `%MD42` / `%MB46` / `%MW38`  
- [ ] Reset also connected to Vision `Reset`  
- [ ] Simulation: PLC online + HMI runtime (or TIA HMI simulation)
- [ ] FB v1.2: wire `Write_Preview` + `Pallet_Tagged` to HMI
- [ ] If Status_Code=10: test Reader 2 in Factory I/O Drivers (Command=0, toggle Execute → Command ID +1)

---

## 6. Related

| File | Role |
|---|---|
| [`TAGS_VisionSensorData.md`](TAGS_VisionSensorData.md) | Vision pin map |
| [`PLC_Tags_RFID.csv`](PLC_Tags_RFID.csv) | Full tag import |
| [`FB_RFID_ReadWrite.scl`](FB_RFID_ReadWrite.scl) | Handshake / Status 10 / Write_Preview |
| [HMI Gesamtanlage](../../docs/03_Technik/HMI_Gesamtanlage.md) | Plant HMI overview |
