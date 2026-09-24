# Main Program Sweep (Cycle) â€” OB1

**Author:** Dereje Hailemariam  
**Date:** 02.09.2026  
**Version:** 1.5  

**TIA-Titel (kurz):** [PLC_Networks.md](PLC_Networks.md) Â· **Hardware:** [Hardware_SPS.md](../03_Technik/Hardware_SPS.md)

## Description

The **Main Program Sweep (Cycle)** is the central cyclic program of the automation system. It coordinates all production areas of the Factory I/O plant, including raw-material feeding, CNC robot stations, conveyor systems, vision and RFID identification, Pick & Place assembly, weighing, palletizing and warehouse handling.

The program is divided into **29 networks** according to the physical zones of the plant. Each network calls or controls the functions assigned to the corresponding process section.

**Naming (Lastenheft / Doku):**

| Station | Zone / NW | Bezeichnung |
|---|---|---|
| Metal Pick & Place 1 | 3A Â· NW 10 | **2-axis Pick and Place** |
| Plastic Pick & Place 2 | 3B Â· NW 18 | **2-axis Pick and Place** |
| Metal Assembly Palletizer (X/Y/Z) | 4A Â· NW 15 | **3-axis Pick and Place** |
| Metal Components Warehouse | 5A Â· NW 28 | **Warehouse_2** |
| Plastic Components Warehouse | 5B Â· NW 29 | **Warehouse_1** |

PLC-Tag-Namen `Gantry_*` / `FB_GantryPickPlace` bleiben in TIA bis zur Umbenennung; in der Dokumentation gilt nur **3-axis Pick and Place**.

---

### Network 1 â€“ Zone 1a: Metal Raw Material Input

Controls the feeding and availability detection of the metal raw-material components.

### Network 2 â€“ Zone 1a: Metal Robot (CNC) Station

Controls the metal machining station (robot + CNC for lids and bases).

### Network 3 â€“ Zone 2a: Metal Conveyor Belts after Robot/CNC Station

Transports finished metal components toward assembly.

### Network 4 â€“ Zone 1b: Plastic Raw Material Input

Controls feeding and detection of plastic raw-material components.

### Network 5 – Zone 2a: Vision Data Sensors (Metal)

Metal vision (`FB_VisionReader_Metal`) — lid/base codes 8/9, `Materialart=2`, production date + article number, `2a_VisionData_Combo_Done` → Warehouse_2 Gate. SCL: `scl/Zone_2a_Foerderbaender/`.

### Network 6 â€“ Zone 1b: Plastic Robot (CNC) Station

Robot and CNC machining for plastic lids and bases.

### Network 7 â€“ Zone 2b: Vision Data Sensors

Primary plastic vision network â€” `FB17` `VisionSensorData` (Lid/Base color, `Combo_Done`, `Materialart`, `Lid_Reject_Metal` / `Base_Reject_Metal`).

### Network 8 â€“ Zone 2b: Plastic Conveyor Belts after Robot/CNC Station

Transports plastic components after machining / vision toward assembly.

### Network 9 â€“ Zone 3a: Metal Conveyor Belts before Pick and Place Assembly

Product transport before metal 2-axis assembly.

### Network 10 â€“ Zone 3a: Metal Pick and Place 1

**2-axis Pick and Place** â€” mounts metal base and lid.

### Network 11 â€“ Zone 3a: Metal Scale 1 (Waage 1)

Weighs the finished metal assembly.

### Network 12 â€“ Zone 3a: Metal Conveyor Belts after Scale 1

Transport toward metal palletizer.

### Network 13 â€“ Zone 4a: Conveyor Belts before Palletizer

Transport before metal palletizing.

### Network 14 â€“ Zone 4a: Roller Conveyor Belts before Palletizer

Roller conveyors at the metal palletizer infeed.

### Network 15 â€“ Zone 4a: Metal Assembly Palletizer

**3-axis Pick and Place** / metal palletizing sequence.

### Network 16 â€“ Zone 4a: Metal Components RFID

RFID handling for metal components / pallets.

### Network 17 â€“ Zone 3b: Plastic Conveyor Belts before Pick and Place Assembly

Transport before plastic 2-axis assembly.

### Network 18 â€“ Zone 3b: Plastic Pick and Place 2

**2-axis Pick and Place** â€” mounts plastic base and lid.

### Network 19 â€“ Zone 3b: Plastic Scale 2

Weighs the finished plastic assembly.

### Network 20 â€“ Zone 3b: Plastic Conveyor Belts after Scale 2

Transport toward plastic palletizer.

### Network 21 â€“ Zone 4a: Metal RFID

Additional metal RFID network (write/read path as wired in TIA).

### Network 22 â€“ Zone 4b: Conveyor Belts before Plastic Palletizer

Transport before plastic palletizing.

### Network 23 â€“ Zone 4b: Roller Conveyor Belts before Plastic Palletizer

Roller conveyors at the plastic palletizer infeed.

### Network 24 â€“ Zone 4b: Plastic Assembly Palletizer

Automatic palletizing of plastic assemblies.

### Network 25 â€“ Zone 4b: Plastic RFID

RFID write/read for plastic pallets (priority Write path for Warehouse_1 gate).

### Network 26 â€“ Zone 5a: Conveyor Belts to Plastic Components Warehouse

Transport from plastic palletizing to the plastic warehouse transfer position.

### Network 27 â€“ Zone 5b: Conveyor Belts to Metal Components Warehouse

Transport from metal palletizing to the metal warehouse transfer position.

### Network 28 – Zone 5a: Metal Components Warehouse

**Warehouse_2** — metal Hochregal (Stacker Crane 1). Merker `%M70+`, DBs `gldb_*_W2`. Automatik **ohne** Reader 0 / State 10 (Produkt von 4A). SCL: `scl/Zone_5a_Metall_Hochregallager/OB1_NW28_Metal_Warehouse.scl`.

### Network 29 â€“ Zone 5b: Plastic Components Warehouse

**Warehouse_1** â€” plastic Hochregal (Stacker Crane 0). SCL: `scl/Zone_5b_Hochregallager/`. Gate + RFID Read Reader 5 + Auto-Einlagern.

---

## Overall Program Function

During every PLC scan cycle, the networks are processed sequentially from **Network 1 to Network 29**, then **`FB_Plant_Start_Stop`** (production Start/Stop + Not-Aus, Q inhibit), then `"OB100_Startup_Init" := FALSE`.

**Startup:** **OB100** runs once on STOP→RUN (`scl/HMI_Plant/OB100_Startup.scl`). Safe modes/commands; warehouse DBs stay remanent. Not part of the cyclic sweep.

Material flow:

**Raw Material â†’ CNC â†’ Conveyor â†’ Vision â†’ Pick & Place â†’ Weighing â†’ Palletizing â†’ RFID â†’ Warehouse Transport â†’ Storage**

Separation into networks improves readability, commissioning and troubleshooting. Detailed sequences live in function blocks; OB1 coordinates the plant.
