# Pflichtenheft — Umsetzung (Wie)

**Version 1.3** · September 2026 · Bezug: **Lastenheft v1.6**

**Word:** [Pflichtenheft_Abschlussprojekt.docx](Pflichtenheft_Abschlussprojekt.docx) · Generator: `scripts/generate_pflichtenheft.py`

Zwei Sprachen:

| Sprache | TIA | Im Git | Inhalt |
|---|---|---|---|
| **SCL** | Structured Control Language | `scl/**/*.scl` | FBs, Sequenzen, Formeln |
| **FUP** | Funktionsplan (FBD) | nur TIA OB1 | Netzwerke NW 1–29 = FB-Aufrufe |

**Tags (vollständig):** [Station_PLC_FIO_Tags.md](Station_PLC_FIO_Tags.md) — je Station SCL + alle Factory-I/O-Tags + alle SPS-Merker · CSV: [PLCTags3_live.csv](PLCTags3_live.csv)

---

## Station × FUP × SCL × Factory I/O / SPS

Quelle: `PLCTags3.xlsx`. **FIO** = `%E/%A/%ED/%AD` (Factory I/O). **PLC** = `%M` (Merker). Alle Adressen: [Station_PLC_FIO_Tags.md](Station_PLC_FIO_Tags.md).

| Station | FUP | SCL (Dateien unter `scl/`) | Factory I/O (Kennwerte) | SPS (Kennwerte) |
|---|---|---|---|---|
| **1A** Roh Metall | NW 1–2 | *(kein FB — geplant)* `Zone_1a_Metall/` | Emitter `%A0.0/.1` · Sensor `%E0.0/.1` | — |
| **1B** Roh Kunststoff | NW 4, 6 | *(kein FB — geplant)* `Zone_1b_Kunststoff/` | Emitter `%A1.1/.2` · Sensor `%E1.0/.1` | — |
| **2A** Band + Vision Metall | NW 3, 5 | `Zone_2a_Foerderbaender/FB_VisionReader_Metal.scl` · `OB1_NW5_Metal_Vision.scl` | Bänder `%A2/%E2` · Lid/Base `%ED170/%ED174` | Combo `%M56.0` · CODE `%MD276` |
| **2B** Band + Vision Kunststoff | NW 7–8 | `Zone_2b_Vision_Foerderbaender/FB_VisionReader.scl` | Bänder `%A3/%E3` · Lid/Base `%ED142/%ED146` | Combo `%M40.0` |
| **3A** 2-axis P&P + Waage 1 | NW 9–12 | `Zone_3a_Metall_PickPlace/PickPlace_DigitalAnalog.scl` | Ist X/Z `%ED30/%ED34` · Soll `%AD16/%AD20` · Waage `%ED38` | `%M0.2` |
| **3B** 2-axis P&P + Waage 2 | NW 17–20 | dieselbe PickPlace-SCL, 2. Instanz | Ist `%ED54/%ED58` · Soll `%AD28/%AD32` · Waage `%ED62` | `%M0.3` |
| **4A** 3-axis + RFID Reader 1 | NW 13–16, 21 | `Zone_4a_…/FB_GantryPickPlace.scl` · `OB1_GantryPickPlace.scl` · `OB1_RFID_Metal.scl` | Ist X/Y/Z `%ED42/46/50` · Reader 1 `%ED102` `%A9.0` | `%M8` · CODE `%MD236` |
| **4B** Palettierer + RFID Reader 2 | NW 22–25 | `Zone_4b_…/FB_Palletizer.scl` · `FB_RFID_ReadWrite.scl` · `OB1_Palletizer.scl` | Ist `%ED86/90/94` · Reader 2 `%ED130` `%A11.1` | `%M40` |
| **5A** W2 Crane 1 + Reader 0 | NW 26, 28 | `Zone_5a_Metall_Hochregallager/Hochregal_Automatik_Betrieb_W2.scl` · `OB1_NW28_….scl` · `FB_*_W2.scl` | Crane Ist `%ED178/%ED182` · Reader 0 `%ED114` `%A15.4` | `%M70+` · State `%MW228` |
| **5B** W1 Crane 0 + Reader 5 | NW 27, 29 | `Zone_5b_Hochregallager/Hochregal_Automatik_Betrieb.scl` · Warehouse_1 FBs · `OB1_NW27_….scl` | Crane Ist `%ED162/%ED166` · Reader 5 `%ED150` `%A13.7` | `%M60+` · State `%MW128` |

---

## FUP-Codes (OB1)

Jedes Main-OB1-Netzwerk ist ein FUP-Netz. Titel: [PLC_Networks.md](PLC_Networks.md).

| FUP | Zone | SCL (Aufruf) |
|---|---|---|
| NW 1–2 | 1A Roh/CNC | — geplant |
| NW 3 | 2A Band Metall | — teilweise |
| NW 4, 6 | 1B Roh/CNC | — geplant |
| **NW 5** | 2A Vision Metall | `FB_VisionReader_Metal.scl` · `OB1_NW5_Metal_Vision.scl` |
| **NW 7** | 2B Vision Kunststoff | `FB_VisionReader.scl` |
| NW 8 | 2B Band | — teilweise |
| **NW 10** | 3A 2-axis P&P | `PickPlace_DigitalAnalog.scl` |
| **NW 15** | 4A 3-axis P&P | `FB_GantryPickPlace.scl` · `OB1_GantryPickPlace.scl` |
| **NW 16/21** | 4A RFID Metall | `OB1_RFID_Metal.scl` · `FB_RFID_ReadWrite.scl` |
| **NW 18** | 3B 2-axis P&P | dieselbe PickPlace-SCL, 2. Instanz |
| **NW 24** | 4B Palettierer | `FB_Palletizer.scl` · `OB1_Palletizer.scl` |
| **NW 25** | 4B RFID Write | `FB_RFID_ReadWrite.scl` · `OB1_RFID_at_PickPlace.scl` |
| NW 26 | Band → W1 | `scl/Zone_5a_Foerderband_Lager/` |
| **NW 27** | Band → W2 | `OB1_NW27_Belts_to_Metal_Warehouse.scl` |
| **NW 28** | Warehouse_2 | `OB1_NW28_Metal_Warehouse.scl` + `FB_*_W2.scl` |
| **NW 29** | Warehouse_1 | FUP-Aufrufe laut `WAREHOUSE_1_SETUP.md` §3 |

---

## SCL-Codes (Dateien)

Pfad immer unter `scl/`.

### Vision / RFID / Handling

| SCL-Datei | AF | FUP |
|---|---|---|
| `Zone_2a_Foerderbaender/FB_VisionReader_Metal.scl` | AF-52 | NW 5 |
| `Zone_2a_Foerderbaender/OB1_NW5_Metal_Vision.scl` | AF-52 | NW 5 |
| `Zone_2b_Vision_Foerderbaender/FB_VisionReader.scl` | AF-10…13 | NW 7 |
| `Zone_3a_Metall_PickPlace/PickPlace_DigitalAnalog.scl` | AF-40 | NW 10, 18 |
| `Zone_4a_Metall_Palletizer_RFID/FB_GantryPickPlace.scl` | AF-42 | NW 15 |
| `Zone_4a_Metall_Palletizer_RFID/OB1_GantryPickPlace.scl` | AF-42 | NW 15 |
| `Zone_4a_Metall_Palletizer_RFID/OB1_RFID_Metal.scl` | AF-24 | NW 16/21 |
| `Zone_4b_Kunststoff_Palletizer_RFID/FB_Palletizer.scl` | AF-43 | NW 24 |
| `Zone_4b_Kunststoff_Palletizer_RFID/OB1_Palletizer.scl` | AF-43 | NW 24 |
| `Zone_4b_Kunststoff_Palletizer_RFID/FB_RFID_ReadWrite.scl` | AF-20…25 | NW 25, 16 |
| `Zone_4b_Kunststoff_Palletizer_RFID/OB1_RFID_at_PickPlace.scl` | AF-14, 22 | NW 25 |
| `HMI_Plant/OB1_Prod_PerDay.scl` | HM-01 | Übersicht |

### Warehouse_1 (FUP NW 29) — `scl/Zone_5b_Hochregallager/`

`Hochregal_Automatik_Betrieb.scl` · `FB_Warehouse_Mode_Select.scl` · `FB_Warehouse_Gate.scl` · `FB_Warehouse_Stacker_IO.scl` · `FB_Warehouse_Manual_Soll.scl` · `FB_Warehouse_Actuators.scl` · `FB_Einlagern.scl` · `FB_Auslagern.scl` · `FB_Suchen.scl` · `FB_Loeschen.scl` · `FB_Freies_Fach_Suchen.scl` · `FB_Datenverwaltung_Lager.scl` · `FB_Berechn_Offset.scl` · `FB_Meldung.scl` · `FB_Lagerstatus.scl` · `FB_Hochregallager.scl` (optional) · `scl/Zone_5a_Foerderband_Lager/OB1_NW27_Belts_to_Metal_Warehouse.scl`

### Warehouse_2 (FUP NW 28) — `scl/Zone_5a_Metall_Hochregallager/`

`Hochregal_Automatik_Betrieb_W2.scl` · `OB1_NW28_Metal_Warehouse.scl` · `OB1_RFID_5a_DB4.scl` · `FB_Warehouse_Mode_Select_W2.scl` · `FB_Warehouse_Gate_W2.scl` · `FB_Warehouse_Stacker_IO_W2.scl` · `FB_Warehouse_Manual_Soll_W2.scl` · `FB_Warehouse_Actuators_W2.scl` · `FB_Einlagern_W2.scl` · `FB_Auslagern_W2.scl` · `FB_Suchen_W2.scl` · `FB_Loeschen_W2.scl` · `FB_Freies_Fach_Suchen_W2.scl` · `FB_Datenverwaltung_Lager_W2.scl` · `FB_Berechn_Offset_W2.scl` · `FB_Meldung_W2.scl` · `FB_Lagerstatus_W2.scl`

Nicht in OB1 verdrahten: `legacy/`, `scl/Zone3_PickPlace/`, `scl/Zone4_Palettierer/`.

---

## Weitere Codes

| Art | Werte |
|---|---|
| Info_Code | 0–17 (`FB_Meldung`) |
| HMI_State | 0, 10, 20, 30, 40–42, 50, 55–58, 60, 70, 80, 900 |
| RFID Status_Code | 0 / 1 / 10 |
| Artikelnummer / RFID_CODE | siehe Lastenheft §12 |

Index SCL: [`scl/README.md`](../../scl/README.md)

Zurück: [01_Projektgrundlagen](README.md)
