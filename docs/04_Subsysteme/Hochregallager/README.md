# Subsystem — Hochregallager (Zone 5)

**Maschinenlogik:** Function Blocks unter `scl/Hochregallager/`  
**Sicherheitszone:** 5 — Hochregallager  
**Teil dieses Abschlussprojekts** (nicht externes Nebenprojekt)  
**Factory-Rolle:** Einlagern, Auslagern, Fachverwaltung, Suche (RFID / Artikel / Fach)

## Code (`scl/Hochregallager/`)

| Datei | Baustein |
|---|---|
| `UDT_Fach.udt.txt` | Fach-Datentyp |
| `FB_Einlagern.scl` | Fach einbuchen |
| `FB_Auslagern.scl` | Fach ausbuchen |
| `FB_Loeschen.scl` | Datensatz löschen |
| `FB_Datenverwaltung_Lager.scl` | Init, HMI-Sync, Status |
| `FB_Freies_Fach_Suchen.scl` | Erstes freies Fach |
| `FB_Lagerstatus.scl` | Zählen + Status-Text |
| `FB_Meldung.scl` | Info_Code → Info_Text |
| `FB_Suchen.scl` | Suche RFID / Artikel / Fach |
| `Hochregal_Automatik_Betrieb.scl` | Automatik + Offset_Z |
| `OB1_Main.scl` | Aufrufreihenfolge der FBs |

## Dokumentation

| Dokument | Inhalt |
|---|---|
| [Hochregallager_Dokumentation.md](Hochregallager_Dokumentation.md) | Gesamtdoku |
| [VARIABLES.md](VARIABLES.md) | Variablen |
| [INFO_CODES.md](INFO_CODES.md) | Melde-/Info-Codes |
| [README_SCL.md](README_SCL.md) | Kurzüberblick Bausteine |

## Schnittstellen in der Factory

| Von / Nach | Material / Signal |
|---|---|
| ← Palettierer / Fördertechnik | einzulagernde Einheiten |
| ← HMI (später Gesamt-TP) | Fachauswahl, Aufträge |
| → Produktion | Auslagerung nach Auftrag |

## Sicherheit (Zone 5) — Stub

Gefahren: Regalbediengerät, Lastabsturz. Schutz: Zaun, Wartungstüren, Endschalter (Details in `docs/02_Sicherheit/`).

Zurück: [04_Subsysteme](../README.md) · [docs](../../README.md)
