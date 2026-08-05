# Abschlussarbeit — Fertigungs- und Lageranlage

**Thema:** Entwicklung und Simulation einer automatisierten Fertigungs- und Lageranlage mit RFID-gestützter Produktverfolgung in **TIA Portal V20** und **Factory I/O**

**Dokumentation:** [`docs/README.md`](docs/README.md)

## Factory — alles in diesem Projekt

| Zone | Subsystem | Code |
|---|---|---|
| 3 | Pick & Place | `scl/PickPlace_DigitalAnalog.scl` |
| 4 | Palettierer | `scl/FB_Palletizer.scl` (+ OB1-Aufruf) |
| 5 | **Hochregallager** | `scl/Hochregallager/*.scl` |

## Schnellzugriff

- [Projektgrundlagen / Freigabe](docs/01_Projektgrundlagen/)
- [**HMI Gesamtanlage (1 TP)**](docs/03_Technik/HMI_Gesamtanlage.md)
- [Palettierer](docs/04_Subsysteme/Palettierer/)
- [Hochregallager](docs/04_Subsysteme/Hochregallager/)
- [Pick & Place](docs/04_Subsysteme/PickPlace_2Axis/)
