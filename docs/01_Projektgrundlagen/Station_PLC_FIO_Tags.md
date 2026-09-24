# Stationen — SCL, FUP, SPS-Tags und Factory I/O

Quelle Tags: `PLCTags3.xlsx`. SCL: `scl/` im Repository.
CSV: [`PLCTags3_live.csv`](PLCTags3_live.csv).

**FIO** = Prozessabbild (`%E` / `%A` / `%ED` / `%AD` …) ↔ Factory I/O Driver.
**PLC** = Merker/DB (`%M` …) in der SPS.

Gesamt: **485** Tags.

| Station | FUP | SCL | Tags | FIO | PLC |
|---|---|---|---:|---:|---:|
| **1A** | NW 1–2 | `— (P)` | 6 | 6 | 0 |
| **1B** | NW 4, 6 | `— (P)` | 6 | 6 | 0 |
| **2A** | NW 3, 5 | `FB_VisionReader_Metal.scl` | 31 | 12 | 19 |
| **2B** | NW 7–8 | `FB_VisionReader.scl` | 31 | 13 | 18 |
| **2A/2B Band** | NW 3 / 8 / 26 / 27 | `—` | 9 | 4 | 5 |
| **3A** | NW 9–12 | `PickPlace_DigitalAnalog.scl` | 33 | 32 | 1 |
| **3B** | NW 17–20 | `PickPlace_DigitalAnalog.scl (2.)` | 36 | 35 | 1 |
| **4A** | NW 13–16, 21 | `FB_GantryPickPlace.scl · RFID` | 83 | 30 | 53 |
| **4B** | NW 22–25 | `FB_Palletizer.scl · FB_RFID_ReadWrite.scl` | 29 | 29 | 0 |
| **5A** | NW 26, 28 Warehouse_2 | `Hochregal_Automatik_Betrieb_W2.scl · FB_*_W2` | 108 | 35 | 73 |
| **5B** | NW 27, 29 Warehouse_1 | `Hochregal_Automatik_Betrieb.scl · Warehouse_1 FBs` | 111 | 33 | 78 |
| **Standard-Variablentabelle** | — | `—` | 2 | 1 | 1 |

## 1A

FUP: NW 1–2 · Tags: 6 (Factory I/O 6 · SPS 0)

### SCL

- (kein FB — geplant) scl/Zone_1a_Metall/

### Factory I/O (6)

| Tag | Adresse | Typ | Tabelle | Kommentar |
|---|---|---|---|---|
| `1a_Emitter_1_Emit` | `%A0.0` | Bool | Standard-Variablentabelle | 1a \| Factory I/O: 1a_Emitter 1 (Emit) |
| `1a_Emitter_2_Emit` | `%A0.1` | Bool | Standard-Variablentabelle | 1a \| Factory I/O: 1a_Emitter 2 (Emit) |
| `1a_M_C_1_AN_WESEND_Belt_Conveyor_2m` | `%A0.2` | Bool | Standard-Variablentabelle | 1a \| Factory I/O: 1a_M_C_1_AN_WESEND_Belt Conveyor (2m) |
| `1a_M_C_ANWESEND_Belt_Conveyor_2m` | `%A0.3` | Bool | Standard-Variablentabelle | 1a \| Factory I/O: 1a_M_C_ANWESEND_Belt Conveyor (2m) |
| `1a_M_C_0_ANWESEND_Sensor` | `%E0.0` | Bool | Standard-Variablentabelle | 1a \| Factory I/O: 1a_M_C_0_ANWESEND_Sensor |
| `1a_M_C_1_ANWESEND_Sensor` | `%E0.1` | Bool | Standard-Variablentabelle | 1a \| Factory I/O: 1a_M_C_1_ANWESEND_Sensor |

### SPS / PLC-Merker (0)

*(keine)*

## 1B

FUP: NW 4, 6 · Tags: 6 (Factory I/O 6 · SPS 0)

### SCL

- (kein FB — geplant) scl/Zone_1b_Kunststoff/

### Factory I/O (6)

| Tag | Adresse | Typ | Tabelle | Kommentar |
|---|---|---|---|---|
| `1b_DC_0_Belt_Conveyor_2m` | `%A1.0` | Bool | Standard-Variablentabelle | 1b \| Factory I/O: 1b_DC_0_Belt_Conveyor(2m) |
| `1b_Emitter_5_Emit` | `%A1.1` | Bool | Standard-Variablentabelle | 1b \| Factory I/O: 1b_Emitter 5 (Emit) |
| `1b_raw_material_emitter_2` | `%A1.2` | Bool | Standard-Variablentabelle | 1b \| Factory I/O: 1b_raw_material_emitter__2 |
| `1b_DC_1_Belt Conveyor (2m)` | `%A1.3` | Bool | Forderband |  |
| `1b_plastic_raw_material_sensor_1` | `%E1.0` | Bool | Standard-Variablentabelle | 1b \| Factory I/O: 1b_plastic_raw_material_sensor_1 |
| `1b_Plastic_raw_material_sensor_2` | `%E1.1` | Bool | Standard-Variablentabelle | 1b \| Factory I/O: 1b_Plastic_raw_material_sensor_2 |

### SPS / PLC-Merker (0)

*(keine)*

## 2A

FUP: NW 3, 5 · Tags: 31 (Factory I/O 12 · SPS 19)

### SCL

- `scl/Zone_2a_Foerderbaender/FB_VisionReader_Metal.scl`
- `scl/Zone_2a_Foerderbaender/OB1_NW5_Metal_Vision.scl`

### Factory I/O (12)

| Tag | Adresse | Typ | Tabelle | Kommentar |
|---|---|---|---|---|
| `2a_After_DC_Our_0` | `%A2.0` | Bool | Standard-Variablentabelle | 2a \| Factory I/O: 2a_After_DC_Our_0 |
| `2a_After_MC_out_0` | `%A2.1` | Bool | Standard-Variablentabelle | 2a \| Factory I/O: 2a_After_MC_out_0 |
| `2a_After_Metal_MC_Base_Conveyor` | `%A2.2` | Bool | Standard-Variablentabelle | 2a \| Factory I/O: 2a_After_Metal_MC_Base_Conveyor |
| `2a_After_Metal_MC_Lid_Conveyor` | `%A2.3` | Bool | Standard-Variablentabelle | 2a \| Factory I/O: 2a_After_Metal_MC_Lid_Conveyor |
| `2a_Motor_Before_PP_Base` | `%A2.4` | Bool | Standard-Variablentabelle | 2a \| Factory I/O: 2a_Motor_Before_PP_Base |
| `2a_Motor_Before_PP_Lid` | `%A2.5` | Bool | Standard-Variablentabelle | 2a \| Factory I/O: 2a_Motor_Before_PP_Lid |
| `2a_Eck_Foerderband_MBase` | `%E2.0` | Bool | Standard-Variablentabelle | 2a \| Factory I/O: 2a_Eck_Foerderband_MBase |
| `2a_Eck_Foerderband_MLid` | `%E2.1` | Bool | Standard-Variablentabelle | 2a \| Factory I/O: 2a_Eck_Foerderband_MLid |
| `2a_Worked_Part_from_MC_out` | `%E2.2` | Bool | Standard-Variablentabelle | 2a \| Factory I/O: 2a_Worked_Part_from_MC_out |
| `2a_Worked_Part_from_MC_out_2` | `%E2.3` | Bool | Standard-Variablentabelle | 2a \| Factory I/O: 2a_Worked_Part_from_MC_out_2 |
| `2a_Vision Sensor Lid(Value)` | `%ED170` | DInt | 2a_VisionDataSensors |  |
| `2a_Vision Sensor Base(Value)` | `%ED174` | DInt | 2a_VisionDataSensors |  |

### SPS / PLC-Merker (19)

| Tag | Adresse | Typ | Tabelle | Kommentar |
|---|---|---|---|---|
| `2a_VisionData_Write_Req` | `%M20.1` | Bool | 2b_VisionDataSensors |  |
| `2a_Metal_VisionData_Combo_Done` | `%M56.0` | Bool | 2a_VisionDataSensors |  |
| `2a_Metal_VisionData_Both_Ready` | `%M56.1` | Bool | 2a_VisionDataSensors |  |
| `2a_Metal_VisionData_Busy` | `%M56.2` | Bool | 2a_VisionDataSensors |  |
| `2a_Metal_VisionData_Error` | `%M56.3` | Bool | 2a_VisionDataSensors |  |
| `2a_Metal_Vision_Lid_Valid` | `%M56.4` | Bool | 2a_VisionDataSensors | Code=8 |
| `2a_Metal_Vision_Base_Valid` | `%M56.5` | Bool | 2a_VisionDataSensors | Code=9 |
| `2a_Metal_Vision_Lid_Reject_Plastic` | `%M56.6` | Bool | 2a_VisionDataSensors | Code 1..6 |
| `2a_Metal_Vision_Base_Reject_Plastic` | `%M56.7` | Bool | 2a_VisionDataSensors | Code 1..6 |
| `2a_Metal_HMI_RFID_Write` | `%M57.0` | Bool | 2a_VisionDataSensors |  |
| `2a_Metal_Vision_Reset` | `%M57.1` | Bool | 2a_VisionDataSensors |  |
| `2a_Metal_VisionData_Waiting_For_Write` | `%M57.2` | Bool | 2a_VisionDataSensors |  |
| `2a_Metal_VisionData_Materialart` | `%MB284` | USInt | 2a_VisionDataSensors | Always 2=Metall |
| `2a_Metal_VisionData_Prod_Month` | `%MB288` | USInt | 2a_VisionDataSensors |  |
| `2a_Metal_VisionData_Prod_Day` | `%MB289` | USInt | 2a_VisionDataSensors |  |
| `2a_Metal_VisionData_RFID_CODE` | `%MD276` | UDInt | 2a_VisionDataSensors | Production date YYMMDD |
| `2a_Metal_VisionData_Artikelnummer` | `%MW250` | UInt | 2a_VisionDataSensors | Sequential article |
| `2a_Metal_VisionData_Prod_Year` | `%MW286` | UInt | 2a_VisionDataSensors |  |
| `2a_Metal_VisionData_State` | `%MW294` | Int | 2a_VisionDataSensors | 1 sense 2 write 3 done 4 wait |

## 2B

FUP: NW 7–8 · Tags: 31 (Factory I/O 13 · SPS 18)

### SCL

- `scl/Zone_2b_Vision_Foerderbaender/FB_VisionReader.scl`

### Factory I/O (13)

| Tag | Adresse | Typ | Tabelle | Kommentar |
|---|---|---|---|---|
| `2b_After_Plastic_DC_out_0` | `%A3.0` | Bool | Standard-Variablentabelle | 2b \| Factory I/O: 2b_After_Plastic_DC_out_0 |
| `2b_After_Plastic_MC_out_1` | `%A3.1` | Bool | Standard-Variablentabelle | 2b \| Factory I/O: 2b_After_Plastic_MC_out_1 |
| `2b_After_Plastic_MC_out_2` | `%A3.2` | Bool | Standard-Variablentabelle | 2b \| Factory I/O: 2b_After_Plastic_MC_out_2 |
| `2b_Curved_Belt_Conveyor_6_CW` | `%A3.3` | Bool | Standard-Variablentabelle | 2b \| Factory I/O: 2b_Curved Belt Conveyor 6 CW \| DUPLICATE source name - verify mapping |
| `2b_Curved_Belt_Conveyor_6_CW_2` | `%A3.4` | Bool | Standard-Variablentabelle | 2b \| Factory I/O: 2b_Curved Belt Conveyor 6 CW \| DUPLICATE source name - verify mapping |
| `2b_Curved_Belt_Conveyor_8_C2` | `%A3.5` | Bool | Standard-Variablentabelle | 2b \| Factory I/O: 2b_Curved Belt Conveyor 8 C2 |
| `2b_Eck_Foerderband_MLid` | `%A3.6` | Bool | Forderband |  |
| `2b_Worked_Part_from_MC_out_1` | `%E3.0` | Bool | Standard-Variablentabelle |  |
| `2b_Diffuse_Sensor_39` | `%E3.1` | Bool | Standard-Variablentabelle | 2b \| Factory I/O: 2b_Diffuse Sensor 39 |
| `2b_Diffuse_Sensor_42` | `%E3.2` | Bool | Standard-Variablentabelle | 2b \| Factory I/O: 2b_Diffuse Sensor 42 |
| `2b_Worked_Part_from_MC_out_2` | `%E3.3` | Bool | Standard-Variablentabelle |  |
| `2b_Vision Sensor Lid (Value)` | `%ED142` | DInt | 2b_VisionDataSensors |  |
| `2b_Vision Sensor Base(Value)` | `%ED146` | DInt | 2b_VisionDataSensors |  |

### SPS / PLC-Merker (18)

| Tag | Adresse | Typ | Tabelle | Kommentar |
|---|---|---|---|---|
| `2b_HMI_RFID_Write` | `%M20.0` | Bool | 2b_VisionDataSensors |  |
| `2b_HMI_RFID_Bereit` | `%M30.0` | Bool | 2b_VisionDataSensors |  |
| `2b_HMI_RFID_Busy` | `%M30.1` | Bool | 2b_VisionDataSensors |  |
| `2b_HMI_RFID_Error` | `%M30.2` | Bool | 2b_VisionDataSensors |  |
| `2b_HMI_RFID_Gueltig` | `%M30.3` | Bool | 2b_VisionDataSensors |  |
| `2b_HMI_RFID_Done` | `%M30.4` | Bool | 2b_VisionDataSensors |  |
| `2b_HMI_RFID_Reset` | `%M30.5` | Bool | 2b_VisionDataSensors |  |
| `2b_HMI_RFID_Fehler` | `%M30.6` | Bool | 2b_VisionDataSensors |  |
| `2b_VisionData_Combo_Done` | `%M40.0` | Bool | 2b_VisionDataSensors |  |
| `2b_VisionData_Both_Ready` | `%M40.1` | Bool | Forderband |  |
| `2b_HMI_RFID_Pallet_Tagged` | `%M40.2` | Bool | Standard-Variablentabelle |  |
| `2b_VisionData_Materialart` | `%MB46` | USInt | 2b_VisionDataSensors |  |
| `2b_VisionData_RFID_CODE` | `%MD42` | UDInt | 2b_VisionDataSensors |  |
| `2b_VisionData_Artikelnumber` | `%MW28` | UInt | 2b_VisionDataSensors |  |
| `2b_VisionData_ProductType` | `%MW38` | UInt | 2b_VisionDataSensors |  |
| `2b_HMI_RFID_Status_Code` | `%MW44` | Int | 2b_VisionDataSensors |  |
| `2b_VisionData_State` | `%MW48` | Int | Forderband |  |
| `2b_VisionData_Color_Code` | `%MW50` | Int | Forderband |  |

## 2A/2B Band

FUP: NW 3 / 8 / 26 / 27 · Tags: 9 (Factory I/O 4 · SPS 5)

### SCL

- (FUP-Bänder; SCL in der jeweiligen Zone)

### Factory I/O (4)

| Tag | Adresse | Typ | Tabelle | Kommentar |
|---|---|---|---|---|
| `Motor` | `%A0.4` | Bool | Forderband |  |
| `Weight_ok` | `%A5.5` | Bool | Forderband |  |
| `Aut_Start_Mode` | `%E5.5` | Bool | Forderband |  |
| `Waage0_Reset` | `%E5.7` | Bool | Forderband |  |

### SPS / PLC-Merker (5)

| Tag | Adresse | Typ | Tabelle | Kommentar |
|---|---|---|---|---|
| `Material_Art_In` | `%MB1` | USInt | Forderband |  |
| `Memory_Index` | `%MD2` | DInt | Forderband |  |
| `RFID_Code_IN` | `%MD22` | UDInt | Forderband |  |
| `ProductType_In` | `%MW26` | UInt | Forderband |  |
| `Artikelnummer_In` | `%MW6` | UInt | Forderband |  |

## 3A

FUP: NW 9–12 · Tags: 33 (Factory I/O 32 · SPS 1)

### SCL

- `scl/Zone_3a_Metall_PickPlace/PickPlace_DigitalAnalog.scl`

### Factory I/O (32)

| Tag | Adresse | Typ | Tabelle | Kommentar |
|---|---|---|---|---|
| `3a_Left_Positioner_2_Raise` | `%A4.0` | Bool | Standard-Variablentabelle | 3a \| Factory I/O: 3a_Left Positioner 2 (Raise) |
| `3a_Left_Positioner_Metal_Baugruppe_Clamp` | `%A4.1` | Bool | Standard-Variablentabelle | 3a \| Factory I/O: 3a_Left Positioner _Metal_Baugruppe(Clamp) |
| `3a_Motor_at_PP_Base` | `%A4.2` | Bool | Standard-Variablentabelle | 3a \| Factory I/O: 3a_Motor_at_PP_Base |
| `3a_Motor_at_PP_Lid` | `%A4.3` | Bool | Standard-Variablentabelle | 3a \| Factory I/O: 3a_Motor_at_PP_Lid |
| `3a_Nach_Waage_Curved_Belt_Conveyor_0_CW` | `%A4.4` | Bool | Standard-Variablentabelle | 3a \| Factory I/O: 3a_Nach_Waage_Curved Belt Conveyor 0 CW |
| `3a_Right_Lid_Positioner_0_Clamp` | `%A4.5` | Bool | Standard-Variablentabelle | 3a \| Factory I/O: 3a_Right_Lid_Positioner 0 (Clamp) |
| `3a_Right_Lid_Positioner_0_Raise` | `%A4.6` | Bool | Standard-Variablentabelle | 3a \| Factory I/O: 3a_Right_Lid_Positioner 0 (Raise) |
| `3a_Two_Axis_Pick_and_Place_0_Grab` | `%A4.7` | Bool | Standard-Variablentabelle | 3a \| Factory I/O: 3a_Two-Axis Pick & Place 0 (Grab) |
| `3a_Two_Axis_Pick_and_Place_0_Rotate_CW` | `%A5.0` | Bool | Standard-Variablentabelle | 3a \| Factory I/O: 3a_Two-Axis Pick & Place 0 Rotate CW |
| `3a_Two_Axis_Pick_and_Place_0_Gripper_CW` | `%A5.1` | Bool | Standard-Variablentabelle | 3a \| Factory I/O: 3a_Two-Axis Pick & Place 0 Gripper CW |
| `3a_Two_Axis_Pick_and_Place_0_Rotate_CCW` | `%A5.2` | Bool | Standard-Variablentabelle | 3a \| Factory I/O: 3a_Two-Axis Pick & Place 0 Rotate CCW |
| `3a_Two_Axis_Pick_and_Place_0_Gripper_CCW` | `%A5.3` | Bool | Standard-Variablentabelle | 3a \| Factory I/O: 3a_Two-Axis Pick & Place 0 Gripper CCW |
| `3a_Waage_Conveyor_Scale_0_Plus` | `%A5.4` | Bool | Standard-Variablentabelle | 3a \| Factory I/O: 3a_Waage_Conveyor Scale 0 (+) |
| `3a_Curved Belt Conveyor 5 CW` | `%A5.7` | Bool | Forderband |  |
| `3a_Two_Axis_Pick_and_Place_0_X_Set_Point_V` | `%AD16` | Real | Standard-Variablentabelle | 3a \| Factory I/O: 3a_Two-Axis Pick & Place 0 X Set Point (V) |
| `3a_Two_Axis_Pick_and_Place_0_Z_Set_Point_V` | `%AD20` | Real | Standard-Variablentabelle | 3a \| Factory I/O: 3a_Two-Axis Pick & Place 0 Z Set Point (V) |
| `3a_Baugruppe_Left_Positioner_2_Clamped` | `%E4.0` | Bool | Standard-Variablentabelle | 3a \| Factory I/O: 3a_Baugruppe_Left Positioner 2 (Clamped) |
| `3a_Part_Left_1` | `%E4.1` | Bool | Standard-Variablentabelle | 3a \| Factory I/O: 3a_Part_Left_1 |
| `3a_Right_Positioner_0_Limit` | `%E4.2` | Bool | Standard-Variablentabelle | 3a \| Factory I/O: 3a_Right Positioner 0 (Limit) |
| `3a_Right_Positioner_0_Clamped` | `%E4.3` | Bool | Standard-Variablentabelle | 3a \| Factory I/O: 3a_Right Positioner 0 (Clamped) |
| `3a_Sensor_at_PP_Base` | `%E4.4` | Bool | Standard-Variablentabelle | 3a \| Factory I/O: 3a_Sensor_at_PP_Base |
| `3a_Sensor_at_PP_Lid` | `%E4.5` | Bool | Standard-Variablentabelle | 3a \| Factory I/O: 3a_Sensor_at_PP_Lid |
| `3a_Sensor_Before_PP_Base` | `%E4.6` | Bool | Standard-Variablentabelle | 3a \| Factory I/O: 3a_Sensor_Before_PP_Base |
| `3a_Sensor_Before_PP_Lid` | `%E4.7` | Bool | Standard-Variablentabelle | 3a \| Factory I/O: 3a_Sensor_Before_PP_Lid |
| `3a_Two_Axis_Pick_and_Place_0_Moving_X` | `%E5.0` | Bool | Standard-Variablentabelle | 3a \| Factory I/O: 3a_Two-Axis Pick & Place 0 (Moving X) |
| `3a_Two_Axis_Pick_and_Place_0_Moving_Z` | `%E5.1` | Bool | Standard-Variablentabelle | 3a \| Factory I/O: 3a_Two-Axis Pick & Place 0 (Moving Z) |
| `3a_Two_Axis_Pick_and_Place_0_Rotating` | `%E5.2` | Bool | Standard-Variablentabelle | 3a \| Factory I/O: 3a_Two-Axis Pick & Place 0 (Rotating) |
| `3a_Two_Axis_Pick_and_Place_0_Item_Detected` | `%E5.3` | Bool | Standard-Variablentabelle | 3a \| Factory I/O: 3a_Two-Axis Pick & Place 0 (Item Detected) |
| `3a_Two_Axis_Pick_and_Place_0_Gripper_Rotating` | `%E5.4` | Bool | Standard-Variablentabelle | 3a \| Factory I/O: 3a_Two-Axis Pick & Place 0 (Gripper Rotating) |
| `3a_Two_Axis_Pick_and_Place_0_X_Position_V` | `%ED30` | Real | Standard-Variablentabelle | 3a \| Factory I/O: 3a_Two-Axis Pick & Place 0 X Position (V) |
| `3a_Two_Axis_Pick_and_Place_0_Z_Position_V` | `%ED34` | Real | Standard-Variablentabelle | 3a \| Factory I/O: 3a_Two-Axis Pick & Place 0 Z Position (V) |
| `3a_Waage_0_Weight_V` | `%ED38` | Real | Standard-Variablentabelle | 3a \| Factory I/O: 3a_Waage 0 Weight (V) |

### SPS / PLC-Merker (1)

| Tag | Adresse | Typ | Tabelle | Kommentar |
|---|---|---|---|---|
| `3a_Material_Placed_PP_Metal` | `%M0.2` | Bool | Standard-Variablentabelle |  |

## 3B

FUP: NW 17–20 · Tags: 36 (Factory I/O 35 · SPS 1)

### SCL

- `scl/Zone_3a_Metall_PickPlace/PickPlace_DigitalAnalog.scl (2. Instanz, NW 18)`

### Factory I/O (35)

| Tag | Adresse | Typ | Tabelle | Kommentar |
|---|---|---|---|---|
| `3b_Belt_Conveyor_2m_6` | `%A6.0` | Bool | Standard-Variablentabelle | 3b \| Factory I/O: 3b_Belt Conveyor (2m) 6 |
| `3b_Belt_Conveyor_2m_13` | `%A6.1` | Bool | Standard-Variablentabelle | 3b \| Factory I/O: 3b_Belt Conveyor (2m) 13 |
| `3b_Conveyor_Scale_2_Plus` | `%A6.2` | Bool | Standard-Variablentabelle | 3b \| Factory I/O: 3b_Conveyor Scale 2 (+) |
| `3b_Conveyor_Scale_2` | `%A6.3` | Bool | Standard-Variablentabelle | 3b \| Factory I/O: 3b_Conveyor Scale 2 (-) |
| `3b_Left_Positioner_1_Clamp` | `%A6.4` | Bool | Standard-Variablentabelle | 3b \| Factory I/O: 3b_Left Positioner 1 (Clamp) |
| `3b_Left_Positioner_1_Raise` | `%A6.5` | Bool | Standard-Variablentabelle | 3b \| Factory I/O: 3b_Left Positioner 1 (Raise) \| DUPLICATE source name - verify mapping |
| `3b_Right_Positioner_3_Clamp` | `%A6.6` | Bool | Standard-Variablentabelle | 3b \| Factory I/O: 3b_Right Positioner 3 (Clamp) |
| `3b_Right_Positioner_1_Raise` | `%A6.7` | Bool | Standard-Variablentabelle | 3b \| Factory I/O: 3b_Left Positioner 1 (Raise) \| DUPLICATE source name - verify mapping |
| `3b_Two_Axis_Pick_and_Place_1_Grab` | `%A7.0` | Bool | Standard-Variablentabelle | 3b \| Factory I/O: 3b_Two-Axis Pick & Place 1 (Grab) |
| `3b_Two_Axis_Pick_and_Place_1_Rotate_CW` | `%A7.1` | Bool | Standard-Variablentabelle | 3b \| Factory I/O: 3b_Two-Axis Pick & Place 1 Rotate CW |
| `3b_Two_Axis_Pick_and_Place_1_Rotate_CCW` | `%A7.2` | Bool | Standard-Variablentabelle | 3b \| Factory I/O: 3b_Two-Axis Pick & Place 1 Rotate CCW \| DUPLICATE source name - verify mapping |
| `3b_Two_Axis_Pick_and_Place_1_Rotate_CCW_2` | `%A7.3` | Bool | Standard-Variablentabelle | 3b \| Factory I/O: 3b_Two-Axis Pick & Place 1 Rotate CCW \| DUPLICATE source name - verify mapping |
| `3b_Two_Axis_Pick_and_Place_1_Gripper_CCW` | `%A7.4` | Bool | Standard-Variablentabelle | 3b \| Factory I/O: 3b_Two-Axis Pick & Place 1 Gripper CCW |
| `3b_stack_light` | `%A7.5` | Bool | Forderband |  |
| `3b_NAch_Waage_Curved_Belt` | `%A7.6` | Bool | Forderband |  |
| `3b_Two-Axis Pick & Place 1 X Set Point (V)` | `%AD28` | Real | Forderband |  |
| `3b_Two-Axis Pick & Place 1 Z Set Point (V)` | `%AD32` | Real | Forderband |  |
| `3b_Diffuse_Sensor_36` | `%E6.0` | Bool | Standard-Variablentabelle | 3b \| Factory I/O: 3b_Diffuse Sensor 36 |
| `3b_Diffuse_Sensor_38` | `%E6.1` | Bool | Standard-Variablentabelle | 3b \| Factory I/O: 3b_Diffuse Sensor 38 |
| `3b_Diffuse_Sensor_40` | `%E6.2` | Bool | Standard-Variablentabelle | 3b \| Factory I/O: 3b_Diffuse Sensor 40 |
| `3b_Left_Positioner_1_Limit` | `%E6.3` | Bool | Standard-Variablentabelle | 3b \| Factory I/O: 3b_Left Positioner 1 (Limit) |
| `3b_Left_Positioner_1_Clamped` | `%E6.4` | Bool | Standard-Variablentabelle | 3b \| Factory I/O: 3b_Left Positioner 1 (Clamped) |
| `3b_Right_Positioner_3_Limit` | `%E6.5` | Bool | Standard-Variablentabelle | 3b \| Factory I/O: 3b_Right Positioner 3 (Limit) |
| `3b_Right_Positioner_3_Clamped` | `%E6.6` | Bool | Standard-Variablentabelle | 3b \| Factory I/O: 3b_Right Positioner 3 (Clamped) |
| `3b_Two_Axis_Pick_and_Place_1_Moving_X` | `%E6.7` | Bool | Standard-Variablentabelle | 3b \| Factory I/O: 3b_Two-Axis Pick & Place 1 (Moving X) |
| `3b_Two_Axis_Pick_and_Place_1_Moving_Z` | `%E7.0` | Bool | Standard-Variablentabelle | 3b \| Factory I/O: 3b_Two-Axis Pick & Place 1 (Moving Z) |
| `3b_Two_Axis_Pick_and_Place_1_Rotating` | `%E7.1` | Bool | Standard-Variablentabelle | 3b \| Factory I/O: 3b_Two-Axis Pick & Place 1 (Rotating) |
| `3b_Two_Axis_Pick_and_Place_1_Item_Detected` | `%E7.2` | Bool | Standard-Variablentabelle | 3b \| Factory I/O: 3b_Two-Axis Pick & Place 1 (Item Detected) |
| `3b_Two_Axis_Pick_and_Place_1_Gripper_Rotating` | `%E7.3` | Bool | Standard-Variablentabelle | 3b \| Factory I/O: 3b_Two-Axis Pick & Place 1 (Gripper Rotating) |
| `3b_Diffuse_Sensor_12` | `%E7.4` | Bool | Standard-Variablentabelle | 2b \| Factory I/O: 2b_Diffuse Sensor 12 |
| `3b_Diffuse_Sensor_0` | `%E7.5` | Bool | Standard-Variablentabelle |  |
| `3b_Diffuse_Sensor_11` | `%E7.6` | Bool | Standard-Variablentabelle |  |
| `3b_Two-Axis Pick & Place 1 X Position (V)` | `%ED54` | Real | Forderband |  |
| `3b_Two-Axis Pick & Place 1 Z Position (V)` | `%ED58` | Real | Forderband |  |
| `3b_Waage 2 Weight (V)` | `%ED62` | Real | Forderband |  |

### SPS / PLC-Merker (1)

| Tag | Adresse | Typ | Tabelle | Kommentar |
|---|---|---|---|---|
| `3b_Pick_and_Place_Done` | `%M0.3` | Bool | Forderband |  |

## 4A

FUP: NW 13–16, 21 · Tags: 83 (Factory I/O 30 · SPS 53)

### SCL

- `scl/Zone_4a_Metall_Palletizer_RFID/FB_GantryPickPlace.scl`
- `scl/Zone_4a_Metall_Palletizer_RFID/OB1_GantryPickPlace.scl`
- `scl/Zone_4a_Metall_Palletizer_RFID/OB1_RFID_Metal.scl`
- `scl/Zone_4b_Kunststoff_Palletizer_RFID/FB_RFID_ReadWrite.scl (Instanz Metall)`

### Factory I/O (30)

| Tag | Adresse | Typ | Tabelle | Kommentar |
|---|---|---|---|---|
| `4a_Warning_Light_1` | `%A8.0` | Bool | Standard-Variablentabelle | 4a \| Factory I/O: 4a_Warning Light 1 |
| `4a_Pick_and_Place_1_C_Plus` | `%A8.1` | Bool | Standard-Variablentabelle | 4a \| Factory I/O: 4a_Pick & Place 1 C(+) |
| `4a_Pick_and_Place_1_Grab` | `%A8.2` | Bool | Standard-Variablentabelle | 4a \| Factory I/O: 4a_Pick & Place 1 (Grab) |
| `4a_Belt_Conveyor_at_palletizer_4m_7` | `%A8.3` | Bool | Standard-Variablentabelle | 4a \| Factory I/O: 4a_Belt _Conveyor_at_palletizer (4m) 7 |
| `4a_Palletizer_Belt_Conveyor_4m_0` | `%A8.4` | Bool | Standard-Variablentabelle | 4a \| Factory I/O: 4a_Palletizer_Belt Conveyor (4m) 0 |
| `4a_Roller_Conveyor_6m_4` | `%A8.5` | Bool | Standard-Variablentabelle | 4a \| Factory I/O: 4a_Roller Conveyor (6m) 4 |
| `4a_Roller Conveyor (2m) 2` | `%A8.6` | Bool | Forderband |  |
| `4a_Emitt_Pallet` | `%A8.7` | Bool | Forderband |  |
| `4a_RFID Reader 1 Execute Command` | `%A9.0` | Bool | 4a_4b_RFID_Readers |  |
| `4a_Pick_and_Place_1_X_Set_Point_V` | `%AD40` | Real | Standard-Variablentabelle | 4a \| Factory I/O: 4a_Pick & Place 1 X Set Point (V) |
| `4a_Pick_and_Place_1_Y_Set_Point_V` | `%AD44` | Real | Standard-Variablentabelle | 4a \| Factory I/O: 4a_Pick & Place 1 Y Set Point(V) |
| `4a_Pick_and_Place_1_Z_Set_Point_V` | `%AD48` | Real | Standard-Variablentabelle | 4a \| Factory I/O: 4a_Pick & Place 1 Z Set Point (V) |
| `4a_RFID Reader 1 Command` | `%AD76` | DInt | 4a_4b_RFID_Readers |  |
| `4a_RFID Reader 1 Write Data` | `%AD80` | DInt | 4a_4b_RFID_Readers |  |
| `4a_RFID Reader 1 Memory Index` | `%AD84` | DInt | 4a_4b_RFID_Readers |  |
| `4a_at_Palletizer_machine` | `%E8.0` | Bool | Standard-Variablentabelle | 4a \| Factory I/O: 4a_at_palletierer machine \| DUPLICATE source name - verify mapping |
| `4a_vor_Palletizer_Band_set` | `%E8.1` | Bool | Standard-Variablentabelle | 4a \| Factory I/O: 4a_vor_Palletizer_Band_set |
| `4a_Pallet_at_Palletizer` | `%E8.2` | Bool | Standard-Variablentabelle | 4a \| Factory I/O: 4a_Pallet_at_Palletizer |
| `4a_at_Palletizer_machine_2` | `%E8.3` | Bool | Standard-Variablentabelle | 4a \| Factory I/O: 4a_at_palletierer machine \| DUPLICATE source name - verify mapping |
| `4a_Pallet_Present` | `%E8.4` | Bool | Standard-Variablentabelle | 4a \| Factory I/O: 4a_Pallet_Present |
| `4a_Pick_and_Place_1_Moving_Z` | `%E8.5` | Bool | Standard-Variablentabelle | 4a \| Factory I/O: 4a_Pick & Place 1 (Moving-Z) |
| `4a_Pick_and_Place_1_Moving_XY` | `%E8.6` | Bool | Standard-Variablentabelle | 4a \| Factory I/O: 4a_Pick & Place 1 (Moving-XY) |
| `4a_pick_and_place__C_Limit` | `%E8.7` | Bool | Forderband |  |
| `4a_Pick & Place 1 (Box Detected)` | `%E9.0` | Bool | Standard-Variablentabelle |  |
| `4a_RFID Reader 1 Status` | `%ED102` | DInt | 4a_4b_RFID_Readers |  |
| `4a_RFID Reader 1 Read Data` | `%ED106` | DInt | 4a_4b_RFID_Readers |  |
| `4a_RFID Reader 1 Command ID` | `%ED110` | DInt | 4a_4b_RFID_Readers |  |
| `4a_Pick_and_Place_1_X_Position_V` | `%ED42` | Real | Standard-Variablentabelle | 4a \| Factory I/O: 4a_Pick & Place 1 X Position (V) |
| `4a_Pick_and_Place_1_Y_Position_V` | `%ED46` | Real | Standard-Variablentabelle | 4a \| Factory I/O: 4a_Pick & Place 1 Y Position (V) |
| `4a_Pick_and_Place_1_Z_Position_V` | `%ED50` | Real | Standard-Variablentabelle | 4a \| Factory I/O: 4a_Pick & Place 1 Z Position (V) |

### SPS / PLC-Merker (53)

| Tag | Adresse | Typ | Tabelle | Kommentar |
|---|---|---|---|---|
| `4b_Done(1)` | `%M10.0` | Bool | Gantry_2 |  |
| `4b_HMI_Lamp_Ready(1)` | `%M10.1` | Bool | Gantry_2 |  |
| `4b_HMI_Lamp_Running(1)` | `%M10.2` | Bool | Gantry_2 |  |
| `4a_Pallet_Ready` | `%M10.3` | Bool | Gantry | HMI compatibility (palletizer name) |
| `4a_Loading_Pallet_Active` | `%M10.4` | Bool | Gantry | TRUE while Grab |
| `4a_Busy` | `%M10.5` | Bool | Gantry | Zone 4A Busy |
| `4a_Done` | `%M10.6` | Bool | Gantry | Zone 4A Done |
| `4a_HMI_Lamp_Ready` | `%M11.0` | Bool | Gantry | Zone 4A |
| `4a_HMI_Lamp_Running` | `%M11.1` | Bool | Gantry | Zone 4A |
| `4a_HMI_Lamp_Done` | `%M11.2` | Bool | Gantry | Zone 4A |
| `4a_HMI_Lamp_Stopped` | `%M11.3` | Bool | Gantry | Zone 4A |
| `4a_HMI_Lamp_Auto` | `%M11.4` | Bool | Gantry | Zone 4A |
| `4a_HMI_Lamp_Manual` | `%M11.5` | Bool | Gantry | Zone 4A |
| `4b_HMI_Lamp_Done(1)` | `%M12.3` | Bool | Gantry_2 |  |
| `4b_HMI_Lamp_Stopped(1)` | `%M12.4` | Bool | Gantry_2 |  |
| `4b_HMI_Lamp_Auto(1)` | `%M12.5` | Bool | Gantry_2 |  |
| `4b_HMI_Lamp_Manual(1)` | `%M12.6` | Bool | Gantry_2 |  |
| `4a_RFID_Busy` | `%M21.0` | Bool | 4a_4b_RFID_Readers |  |
| `4a_RFID_Done` | `%M21.1` | Bool | 4a_4b_RFID_Readers |  |
| `4a_RFID_Error` | `%M21.2` | Bool | 4a_4b_RFID_Readers |  |
| `4a_RFID_Tag_Present` | `%M21.3` | Bool | 4a_4b_RFID_Readers |  |
| `4a_RFID_Metal_Bereit` | `%M34.0` | Bool | 4a_4b_RFID_Readers |  |
| `4a_RFID_Metal_Gueltig` | `%M34.1` | Bool | 4a_4b_RFID_Readers |  |
| `4a_RFID_Metal_Fehler` | `%M34.2` | Bool | 4a_4b_RFID_Readers |  |
| `4a_HMI_Start` | `%M8.0` | Bool | Gantry | Zone 4A HMI (same as previous Palletizer screen) |
| `4a_HMI_Stop` | `%M8.1` | Bool | Gantry | Zone 4A |
| `4a_HMI_Reset` | `%M8.2` | Bool | Gantry | Zone 4A |
| `4a_HMI_Auto` | `%M8.3` | Bool | Gantry | Zone 4A |
| `4a_HMI_SingleCycle` | `%M8.4` | Bool | Gantry | Zone 4A |
| `4b_HMI_Start(1)` | `%M9.0` | Bool | Gantry_2 |  |
| `4b_HMI_Stop(1)` | `%M9.1` | Bool | Gantry_2 |  |
| `4b_HMI_Reset(1)` | `%M9.2` | Bool | Gantry_2 |  |
| `4b_HMI_Auto(1)` | `%M9.3` | Bool | Gantry_2 |  |
| `4b_HMI_SingleCycle(1)` | `%M9.4` | Bool | Gantry_2 |  |
| `4b_Pallet_Ready(1)` | `%M9.5` | Bool | Gantry_2 |  |
| `4b_Loading_Pallet_Active(1)` | `%M9.6` | Bool | Gantry_2 |  |
| `4b_Busy(1)` | `%M9.7` | Bool | Gantry_2 |  |
| `4a_RFID_Code_Out` | `%MD236` | UDInt | 4a_4b_RFID_Readers |  |
| `4a_RFID_Data_Out` | `%MD240` | UDInt | 4a_4b_RFID_Readers |  |
| `4a_RFID_Serial_Number` | `%MD244` | UDInt | 4a_4b_RFID_Readers |  |
| `4a_State` | `%MW12` | Int | Gantry | Zone 4A step |
| `4a_Assembly_Count` | `%MW14` | Int | Gantry | HMI compatibility |
| `4a_RFID_Artikelnummer_Out` | `%MW150` | UInt | 4a_4b_RFID_Readers |  |
| `4a_RFID_State` | `%MW152` | Int | 4a_4b_RFID_Readers |  |
| `4a_RFID_Status_Code` | `%MW154` | Int | 4a_4b_RFID_Readers |  |
| `4a_RFID_Metal_ProductTyp_Out` | `%MW156` | UInt | 4a_4b_RFID_Readers |  |
| `4a_HMI_Cycle_Count` | `%MW16` | Int | Gantry | Zone 4A |
| `4a_HMI_Step_Text_ID` | `%MW18` | Int | Gantry | Zone 4A |
| `4a_RFID_RFID_Materialart_Out` | `%MW182` | UInt | 4a_4b_RFID_Readers |  |
| `4b_State(1)` | `%MW30` | Int | Gantry_2 |  |
| `4b_HMI_Cycle_Count(1)` | `%MW32` | Int | Gantry_2 |  |
| `4b_Assembly_Count(1)` | `%MW34` | Int | Gantry_2 |  |
| `4b_HMI_Step_Text_ID(1)` | `%MW36` | Int | Gantry_2 |  |

## 4B

FUP: NW 22–25 · Tags: 29 (Factory I/O 29 · SPS 0)

### SCL

- `scl/Zone_4b_Kunststoff_Palletizer_RFID/FB_Palletizer.scl`
- `scl/Zone_4b_Kunststoff_Palletizer_RFID/OB1_Palletizer.scl`
- `scl/Zone_4b_Kunststoff_Palletizer_RFID/UDT_Palletizer.scl`
- `scl/Zone_4b_Kunststoff_Palletizer_RFID/FB_RFID_ReadWrite.scl`
- `scl/Zone_4b_Kunststoff_Palletizer_RFID/OB1_RFID_at_PickPlace.scl`
- `scl/Zone_4b_Kunststoff_Palletizer_RFID/OB1_Vision_RFID_before_Pallet.scl`

### Factory I/O (29)

| Tag | Adresse | Typ | Tabelle | Kommentar |
|---|---|---|---|---|
| `4b_Belt Conveyor (4m) 6` | `%A10.0` | Bool | Forderband |  |
| `4b_Pick & Place 1 C(+)` | `%A10.2` | Bool | Standard-Variablentabelle |  |
| `4b_Pick & Place 1 (Grab)` | `%A10.3` | Bool | Standard-Variablentabelle |  |
| `4b_Roller Conveyor (2m) 3` | `%A10.4` | Bool | Forderband |  |
| `4b_Roller Conveyor (6m) 1` | `%A10.5` | Bool | Forderband |  |
| `4b_Stacker_BeltConveyor_Plastic(6m)` | `%A10.6` | Bool | Standard-Variablentabelle |  |
| `4b_Warning_Light_6` | `%A10.7` | Bool | Standard-Variablentabelle |  |
| `4b_RFID Reader 2 Execute Command` | `%A11.1` | Bool | Forderband |  |
| `4b_RFID Reader 2 Command` | `%AD104` | DInt | 4a_4b_RFID_Readers |  |
| `4b_RFID Reader 2 Write Data` | `%AD108` | DInt | 4a_4b_RFID_Readers |  |
| `4b_RFID Reader 2 Memory Index` | `%AD112` | DInt | 4a_4b_RFID_Readers |  |
| `4b_Pick & Place 1 Y Set Point(V)` | `%AD60` | Real | Standard-Variablentabelle |  |
| `4b_Pick & Place 1 X Set Point (V)` | `%AD64` | Real | Standard-Variablentabelle |  |
| `4b_Pick & Place 1 Z Set Point (V)` | `%AD68` | Real | Standard-Variablentabelle |  |
| `4b_Diffuse_Sensor_10` | `%E10.0` | Bool | Standard-Variablentabelle |  |
| `4b_Diffuse_Sensor_26` | `%E10.1` | Bool | Forderband |  |
| `4b_Diffuse Sensor 41` | `%E10.2` | Bool | Standard-Variablentabelle |  |
| `4b_Pallet_Present` | `%E10.3` | Bool | Forderband |  |
| `4b_Pick & Place 0 (C Limit)` | `%E10.4` | Bool | Standard-Variablentabelle |  |
| `4b_Pick & Place 0 (Moving-Z)` | `%E10.5` | Bool | Standard-Variablentabelle |  |
| `4b_Pick & Place 0 (Moving-XY)` | `%E10.6` | Bool | Standard-Variablentabelle |  |
| `4b_Pick & Place 0 (Box Detected)` | `%E10.7` | Bool | Standard-Variablentabelle |  |
| `4b_Diffuse Sensor 13` | `%E11.0` | Bool | Forderband |  |
| `4b_RFID Reader 2 Status` | `%ED130` | DInt | 4a_4b_RFID_Readers |  |
| `4b_RFID Reader 2 Read Data` | `%ED134` | DInt | 4a_4b_RFID_Readers |  |
| `4b_RFID Reader 2 Command ID` | `%ED138` | DInt | 4a_4b_RFID_Readers |  |
| `4b_Pick & Place 0 X Position (V)` | `%ED86` | Real | Standard-Variablentabelle |  |
| `4b_Pick & Place 0 Y Position (V)` | `%ED90` | Real | Standard-Variablentabelle |  |
| `4b_Pick & Place 0 Z Position (V)` | `%ED94` | Real | Standard-Variablentabelle |  |

### SPS / PLC-Merker (0)

*(keine)*

## 5A

FUP: NW 26, 28 Warehouse_2 · Tags: 108 (Factory I/O 35 · SPS 73)

### SCL

- `scl/Zone_5a_Metall_Hochregallager/Hochregal_Automatik_Betrieb_W2.scl`
- `scl/Zone_5a_Metall_Hochregallager/OB1_NW28_Metal_Warehouse.scl`
- `scl/Zone_5a_Metall_Hochregallager/OB1_RFID_5a_DB4.scl`
- `scl/Zone_5a_Metall_Hochregallager/FB_Warehouse_Mode_Select_W2.scl`
- `scl/Zone_5a_Metall_Hochregallager/FB_Warehouse_Gate_W2.scl`
- `scl/Zone_5a_Metall_Hochregallager/FB_Warehouse_Stacker_IO_W2.scl`
- `scl/Zone_5a_Metall_Hochregallager/FB_Warehouse_Manual_Soll_W2.scl`
- `scl/Zone_5a_Metall_Hochregallager/FB_Warehouse_Actuators_W2.scl`
- `scl/Zone_5a_Metall_Hochregallager/FB_Einlagern_W2.scl`
- `scl/Zone_5a_Metall_Hochregallager/FB_Auslagern_W2.scl`
- `scl/Zone_5a_Metall_Hochregallager/FB_Suchen_W2.scl`
- `scl/Zone_5a_Metall_Hochregallager/FB_Loeschen_W2.scl`
- `scl/Zone_5a_Metall_Hochregallager/FB_Freies_Fach_Suchen_W2.scl`
- `scl/Zone_5a_Metall_Hochregallager/FB_Datenverwaltung_Lager_W2.scl`
- `scl/Zone_5a_Metall_Hochregallager/FB_Berechn_Offset_W2.scl`
- `scl/Zone_5a_Metall_Hochregallager/FB_Meldung_W2.scl`
- `scl/Zone_5a_Metall_Hochregallager/FB_Lagerstatus_W2.scl`
- (NW 26 Bänder → W1: kein eigenes SCL, nur FUP)

### Factory I/O (35)

| Tag | Adresse | Typ | Tabelle | Kommentar |
|---|---|---|---|---|
| `5a_Roller Conveyor (6m) 2` | `%A12.0` | Bool | Forderband |  |
| `5a_Curved Roller Conveyor 1 CCW` | `%A12.1` | Bool | Forderband |  |
| `5a_Curved Roller Conveyor 7 CW` | `%A12.2` | Bool | Standard-Variablentabelle |  |
| `5a_Curved Roller Conveyor 0 CW` | `%A12.3` | Bool | Forderband |  |
| `5a_Roller Conveyor (2m) 0` | `%A12.4` | Bool | Forderband |  |
| `5a_Roller Conveyor (2m) 5` | `%A12.5` | Bool | Standard-Variablentabelle |  |
| `5a_Roller Conveyor (4m) 5` | `%A12.6` | Bool | Forderband |  |
| `5a_Roller Conveyor (6m) 3` | `%A12.7` | Bool | Forderband |  |
| `5a_Loading Conveyor` | `%A14.5` | Bool | Standard-Variablentabelle |  |
| `5a_Stacker Crane 1 (Left)` | `%A15.0` | Bool | HMI_Tags_Warehouse_2 |  |
| `5a_Stacker Crane 1 (Right)` | `%A15.1` | Bool | HMI_Tags_Warehouse_2 |  |
| `5a_Warning Light 4` | `%A15.2` | Bool | HMI_Tags_Warehouse_2 |  |
| `5a_Alarm Siren 0` | `%A15.3` | Bool | HMI_Tags_Warehouse_2 |  |
| `5a_RFID Reader 0 Execute Command` | `%A15.4` | Bool | 5a_RFID |  |
| `5a_Stacker Crane 1 X Set Point (V)` | `%AD144` | Real | HMI_Tags_Warehouse_2 |  |
| `5a_Stacker Crane 1 Z Set Point (V)` | `%AD148` | Real | HMI_Tags_Warehouse_2 |  |
| `5a_RFID Reader 0 Command` | `%AD88` | DInt | 5a_RFID |  |
| `5a_RFID Reader 0 Write Data` | `%AD92` | DInt | 5a_RFID |  |
| `5a_RFID Reader 0 Memory Index` | `%AD96` | DInt | 5a_RFID |  |
| `5a_to_warehouse` | `%E12.0` | Bool | Forderband |  |
| `5a_Diffuse Sensor 21` | `%E12.1` | Bool | Forderband |  |
| `5a_Diffuse Sensor 25` | `%E12.2` | Bool | Forderband |  |
| `5a_Diffuse Sensor 55` | `%E12.3` | Bool | Standard-Variablentabelle |  |
| `5a_Metal_Palette_vor_regal` | `%E15.0` | Bool | HMI_Tags_Warehouse_2 |  |
| `5a_Stacker Crane 1 Moving-X` | `%E15.1` | Bool | HMI_Tags_Warehouse_2 |  |
| `5a_Stacker Crane 1 Moving-Z` | `%E15.2` | Bool | HMI_Tags_Warehouse_2 |  |
| `5a_Stacker Crane 1 Left Limit` | `%E15.3` | Bool | HMI_Tags_Warehouse_2 |  |
| `5a_Stacker Crane 1 Right Limit` | `%E15.4` | Bool | HMI_Tags_Warehouse_2 |  |
| `5a_Stacker Crane 1 Middle Limit` | `%E15.5` | Bool | HMI_Tags_Warehouse_2 |  |
| `5a_Metal_Pallette_A_Regal` | `%E15.6` | Bool | Standard-Variablentabelle |  |
| `5a_RFID Reader 0 Status` | `%ED114` | DInt | 5a_RFID |  |
| `5a_RFID Reader 0 Read Data` | `%ED118` | DInt | 5a_RFID |  |
| `5a_RFID Reader 0 Command ID` | `%ED122` | DInt | 5a_RFID |  |
| `5a_Stacker Crane 1 X Position (V)` | `%ED178` | Real | HMI_Tags_Warehouse_2 |  |
| `5a_Stacker Crane 1 Z Position (V)` | `%ED182` | Real | HMI_Tags_Warehouse_2 |  |

### SPS / PLC-Merker (73)

| Tag | Adresse | Typ | Tabelle | Kommentar |
|---|---|---|---|---|
| `Mode_Einricht_W2` | `%M70.0` | Bool | HMI_Tags_Warehouse_2 |  |
| `Mode_Auto_W2` | `%M70.1` | Bool | HMI_Tags_Warehouse_2 |  |
| `Mode_Hand_W2` | `%M70.2` | Bool | HMI_Tags_Warehouse_2 |  |
| `Not_Aus_W2` | `%M70.3` | Bool | HMI_Tags_Warehouse_2 |  |
| `HMI_Initialisieren_W2` | `%M70.4` | Bool | HMI_Tags_Warehouse_2 |  |
| `HMI_Reset_Meldung_W2` | `%M70.5` | Bool | HMI_Tags_Warehouse_2 |  |
| `HMI_Pos_Speichern_W2` | `%M70.6` | Bool | HMI_Tags_Warehouse_2 |  |
| `HMI_Raster_Berechnen_W2` | `%M70.7` | Bool | HMI_Tags_Warehouse_2 |  |
| `HMI_Loeschen_W2` | `%M71.0` | Bool | HMI_Tags_Warehouse_2 |  |
| `HMI_Suchen_W2` | `%M71.1` | Bool | HMI_Tags_Warehouse_2 |  |
| `HMI_FreiesFach_W2` | `%M71.2` | Bool | HMI_Tags_Warehouse_2 |  |
| `HMI_Start_Einlagern_W2` | `%M71.3` | Bool | HMI_Tags_Warehouse_2 |  |
| `HMI_Start_Auslagern_W2` | `%M71.4` | Bool | HMI_Tags_Warehouse_2 |  |
| `HMI_Reset_W2` | `%M71.5` | Bool | HMI_Tags_Warehouse_2 |  |
| `HMI_Stop_W2` | `%M71.6` | Bool | HMI_Tags_Warehouse_2 |  |
| `HMI_Copy_Ist_to_Soll_W2` | `%M71.7` | Bool | HMI_Tags_Warehouse_2 |  |
| `Paket_Vor_Regal_W2` | `%M72.0` | Bool | HMI_Tags_Warehouse_2 |  |
| `Paket_Fuer_Hochregal_W2` | `%M72.1` | Bool | HMI_Tags_Warehouse_2 |  |
| `Palette_Aufgenommen_W2` | `%M72.2` | Bool | HMI_Tags_Warehouse_2 |  |
| `Palette_Abgelegt_W2` | `%M72.3` | Bool | HMI_Tags_Warehouse_2 |  |
| `Position_Erricht_W2` | `%M72.4` | Bool | HMI_Tags_Warehouse_2 |  |
| `Gabel_Rechts_Ausgefahren_W2` | `%M72.5` | Bool | HMI_Tags_Warehouse_2 |  |
| `Gabel_Links_Ausgefahren_W2` | `%M72.6` | Bool | HMI_Tags_Warehouse_2 |  |
| `Gabel_Eingefahren_W2` | `%M72.7` | Bool | HMI_Tags_Warehouse_2 |  |
| `Fahre_Zu_Position_W2` | `%M73.0` | Bool | HMI_Tags_Warehouse_2 |  |
| `Palette_Aufnehmen_Cmd_W2` | `%M73.1` | Bool | HMI_Tags_Warehouse_2 |  |
| `Palette_Ablegen_Cmd_W2` | `%M73.2` | Bool | HMI_Tags_Warehouse_2 |  |
| `Gabel_Rechts_Cmd_W2` | `%M73.3` | Bool | HMI_Tags_Warehouse_2 |  |
| `Gabel_Links_Cmd_W2` | `%M73.4` | Bool | HMI_Tags_Warehouse_2 |  |
| `Gabel_Mitte_Cmd_W2` | `%M73.5` | Bool | HMI_Tags_Warehouse_2 |  |
| `HRL2_Busy` | `%M74.0` | Bool | HMI_Tags_Warehouse_2 |  |
| `HRL2_Done` | `%M74.1` | Bool | HMI_Tags_Warehouse_2 |  |
| `HRL2_Error` | `%M74.2` | Bool | HMI_Tags_Warehouse_2 |  |
| `HMI_Soll_X_Plus_W2` | `%M75.7` | Bool | HMI_Tags_Warehouse_2 |  |
| `HMI_Soll_X_Minus_W2` | `%M76.0` | Bool | HMI_Tags_Warehouse_2 |  |
| `HMI_Soll_Z_Plus_W2` | `%M76.1` | Bool | HMI_Tags_Warehouse_2 |  |
| `HMI_Soll_Z_Minus_W2` | `%M76.2` | Bool | HMI_Tags_Warehouse_2 |  |
| `HMI_Copy_Ist_to_Band_W2` | `%M76.3` | Bool | HMI_Tags_Warehouse_2 |  |
| `5a_RFID_Lesen` | `%M77.0` | Bool | 5a_RFID |  |
| `5a_RFID_Busy` | `%M77.1` | Bool | 5a_RFID |  |
| `5a_RFID_Done` | `%M77.2` | Bool | 5a_RFID |  |
| `5a_RFID_Error` | `%M77.3` | Bool | 5a_RFID |  |
| `5a_RFID_Bereit` | `%M77.4` | Bool | 5a_RFID |  |
| `5a_RFID_Gueltig` | `%M77.5` | Bool | 5a_RFID |  |
| `5a_RFID_Fehler` | `%M77.6` | Bool | 5a_RFID |  |
| `5a_RFID_Materialart_Out` | `%MB286` | USInt | 5a_RFID |  |
| `HMI_Pitch_X_W2` | `%MD184` | Real | HMI_Tags_Warehouse_2 |  |
| `HMI_Pitch_Z_W2` | `%MD188` | Real | HMI_Tags_Warehouse_2 |  |
| `Ist_X_W2` | `%MD196` | Real | HMI_Tags_Warehouse_2 |  |
| `Ist_Z_W2` | `%MD200` | Real | HMI_Tags_Warehouse_2 |  |
| `Soll_X_W2` | `%MD204` | Real | HMI_Tags_Warehouse_2 |  |
| `Soll_Z_W2` | `%MD208` | Real | HMI_Tags_Warehouse_2 |  |
| `Home_X_W2` | `%MD212` | Real | HMI_Tags_Warehouse_2 |  |
| `Home_Z_W2` | `%MD216` | Real | HMI_Tags_Warehouse_2 |  |
| `Ausgabe_X_W2` | `%MD220` | Real | HMI_Tags_Warehouse_2 |  |
| `Ausgabe_Z_W2` | `%MD224` | Real | HMI_Tags_Warehouse_2 |  |
| `HMI_Soll_X_W2` | `%MD252` | Real | HMI_Tags_Warehouse_2 |  |
| `HMI_Soll_Z_W2` | `%MD256` | Real | HMI_Tags_Warehouse_2 |  |
| `HMI_Jog_Step_W2` | `%MD260` | Real | HMI_Tags_Warehouse_2 |  |
| `Band_X_W2` | `%MD264` | Real | HMI_Tags_Warehouse_2 |  |
| `Band_Z_W2` | `%MD268` | Real | HMI_Tags_Warehouse_2 |  |
| `Band_Z_Lift_W2` | `%MD272` | Real | HMI_Tags_Warehouse_2 |  |
| `5a_RFID_Code_Out` | `%MD300` | UDInt | 5a_RFID |  |
| `HMI_Fachnummer_W2` | `%MW180` | UInt | HMI_Tags_Warehouse_2 |  |
| `HMI_Spalten_W2` | `%MW192` | Int | HMI_Tags_Warehouse_2 |  |
| `HMI_Spalten_Rechts_W2` | `%MW194` | Int | HMI_Tags_Warehouse_2 |  |
| `HMI_State_W2` | `%MW228` | Int | HMI_Tags_Warehouse_2 |  |
| `HMI_Ziel_Fach_W2` | `%MW230` | Int | HMI_Tags_Warehouse_2 |  |
| `HRL2_Anzahl_Belegt` | `%MW232` | UInt | HMI_Tags_Warehouse_2 |  |
| `HRL2_Anzahl_Frei` | `%MW234` | UInt | HMI_Tags_Warehouse_2 |  |
| `5a_RFID_Artikelnummer_Out` | `%MW304` | UInt | 5a_RFID |  |
| `5a_RFID_ProductTyp_Out` | `%MW308` | UInt | 5a_RFID |  |
| `5a_RFID_State` | `%MW310` | Int | 5a_RFID |  |

## 5B

FUP: NW 27, 29 Warehouse_1 · Tags: 111 (Factory I/O 33 · SPS 78)

### SCL

- `scl/Zone_5b_Hochregallager/Hochregal_Automatik_Betrieb.scl`
- `scl/Zone_5b_Hochregallager/FB_Warehouse_Mode_Select.scl`
- `scl/Zone_5b_Hochregallager/FB_Warehouse_Gate.scl`
- `scl/Zone_5b_Hochregallager/FB_Warehouse_Stacker_IO.scl`
- `scl/Zone_5b_Hochregallager/FB_Warehouse_Manual_Soll.scl`
- `scl/Zone_5b_Hochregallager/FB_Warehouse_Actuators.scl`
- `scl/Zone_5b_Hochregallager/FB_Einlagern.scl`
- `scl/Zone_5b_Hochregallager/FB_Auslagern.scl`
- `scl/Zone_5b_Hochregallager/FB_Suchen.scl`
- `scl/Zone_5b_Hochregallager/FB_Loeschen.scl`
- `scl/Zone_5b_Hochregallager/FB_Freies_Fach_Suchen.scl`
- `scl/Zone_5b_Hochregallager/FB_Datenverwaltung_Lager.scl`
- `scl/Zone_5b_Hochregallager/FB_Berechn_Offset.scl`
- `scl/Zone_5b_Hochregallager/FB_Meldung.scl`
- `scl/Zone_5b_Hochregallager/FB_Lagerstatus.scl`
- `scl/Zone_5b_Hochregallager/FB_Hochregallager.scl (optional, nicht in OB1)`
- `scl/Zone_5a_Foerderband_Lager/OB1_NW27_Belts_to_Metal_Warehouse.scl`

### Factory I/O (33)

| Tag | Adresse | Typ | Tabelle | Kommentar |
|---|---|---|---|---|
| `5b_Roller Conveyor (4m) 0` | `%A13.0` | Bool | Forderband |  |
| `5b_Curved Roller Conveyor 2 CCW` | `%A13.1` | Bool | Forderband |  |
| `5b_Roller Conveyor (2m) 1` | `%A13.2` | Bool | Forderband |  |
| `5b_Curved Roller Conveyor 4` | `%A13.3` | Bool | Forderband |  |
| `5b_Roller Conveyor (6m) 0` | `%A13.4` | Bool | Forderband |  |
| `5b_Curved Roller Conveyor 3 CCW` | `%A13.5` | Bool | Forderband |  |
| `5b_RFID Reader 5 Execute Command` | `%A13.7` | Bool | 5b_RFID |  |
| `5b_Stacker Crane 0 (Left)` | `%A14.0` | Bool | Warehouse |  |
| `5b_Stacker Crane 0 (Right)` | `%A14.1` | Bool | Warehouse |  |
| `5b_Warning_Light_5` | `%A14.2` | Bool | Warehouse |  |
| `5b_Loading Conveyor 1` | `%A14.3` | Bool | Warehouse |  |
| `5b_Alarm Siren 2` | `%A14.4` | Bool | Warehouse |  |
| `5b_RFID Reader 5 Command` | `%AD124` | DInt | 5b_RFID |  |
| `5b_RFID Reader 5 Write Data` | `%AD128` | DInt | 5b_RFID |  |
| `5b_RFID Reader 5 Memory Index` | `%AD132` | DInt | 5b_RFID |  |
| `5b_Stacker Crane 0 X Set Point (V)` | `%AD136` | Real | Warehouse |  |
| `5b_Stacker Crane 0 Z Set Point (V)` | `%AD140` | Real | Warehouse |  |
| `5b_1_to_Warehouse` | `%E13.0` | Bool | Forderband |  |
| `5b_2_to_Warehouse` | `%E13.1` | Bool | Forderband |  |
| `5b_3_to_Warehouse` | `%E13.2` | Bool | Forderband |  |
| `5b_Pallet_vor_Regal_E13` | `%E13.3` | Bool | Warehouse |  |
| `5b_Diffuse Sensor 48` | `%E13.4` | Bool | Warehouse |  |
| `5b_Stacker Crane 0 Moving-X` | `%E13.6` | Bool | Warehouse |  |
| `5b_Stacker Crane 0 Moving-Z` | `%E13.7` | Bool | Warehouse |  |
| `5b_Stacker Crane 0 Left Limit` | `%E14.0` | Bool | Warehouse |  |
| `5b_Stacker Crane 0 Right Limit` | `%E14.1` | Bool | Warehouse |  |
| `5b_Stacker Crane 0 Middle Limit` | `%E14.2` | Bool | Warehouse |  |
| `5b_Pallet_vor_Regal` | `%E14.3` | Bool | Warehouse |  |
| `5b_RFID Reader 5 Status` | `%ED150` | DInt | 5b_RFID |  |
| `5b_RFID Reader 5 Read Data` | `%ED154` | DInt | 5b_RFID |  |
| `5b_RFID Reader 5 Command ID` | `%ED158` | DInt | 5b_RFID |  |
| `5b_Stacker Crane 0 X Position (V)` | `%ED162` | Real | Warehouse |  |
| `5b_Stacker Crane 0 Z Position (V)` | `%ED166` | Real | Warehouse |  |

### SPS / PLC-Merker (78)

| Tag | Adresse | Typ | Tabelle | Kommentar |
|---|---|---|---|---|
| `Mode_Einricht` | `%M60.0` | Bool | Warehouse |  |
| `Mode_Auto` | `%M60.1` | Bool | Warehouse |  |
| `Mode_Hand` | `%M60.2` | Bool | Warehouse |  |
| `Not_Aus` | `%M60.3` | Bool | Warehouse |  |
| `HMI_Initialisieren` | `%M60.4` | Bool | Warehouse |  |
| `HMI_Reset_Meldung` | `%M60.5` | Bool | Warehouse |  |
| `HMI_Pos_Speichern` | `%M60.6` | Bool | Warehouse |  |
| `HMI_Raster_Berechnen` | `%M60.7` | Bool | Warehouse |  |
| `HMI_Loeschen` | `%M61.0` | Bool | Warehouse |  |
| `HMI_Suchen` | `%M61.1` | Bool | Warehouse |  |
| `HMI_FreiesFach` | `%M61.2` | Bool | Warehouse |  |
| `HMI_Start_Einlagern` | `%M61.3` | Bool | Warehouse |  |
| `HMI_Start_Auslagern` | `%M61.4` | Bool | Warehouse |  |
| `HMI_Reset` | `%M61.5` | Bool | Warehouse |  |
| `HMI_Stop` | `%M61.6` | Bool | Warehouse |  |
| `HMI_Copy_Ist_to_Soll` | `%M61.7` | Bool | Warehouse |  |
| `Paket_vor_Regal` | `%M62.0` | Bool | Warehouse |  |
| `Paket_Fuer_Hochregal` | `%M62.1` | Bool | Warehouse |  |
| `Palette_Aufgenommen` | `%M62.2` | Bool | Warehouse |  |
| `Palette_Abgelegt` | `%M62.3` | Bool | Warehouse |  |
| `Position_Erreicht` | `%M62.4` | Bool | Warehouse |  |
| `Gabel_Rechts_Ausgefahren` | `%M62.5` | Bool | Warehouse |  |
| `Gabel_Links_Ausgefahren` | `%M62.6` | Bool | Warehouse |  |
| `Gabel_Eingefahren` | `%M62.7` | Bool | Warehouse |  |
| `Fahre_Zu_Position` | `%M63.0` | Bool | Warehouse |  |
| `Palette_Aufnehmen_Cmd` | `%M63.1` | Bool | Warehouse |  |
| `Palette_Ablegen_Cmd` | `%M63.2` | Bool | Warehouse |  |
| `Gabel_Rechts_Cmd` | `%M63.3` | Bool | Warehouse |  |
| `Gabel_Links_Cmd` | `%M63.4` | Bool | Warehouse |  |
| `Gabel_Mitte_Cmd` | `%M63.5` | Bool | Warehouse |  |
| `HRL_Busy` | `%M64.0` | Bool | Warehouse |  |
| `HRL_Done` | `%M64.1` | Bool | Warehouse |  |
| `HRL_Error` | `%M64.2` | Bool | Warehouse |  |
| `HRL_Mode_Auto` | `%M64.3` | Bool | Warehouse |  |
| `HRL_Mode_Hand` | `%M64.4` | Bool | Warehouse |  |
| `HRL_Mode_Einricht` | `%M64.5` | Bool | Warehouse |  |
| `5b_RFID_Lesen` | `%M65.0` | Bool | 5b_RFID |  |
| `RFID_5b_Busy` | `%M65.1` | Bool | 5b_RFID |  |
| `RFID_5b_Done` | `%M65.2` | Bool | 5b_RFID |  |
| `RFID_5b_Error` | `%M65.3` | Bool | 5b_RFID |  |
| `RFID_5b_Bereit` | `%M65.4` | Bool | 5b_RFID |  |
| `RFID_5b_Gueltig` | `%M65.5` | Bool | 5b_RFID |  |
| `RFID_5b_Fehler` | `%M65.6` | Bool | 5b_RFID |  |
| `HMI_Soll_X_Plus` | `%M65.7` | Bool | Warehouse |  |
| `HMI_Soll_X_Minus` | `%M66.0` | Bool | Warehouse |  |
| `HMI_Soll_Z_Plus` | `%M66.1` | Bool | Warehouse |  |
| `HMI_Soll_Z_Minus` | `%M66.2` | Bool | Warehouse |  |
| `RFID_5b_Materialart_Out` | `%MB146` | USInt | 5b_RFID |  |
| `Ist_Z` | `%MD100` | Real | Warehouse |  |
| `Soll_X` | `%MD104` | Real | Warehouse |  |
| `Soll_Z` | `%MD108` | Real | Warehouse |  |
| `Home_X` | `%MD112` | Real | Warehouse |  |
| `Home_Z` | `%MD116` | Real | Warehouse |  |
| `Ausgabe_X` | `%MD120` | Real | Warehouse |  |
| `Ausgabe_Z` | `%MD124` | Real | Warehouse |  |
| `RFID_5b_Code_Out` | `%MD140` | UDInt | 5b_RFID |  |
| `HMI_Soll_X` | `%MD152` | Real | Warehouse |  |
| `HMI_Soll_Z` | `%MD156` | Real | Warehouse |  |
| `HMI_Jog_Step` | `%MD160` | Real | Warehouse |  |
| `Band_X` | `%MD164` | Real | Warehouse |  |
| `Band_Z` | `%MD168` | Real | Warehouse |  |
| `Band_Z_Lift` | `%MD172` | Real | Warehouse |  |
| `HMI_5b_Offset` | `%MD176` | Real | Warehouse |  |
| `HMI_5a_Offset` | `%MD52` | Real | HMI_Tags_Warehouse_2 |  |
| `HMI_Pitch_X` | `%MD84` | Real | Warehouse |  |
| `HMI_Pitch_Z` | `%MD88` | Real | Warehouse |  |
| `Ist_X` | `%MD96` | Real | Warehouse |  |
| `HMI_State` | `%MW128` | Int | Warehouse |  |
| `HMI_Ziel_Fach` | `%MW130` | Int | Warehouse |  |
| `HRL_Anzahl_Belegt` | `%MW132` | UInt | Warehouse |  |
| `HRL_Anzahl_Frei` | `%MW134` | UInt | Warehouse |  |
| `RFID_5b_State` | `%MW136` | Int | 5b_RFID |  |
| `RFID_5b_Status_Code` | `%MW138` | Int | 5b_RFID |  |
| `RFID_5b_Artikelnummer_Out` | `%MW144` | UInt | 5b_RFID |  |
| `RFID_5b_ProductTyp_Out` | `%MW148` | UInt | 5b_RFID |  |
| `HMI_Fachnummer` | `%MW80` | UInt | Warehouse |  |
| `HMI_Spalten` | `%MW92` | Int | Warehouse |  |
| `HMI_Spalten_Rechts` | `%MW94` | Int | Warehouse |  |

## Standard-Variablentabelle

FUP: — · Tags: 2 (Factory I/O 1 · SPS 1)

### SCL

- (Querschnitt, z. B. Clock_Byte)

### Factory I/O (1)

| Tag | Adresse | Typ | Tabelle | Kommentar |
|---|---|---|---|---|
| `Gewicht` | `%AD24` | DInt | Standard-Variablentabelle | System \| Factory I/O: Gewicht |

### SPS / PLC-Merker (1)

| Tag | Adresse | Typ | Tabelle | Kommentar |
|---|---|---|---|---|
| `Clock_Byte` | `%MB20` | Byte | Standard-Variablentabelle |  |

Zurück: [Pflichtenheft.md](Pflichtenheft.md) · [PLC_Networks.md](PLC_Networks.md)
