# PLC tags — VisionSensorData (FB17 / VisionFID_DB)

Use these for the Vision call in TIA. Names follow your `2a_` / `2b_` style.

**Instance:** `%DB82 "VisionFID_DB"`  
**FB:** `%FB17 "VisionSensorData"` (repo: `FB_VisionReader`)

---

## Factory I/O → Vision (inputs)

| Tag name | Type | Address (yours) | FB pin | Comment |
|---|---|---|---|---|
| `2b_Vision Sensor Lid ( Value)` | DInt | `%ED142` / `%ID142` | `Vision_Lid_Value` | All Numerical |
| `2b_Vision Sensor Base( Value)` | DInt | `%ED146` / `%ID146` | `Vision_Base_Value` | All Numerical |
| `4b_Done(1)` | Bool | `%M10.0` | `Allow_Write` | After assembly — arm RFID write |
| — | — | — | — | Vision cameras: **3B 2-axis P&P** infeed (pre-assembly) |

---

## RFID handshake → Vision (inputs)

Wire from **RFID FB outputs** (not from HMI lamps only):

| Tag name | Type | Address (yours) | Vision pin | From RFID pin |
|---|---|---|---|---|
| `2a_HMI_RFID_Bereit` | Bool | `%M30.0` | `RFID_Bereit` | `RFID_Bereit` OUT |
| `2a_HMI_RFID_Busy` | Bool | `%M30.1` | `RFID_Busy` | `Busy` OUT |
| `2a_HMI_RFID_Done` | Bool | `%M30.4` | `RFID_Done` | `Done` OUT |
| `2a_HMI_RFID_Reset` | Bool | `%M30.5` | `Reset` | same as RFID `HMI_Reset` |

---

## Vision → product data (outputs) → RFID `*_In`

| Tag name | Type | Address (yours) | Vision pin | RFID pin |
|---|---|---|---|---|
| `2a_VisionData_Artikelnumber` | UInt | `%MW28` | `Artikelnummer` | `Artikelnummer_In` |
| `2a_VisionData_ProductType` | UInt | `%MW38` | `ProductTyp` | `ProductTyp_In` |
| `2a_VisionData_RFID_CODE` | UDInt | `%MD42` | `RFID_Code` | `RFID_Code_In` |
| `2a_VisionData_Materialart` | USInt | *assign e.g. `%MB46`* | `Materialart` | `Materialart_In` |

---

## Vision → write pulse (output)

| Tag name | Type | Address (yours) | Vision pin | RFID pin |
|---|---|---|---|---|
| `2a_HMI_RFID_Write` | Bool | `%M20.0` | `Write_Req` | `HMI_Write` |

---

## Vision status (outputs — optional for HMI)

| Tag name | Type | Suggest address | Vision pin |
|---|---|---|---|
| `2a_VisionData_Combo_Done` | Bool | `%M40.0` | `Combo_Done` |
| `2a_VisionData_Both_Ready` | Bool | `%M40.1` | `Both_Ready` |
| `2a_VisionData_Busy` | Bool | `%M40.2` | `Busy` |
| `2a_VisionData_Error` | Bool | `%M40.3` | `Error` |
| `2a_VisionData_State` | Int | `%MW48` | `State` |
| `2a_VisionData_Color_Code` | USInt | `%MB50` | `Color_Code` |
| `2a_VisionData_Latch_Lid` | Int | `%MW52` | `Latch_Lid` |
| `2a_VisionData_Latch_Base` | Int | `%MW54` | `Latch_Base` |
| `2a_Vision_Lid_Valid` | Bool | `%M40.4` | `Lid_Valid` |
| `2a_Vision_Base_Valid` | Bool | `%M40.5` | `Base_Valid` |
| `2a_Vision_Lid_Reject_Metal` | Bool | `%M40.6` | `Lid_Reject_Metal` |
| `2a_Vision_Base_Reject_Metal` | Bool | `%M40.7` | `Base_Reject_Metal` |

---

## Constants on your call

| Pin | Your value | Note |
|---|---|---|
| `Enable` | `True` | OK |
| `Part_Present` | `false` | Not used in repo v2.2 — leave false or delete pin |

---

## Minimum wiring (must have)

```
Enable                    := True
Vision_Lid_Value          := "2b_Vision Sensor Lid ( Value)"
Vision_Base_Value         := "2b_Vision Sensor Base( Value)"
Allow_Write               := "4b_Done(1)"                  // write after assembly
RFID_Bereit               := "2b_HMI_RFID_Bereit"          // %M30.0
RFID_Busy                 := "2b_HMI_RFID_Busy"            // %M30.1
RFID_Done                 := "2b_HMI_RFID_Done"            // %M30.4
Reset                     := "2b_HMI_RFID_Reset"           // %M30.5

Artikelnummer             => "2b_VisionData_Artikelnumber"
ProductTyp                => "2b_VisionData_ProductType"
RFID_Code                 => "2b_VisionData_RFID_CODE"
Materialart               => "2b_VisionData_Materialart"
Write_Req                 => "2b_HMI_RFID_Write"           // %M20.0 only
Combo_Done                => "2b_VisionData_Combo_Done"
```

On RFID FB: same product tags on `*_In`, and `HMI_Write := "2b_HMI_RFID_Write"`.  
`HMI_Read` / `Check` / `Clear` = FALSE for automatic production.
