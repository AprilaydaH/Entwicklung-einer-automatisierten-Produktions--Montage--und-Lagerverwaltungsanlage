# Subsystem — Hochregallager (Zone 5)

**Sicherheitszone:** 5 — Hochregallager  
**Repository:** [`Hochregallager-SCL`](../../../../Hochregallager-SCL) (Schwester-Repo unter `Projects/`)  
**Factory-Rolle:** Einlagern, Auslagern, Fachverwaltung, Suche (RFID / Artikel / Fach)

## Code (im Repo `Hochregallager-SCL`)

| Baustein / Datei | Funktion |
|---|---|
| `UDT_Fach` | Fach-Datentyp |
| `FB_Einlagern` / `FB_Auslagern` / `FB_Loeschen` | Buchungen |
| `FB_Suchen` / `FB_Freies_Fach_Suchen` | Suche |
| `FB_Datenverwaltung_Lager` / `FB_Lagerstatus` / `FB_Meldung` | Verwaltung / Status |
| `Hochregal_Automatik_Betrieb` | Automatik inkl. Offset_Z |

## Dokumentation (im Repo `Hochregallager-SCL`)

- `README.md`
- `VARIABLES.md`, `INFO_CODES.md`
- `docs/Hochregallager_Dokumentation.md` (+ PDF falls erzeugt)

## Schnittstellen in der Factory (konzeptionell)

| Von / Nach | Signal / Material |
|---|---|
| ← Palettierer / Fördertechnik | einzulagernde Einheiten |
| ← HMI | Fachauswahl, Aufträge |
| → Produktion | Auslagerung Roh-/Fertigteile nach Auftrag |

## Sicherheit (Zone 5) — Stub

Gefahren: Regalbediengerät, Lastabsturz. Schutz: Zaun, Wartungstüren, Endschalter, sichere Positionierung (Details in `docs/02_Sicherheit/`).
