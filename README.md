# Entwicklung einer automatisierten Produktions-, Montage- und Lagerverwaltungsanlage

Abschlussprojekt: **TIA Portal V20** + **Factory I/O** + RFID-Produktverfolgung.  
Autor: **Dereje Hailemariam**

**Freigabe-Thema:** Entwicklung und Simulation einer automatisierten Fertigungs- und Lageranlage mit RFID-gestützter Produktverfolgung.

| Dokument | Link |
|---|---|
| Factory-Haupttext | [`docs/01_Projektgrundlagen/Gesamtanlage.md`](docs/01_Projektgrundlagen/Gesamtanlage.md) |
| Doku-Index | [`docs/README.md`](docs/README.md) |
| SCL-Index | [`scl/README.md`](scl/README.md) |
| SPS-Netzwerke | [`docs/01_Projektgrundlagen/PLC_Networks.md`](docs/01_Projektgrundlagen/PLC_Networks.md) |
| HMI-Konzept | [`docs/03_Technik/HMI_Gesamtanlage.md`](docs/03_Technik/HMI_Gesamtanlage.md) |
| Lagerverwaltung Web | [`docs/03_Technik/Lagerverwaltung_Online.md`](docs/03_Technik/Lagerverwaltung_Online.md) |

---

## Was ist dieses Projekt?

Eine **gesamte Factory** in **einem Git-Repository**:

- zwei Linien: **Metall** und **Kunststoff**
- Rohannahme → Vision → Pick & Place → Palettierer/RFID → Hochregal
- **eine SPS** (S7-1500 / PLCSIM) und **ein HMI** (Touch Panel)
- Simulation in **Factory I/O**, optional Web-Lagerverwaltung über **OPC UA**

**Nicht im Scope:** Wasserverbrauch / Waage-Wasserwirtschaft.

---

## Repository-Struktur

```
docs/          Dokumentation (Projekt, Sicherheit, Technik, Zonen, CE)
scl/           SCL-Quellen nach Lageplan-Zonen (Zone_1a … Zone_5b)
simulation/    Factory I/O Szenen + TIA-Pfad-Hinweis
scripts/       Lokale Hilfsskripte (Organisieren, Präsentation)
nodered/       Optional Node-RED Flows
```

### Zonen → Code

| Zone | Inhalt | Ordner |
|---|---|---|
| 1A / 1B | Roh + CNC Metall / Kunststoff | `scl/Zone_1a_Metall/` · `Zone_1b_Kunststoff/` |
| 2A / 2B | Förder + Vision | `scl/Zone_2a_Foerderbaender/` · `Zone_2b_Vision_Foerderbaender/` |
| 3A / 3B | 2-axis Pick & Place + Waage | `scl/Zone_3a_Metall_PickPlace/` · `Zone_3b_Kunststoff_PickPlace/` |
| 4A | 3-axis P&P + RFID Metall | `scl/Zone_4a_Metall_Palletizer_RFID/` |
| 4B | Palettierer + RFID Kunststoff | `scl/Zone_4b_Kunststoff_Palletizer_RFID/` |
| 5A | Bänder + Metall-Hochregal W2 | `scl/Zone_5a_Foerderband_Lager/` · `Zone_5a_Metall_Hochregallager/` |
| 5B | Kunststoff-Hochregal W1 | `scl/Zone_5b_Hochregallager/` |
| Plant | Start/Stop, Startup, Prod/Day | `scl/HMI_Plant/` |

**Warehouses:** W1 Kunststoff NW **29** · W2 Metall NW **28**

---

## So implementierst du (TIA + Factory I/O)

### 1) Voraussetzungen
- TIA Portal **V20**
- Factory I/O
- PLCSIM (Simulation) oder echte CPU
- Optional: Comfort/Unified Panel für HMI

### 2) Projekt öffnen
1. TIA: lokales `.ap20` öffnen (Pfad siehe `simulation/TIA/README.md`)
2. Factory I/O: Szene aus `simulation/FactoryIO/` laden (z. B. `aBSCHLUSSPROJEKT.factoryio`)

### 3) SCL importieren
1. In TIA: **Externe Quellen** → `.scl` aus dem passenden `scl/Zone_*/` Ordner hinzufügen
2. Blöcke generieren (FB / FC / UDT)
3. Instanz-DBs anlegen (z. B. `FB_Palletizer_DB`, Warehouse-Instanzen)

### 4) Tags und I/O
1. PLC-Tags aus den CSV-Dateien im jeweiligen Zone-Ordner importieren
2. Factory I/O Driver auf **dieselben** `%I` / `%Q` Adressen mappen
3. Konflikte zwischen Zonen vermeiden (Adressräume getrennt halten)

### 5) OB1 verdrahten
1. Netzwerkaufrufe laut [`PLC_Networks.md`](docs/01_Projektgrundlagen/PLC_Networks.md)
2. Pro Zone den passenden `OB1_*.scl` als Vorlage nutzen
3. Plant Start/Stop zuletzt (`scl/HMI_Plant/`)

### 6) Inbetriebnahme-Reihenfolge
1. **Manual** je Station (Jog + Sensoren)
2. **Auto** Single-Cycle
3. Linie verbinden (Vision → RFID → Palettierer → Lager)
4. HMI-Screens anbinden (ein TP für alle Zonen)

### 7) Schnellstart empfohlen
| Ziel | Start hier |
|---|---|
| Palettierer Kunststoff | `scl/Zone_4b_Kunststoff_Palletizer_RFID/` |
| Hochregal Kunststoff W1 | `scl/Zone_5b_Hochregallager/PLASTIC_WAREHOUSE_GOLIVE.md` |
| Hochregal Metall W2 | `scl/Zone_5a_Metall_Hochregallager/WAREHOUSE_2_SETUP.md` |
| Lokal sync | `.\scripts\organize-local.ps1` |

---

## Lokale Pfade (dieser PC)

| Was | Pfad |
|---|---|
| Git-Repo | `C:\Users\derej\Projects\PickPlace-2Axis-SCL` |
| Factory I/O Kopien | `simulation/FactoryIO/` |
| TIA `.ap20` | OneDrive `...\Abschlussprojekt\Abschlussprojekt\` (nicht im Git) |

---

## Status (Kurz)

| Fertig / weit | Offen |
|---|---|
| Zonen-SCL (P&P, Palettierer, RFID, Vision, W1/W2) | HMI-Screens am TP final verdrahten |
| Factory I/O + PLCSIM lauffähig | W2 erste Auto-Palette |
| Doku-Gerüst 01–05 | CNC-Feinsteuerung, CE ausfüllen |

---

## Legacy / Aufräumen

Aktuelle Ordner nutzen das Schema `Zone_1a_…` … `Zone_5b_…`.  
Ältere Pfade (`scl/Zone4_Palettierer/`, `Zone3_PickPlace/`, …) sind **Legacy** — für neue Arbeit die Zone-Ordner mit Unterstrich verwenden.
