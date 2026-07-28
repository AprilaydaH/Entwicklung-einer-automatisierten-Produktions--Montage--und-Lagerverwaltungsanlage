# Variablenübersicht — Pick & Place 2-Axis SCL

## 1. FB_Axis_Analog

### VAR_INPUT
| Name | Typ | Beschreibung |
|---|---|---|
| Enable | Bool | Achse freigeben |
| Start | Bool | Flanke: Target anfahren |
| Reset | Bool | Abbruch / Idle |
| Target | Real | Zielposition |
| Ist | Real | Istposition |
| Moving | Bool | Achse bewegt sich |
| Tol | Real | Toleranz (Default 0.05) |
| Ramp_Limit | Real | 0 = Sprung; sonst max. Delta/Zyklus |

### VAR_OUTPUT
| Name | Typ | Beschreibung |
|---|---|---|
| Busy / Done / Error | Bool | Status |
| ErrorCode | UInt | Reserve |
| AO_Target | Real | Sollwert an Factory I/O |

---

## 2. FB_Axis_Digital

### VAR_INPUT
| Name | Typ | Beschreibung |
|---|---|---|
| Enable / Start / Reset | Bool | Steuerung |
| Target_Pos | USInt | 0..3 Positions-ID |
| Sensor_At_0..3 | Bool | Endlagen / Pos-Bits |
| Current_Guess | USInt | Fallback wenn kein Sensor |
| Timeout_Ms | Time | Default 10 s (0 = aus) |

### VAR_OUTPUT
| Name | Typ | Beschreibung |
|---|---|---|
| DO_Plus / DO_Minus | Bool | Fahrbefehle |
| At_Target | Bool | Sensor am Ziel |
| ErrorCode | UInt | 1001 Timeout, 1002 ungültig |

---

## 3. FB_Gripper

### VAR_INPUT
| Name | Typ | Beschreibung |
|---|---|---|
| Grab / Release | Bool | Flanken |
| Item_Detected | Bool | Greifer-Sensor |
| Grab_Delay / Release_Delay | Time | Default 300 ms |
| Timeout_Ms | Time | Default 3 s |

### VAR_OUTPUT
| Name | Typ | Beschreibung |
|---|---|---|
| DO_Gripper | Bool | Magnet / Greifer |
| Has_Item | Bool | Teil gegriffen |
| ErrorCode | UInt | 2001 / 2002 |

---

## 4. FB_PickPlace_2Axis

Wesentliche Inputs: Modi, HMI Start/Stop/Reset, Hand-Jog, Teach, Factory-I/O-Sensoren, `Achs_Modus`, Teach-Punkte.

Wesentliche Outputs: `State`, `Busy`, `Done_Cycle`, `ErrorCode`, Conveyor/Gripper, Analog-Targets, Digital +/- .

### States (Auto)

| State | Bedeutung |
|---|---|
| 0 | Idle |
| 10 | Entry-Band bis Sensor |
| 20/21 | X Pick + Z Up |
| 30/31 | Z Down Pick |
| 40/41 | Grab |
| 50/51 | Z Up |
| 60/61 | X Place + Z Up |
| 70/71 | Z Down Place |
| 80/81 | Release |
| 90/91 | Z Up |
| 100/101 | Exit-Band + Home |
| 110 | Done → Idle |
| 200 | Fehler |

### ErrorCodes

| Code | Bedeutung |
|---|---|
| 1001 | Achse Digital Timeout |
| 1002 | Ungültiges Digital-Target |
| 2001 | Grab Timeout |
| 2002 | Release Timeout |
| 9001 | Not-Aus |

---

## 5. Globale DBs

### gldb_FactoryIO_IO (`UDT_FactoryIO_IO`)
Siehe `FACTORY_IO_IO.md` und `scl/gldb_FactoryIO_IO.udt.txt`.

### gldb_Config (`UDT_PickPlace_Config`)

| Name | Typ | Default-Vorschlag |
|---|---|---|
| Achs_Modus | USInt | 0 (Analog) |
| Tol_X / Tol_Z | Real | 0.05 |
| Pos.Home_X/Z | Real | teachen |
| Pos.Pick_X/Z / Pick_Z_Up | Real | teachen |
| Pos.Place_X/Z / Place_Z_Up | Real | teachen |

### HMI-Tags (Bool / Status)

`Mode_Auto`, `Mode_Hand`, `Mode_Einricht`, `HMI_Start`, `HMI_Stop`, `HMI_Reset`, Jog/Teach/Goto, `HMI_Busy`, `HMI_Done`, `HMI_Error`, `HMI_ErrorCode`, `HMI_State`
