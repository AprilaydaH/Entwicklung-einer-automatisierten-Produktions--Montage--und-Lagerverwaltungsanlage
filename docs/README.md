# Entwicklung einer automatisierten Produktions-, Montage- und Lagerverwaltungsanlage

**Dokumentation der Abschlussarbeit**

**Freigabe-Thema:** Fertigungs- und Lageranlage mit RFID · TIA Portal V20 · Factory I/O  

**Freigabe:** [PDF](01_Projektgrundlagen/Freigabedokument_Abschlussarbeit_Dereje_Hailemariam.pdf) · [Zusammenfassung](01_Projektgrundlagen/Freigabe_Zusammenfassung.md)  
**Lageplan:** [PDF](01_Projektgrundlagen/Lageplan.pdf) · [Zonenübersicht](01_Projektgrundlagen/Lageplan.md)

---

## Gliederung

| Kap. | Ordner | Inhalt |
|---|---|---|
| **1** | [01_Projektgrundlagen](01_Projektgrundlagen/) | Freigabe, Lageplan, Grenzen, Verwendung |
| **2** | [02_Sicherheit](02_Sicherheit/) | EN ISO 12100 |
| **3** | [03_Technik](03_Technik/) | SPS, **ein Gesamt-HMI**, Netzwerk |
| **4** | [04_Anlagenbereiche](04_Anlagenbereiche/) | Zone 1–5 · Förder · Hochregal |
| **5** | [05_CE_Dokumentation](05_CE_Dokumentation/) | CE (später) |

---

## Ein Repository = gesamte Factory

| Zone | Bereich | Code |
|---|---|---|
| 1 | Metall CNC | `scl/Zone1_Metall/` |
| 2 | Kunststoff CNC | `scl/Zone2_Kunststoff/` |
| 3A/3B | Pick & Place | `scl/Zone3_PickPlace/` |
| 4A/4B | Palettierer Metal/Plastic | `scl/Zone4_Palettierer/` |
| 5A/5B | Roboter a–d | `scl/Zone5_Roboter/` |
| — | Förderbänder | `scl/Foerderbaender/` |
| — | Hochregallager | `scl/Hochregallager/` |

**HMI:** ein TP → [HMI_Gesamtanlage.md](03_Technik/HMI_Gesamtanlage.md)

**Nicht im Scope:** Wasserverbrauch.

---

## Status

| Vorhanden | Offen |
|---|---|
| Lageplan + Projektgerüst | Zone 1/2 CNC-FBs |
| Zone 3 Pick&Place FB | Zone 5 Roboter |
| Zone 4 Palettierer FB (+ 4A/4B Instanzen) | Förderbänder-FBs |
| Hochregallager FBs | Gesamt-HMI Screens im TP |
| HMI-Konzept | RFID / Sicherheit ausfüllen |

**Weiter mit:** Zone 4 Palettierer testen → [Test_und_Inbetriebnahme](04_Anlagenbereiche/Zone4_Palettierer/Test_und_Inbetriebnahme.md)
