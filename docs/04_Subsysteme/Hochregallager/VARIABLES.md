# Variablenübersicht — Hochregallager SCL (V1.1)

Alle Baustein-Interfaces für TIA Portal. Globale DBs am Ende.

Konvention: Fachbereich **1..54**

---

## 1. FB_Auslagern

### VAR_TEMP
| Name | Typ | Beschreibung |
|---|---|---|
| iFach | Int | Index 1..54 |

### Globale Zugriffe
- `gldb_AktuellerFach_HMI` (Fachaktuell, Ausgewaeltes_Fach, Info_Code, Funktion_Meldung_Ok)
- `gldb_LagerverwaltungData.Fach[]`

---

## 2. FB_Einlagern

### VAR_TEMP
| Name | Typ | Beschreibung |
|---|---|---|
| iFach | Int | Index 1..54 |
| RetValTime | Int | Rückgabe von `RD_LOC_T` |

### Globale Zugriffe
- `gldb_AktuellerFach_HMI`
- `gldb_LagerverwaltungData` (Fach[], Ziel_Fachnummer)

---

## 3. FB_Loeschen

### VAR_TEMP
| Name | Typ | Beschreibung |
|---|---|---|
| iFach | Int | Index 1..54 |

### Globale Zugriffe
- `gldb_AktuellerFach_HMI`
- `gldb_LagerverwaltungData.Fach[]`

---

## 4. FB_FachAnzeigen

### VAR_TEMP
| Name | Typ | Beschreibung |
|---|---|---|
| iIndex | Int | Index aus Ausgewaeltes_Fach |

### Globale Zugriffe
- `gldb_AktuellerFach_HMI` (Ausgewaeltes_Fach, Fachaktuell, Anzeige_noch_Frei)
- `gldb_LagerverwaltungData.Fach[]`

---

## 5. FB_Freies_Fach_Suchen

### VAR_INPUT
| Name | Typ | Beschreibung |
|---|---|---|
| Start | Bool | Startsuche (Flanke) |

### VAR_OUTPUT
| Name | Typ | Beschreibung |
|---|---|---|
| Gefunden | Bool | Freies Fach gefunden |
| Lager_Voll | Bool | Kein freies Fach |
| Fachnummer | USInt | Gefundenes Fach 1..54 (0 = keines) |
| Fehler | Bool | Fehler aktiv |
| Fehlercode | UInt | z.B. 912 |

### VAR_STAT
| Name | Typ | Beschreibung |
|---|---|---|
| R_TRIG_Start | R_TRIG | Flankenerkennung Start |

### VAR_TEMP
| Name | Typ | Beschreibung |
|---|---|---|
| i | Int | Schleifenindex |

### Globale Zugriffe
- `gldb_AktuellerFach_HMI` (Fachaktuell.Fachnummer, Ausgewaeltes_Fach, Info_Code)
- `gldb_LagerverwaltungData` (Fach[], Lager_Voll)
- `gldb_Meldungen` (Meldecode, Fehlercode, Fehler_Aktiv)

---

## 6. FB_Datenverwaltung_Lager

### VAR_INPUT
| Name | Typ | Beschreibung |
|---|---|---|
| Initialisieren | Bool | Fachnummern neu setzen (Flanke) |
| Reset_Meldung | Bool | Meldung quittieren (Flanke) |
| Position_Speichern | Bool | X/Z speichern (Flanke, nur Einricht) |
| HMI_Fachnummer | UInt | Gewähltes Fach von HMI |
| Einricht_Mode | Bool | Einrichtbetrieb aktiv |
| Ist_X | Real | Aktuelle X-Position (Einricht) |
| Ist_Z | Real | Aktuelle Z-Position (Einricht) |

### VAR_OUTPUT
| Name | Typ | Beschreibung |
|---|---|---|
| Fertig | Bool | Aktion abgeschlossen |
| Fehler | Bool | Fehler aktiv |
| Fehlercode | UInt | 101=ungültige Fachnr, 102=Pos nicht erlaubt |
| HMI_Fach_Gueltig | Bool | Fachnummer 1..54 |
| HMI_Fach_Belegt | Bool | Gewähltes Fach belegt |
| Anzahl_Belegt | UInt | Belegte Fächer |
| Anzahl_Frei | UInt | Freie Fächer |

### VAR_STAT
| Name | Typ | Beschreibung |
|---|---|---|
| Init_done | Bool | Einmal-Init erledigt |
| R_TRIG_Initialisieren | R_TRIG | Flanke Init |
| R_TRIG_Reset_Meldung | R_TRIG | Flanke Reset |
| R_TRIG_Pos_Speichern | R_TRIG | Flanke Position |

### VAR_TEMP
| Name | Typ | Beschreibung |
|---|---|---|
| i | Int | Schleifenindex |
| iFach | Int | Aktueller Fachindex |

### Globale Zugriffe
- `gldb_AktuellerFach_HMI`
- `gldb_LagerverwaltungData`
- `gldb_Meldungen`

---

## 7. FC_Lagerstatus

### VAR_TEMP
| Name | Typ | Beschreibung |
|---|---|---|
| iLaufvar | Int | Schleifenindex |
| Anzahl_Belegt | UInt | Zähler belegt |
| Anzahl_Frei | UInt | Zähler frei |
| sFrei | String[10] | Zahl als Text |
| sBelegt | String[10] | Zahl als Text |

### Globale Zugriffe
- `gldb_AktuellerFach_HMI` (Anzahl_*, Lagerstatus_Text)
- `gldb_LagerverwaltungData` (Fach[], Lager_Voll, Lager_Leer)

---

## 8. FC_Meldung

Keine lokalen Variablen.

### Globale Zugriffe
- `gldb_AktuellerFach_HMI` (Info_Code, Info_Text, Funktion_Meldung_Ok)
- `gldb_Meldungen.Meldung`

---

## 9. FC_Suchen

### VAR_TEMP
| Name | Typ | Beschreibung |
|---|---|---|
| Gefunden | Bool | Suchergebnis |
| Such_RFID | UDInt | Suchkriterium RFID |
| Such_Artikel | UInt | Suchkriterium Artikel |
| Such_Fach | USInt | Suchkriterium Fach |
| iLaufvar | Int | Index / Schleife |
| sFachnummer | String[10] | Text Fach |
| sArtikelnummer | String[10] | Text Artikel |
| sRFID | String[20] | Text RFID |

### Globale Zugriffe
- `gldb_AktuellerFach_HMI`
- `gldb_LagerverwaltungData.Fach[]`

---

## 10. Hochregal_Automatik_Betrieb

### VAR_INPUT — Betrieb / HMI
| Name | Typ | Beschreibung |
|---|---|---|
| Auto_Mode | Bool | Automatikbetrieb |
| Hand_Mode | Bool | Handbetrieb |
| Einricht_Mode | Bool | Einrichtbetrieb (sperrt Automatik) |
| Not_Aus | Bool | Not-Aus aktiv |
| HMI_Start_Einlagern | Bool | HMI Start Einlagern |
| HMI_Start_Auslagern | Bool | HMI Start Auslagern |
| Reset | Bool | Fehler/Ablauf zurücksetzen |
| Stop | Bool | Ablauf abbrechen |

### VAR_INPUT — Sensorik / Feedback
| Name | Typ | Beschreibung |
|---|---|---|
| Paket_Vor_Regal | Bool | Paket erkannt |
| RFID_Bereit | Bool | RFID-Leser bereit |
| RFID_Gueltig | Bool | RFID erfolgreich gelesen |
| RFID_Fehler | Bool | RFID-Fehler |
| RFID_Artikelnummer | UInt | Gelesene Artikelnummer |
| RFID_Materialart | USInt | Gelesene Materialart |
| RFID_ProduktTyp | UInt | Gelesener Produkttyp |
| RFID_Code | UDInt | Gelesener RFID-Code |
| Palette_Aufgenommen | Bool | Palette aufgenommen |
| Palette_Abgelegt | Bool | Palette abgelegt |
| Position_Erreicht | Bool | Sollposition erreicht |
| Gabel_Rechts_Ausgefahren | Bool | Gabel rechts raus |
| Gabel_Links_Ausgefahren | Bool | Gabel links raus |
| Gabel_Eingefahren | Bool | Gabel eingefahren |

### VAR_INPUT — Parameter Positionen
| Name | Typ | Beschreibung |
|---|---|---|
| Home_X | Real | Home X |
| Home_Z | Real | Home Z |
| Ausgabe_X | Real | Ausgabe X |
| Ausgabe_Z | Real | Ausgabe Z |

### VAR_OUTPUT — Status
| Name | Typ | Beschreibung |
|---|---|---|
| Busy | Bool | Ablauf läuft |
| Done | Bool | Ablauf fertig (gehalten bis neuem Start) |
| Error | Bool | Fehler aktiv |
| State_Out | Int | Aktueller State (HMI) |
| Ziel_Fachnummer_Out | Int | Aktuelles Zielfach (HMI) |
| Soll_X | Real | Sollposition X |
| Soll_Z | Real | Sollposition Z |

### VAR_OUTPUT — Aktoren
| Name | Typ | Beschreibung |
|---|---|---|
| Fahre_Zu_Position | Bool | Fahren aktiv |
| Palette_Aufnehmen | Bool | Aufnehmen |
| Palette_Ablegen | Bool | Ablegen |
| Gabel_Rechts_Aus | Bool | Gabel rechts |
| Gabel_Links_Aus | Bool | Gabel links |
| Gabel_Einfahren | Bool | Gabel einfahren |
| RFID_Lesen | Bool | RFID lesen anfordern |

### VAR_STAT — Ablaufzustand
| Name | Typ | Beschreibung |
|---|---|---|
| State | Int | Zustandsautomat |
| Ziel_Fachnummer | Int | Internes Zielfach |
| Regalseite | USInt | 1=rechts, sonst links |
| Mode_Einlagern | Bool | Modus Einlagern |
| Mode_Auslagern | Bool | Modus Auslagern |
| Startquelle_Auto | Bool | Start aus Automatik |
| Startquelle_HMI | Bool | Start aus HMI |
| Start_FreiesFach | Bool | Puls Start FreiesFach |
| Paket_Uebernommen | Bool | Handshake Auto-Einlagern |

### VAR_STAT — Flanken
| Name | Typ | Beschreibung |
|---|---|---|
| R_TRIG_Einlagern | R_TRIG | Flanke HMI Einlagern |
| R_TRIG_HMI_Auslagern | R_TRIG | Flanke HMI Auslagern |
| R_TRIG_Reset | R_TRIG | Flanke Reset |
| R_TRIG_Stop | R_TRIG | Flanke Stop |

### VAR_STAT — Multiinstanzen
| Name | Typ | Beschreibung |
|---|---|---|
| instFreiesFachSuchen | FB_Freies_Fach_Suchen | Freies Fach |
| instEinlagern | FB_Einlagern | Einbuchen |
| instAuslagern | FB_Auslagern | Ausbuchen |
| instSuchen | FC_Suchen / FB | Suche (falls als FB) |
| instLagerstatus | FC_Lagerstatus / FB | Status |
| instFachanzeigen | FB_FachAnzeigen | HMI-Anzeige |

> Hinweis: FC-Aufrufe brauchen in TIA keine Multiinstanz-DB; wenn als FB angelegt, dann wie oben.

### Globale Zugriffe
- `gldb_AktuellerFach_HMI`
- `gldb_LagerverwaltungData`
- `gldb_Meldungen`

---

## Globale Datenbausteine

### gldb_LagerverwaltungData
| Name | Typ | Beschreibung |
|---|---|---|
| Fach | Array[1..54] of UDT_Fach | Lagerfächer |
| Lager_Voll | Bool | Kein freies Fach |
| Lager_Leer | Bool | Kein belegtes Fach |
| Ziel_Fachnummer | Int | Letztes Zielfach |

### gldb_AktuellerFach_HMI
| Name | Typ | Beschreibung |
|---|---|---|
| Ausgewaeltes_Fach | UInt | HMI-Fachwahl 1..54 |
| Fachaktuell | UDT_Fach | Aktuelles Fach (Anzeige/Eingabe) |
| Anzahl_Belegt | UInt | Belegte Fächer |
| Anzahl_Frei | UInt | Freie Fächer |
| Lagerstatus_Text | String[80] | Statuszeile |
| Anzeige_noch_Frei | Bool | Fach frei? |
| Info_Code | UInt | Meldecode 0..16 |
| Info_Text | String[100] | Meldetext |
| Funktion_Meldung_Ok | Bool | Letzte Aktion OK |

### gldb_Meldungen
| Name | Typ | Beschreibung |
|---|---|---|
| Meldung | String[100] | Anzeigetext |
| Meldecode | UInt | Ablauf-/Statuscode |
| Fehlercode | UInt | Fehlercode |
| Fehler_Aktiv | Bool | Fehler aktiv |

### UDT_Fach (Felder)
| Name | Typ |
|---|---|
| Fachnummer | USInt |
| Materialart | USInt |
| Artikelnummer | UInt |
| ProductTyp | UInt |
| Kennzeichnung | String[40] |
| Datum eingelagert | String[30] |
| Datum_Ziffer | DTL |
| RFID_CODE | UDInt |
| Belegt | Bool |
| Gesperrt | Bool |
| Position_X | Real |
| Position_Z | Real |
| RegalSeite | USInt |
| Inf_Text | String[100] |

---

## State-Übersicht Automatik

| State | Bedeutung |
|---:|---|
| 0 | Bereit |
| 10 | RFID lesen |
| 20 | Freies Fach suchen |
| 30 | Palette aufnehmen |
| 40 | Zielposition laden |
| 50 | Zum Fach fahren |
| 60 | Gabel ausfahren |
| 70 | Palette ablegen |
| 80 | Gabel einfahren |
| 90 | Einlagern (DB) |
| 100 | Auslager-Auswahl prüfen |
| 110 | Produkt suchen |
| 120 | Fach prüfen |
| 130 | Auslagerposition laden |
| 140 | Zum Auslagerfach fahren |
| 150 | Gabel ausfahren |
| 160 | Palette aufnehmen |
| 170 | Gabel einfahren |
| 180 | Auslagern (DB) |
| 190 | Zur Ausgabe fahren |
| 200 | An Ausgabe ablegen |
| 300 | Home fahren |
| 310 | Fertig |
| 900 | Fehler |
