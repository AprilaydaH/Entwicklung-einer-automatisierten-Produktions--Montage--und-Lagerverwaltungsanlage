# Gesamtanlage â€” Factory-Dokumentation

**Projekttitel:** Entwicklung einer automatisierten Produktions-, Montage- und Lagerverwaltungsanlage  

**Freigabe-Thema:** Entwicklung und Simulation einer automatisierten Fertigungs- und Lageranlage mit RFID-gestÃ¼tzter Produktverfolgung in **TIA Portal V20** und **Factory I/O**

**Autor:** Dereje Hailemariam  
**Stand:** 19.09.2026 · Lastenheft **v1.6** · OPC UA live · HMI am TP noch offen  

---

## 1. Zweck dieses Dokuments

Dieses Dokument beschreibt die **gesamte Factory** aus SPS-, Materialfluss- und Software-Sicht: Zonen, Querschnittsfunktionen (RFID, Vision, Lager), Implementierungsstand und nÃ¤chste Schritte.

Detaildokumente liegen in [`docs/`](../README.md) und [`scl/`](../../scl/) je Anlagenbereich.

---

## 2. SystemÃ¼bersicht

Die Anlage ist eine **modular aufgebaute Fertigungs- und Lagerlinie** in Factory I/O, gesteuert durch **eine SPS** (S7-1500 / PLCSIM) und bedient Ã¼ber **ein Touch Panel (HMI)**.

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                         GESAMTANLAGE (Factory I/O)                          â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚  Zone 1A â€” METALL            â”‚  Zone 1B â€” KUNSTSTOFF                        â”‚
â”‚  Roh Â· Roboter A/B Â· CNC     â”‚  Roh Â· Roboter C/D Â· CNC                     â”‚
â”‚  Base + Deckel               â”‚  Base + Deckel                               â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚  Zone 2A â€” Transportband     â”‚  Zone 2B â€” Transportband                     â”‚
â”‚  (Metall)                    â”‚  + Vision Farbregistrierung (RFID-Daten)     â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚  Zone 3A â€” 2-axis P&P Metall â”‚  Zone 3B â€” 2-axis P&P Kunststoff             â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚  Zone 4A â€” 3-axis P&P + Pal. â”‚  Zone 4B â€” Palettierer Kunststoff            â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚  Zone 5A â€” Hochregal Metall  â”‚  Zone 5B â€” Hochregal Kunststoff + RFID       â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                              â†•
                    TIA Portal V20 Â· ein HMI (TP)
```

| Querschnitt | Funktion | Code |
|---|---|---|
| **RFID** | Produkt-Tag lesen/schreiben (Kunststoff + spÃ¤ter Metall) | `scl/Zone_4b_Kunststoff_Palletizer_RFID/` |
| **Vision** | Kunststoff Lid/Base erkennen, Farbe/Material encodieren | `scl/Zone_2b_Vision_Foerderbaender/FB_VisionReader.scl` |
| **Hochregallager** | 54 FÃ¤cher, Ein-/Auslagern, Lagerverwaltung | `scl/Zone_5b_Hochregallager/` |
| **HMI** | Ein TP fÃ¼r alle Zonen | `docs/03_Technik/HMI_Gesamtanlage.md` |

**Nicht im Scope:** Wasserverbrauch / Wasserwirtschaft.

---

## 3. Materialfluss

### 3.1 Kunststofflinie (PrioritÃ¤t â€” zuerst vollstÃ¤ndig in Betrieb)

```
Zone 1B Roh + Roboter C/D + CNC (Deckel / Base)
    â†’ Zone 2B Transportband
    â†’ Zone 3B Vision latch (Lid + Base at 2-axis P&P, before assembly)
         â†’ FB_VisionReader / VisionSensorData
         â†’ Color_Code, Artikelnummer, ProductTyp, RFID_CODE
         â†’ Montage Base + Deckel
    â†’ Zone 4B Palettierer + RFID Write Reader 2 (Allow_Write := 4b_Done)
         â†’ Pallet_Tagged (%M40.2) / Combo_Done (%M40.0)
    â†’ Zone 5A Band zum Kunststoff-Lager (NW 26)
    â†’ Zone 5B Warehouse_1 (NW 29)
         â†’ Gate: Paket_Fuer_Hochregal
         â†’ Auto: State 10 RFID Read Reader 5 (RFID_Lesen + RFID_Busy â†’ Gueltig)
         â†’ Freies Fach â†’ RegalbediengerÃ¤t â†’ Einlagern
         â†’ gldb_LagerverwaltungData.Fach[1..54]
```

**Gate Hochregallager:**  
`Paket_Fuer_Hochregal = Paket_Vor_Regal AND (Vision_Combo_Done OR Pallet_Tagged)`  
â†’ Palette erst nach erfolgreichem RFID-Schreiben fÃ¼r Auto-Einlagerung freigegeben.

**OB1-Reihenfolge (Kunststoff):** Vision â†’ DB_1 Write â†’ Gate â†’ Datenverwaltung â†’ Automatik â†’ Manual Soll â†’ Stacker â†’ DB_2 Read  

**Go-live:** [`WAREHOUSE_AUTO_START.md`](../../scl/Zone_5b_Hochregallager/WAREHOUSE_AUTO_START.md) Â· [`SYSTEM_AUDIT.md`](../../scl/Zone_5b_Hochregallager/SYSTEM_AUDIT.md) Â· [`PLASTIC_WAREHOUSE_GOLIVE.md`](../../scl/Zone_5b_Hochregallager/PLASTIC_WAREHOUSE_GOLIVE.md)  
I/O-Glue: [`OB1_Warehouse_1_IO.scl`](../../scl/Zone_5b_Hochregallager/OB1_Warehouse_1_IO.scl)  
Lastenheft: [`Lastenheft_Abschlussprojekt.docx`](Lastenheft_Abschlussprojekt.docx) (v1.6)

### 3.2 Metalllinie — Warehouse_2 (SCL + FIO, erste Auto-Palette offen)

```
Zone 1A Roh + Roboter A/B + CNC
    â†’ Zone 2A Transportband + Vision NW 5
    â†’ Zone 3A Montage (Metall)
    â†’ Zone 4A Palettierer + RFID
    â†’ Zone 5B Band zum Metall-Lager (NW 27)
    â†’ Zone 5A Metal Components Warehouse (NW 28) â€” Warehouse_2
```

**Code:** [`scl/Zone_5a_Metall_Hochregallager/`](../../scl/Zone_5a_Metall_Hochregallager/) — Spiegel Kunststoff (eigene DBs/tags `*_W2`).  
Automatik **ohne State 10 / Reader 0**; Produkt und RFID kommen von **Zone 4A Reader 1**. Occupancy `HRL_2_Occ_*` `%MB407`.

---

## 4. Zonen im Detail

| Zone | Bezeichnung | Aufgabe | SCL / Status |
|---|---|---|---|
| **1A** | Metall Roh + Roboter + CNC | Rohmaterial, Robotstation A/B, CNC Base + Deckel | `scl/Zone_1a_Metall/` â€” *Geplant* |
| **1B** | Kunststoff Roh + Roboter + CNC | Rohmaterial, Robotstation C/D, CNC Base + Deckel | `scl/Zone_1b_Kunststoff/` â€” *Geplant* |
| **2A** | Transportband Metall + Vision | FÃ¶rderung nach 1A; Vision NW 5 | `scl/Zone_2a_Foerderbaender/` — Vision **implementiert** · Band Feinsteuerung *offen* |
| **2B** | Transportband + Vision | FÃ¶rderung nach 1B; Farbregistrierung Lid/Base â†’ RFID-Daten | `scl/Zone_2b_Vision_Foerderbaender/FB_VisionReader.scl` â€” **implementiert** Â· Band *geplant* |
| **3A/3B** | 2-axis Pick and Place | Montage Base + Deckel | `scl/Zone_3a_â€¦` NW **10** Â· `scl/Zone_3b_â€¦` NW **18** |
| **4A** | 3-axis Pick and Place + Palettierer Metall | X/Y/Z + RFID (NW 15â€“16, 21) | `scl/Zone_4a_Metall_Palletizer_RFID/` â€” **implementiert** |
| **4B** | Palettierer Kunststoff | Palettierung + RFID (NW 24â€“25) | `scl/Zone_4b_Kunststoff_Palletizer_RFID/` â€” **implementiert** |
| **5A** | **Metall-Hochregal** (Warehouse_2) | **NW 28** + Band NW 26 | scl/Zone_5a_Metall_Hochregallager/ — **SCL + FIO**; erste Auto-Palette *offen* |
| **5B** | **Kunststoff-Hochregal** (Warehouse_1) | **NW 29** + Band NW 27 | scl/Zone_5b_Hochregallager/ — **E2E live** |

ZonenÃ¼bersicht mit Links: [`Lageplan.md`](Lageplan.md) Â· [`04_Anlagenbereiche/`](../04_Anlagenbereiche/README.md)

---

## 5. Produkt- und Lagercodierung

### 5.1 Vision (Zone 2B â€” TIA NW 5 / NW 7)

`FB17` `VisionSensorData` (Instanz-DB z. B. `2a_VisionSensor Data_DB`): Lid/Base-Werte, Color_Code, Materialart, Artikelnummer, ProductTyp, RFID_CODE, Combo_Done, Write_Req; AusgÃ¤nge `Lid_Reject_Metal` / `Base_Reject_Metal` fÃ¼r Metall-Reject.

Zwei Kameras (**Detects All Numerical**):

| Wert | Bedeutung |
|---:|---|
| 1 | Blue Raw |
| 2 | Blue Lid |
| 3 | Blue Base |
| 4 | Green Raw |
| 5 | Green Lid |
| 6 | Green Base |
| 7â€“9 | Metall â†’ `Reject_Metal` |

**Color_Code:** 1 = Blau, 2 = GrÃ¼n, 3 = Mixed (Lid/Base unterschiedlich)  
**ProductTyp:** LidÃ—10 + Base (z. B. 26 = Blue Lid + Green Base)

### 5.2 Artikelnummer (remanent, UInt)

```
Artikelnummer = YY Ã— 1000 + Materialart Ã— 100 + Color_Code
```

Beispiel: 20.08.2026, Kunststoff, Blau â†’ **26101**

### 5.3 RFID_CODE (Paletten-Tag, UDInt)

```
RFID_CODE = YYMMDD Ã— 1000 + Materialart Ã— 100 + Color_Code
```

Beispiel: 20.08.2026, Kunststoff, Blau â†’ **260820101**

### 5.4 Lagerverwaltung (UDT_Fach)

Jedes der **54 FÃ¤cher** speichert u. a.:

| Feld | Inhalt |
|---|---|
| `Materialart` | 1 Kunststoff, 2 Metall |
| `Color_Code` | 1 Blau, 2 GrÃ¼n, 3 Mixed |
| `Artikelnummer` | Produktnummer |
| `ProductTyp` | Montagekombination |
| `RFID_CODE` | Tag-Inhalt |
| `Position_X/Z` | Regalposition (Raster oder Einzel-Teach) |
| `Belegt` / `Gesperrt` | Lagerstatus |

---

## 6. RFID & Vision â€” Architektur

**Getrennte Function Blocks** (nicht kombiniert):

| Baustein | Rolle |
|---|---|
| `FB_VisionReader` (%FB17 VisionSensorData) | Lid/Base an 3B P&P latchen; Write_Req bei `4b_Done` |
| `FB_RFID_ReadWrite` DB_1 | **Write** Reader **2** (Zone 4b) |
| `FB_RFID_ReadWrite` DB_2 | **Read** Reader **5** (Zone 5b) |

**Kunststoff-Kette:** Vision latch â†’ Montage â†’ `4b_Done` â†’ DB_1 Write â†’ `Pallet_Tagged` â†’ Gate â†’ Auto State 10 â†’ DB_2 Read â†’ Einlagern.

Dokumentation: [`Zone_2b`](../04_Anlagenbereiche/Zone_2b_Vision_Foerderbaender/README.md) Â· [`Zone_4b`](../04_Anlagenbereiche/Zone_4b_Kunststoff_Palletizer_RFID/README.md) Â· [`Zone_5b`](../04_Anlagenbereiche/Zone_5b_Hochregallager/README.md)

---

## 7. Hochregallager

| Merkmal | Wert |
|---|---|
| FÃ¤cher | 54 (Factory I/O Automated Warehouse) |
| TIA | Warehouse_1 = Kunststoff (**NW 29**); Warehouse_2 = Metall (**NW 28**) |
| Gate W1 | `FB_Warehouse_Gate` â†’ `Paket_Fuer_Hochregal` |
| Gate W2 | `FB_Warehouse_Gate_W2` â†’ sensor only (phase1) |
| Stacker | W1 Crane 0 Â· W2 Crane 1 (`FB_Warehouse_Stacker_IO_W2`) |
| Automatik | W1 V5.6 Â· W2 `Hochregal_Automatik_Betrieb_W2` |
| Daten W2 | `gldb_LagerverwaltungData_W2` + `FB_Datenverwaltung_Lager_W2` |

**Plastic audit:** [`SYSTEM_AUDIT.md`](../../scl/Zone_5b_Hochregallager/SYSTEM_AUDIT.md)  
**Metal setup:** [`WAREHOUSE_2_SETUP.md`](../../scl/Zone_5a_Metall_Hochregallager/WAREHOUSE_2_SETUP.md)

### Raster-Teach (Fanuc-Methode)

Statt 54 Einzelpositionen: **Fach 1** als Basis + **Pitch_X/Pitch_Z** â†’ alle Positionen berechnen:

```
Mult_X = (Fach - 1) MOD Spalten
Mult_Z = (Fach - 1) DIV Spalten
Pos_X  = Basis_X + Pitch_X Ã— Mult_X
Pos_Z  = Basis_Z + Pitch_Z Ã— Mult_Z
```

Standard-Raster: **6 Spalten Ã— 9 Ebenen = 54**.  
Baustein: `FB_Berechn_Offset` Â· Anleitung: [`scl/Zone_5b_Hochregallager/RASTER_TEACH.md`](../../scl/Zone_5b_Hochregallager/RASTER_TEACH.md)

Dokumentation: [`docs/04_Anlagenbereiche/Zone_5b_Hochregallager/`](../04_Anlagenbereiche/Hochregallager/README.md)

---

## 8. Software-Architektur

### 8.1 Repository-Struktur

```
PickPlace-2Axis-SCL/
â”œâ”€â”€ docs/                    # Projektdokumentation (Abschlussarbeit)
â”œâ”€â”€ scl/                     # SCL-Quellcode je Zone / Querschnitt
â”œâ”€â”€ simulation/FactoryIO/    # Factory I/O Szenen
â””â”€â”€ scripts/                 # Hilfsskripte (Sync, Organisation)
```

### 8.2 OB1-Strategie

| OB1-Datei | Verwendung |
|---|---|
| **`OB1_Plastic_Warehouse.scl`** | **Go-live:** Vision â†’ RFID â†’ Hochregal (Kunststoff) |
| `OB1_Hochregallager.scl` | Nur Hochregallager (Test ohne Vision) |
| `Zone_4a_Metall_Palletizer_RFID/OB1_GantryPickPlace.scl` | 4A 3-axis P&P isoliert |
| `OB1_Palletizer.scl` | Zone 4B isoliert |
| `OB1_Hochregallager.scl` | Nur Hochregal (Test ohne Vision/RFID) |
| `legacy/OB1_Main_LEGACY.scl` | **Archiv** â€” flacher OB1 |

### 8.3 Tag-CSV (TIA Import)

| CSV | Bereich |
|---|---|
| `scl/Zone_4b_Kunststoff_Palletizer_RFID/PLC_Tags_RFID.csv` | Vision, RFID, Gates |
| `scl/Zone_5b_Hochregallager/PLC_Tags_Hochregallager.csv` | HMI, Raster, Kran |
| `scl/Zone_4a_Metall_Palletizer_RFID/PLC_Tags_GantryPickPlace.csv` | 3-axis P&P 4A (Tags `Gantry_*`) |
| `scl/Zone_4b_Kunststoff_Palletizer_RFID/PLC_Tags_Palletizer.csv` | Palettierer 4B |

---

## 9. HMI â€” Gesamtkonzept

**Ein Touch Panel** fÃ¼r alle Zonen. Empfohlene Screens:

| Screen | Inhalt |
|---|---|
| Ãœbersicht | Materialfluss, Zonenstatus |
| Zone 1A / 1B | Roh, Roboter, CNC Metall / Kunststoff |
| Zone 2A / 2B | TransportbÃ¤nder; 2B Vision-Farbe fÃ¼r RFID |
| Zone 3A / 3B | 2-axis Pick and Place |
| Zone 4A / 4B | 3-axis P&P + Palettierer |
| Zone 5A / 5B | Hochregallager, RFID, Einricht |
| Diagnose | Alarme, I/O, States |

Detail: [`docs/03_Technik/HMI_Gesamtanlage.md`](../03_Technik/HMI_Gesamtanlage.md)  
Web: SQLite-Suche + **OPC UA live** Belegung: [`Lagerverwaltung_Online.md`](../03_Technik/Lagerverwaltung_Online.md)

---

## 10. Implementierungsstand (19.09.2026)

| Bereich | Status | Nächster Schritt |
|---|---|---|
| Zone 3 Pick & Place | SCL + FIO | Feinabstimmung |
| Zone 4A 3-axis P&P | FB + OB1 + Tags | — |
| Zone 4B Palettierer | FB + OB1 + Tags | — |
| RFID + Vision | Kunststoff + Metall-FB | — |
| Warehouse_1 Kunststoff | E2E live (NW 29) | — |
| Warehouse_2 Metall | SCL + FIO + NW 28 + OPC UA | Erste Palette Hand/Auto |
| Zone 1A/1B CNC + Roboter | in OB1 | Feinsteuerung |
| Zone 2A/2B Band + Vision | Vision SCL | Band-Feinabstimmung |
| Plant Start/Stop | Tags `%M58` / `%E9`, Rezept FUP | FB in TIA zeichnen |
| OPC UA Web | **live** `Si_Lagerverwaltung_Online` @ `192.168.0.1:4840` | Belegung im Automatikzyklus zeigen |
| Gesamt-HMI TP2200 | Tags/Konzepte; Simulation nur über **PLCSIM** | Events Start/Stop, 54-Fach-Animation |
| Sicherheit / CE | Gerüst | Kapitel 2 / 5 |

**Aktuelle Priorität:** HMI am Panel verdrahten; W2 erste Palette. Kunststofflinie bleibt der E2E-Nachweis. CPU bleibt **1518F-4 PN/DP** (kein Tausch auf 1518T).

---

## 11. Inbetriebnahme-Reihenfolge (empfohlen)

1. **Tags importieren** (RFID + Hochregallager CSV)
2. **UDTs + globale DBs** kompilieren (`Color_Code`, `Raster` in UDT_Fach / Lager)
3. **FBs importieren** (Reihenfolge: siehe `README_SCL.md` je Bereich)
4. **Einricht:** Home/Ausgabe, Raster teach (Fach 1 + Pitch â†’ Raster berechnen)
5. **Vision:** beide Sensoren = All Numerical, Werte 1..6 prÃ¼fen
6. **RFID Write** an Reader 4b testen (`Vision_Combo_Done`)
7. **Automatik Einlagern** â€” Fach prÃ¼fen in `gldb_LagerverwaltungData`
8. Zone 4A/4B und Ã¼brige Zonen schrittweise integrieren
9. Metall-Lager (zweite Instanz) erst nach stabiler Kunststofflinie

---

## 12. Verweise

| Dokument | Inhalt |
|---|---|
| [Freigabe_Zusammenfassung.md](Freigabe_Zusammenfassung.md) | Offizielles Thema, Ziele |
| [Lastenheft_Abschlussprojekt.docx](Lastenheft_Abschlussprojekt.docx) | Lastenheft (Anforderungen, Word) v1.6 |
| [Pflichtenheft_Abschlussprojekt.docx](Pflichtenheft_Abschlussprojekt.docx) | Pflichtenheft (Umsetzung, Codes → SCL) v1.3 |
| [Lagerverwaltung_Online.md](../03_Technik/Lagerverwaltung_Online.md) | Web-Suche + OPC UA live Belegung |
| [Lageplan.md](Lageplan.md) | ZonenÃ¼bersicht |
| [PLC_Networks.md](PLC_Networks.md) | 29 TIA-OB1-Netzwerke |
| [Projektorganisation.md](Projektorganisation.md) | Vorgehen, Ordner |
| [Maschinengrenzen.md](Maschinengrenzen.md) | Scope In/Out |
| [docs/README.md](../README.md) | Dokumentations-Gliederung |
| [README.md](../../README.md) | Repository-Einstieg |

---

*Dieses Dokument ist die zentrale Textgrundlage fÃ¼r die Gesamtanlage. Bei Ã„nderungen an Materialfluss oder OB1-Strategie hier und in den betroffenen Zonen-READMEs aktualisieren.*
