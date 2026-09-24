# Info_Code Referenz (FB_Meldung)

| Code | Bedeutung | Ok |
|---:|---|---|
| 0 | Keine Meldung | — |
| 1 | Einlagerung erfolgreich | ja |
| 2 | Fach bereits belegt | nein |
| 3 | Fachnummer ungültig | nein |
| 4 | Auslagerung erfolgreich | ja |
| 5 | Fach bereits frei | nein |
| 6 | Datensatz gelöscht | ja |
| 7 | RFID-Code fehlt | nein |
| 8 | Kein passendes Fach gefunden | nein |
| 9 | Produkt gefunden | ja |
| 10 | Lager voll | nein |
| 11 | Factory I/O Zielposition geladen | ja |
| 12 | Factory I/O Ziel erreicht | ja |
| 13 | Not-Aus aktiv | nein |
| 14 | Freies Fach gefunden | ja |
| 15 | Fach gesperrt | nein |
| 16 | Fachposition gespeichert | ja |
| 17 | Raster: alle Positionen berechnet | ja |

## TIA-Anpassungen vor dem Übersetzen

1. `UDT_Fach`: Aggregate entfernen (`Anzahl_*`, `Lager_Voll`, `Lager_Leer`).
2. `gldb_AktuellerFach_HMI`: ergänzen falls fehlend:
   - `Anzahl_Belegt : UInt`
   - `Anzahl_Frei : UInt`
   - `Anzeige_noch_Frei : Bool`
   - `Lagerstatus_Text` → mind. `String[80]`
3. `gldb_LagerverwaltungData`: `Lager_Voll`, `Lager_Leer`, `Ziel_Fachnummer`.
4. `Hochregal_Automatik_Betrieb` Interface ergänzen:
   - In: `Not_Aus`
   - Static: `Paket_Uebernommen`, `Start_FreiesFach`
   - Multiinstanzen: `instFreiesFachSuchen`, `instEinlagern`, `instAuslagern`, `instSuchen`, `instLagerstatus`
5. `FB_Freies_Fach_Suchen` Out: `Fachnummer : USInt` (nicht UInt).
6. Zählung nur **einmal** zyklisch: entweder Datenverwaltung **oder** `FB_Lagerstatus`.
7. `FB_Meldung` **nach** allen Lager-FBs aufrufen (einzige Textquelle für `Info_Code`).
8. `FB_Suchen` bei Misserfolg setzt `Fachnummer := 0` — Automatik State 110 prüft `Info_Code = 9`.
9. Automatik: Input `Offset_Z` (z.B. 0.01) für Pick/Place über Ruheposition (States 65 / 155 / 195).
10. HMI-Pfade: `.Auswahl.*` / `.Lagerstatus.*` / `.Meldung.*` — Meldungen: `.Status.*` / `.Fehler.*`.
11. `gldb_LagerverwaltungData.Raster` (`UDT_Lager_Raster`) + `FB_Berechn_Offset` + Datenverwaltung V1.3 pins.
12. Tags: `PLC_Tags_Hochregallager.csv` (HMI + crane), `PLC_Tags_RFID.csv` (Vision/RFID).
