# Entwicklung einer automatisierten Produktions-, Montage- und Lagerverwaltungsanlage

**Projekttitel** (wie Repository / Abschlussarbeit)  
**Freigabe-Thema:** Entwicklung und Simulation einer automatisierten Fertigungs- und Lageranlage mit RFID-gestützter Produktverfolgung in **TIA Portal V20** und **Factory I/O**

**Dokumentation:** [`docs/README.md`](docs/README.md)  
**Lageplan:** [`docs/01_Projektgrundlagen/Lageplan.pdf`](docs/01_Projektgrundlagen/Lageplan.pdf)

## Struktur laut Lageplan

| Zone | Inhalt | Code |
|---|---|---|
| 1 | Metall CNC Deckel/Base | `scl/Zone1_Metall/` |
| 2 | Kunststoff CNC Deckel/Base | `scl/Zone2_Kunststoff/` |
| 3A/3B | Pick & Place | `scl/Zone3_PickPlace/` |
| 4A/4B | Palettierer Metal/Plastic | `scl/Zone4_Palettierer/` |
| 5A/5B | Robot stations a–d | `scl/Zone5_Roboter/` |
| — | Förderbänder | `scl/Foerderbaender/` |
| — | Hochregallager | `scl/Hochregallager/` |

**Ein HMI** für alle Maschinen: [HMI_Gesamtanlage](docs/03_Technik/HMI_Gesamtanlage.md)
