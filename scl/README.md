# SCL — nach TIA-Netzwerken

**Netzwerke:** [PLC_Networks.md](../docs/01_Projektgrundlagen/PLC_Networks.md) · [Main_Program_Sweep.md](../docs/01_Projektgrundlagen/Main_Program_Sweep.md)  
**Factory:** [Gesamtanlage.md](../docs/01_Projektgrundlagen/Gesamtanlage.md)  
**Pflichtenheft (Codes → SCL):** [Pflichtenheft.md](../docs/01_Projektgrundlagen/Pflichtenheft.md)  
**Organisation:** [Projektorganisation.md](../docs/01_Projektgrundlagen/Projektorganisation.md)

Ordnernamen = Zone laut OB1 (`Zone_1a` … `Zone_5b`).  
Ältere Ordner: siehe [`LEGACY.md`](LEGACY.md).

## Warehouses

| WH | Zone | NW | Crane | Merker | Ordner |
|---|---|---:|---|---|---|
| **Warehouse_1** plastic | 5B | **29** | 0 | `%M60+` | [`Zone_5b_Hochregallager/`](Zone_5b_Hochregallager/) |
| **Warehouse_2** metal | 5A | **28** | 1 | `%M70+` | [`Zone_5a_Metall_Hochregallager/`](Zone_5a_Metall_Hochregallager/) |

## Ordner ↔ Netzwerke

| Ordner | TIA-NW | Inhalt |
|---|---|---|
| [`Zone_1a_Metall/`](Zone_1a_Metall/) | 1–2 | Rohannahme + CNC/Roboter Metall |
| [`Zone_1b_Kunststoff/`](Zone_1b_Kunststoff/) | 4, 6 | Rohannahme + CNC/Roboter Kunststoff |
| [`Zone_2a_Foerderbaender/`](Zone_2a_Foerderbaender/) | **3, 5** | Band Metall · **Vision Metall** (`FB_VisionReader_Metal`) |
| [`Zone_2b_Vision_Foerderbaender/`](Zone_2b_Vision_Foerderbaender/) | 7–8 | Vision Kunststoff + Band |
| [`Zone_3a_Metall_PickPlace/`](Zone_3a_Metall_PickPlace/) | 9–12 | Band, 2-axis P&P, Waage 1 |
| [`Zone_3b_Kunststoff_PickPlace/`](Zone_3b_Kunststoff_PickPlace/) | 17–20 | Band, 2-axis P&P, Waage 2 |
| [`Zone_4a_Metall_Palletizer_RFID/`](Zone_4a_Metall_Palletizer_RFID/) | 13–16, 21 | Palettierer + RFID Metall |
| [`Zone_4b_Kunststoff_Palletizer_RFID/`](Zone_4b_Kunststoff_Palletizer_RFID/) | 22–25 | Palettierer + RFID Kunststoff |
| [`Zone_5a_Foerderband_Lager/`](Zone_5a_Foerderband_Lager/) | **26, 27** | NW26→plastic W1 · NW27→metal W2 |
| [`Zone_5a_Metall_Hochregallager/`](Zone_5a_Metall_Hochregallager/) | **28** | Metall-Hochregal Warehouse_2 |
| [`Zone_5b_Hochregallager/`](Zone_5b_Hochregallager/) | **29** | Kunststoff-Hochregal Warehouse_1 |

## Go-live Einstieg

| Linie | Datei |
|---|---|
| Kunststoff W1 | [`Zone_5b_Hochregallager/PLASTIC_WAREHOUSE_GOLIVE.md`](Zone_5b_Hochregallager/PLASTIC_WAREHOUSE_GOLIVE.md) |
| Metall W2 | [`Zone_5a_Metall_Hochregallager/WAREHOUSE_2_SETUP.md`](Zone_5a_Metall_Hochregallager/WAREHOUSE_2_SETUP.md) |
| Web-Suche W1/W2 + OPC UA live | [`docs/03_Technik/Lagerverwaltung_Online.md`](../docs/03_Technik/Lagerverwaltung_Online.md) |
| OB1 NW 28 | [`Zone_5a_Metall_Hochregallager/OB1_NW28_Metal_Warehouse.scl`](Zone_5a_Metall_Hochregallager/OB1_NW28_Metal_Warehouse.scl) |
| OB100 Startup | [`HMI_Plant/OB100_Startup.scl`](HMI_Plant/OB100_Startup.scl) |
| OB1 NW 5 Vision | [`Zone_2a_Foerderbaender/OB1_NW5_Metal_Vision.scl`](Zone_2a_Foerderbaender/OB1_NW5_Metal_Vision.scl) |
| OB1 NW 27 Bänder | [`Zone_5a_Foerderband_Lager/OB1_NW27_Belts_to_Metal_Warehouse.scl`](Zone_5a_Foerderband_Lager/OB1_NW27_Belts_to_Metal_Warehouse.scl) |
| OB1 nach NW 29 | [`HMI_Plant/FB_Plant_Start_Stop.md`](HMI_Plant/FB_Plant_Start_Stop.md) — Produktion Start/Stop + Not-Aus (FUP, letzter FB-Aufruf) · Adressen [`PLC_TAG_ADDRESS_FIXES.md`](HMI_Plant/PLC_TAG_ADDRESS_FIXES.md) |

## Wichtige OB1-Dateien

| Datei | NW / Zweck |
|---|---|
| `Zone_5b_Hochregallager/OB1_Plastic_Warehouse.scl` | Kunststoff Vision→RFID→Lager |
| `Zone_5a_Metall_Hochregallager/OB1_NW28_Metal_Warehouse.scl` | Metall Warehouse_2 |
| `Zone_4a_Metall_Palletizer_RFID/OB1_GantryPickPlace.scl` | 4A 3-axis P&P |
| `Zone_4a_Metall_Palletizer_RFID/OB1_RFID_Metal.scl` | RFID Metall Write (4a) |
| `Zone_4b_Kunststoff_Palletizer_RFID/OB1_Palletizer.scl` | 4B Palettierer |
