# Entwicklung einer automatisierten Produktions-, Montage- und Lagerverwaltungsanlage

**Dokumentation der Abschlussarbeit**

**Freigabe-Thema:** Fertigungs- und Lageranlage mit RFID · TIA Portal V20 · Factory I/O  

| | |
|---|---|
| **Gesamtanlage (Haupttext)** | **[Gesamtanlage.md](01_Projektgrundlagen/Gesamtanlage.md)** |
| **Lastenheft (Word)** | **[Lastenheft_Abschlussprojekt.docx](01_Projektgrundlagen/Lastenheft_Abschlussprojekt.docx)** |
| **Pflichtenheft (Word)** | **[Pflichtenheft_Abschlussprojekt.docx](01_Projektgrundlagen/Pflichtenheft_Abschlussprojekt.docx)** · [MD](01_Projektgrundlagen/Pflichtenheft.md) · [Station-Tags](01_Projektgrundlagen/Station_PLC_FIO_Tags.md) |
| Main Program Sweep | [Main_Program_Sweep.md](01_Projektgrundlagen/Main_Program_Sweep.md) |
| Hardware | [Hardware_SPS.md](03_Technik/Hardware_SPS.md) |
| SPS-Netzwerke | [PLC_Networks.md](01_Projektgrundlagen/PLC_Networks.md) |
| Freigabe | [PDF](01_Projektgrundlagen/Freigabedokument_Abschlussarbeit_Dereje_Hailemariam.pdf) · [Zusammenfassung](01_Projektgrundlagen/Freigabe_Zusammenfassung.md) |
| Lageplan | [PDF](01_Projektgrundlagen/Lageplan.pdf) · [Zonenübersicht](01_Projektgrundlagen/Lageplan.md) |

---

## Gliederung

| Kap. | Ordner | Inhalt |
|---|---|---|
| **1** | [01_Projektgrundlagen](01_Projektgrundlagen/) | Freigabe, **Gesamtanlage**, Lageplan, Grenzen |
| **2** | [02_Sicherheit](02_Sicherheit/) | EN ISO 12100 |
| **3** | [03_Technik](03_Technik/) | SPS, **ein Gesamt-HMI**, Netzwerk |
| **4** | [04_Anlagenbereiche](04_Anlagenbereiche/) | Zone 1–5 · Förder · RFID · Hochregal |
| **5** | [05_CE_Dokumentation](05_CE_Dokumentation/) | CE (später) |

---

## Ein Repository = gesamte Factory

| Zone | Bereich | Code |
|---|---|---|
| 1A | Metall Roh + CNC | `scl/Zone_1a_Metall/` |
| 1B | Kunststoff Roh + CNC | `scl/Zone_1b_Kunststoff/` |
| 2A | Band Metall + Vision NW 5 | `scl/Zone_2a_Foerderbaender/` |
| 2B | Vision + Band Kunststoff | `scl/Zone_2b_Vision_Foerderbaender/` |
| 3A/3B | 2-axis Pick and Place + Waage | `scl/Zone_3a_Metall_PickPlace/` · `Zone_3b_…` |
| 4A | 3-axis Pick and Place + RFID Metall | `scl/Zone_4a_Metall_Palletizer_RFID/` |
| 4B | Palettierer + RFID Kunststoff | `scl/Zone_4b_Kunststoff_Palletizer_RFID/` |
| 5A | Band NW26→W1 · **Metall-Hochregal W2 NW28** | `scl/Zone_5a_Foerderband_Lager/` · `scl/Zone_5a_Metall_Hochregallager/` |
| 5B | Band NW27→W2 · **Kunststoff-Hochregal W1 NW29** | `scl/Zone_5a_Foerderband_Lager/` · `scl/Zone_5b_Hochregallager/` |

**Warehouses:** W1 plastic NW **29** (`%M60+`) · W2 metal NW **28** (`%M70+`)

**HMI:** ein TP → [HMI_Gesamtanlage.md](03_Technik/HMI_Gesamtanlage.md)  
**Web:** [Lagerverwaltung_Online.md](03_Technik/Lagerverwaltung_Online.md) — SQLite-Suche + **OPC UA live** (`Si_Lagerverwaltung_Online`)

**SCL:** [`scl/README.md`](../scl/README.md)

**Nicht im Scope:** Wasserverbrauch.

---

## Implementierungsstand (Kurz) — 19.09.2026

| Fertig / weit | Offen |
|---|---|
| Zone 3 Pick & Place SCL | Zone 1/2 CNC-Feinsteuerung |
| Zone 4A 3-axis P&P, 4B Palettierer | Förderband-Feinabstimmung |
| RFID + Vision (Kunststoff + Metall) | **HMI am TP:** Events Start/Stop, 54-Fach-Animation |
| **Warehouse_1** plastic E2E (NW 29) | W2 erste Palette Hand + Automatik |
| **Warehouse_2** metal SCL + FIO + NW 28 | W2 Automatik ohne Reader 0 (Produkt von 4A) |
| Raster-Teach W1/W2 | Sicherheit / CE ausfüllen |
| **OPC UA live** Streamlit ↔ CPU `192.168.0.1:4840` | Live-Sync Web-SQLite ↔ Lager-DB (nicht im Scope) |
| Plant Start/Stop-Rezept (`%M58` / `%E9`) | FUP `FB_Plant_Start_Stop` in TIA zeichnen |

**Simulation:** PLCSIM Advanced, CPU **1518F-4 PN/DP**, Instanz `192.168.0.1`. HMI-Runtime auf dem Laptop: Verbindung **PLCSIM**, nicht Ethernet.

**Weiter mit:** [WAREHOUSE_2_SETUP](../scl/Zone_5a_Metall_Hochregallager/WAREHOUSE_2_SETUP.md) · [WAREHOUSE_FIRST_PALLET](../scl/Zone_5a_Metall_Hochregallager/WAREHOUSE_FIRST_PALLET.md) · [HMI_Gesamtanlage](03_Technik/HMI_Gesamtanlage.md) · [Projektorganisation](01_Projektgrundlagen/Projektorganisation.md)
