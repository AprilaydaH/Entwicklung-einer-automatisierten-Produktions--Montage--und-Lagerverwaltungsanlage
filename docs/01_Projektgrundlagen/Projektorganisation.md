# Phase 1 — Projektorganisation

## Projektname

**Projekttitel:**  
Entwicklung einer automatisierten Produktions-, Montage- und Lagerverwaltungsanlage

**Freigabe-Thema (offiziell genehmigt):**  
Entwicklung und Simulation einer automatisierten Fertigungs- und Lageranlage mit RFID-gestützter Produktverfolgung in TIA Portal und Factory I/O

## Ein Repository

Die gesamte Factory laut [Lageplan](Lageplan.md) liegt in **diesem einen Git-Repository** (Zone 1–5, Förderbänder, Hochregallager, ein HMI).

| Zone | Inhalt | Ordner |
|---|---|---|
| 1 | Metall CNC | `scl/Zone1_Metall/` |
| 2 | Kunststoff CNC | `scl/Zone2_Kunststoff/` |
| 3A/3B | Pick & Place | `scl/Zone3_PickPlace/` |
| 4A/4B | Palettierer Metal/Plastic | `scl/Zone4_Palettierer/` |
| 5A/5B | Roboter a–d | `scl/Zone5_Roboter/` |
| — | Förderbänder | `scl/Foerderbaender/` |
| — | Hochregallager | `scl/Hochregallager/` |

**HMI:** ein Touch Panel — [HMI_Gesamtanlage](../03_Technik/HMI_Gesamtanlage.md)

## Vorgehen

1. Maschinen-FBs je Zone fertigstellen (zuerst Zone 4 Palettierer)  
2. Screens am Gesamt-HMI anbinden  
3. Förder + CNC + Roboter ergänzen  
4. Sicherheit / CE dokumentieren  

Zurück: [Kapitel 1](README.md) · [docs](../README.md)
