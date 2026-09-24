# Phase 2 — Grenzen der Maschine

## Zur Maschine gehören (Lageplan + TIA-Netzwerke)

**Linie A = Metall, Linie B = Kunststoff.**  
Netzwerkliste: [PLC_Networks.md](PLC_Networks.md) — **29** OB1-Netzwerke

- **Zone 1A (NW 1–2):** Rohmaterial-Annahme Metall, Bearbeitungszentren (Roboter + CNC, Base und Deckel)
- **Zone 1B (NW 4, 6):** Rohmaterial-Annahme Kunststoff, Bearbeitungszentren (Roboter + CNC, Base und Deckel)
- **Zone 2A (NW 3, 5):** Transportband Metall; VisionData Sensors (NW 5)
- **Zone 2B (NW 7–8):** Vision FB17 (`VisionSensorData`) + Transportband Kunststoff
- **Zone 3A (NW 9–12):** Bänder, **2-axis Pick and Place** Metall (NW 10), Waage 1
- **Zone 3B (NW 17–20):** Bänder, **2-axis Pick and Place** Kunststoff (NW 18), Waage 2
- **Zone 4A (NW 13–16, 21):** Band/Rollenbahn, **3-axis Pick and Place** (NW 15), RFID Metall
- **Zone 4B (NW 22–25):** Band/Rollenbahn, Palettierer Kunststoff, RFID Write (NW 25)
- **Zone 5A (NW 26, 28):** **Metall-Hochregal Warehouse_2 (NW 28)**; Band zum Kunststoff-Hochregal (NW 26)
- **Zone 5B (NW 27, 29):** **Kunststoff-Hochregal Warehouse_1 (NW 29)**; Band zum Metall-Hochregal (NW 27)
- **SPS:** CPU 1518F-4 PN/DP (`PLC_1`), HMI TP2200 Comfort (`HMI_1`) — [Hardware_SPS.md](../03_Technik/Hardware_SPS.md)
- **OB100** (Startup) — `scl/HMI_Plant/OB100_Startup.scl`
- **Ein** HMI (TP) für alle Bereiche
- **Lagerverwaltung Online** (Streamlit): Web-Suche W1/W2 (SQLite) + **OPC UA live** Occupancy/Ziel — [Lagerverwaltung_Online.md](../03_Technik/Lagerverwaltung_Online.md)
- **Plant Start/Stop:** HMI `%M58` ODER Factory I/O `%E9` / `%A15` — [HMI_Gesamtanlage.md](../03_Technik/HMI_Gesamtanlage.md)
- SPS (TIA Portal V20), Schaltschrank, Sicherheitskreise (konzeptionell)

## Nicht Bestandteil

- externe Energieversorgung
- Gabelstapler / Transport außerhalb der Anlage
- Bedienpersonal
- ERP-System
- Live-Sync Web-Lagerverwaltung ↔ SPS-DBs (`gldb_LagerverwaltungData`)
- **Wasserverbrauch / Wasserwirtschaft**
