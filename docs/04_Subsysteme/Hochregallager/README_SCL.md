# Hochregallager — SCL-Bausteine (V1.2)

Automatisiertes Hochregallager mit 54 Fächern (Factory I/O / S7-1513-1 PN).

## Inhalt (`scl/`)

| Datei | Baustein |
|---|---|
| `UDT_Fach.udt.txt` | Fach-Datentyp |
| `FB_Auslagern.scl` | Fach ausbuchen |
| `FB_Einlagern.scl` | Fach einbuchen |
| `FB_Loeschen.scl` | Datensatz löschen (ohne Mechanik) |
| `FB_Datenverwaltung_Lager.scl` | Init, HMI-Sync, Status, Einricht |
| `FB_Fachanzeigen.scl` | Fach → HMI kopieren |
| `FB_Freies_Fach_Suchen.scl` | Erstes freies Fach |
| `FB_Lagerstatus.scl` | Zählen + Status-Text |
| `FB_Meldung.scl` | Info_Code → Info_Text |
| `FB_Suchen.scl` | Suche RFID / Artikel / Fach |
| `Hochregal_Automatik_Betrieb.scl` | Automatik + Offset_Z Pick/Place |

Siehe `INFO_CODES.md`, `VARIABLES.md` und die Gesamtdoku:

- Markdown: `docs/Hochregallager_Dokumentation.md`
- PDF: `docs/Hochregallager_Dokumentation.pdf`

## DB-Hierarchie (TIA)

```
gldb_AktuellerFach_HMI
  Auswahl.{Ausgewaeltes_Fach, Fachaktuell}
  Lagerstatus.{Anzahl_*, Anzeige_noch_Frei, Lagerstatus_Text}
  Meldung.{Info_Code, Info_Text, Funktion_Meldung_Ok}

gldb_Meldungen
  Status.{Meldecode, Meldung}
  Fehler.{Fehlercode, Fehler_Aktiv}

gldb_LagerverwaltungData
  Fach[1..54], Lager_Voll, Lager_Leer, Ziel_Fachnummer
```

## Aufrufreihenfolge (OB1)

1. `FB_Datenverwaltung_Lager`
2. HMI-Flanken: Einlagern / Auslagern / Löschen / Suchen / FreiesFach
3. `Hochregal_Automatik_Betrieb` — `#Offset_Z` verdrahten (z.B. `0.01`)
4. `FB_Lagerstatus` — nur wenn Zählung **nicht** in Datenverwaltung
5. `FB_Meldung` — **zuletzt**

## Gabel: 3 Positionen

| Position | Bedeutung |
|---|---|
| **Links** | Regal links **oder** Förderband (wenn `Foerderband_Seite <> 1`) |
| **Mitte** | Fahrtposition (mit/ohne Last) — immer vor X/Z-Fahrt |
| **Rechts** | Regal rechts (`RegalSeite = 1`) **oder** Förderband (`Foerderband_Seite = 1`) |

### Pick / Place + Offset_Z

**Einlagern:** Förderband-Seite aufnehmen → Mitte → Fach `Z+Offset` → Regal-Seite → absenken → ablegen → Mitte → Home  

**Auslagern:** Mitte → Fach Ruhe-Z → Regal-Seite → anheben → aufnehmen → Mitte → Ausgabe `Z+Offset` → Förderband-Seite → absenken → ablegen → Mitte → Home  

Wichtige States: **22/32** (Band pick + Mitte), **60/65/72** (Regal drop), **150/155/162** (Regal pick), **192/195/202** (Band drop).
