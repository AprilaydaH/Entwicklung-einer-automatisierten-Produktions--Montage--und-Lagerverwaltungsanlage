# HMI Gesamtanlage — ein Touch Panel

**Prinzip:** **Eine** HMI (Siemens TP) für die **gesamte** Factory laut [Lageplan](../01_Projektgrundlagen/Lageplan.md).

---

## Screens nach Lageplan

| Screen | Zone / Bereich |
|---|---|
| **Übersicht** | Materialfluss, Status aller Zonen |
| **Zone 1 Metall** | CNC Deckel + Base |
| **Zone 2 Kunststoff** | CNC Deckel + Base |
| **Zone 3 Pick&Place** | 3A + 3B |
| **Zone 4 Palettierer** | 4A Metal + 4B Plastic |
| **Zone 5 Roboter** | Stations a–d |
| **Förderbänder** | Verbindungsstrecken |
| **Hochregallager** | Ein-/Auslagern, Fächer, Suche |
| **Rezept / Diagnose** | Parameter, Alarme, I/O |

Header (immer): Betriebsart, zentraler Stop, Sammelmeldung, Zonenlampen.

Palettierer-Detail: [Zone4 HMI_Organisation](../04_Anlagenbereiche/Zone4_Palettierer/HMI_Organisation.md)

---

## SPS-Zuordnung (ein Projekt)

| Screen | FB / Ordner |
|---|---|
| Zone 3 | `scl/Zone3_PickPlace/` — 2 Instanzen |
| Zone 4 | `scl/Zone4_Palettierer/FB_Palletizer` — 2 Instanzen (4A/4B) |
| Hochregal | `scl/Hochregallager/` |
| Zone 1/2/5/Förder | *folgt* |

**Nicht im Scope:** Wasserverbrauch.
