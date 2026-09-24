# Phase 1 — Projektorganisation

## Projektname

**Projekttitel:**  
Entwicklung einer automatisierten Produktions-, Montage- und Lagerverwaltungsanlage

**Freigabe-Thema (offiziell genehmigt):**  
Entwicklung und Simulation einer automatisierten Fertigungs- und Lageranlage mit RFID-gestützter Produktverfolgung in TIA Portal und Factory I/O

**Zentrale Factory-Doku:** [Gesamtanlage.md](Gesamtanlage.md)

## Ein Repository

Die gesamte Factory laut [Lageplan](Lageplan.md) liegt in **diesem einen Git-Repository** (Zone 1–5, Förderbänder, Hochregallager, RFID, ein HMI).

| Zone | Inhalt | Ordner |
|---|---|---|
| 1A | Metall Roh + Roboter + CNC | `scl/Zone_1a_Metall/` |
| 1B | Kunststoff Roh + Roboter + CNC | `scl/Zone_1b_Kunststoff/` |
| 2A | Transportband Metall + **Vision NW 5** | `scl/Zone_2a_Foerderbaender/` |
| 2B | Band Kunststoff + Vision (RFID-Daten) | `scl/Zone_2b_Vision_Foerderbaender/` |
| 3A/3B | 2-axis Pick and Place + Waage | `scl/Zone_3a_Metall_PickPlace/` · `scl/Zone_3b_Kunststoff_PickPlace/` |
| 4A | Palettierer + RFID Metall | `scl/Zone_4a_Metall_Palletizer_RFID/` |
| 4B | Palettierer + RFID Kunststoff | `scl/Zone_4b_Kunststoff_Palletizer_RFID/` |
| 5A | Band NW26→W1 · **Metall-Hochregal W2 NW28** | `scl/Zone_5a_Foerderband_Lager/` · `scl/Zone_5a_Metall_Hochregallager/` |
| 5B | Band NW27→W2 · **Kunststoff-Hochregal W1 NW29** | `scl/Zone_5a_Foerderband_Lager/` · `scl/Zone_5b_Hochregallager/` |

TIA-Netzwerke (29): [PLC_Networks.md](PLC_Networks.md) · [Main_Program_Sweep.md](Main_Program_Sweep.md)

**HMI:** ein Touch Panel — [HMI_Gesamtanlage](../03_Technik/HMI_Gesamtanlage.md)  
**Web:** [Lagerverwaltung Online](../03_Technik/Lagerverwaltung_Online.md) — SQLite-Suche + OPC UA live

## Warehouse-Zuordnung (verbindlich)

| Warehouse | Material | Zone | NW | Crane | Merker | DBs |
|---|---|---|---:|---|---|---|
| **Warehouse_1** | Kunststoff | 5B | **29** | Stacker **0** | `%M60+` | `gldb_*` |
| **Warehouse_2** | Metall | 5A | **28** | Stacker **1** | `%M70+` | `gldb_*_W2` |

## Vorgehen

1. ~~Kunststoff-Warehouse E2E~~ — [PLASTIC_WAREHOUSE_GOLIVE](../../scl/Zone_5b_Hochregallager/PLASTIC_WAREHOUSE_GOLIVE.md)  
2. ~~Metall-Warehouse (W2) SCL + FIO + NW 28~~ — [WAREHOUSE_2_SETUP](../../scl/Zone_5a_Metall_Hochregallager/WAREHOUSE_2_SETUP.md)  
3. ~~OPC UA `Si_Lagerverwaltung_Online` live~~ — Streamlit auf `192.168.0.1:4840` (PLCSIM Advanced)  
4. W2 Inbetriebnahme: Raster-Teach, erste Palette Hand/Auto — **kein** Reader 0 / State 10 (Produkt von 4A Reader 1)  
5. 2-axis / 3-axis P&P und Bänder in Gesamt-OB1 festziehen  
6. **Gesamt-HMI** am TP: Start/Stop `%M58`, Verbindung Simulation = **PLCSIM**, 54-Fach-Animation  
7. Sicherheit / CE dokumentieren  

Zurück: [Kapitel 1](README.md) · [docs](../README.md)
