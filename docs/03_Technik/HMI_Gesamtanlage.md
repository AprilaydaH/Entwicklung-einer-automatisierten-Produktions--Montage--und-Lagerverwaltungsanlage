# HMI Gesamtanlage — ein Touch Panel

**Stand 19.09.2026:** SPS und Factory I/O laufen. **HMI-Runtime auf dem Laptop** nur mit Verbindung **PLCSIM**. Ethernet-Verbindung schreibt nicht (`190011`), weil die Simulation nicht `192.168.0.2` ist. Start/Stop-Events in WinCC noch umbiegen (nicht `HMI_Productopn_Stop`).

**Prinzip:** **Eine** HMI (Siemens TP) für die **gesamte** Factory laut [Lageplan](../01_Projektgrundlagen/Lageplan.md).

**Gesamtkontext:** [Gesamtanlage.md](../01_Projektgrundlagen/Gesamtanlage.md)

---

## Screens nach Lageplan

| Screen | Zone / Bereich | SCL / Tags |
|---|---|---|
| **Übersicht** | Materialfluss, Status aller Zonen | — |
| **Zone 1A Metall** | Roh, Roboter, CNC | `scl/Zone_1a_Metall/` *(folgt)* |
| **Zone 1B Kunststoff** | Roh, Roboter, CNC | `scl/Zone_1b_Kunststoff/` *(folgt)* |
| **Zone 2A / 2B** | Bänder; 2B Vision-Farbe | `scl/Zone_2a_Foerderbaender/` · `scl/Zone_2b_Vision_Foerderbaender/` |
| **Zone 3A / 3B** | 2-axis Pick and Place + Waage | `scl/Zone_3a_Metall_PickPlace/` |
| **Zone 4A** | 3-axis Pick and Place + RFID Metall | `scl/Zone_4a_Metall_Palletizer_RFID/` |
| **Zone 4B** | Palettierer + RFID Kunststoff | `scl/Zone_4b_Kunststoff_Palletizer_RFID/` |
| **Zone 5A / 5B** | Bänder + Hochregal | `PLC_Tags_Hochregallager.csv` + `PLC_Tags_RFID.csv` |
| **Rezept / Diagnose** | Parameter, Alarme, I/O | Meldungen `gldb_Meldungen` |

Header (immer): **zwei** Bedienstellen — TP **Produktion Start/Stop** und Factory-I/O-Taster; gleiche Logik im FB (ODER).

**Set 1 — HMI** (Momentary, Press = SetBit, Release = ResetBit):

| HMI-Beschriftung | Tag | Adresse | Zugriff |
|---|---|---|---|
| Produktion Start | `HMI_Plant_Start` | `%M58.0` | Momentary |
| Produktion Stop | `HMI_Plant_Stop` | `%M58.1` | Momentary |
| Not-Aus | `HMI_Plant_Not_Aus` | `%M58.2` | Momentary |
| Reset (nach Not-Aus) | `HMI_Plant_Reset` | `%M58.3` | Momentary |
| Lampe läuft | `Plant_Running` | `%M58.4` | R |
| Lampe Not-Aus | `Plant_Not_Aus` | `%M58.5` | R |
| Lampe bereit | `Plant_Ready` | `%M58.7` | R |

**Set 2 — Factory I/O** (nicht an WinCC binden):

| FIO | Tag | Adresse |
|---|---|---|
| Start | `Production_Start` | `%E9.1` |
| Stop | `Production_Stop` | `%E9.2` |
| Not-Aus | `Main_Not_Aus` | `%E9.3` |
| Reset | `Main_Reset` | `%E9.4` |
| Grün / Rot / Start-Lampe | `Main_Green_Stack_Light` / `Main_Red_Light` / `Main_Start_Button_Light` | `%A15.5` / `.6` / `.7` |

FUP: [`scl/HMI_Plant/FB_Plant_Start_Stop.md`](../../scl/HMI_Plant/FB_Plant_Start_Stop.md). Tags: [`PLC_Tags_Plant_Start_Stop.csv`](../../scl/HMI_Plant/PLC_Tags_Plant_Start_Stop.csv). Adress-Audit: [`PLC_TAG_ADDRESS_FIXES.md`](../../scl/HMI_Plant/PLC_TAG_ADDRESS_FIXES.md). `HMI_Prod_Reset_Day` `%M78.0` setzt nur den **Tageszähler**.

Nicht `%E18` / `%A18` / `%M100`.

**WinCC-Events (eine Taste = eine Variable):**

| Taste | Drücken | Loslassen |
|---|---|---|
| Start | SetzeBit `HMI_Plant_Start` | RücksetzeBit `HMI_Plant_Start` |
| Stop | SetzeBit `HMI_Plant_Stop` | RücksetzeBit `HMI_Plant_Stop` |

Nicht auf **Drücken** Start setzen und gleichzeitig Stop rücksetzen. Tag `HMI_Productopn_Stop` nicht verwenden.

### PROFINET / Verbindung

| | IP / Einstellung |
|---|---|
| CPU X1 | **`192.168.0.1`** · PN/IE_1 |
| HMI X1 | **`192.168.0.2`** · PN/IE_1 |
| HMI X3 | anderes Netz, z. B. `192.168.1.3` + neues Subnetz (nicht PN/IE_1) |
| Simulation Laptop | HMI-Verbindung **PLCSIM** |
| Echtes TP | Verbindung **ETHERNET**, S7ONLINE → Siemens PLCSIM Virtual Ethernet Adapter |

CPU bleibt **1518F-4 PN/DP** (kein 1518T). F-CPU nur auf F-Instanz in PLCSIM Advanced laden.

**Geplante / Ist-Produktion (pro Tag)** — Übersicht-IO-Felder:

| HMI-Beschriftung | Tag | Adresse | Zugriff |
|---|---|---|---|
| Geplante Produktion | `HMI_Prod_Planned_PerDay` | `%MD320` | RW |
| Ist-Produktion | `HMI_Prod_Actual_PerDay` | `%MD324` | R |

WinCC-Format **`9999`** (nicht 14 Nullen). Import [`scl/HMI_Plant/PLC_Tags_Prod_PerDay.csv`](../../scl/HMI_Plant/PLC_Tags_Prod_PerDay.csv). Logik: [`OB1_Prod_PerDay.scl`](../../scl/HMI_Plant/OB1_Prod_PerDay.scl). Ist zählt Hochregal-**Done** (W1+W2) und setzt um Mitternacht zurück.

---

## Intro script — Übersicht (main page of the whole plant)

Spoken ~2 minutes. Point at the screen as you talk. **A = metal (left), B = plastic (right).**

### English

This is the **plant overview** — one HMI for the whole factory. One PLC, two parallel lines: **metal on the left, plastic on the right**. Flow is always top to bottom: raw material, conveyor, assembly, palletizing with RFID, then high-bay warehouse.

**Header** stays on every screen: **Produktion Start / Stop**, Not-Aus, Reset, and a collective alarm. Zone lamps show which area is running or in fault. Start the whole plant from this picture, then open the zone pages.

**Metal line, 1A to 5A.** Raw parts and CNC in 1A. Conveyor 2A, with vision latching lid and base. Two-axis pick-and-place in 3A assembles the box. Three-axis palletizer in 4A puts it on a pallet. **RFID Reader 1 writes the vision data onto the pallet tag** — date code and article, material 2 for metal. The pallet then goes to **Warehouse 2**, the metal high bay, fifty-four slots.

**Plastic line, 1B to 5B.** Same idea: 1B raw and CNC, 2B conveyor plus **colour vision**, 3B assembly, 4B palletizer. **RFID Reader 2 writes colour, article and RFID code** when the palletizer is done. Then **Warehouse 1**, plastic high bay — also fifty-four slots. Auto put-away only after the tag is written.

**Traceability:** every stored pallet keeps RFID code, article, material and colour in the warehouse database. Metal is material 2, no colour; plastic is material 1 with blue, green or mixed.

To operate a warehouse, open **5A Metal** or **5B Plastic**. **Produktion Stop** here stops the plant.

### Deutsch

Das ist die **Anlagenübersicht** — ein HMI für die ganze Factory. Eine SPS, zwei parallele Linien: **links Metall, rechts Kunststoff**. Der Fluss geht immer von oben nach unten: Rohteil, Band, Montage, Palettieren mit RFID, dann Hochregal.

Der **Header** bleibt auf jedem Bild: **Produktion Start / Stop**, Not-Aus, Reset, Sammelmeldung. Die Zonenlampen zeigen Lauf und Störung. Die ganze Anlage starten Sie auf dieser Seite, danach die Zonenbilder.

**Metalllinie 1A bis 5A.** Rohteile und CNC in 1A. Band 2A mit Vision für Deckel und Boden. Zweiachs-Pick-and-Place in 3A montiert. Dreiachs-Palettierer in 4A setzt auf die Palette. **RFID-Reader 1 schreibt die Vision-Daten auf den Paletten-Tag** — Datumscode, Artikel, Material 2. Danach **Warehouse 2**, Metall-Hochregal, 54 Fächer.

**Kunststofflinie 1B bis 5B.** Gleicher Aufbau: 1B Roh und CNC, 2B Band plus **Farb-Vision**, 3B Montage, 4B Palettierer. **RFID-Reader 2 schreibt Farbe, Artikel und RFID-Code**, wenn der Palettierer fertig ist. Dann **Warehouse 1**, Kunststoff-Hochregal, ebenfalls 54 Fächer. Auto-Einlagern erst nach erfolgreichem Schreibvorgang.

**Rückverfolgung:** jede eingelagerte Palette speichert RFID-Code, Artikel, Material und Farbe in der Lager-DB. Metall ist Material 2 ohne Farbe; Kunststoff Material 1 mit Blau, Grün oder Mixed.

Zum Bedienen: **5A Metall** oder **5B Kunststoff**. **Produktion Stop** hier hält die Anlage.


---

## Hochregallager-Screen (Einricht + Auto)

**Detail (Warehouse_1):** [`scl/Zone_5b_Hochregallager/HMI_Warehouse_1.md`](../../scl/Zone_5b_Hochregallager/HMI_Warehouse_1.md) · tags [`HMI_Tags_Warehouse_1.csv`](../../scl/Zone_5b_Hochregallager/HMI_Tags_Warehouse_1.csv)

| Element | Tag / Quelle |
|---|---|
| Mode Einricht / Auto / Hand | `Mode_Einricht`, `Mode_Auto`, `Mode_Hand` |
| Fach wählen | `HMI_Fachnummer` |
| Hand product (skip RFID) | `gldb_AktuellerFach_HMI.Auswahl.Fachaktuell.*` |
| Position speichern | `HMI_Pos_Speichern` + `Ist_X`, `Ist_Z` |
| **Raster berechnen** | `HMI_Raster_Berechnen` (alle 54 Fächer) |
| Pitch / Spalten | `HMI_Pitch_X/Z`, `HMI_Spalten` |
| Start Ein/Auslagern | `HMI_Start_Einlagern`, `HMI_Start_Auslagern` |
| Status | `HMI_State`, `HMI_Ziel_Fach`, `HRL_Anzahl_Belegt/Frei` |
| **Regal-Animation** | `gldb_AktuellerFach_HMI.Lagerstatus.Farbe[1..54]` / `.Ziel[n]` — [HMI_Regal_Animation.md](HMI_Regal_Animation.md) |
| Meldung | `gldb_AktuellerFach_HMI.Meldung.Info_Text` |

Raster-Anleitung: [`scl/Zone_5b_Hochregallager/RASTER_TEACH.md`](../../scl/Zone_5b_Hochregallager/RASTER_TEACH.md)


---

## RFID / Vision (Kunststoff)

**Screen first:** [`scl/Zone_4b_Kunststoff_Palletizer_RFID/HMI_RFID_Vision.md`](../../scl/Zone_4b_Kunststoff_Palletizer_RFID/HMI_RFID_Vision.md) · tags [`HMI_Tags_RFID_Vision.csv`](../../scl/Zone_4b_Kunststoff_Palletizer_RFID/HMI_Tags_RFID_Vision.csv)

| Element | Tag (live `2b_`) |
|---|---|
| RESET / CHECK / WRITE / READ / CLEAR | `2b_HMI_RFID_*` (momentary) |
| Status lamps | `2b_RFID_Lamp_Ready/Running/Done/Error` |
| Produkt live | `2b_VisionData_*` (`%MW28`, `%MD42`, …) |
| Tag readback | `2b_RFID_*_Out`, `Tag_Present`, `Gueltig` |
| Pallet gate | `Paket_Fuer_Hochregal` / `Combo_Done` |

Detail: [RFID](../04_Anlagenbereiche/RFID/README.md)

---

## SPS-Zuordnung (ein Projekt)

| Bereich | FB / OB1 |
|---|---|
| **Übersicht Start/Stop** | `FB_Plant_Start_Stop` (FUP) — nach NW 29 — [`FB_Plant_Start_Stop.md`](../../scl/HMI_Plant/FB_Plant_Start_Stop.md) |
| Zone 3 | `PickPlace_DigitalAnalog.scl` — 2 Instanzen |
| Zone 4A | `FB_GantryPickPlace` (3-axis P&P) — `OB1_GantryPickPlace.scl` |
| Zone 4B | `FB_Palletizer` — `OB1_Palletizer.scl` |
| Kunststoff E2E | **`OB1_Plastic_Warehouse.scl`** (Vision + RFID + Hochregal) |
| Hochregal allein | `FB_Hochregallager` — `OB1_Hochregallager.scl` |
| RFID | `FB_RFID_ReadWrite`, `FB_VisionReader` |
| Zone 1A/1B, 2A/2B, Waage | *folgt* |

Palettierer-Detail: [Zone4 HMI_Organisation](../04_Anlagenbereiche/Zone_4b_Kunststoff_Palletizer_RFID/HMI_Organisation.md)

**Nicht im Scope:** Wasserverbrauch.

---

## Lagerverwaltung Online (Web, ohne SPS-Änderung)

Browser-Suche für beide Hochregale: [Lagerverwaltung_Online.md](Lagerverwaltung_Online.md). Streamlit-Tabs Warehouse 1 (Kunststoff) und Warehouse 2 (Metall), je 54 Fächer, Suche RFID → Artikel → Fach. Das TP-HMI bleibt führend für Betrieb.
