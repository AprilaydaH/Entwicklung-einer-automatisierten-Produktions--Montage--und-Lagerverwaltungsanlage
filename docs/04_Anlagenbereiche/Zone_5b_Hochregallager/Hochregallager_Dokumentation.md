# Hochregallager — Projektdokumentation

**Projekt:** LAGERVERWALTUNG  
**Steuerung:** Siemens S7-1513-1 PN  
**Simulation:** Factory I/O  
**Softwarestand:** SCL V1.3 (Automatik) / V1.2–V1.5 (Lager-FBs)  
**Datum:** 26.07.2026  

---

## 1. Überblick

Automatisiertes Hochregallager mit **54 Fächern**. Die SPS verwaltet Lagerdaten, bedient die HMI und steuert die Mechanik (Regalbediengerät) über Factory I/O.

### Hauptfunktionen
- Einlagern (Automatik oder Hand)
- Auslagern (Hand)
- Suchen (RFID / Artikel / Fachnummer)
- Freies Fach suchen
- Datensatz löschen (ohne Mechanik)
- Einrichten: Fachpositionen X/Z speichern **oder** Raster (1 Fach + Pitch → alle 54)
- Meldungen über Info_Code

---

## 2. Projektstruktur (TIA)

```
PLC_1 [CPU 1513-1 PN]
├── Programmbausteine
│   ├── Main [OB1]
│   ├── 01_Daten
│   │   ├── gldb_AktuellerFach_HMI
│   │   ├── gldb_LagerverwaltungData
│   │   ├── gldb_Meldungen
│   │   ├── gldb_FactoryIO_IO
│   │   └── fb_Datenverwaltung_Lager_DB
│   ├── 02_Lagerverwaltung
│   │   ├── FB_Datenverwaltung_Lager
│   │   ├── FB_Einlagern / FB_Auslagern / FB_Loeschen
│   │   ├── FB_Fachanzeigen / FB_Freies_Fach_Suchen
│   │   ├── FB_Lagerstatus / FB_Meldung / FB_Suchen
│   └── 03_Automatik_Betrieb
│       └── Hochregal_Automatik_Betrieb
├── PLC-Datentypen
│   └── UDT_Fach
└── PLC-Variablen
```

---

## 3. Datenbausteine

### 3.1 UDT_Fach
Nur Fachdaten (keine Aggregate):

| Feld | Typ | Bedeutung |
|---|---|---|
| Fachnummer | USInt | 1..54 |
| Materialart | USInt | Material |
| Artikelnummer | UInt | Artikel |
| ProductTyp | UInt | Produkttyp |
| Kennzeichnung | String[40] | Textkennzeichnung |
| Datum eingelagert | String[30] | Datum Text |
| Datum_Ziffer | DTL | Zeitstempel |
| RFID_CODE | UDInt | RFID (from `FB_RFID_ReadWrite`, later) |
| Belegt | Bool | Belegt |
| Gesperrt | Bool | Gesperrt |
| Position_X / Position_Z | Real | Ruheposition |
| RegalSeite | USInt | 1=rechts, sonst links |
| Inf_Text | String[100] | Fachnotiz |

### 3.2 gldb_LagerverwaltungData
| Element | Typ | Bedeutung |
|---|---|---|
| Fach[1..54] | Array of UDT_Fach | Lagertabelle (Remanenz empfohlen) |
| Lager_Voll / Lager_Leer | Bool | Status |
| Ziel_Fachnummer | Int | Letztes Zielfach |

### 3.3 gldb_AktuellerFach_HMI
```
Auswahl
  Ausgewaeltes_Fach : UInt
  Fachaktuell       : UDT_Fach
Lagerstatus
  Anzahl_Belegt / Anzahl_Frei : UInt
  Anzeige_noch_Frei : Bool
  Lagerstatus_Text  : String[80]
Meldung
  Info_Code : UInt
  Info_Text : String[…]
  Funktion_Meldung_Ok : Bool
```

### 3.4 gldb_Meldungen
```
Status  : Meldecode, Meldung
Fehler  : Fehlercode, Fehler_Aktiv
```

### 3.5 gldb_FactoryIO_IO
```
Mode    : Automatik_Betrieb
Input   : Paket, RFID, Ziel_Erreicht, NotAus, …
Output  : Fahren, Ziel_X/Z, Ein-/Auslagern_Aktiv, …
```

---

## 4. Aufrufreihenfolge OB1

1. Modi auflösen (Einricht > Auto > Hand)
2. `FB_Datenverwaltung_Lager` — Init, Sync, Zählung, Einricht
3. HMI-Daten: Löschen / Suchen / Freies Fach
4. `Hochregal_Automatik_Betrieb` — Mechanik
5. `FB_Meldung` — **zuletzt** (Info_Code → Text)

**Hinweis:** Zählung nur einmal (Datenverwaltung **oder** FB_Lagerstatus).

---

## 5. Betriebsarten

| Modus | Wirkung |
|---|---|
| **Automatik** | Einlagern startet bei Paket + RFID; Auslagern nur Hand |
| **Hand** | Start über HMI Einlagern / Auslagern |
| **Einricht** | Automatik-Start gesperrt; Positionen speichern erlaubt |

Nur ein Modus gleichzeitig aktiv schalten.

---

## 6. Gabel — 3 Positionen

| Position | Bedeutung |
|---|---|
| Links | Regal links oder Förderband (Foerderband_Seite <> 1) |
| **Mitte** | Fahrtposition (mit/ohne Last) — Sensor `Gabel_Eingefahren` |
| Rechts | Regal rechts (RegalSeite=1) oder Band (Foerderband_Seite=1) |

**Regel:** X/Z-Fahrt nur bei Gabel in der Mitte.

**Offset_Z:** wenige mm/cm über der Ruheposition beim Aufnehmen/Ablegen (z.B. 0.01).

### Raster teach (Fanuc BERECHN_OFFSET)

Statt 54 Einzelpositionen: **Fach 1** als Basis, **Pitch_X** / **Pitch_Z** als Rasterabstand, dann `HMI_Raster_Berechnen`:

```
Mult_X = (Fach - 1) MOD Spalten
Mult_Z = (Fach - 1) DIV Spalten
Pos_X  = Basis_X + Pitch_X × Mult_X
Pos_Z  = Basis_Z + Pitch_Z × Mult_Z
```

Standard: Spalten=6, 9 Ebenen → 54 Fächer. Siehe `scl/Zone_5b_Hochregallager/RASTER_TEACH.md`.

### Einlagern
Band-Seite aufnehmen → Mitte → Fach (Z+Offset) → Regal-Seite → absenken → ablegen → Mitte → Home

### Auslagern
Mitte → Fach → Regal-Seite → anheben → aufnehmen → Mitte → Ausgabe (Z+Offset) → Band-Seite → absenken → ablegen → Mitte → Home

---

## 7. Bausteine (Kurz)

| Baustein | Aufgabe |
|---|---|
| FB_Datenverwaltung_Lager | Init, HMI-Sync, Zählung, Position speichern, Raster |
| FB_Berechn_Offset | MOD/DIV Offset pro Fachnummer |
| FB_Einlagern | Produktdaten in freies Fach schreiben |
| FB_Auslagern | Produktdaten löschen (nach Mechanik) |
| FB_Loeschen | Produktdaten löschen ohne Mechanik |
| FB_Freies_Fach_Suchen | Erstes freies, nicht gesperrtes Fach |
| FB_Lagerstatus | Lagerstatus_Text (in Automatik nach Ein/Auslagern) |
| FB_Suchen | RFID → Artikel → Fachnummer |
| FB_Meldung | Info_Code → Info_Text |
| Hochregal_Automatik_Betrieb | Ablaufsteuerung Mechanik |
| FB_RFID_ReadWrite | RFID lesen/schreiben (`scl/Zone_4b_Kunststoff_Palletizer_RFID/`) |
| FB_VisionReader | Kunststoff Vision → Produktfelder (`scl/Zone_4b_Kunststoff_Palletizer_RFID/`) |

### 7.1 RFID → Lagerbuch (implementiert)

Verdrahtung in **`OB1_Plastic_Warehouse.scl`**:

1. **Write:** `FB_VisionReader` → `HMI_RFID_Write` wenn `Paket_Vor_Regal`
2. **Gate:** `Paket_Fuer_Hochregal = Paket_Vor_Regal AND Vision_Combo_Done`
3. **Read:** Automatik State **10** → `RFID_Lesen` → `FB_RFID_ReadWrite`
4. Bei `RFID_Gueltig` → `Fachaktuell` → `FB_Einlagern` → `gldb_LagerverwaltungData.Fach[n]`

`FB_Einlagern` verlangt `RFID_CODE <> 0` (sonst Info_Code 7).

Siehe [`PLASTIC_WAREHOUSE_GOLIVE.md`](../../../scl/Zone_5b_Hochregallager/PLASTIC_WAREHOUSE_GOLIVE.md).

---

## 8. Info_Code (FB_Meldung)

| Code | Text | Ok |
|---:|---|---|
| 0 | Keine Meldung | — |
| 1 | Einlagerung erfolgreich | ja |
| 2 | Fach ist bereits belegt | nein |
| 3 | Fachnummer ungültig | nein |
| 4 | Auslagerung erfolgreich | ja |
| 5 | Fach ist bereits frei | nein |
| 6 | Datensatz gelöscht | ja |
| 7 | RFID-Code fehlt | nein |
| 8 | Kein passendes Fach gefunden | nein |
| 9 | Produkt gefunden | ja |
| 10 | Lager voll | nein |
| 11 | Factory I/O Zielposition geladen | ja |
| 12 | Factory I/O Ziel erreicht | ja |
| 13 | Not-Aus aktiv | nein |
| 14 | Freies Fach gefunden | ja |
| 15 | Fach ist gesperrt | nein |
| 16 | Fachposition gespeichert | ja |

---

## 9. Automatik — wichtige States

| State | Bedeutung |
|---:|---|
| 0 | Bereit |
| 10 | RFID lesen |
| 20 | Freies Fach suchen |
| 22 / 30 / 32 | Band-Seite / aufnehmen / Mitte |
| 40–72 | Zum Fach, Regal-Seite, absenken, ablegen, Mitte |
| 90 | DB einbuchen |
| 100–120 | Auslager-Auswahl / Suche / prüfen |
| 125–162 | Zum Fach, Regal pick, Mitte |
| 180 | DB ausbuchen |
| 190–202 | Zur Ausgabe, Band drop, Mitte |
| 300 / 310 | Home / Fertig |
| 900 | Fehler |

---

## 10. Fehlercodes (Auswahl)

| Code | Quelle | Bedeutung |
|---:|---|---|
| 101 | Datenverwaltung | Fachnummer ungültig |
| 102 | Datenverwaltung | Position speichern nicht erlaubt |
| 103 | Datenverwaltung | Raster berechnen nicht erlaubt (nicht Einricht) |
| 911 | Automatik | RFID-Fehler |
| 912 | Freies Fach / Automatik | Lager voll |
| 921–924 | Automatik Auslagern | Suche/Fach/Belegt/Gesperrt |
| 999 | Automatik | Ungültiger State |

---

## 11. HMI — geplante Anbindung (nächster Schritt)

Empfohlene HMI-Bereiche:

1. **Betrieb:** Mode Auto / Hand / Einricht, Start Ein/Aus, Reset, Stop, Not-Aus-Anzeige  
2. **Fach:** Nummer wählen, Belegt/Gesperrt, Artikel, RFID, Position X/Z  
3. **Lagerstatus:** Frei/Belegt, Status-Text  
4. **Meldung:** Info_Text, Info_Code, Ok-Flag, Quittieren  
5. **Automatik:** State, Busy, Done, Error, Ziel-Fach  
6. **Einricht:** Ist-Position, Position speichern, Raster berechnen  

Datenquellen: vor allem `gldb_AktuellerFach_HMI` und Outputs der Automatik. Tags: `PLC_Tags_Hochregallager.csv`.

---

## 12. Quelldateien (Repository)

Ordner `scl/`:
- FB_*.scl, Hochregal_Automatik_Betrieb.scl, OB1_Plastic_Warehouse.scl, UDT_Fach.udt.txt  
- README.md, INFO_CODES.md, VARIABLES.md  

---

## 13. Checkliste vor Inbetriebnahme

- [ ] UDT_Fach ohne Aggregate  
- [ ] HMI-DB mit Auswahl / Lagerstatus / Meldung  
- [ ] Meldungen mit Status / Fehler  
- [ ] Offset_Z und Foerderband_Seite verdrahtet  
- [ ] Gabel-Mitte-Sensor = Gabel_Eingefahren  
- [ ] OB1: Meldung zuletzt  
- [ ] Nur eine Zählquelle  
- [ ] Fachpositionen im Einrichtbetrieb gespeichert **oder** Raster berechnet (Info_Code 17)  
- [ ] Factory-I/O I/O-Mapping vollständig  
- [ ] *Später:* `FB_RFID_ReadWrite` statt `RFID_Gelesen` / `RFID_ID`  

---

*Ende der Dokumentation — Stand V1.3*
