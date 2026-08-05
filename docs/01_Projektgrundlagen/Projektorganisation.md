# Phase 1 — Projektorganisation

## Projektname

**Offiziell (Freigabe):**  
Entwicklung und Simulation einer automatisierten Fertigungs- und Lageranlage mit RFID-gestützter Produktverfolgung in TIA Portal und Factory I/O

**Untertitel / Gesamtanlage:**  
Automatisierte Produktions-, Montage- und Lagerverwaltungsanlage für Kunststoff- und Metallprodukte mit RFID-Identifikation

## Teilnehmer

| Rolle | Name |
|---|---|
| Verfasser | Dereje Hailemariam |
| Freigabe | ja (Berlin, 29.06.2026) |

## Projektziel

Entwicklung einer automatisierten Industrieanlage zur:

- Bearbeitung von Kunststoff- und Metallteilen (Base und Deckel getrennt)
- RFID-Identifikation und Produktverfolgung
- automatischen Montage (Pick & Place)
- Palettierung
- Hochregallagerverwaltung (Ein- und Auslagerung nach Auftrag)
- Visualisierung über HMI (Touch Panel)
- Sicherheitsbewertung nach EN ISO 12100 (Schritt für Schritt)

**Quantitativ:** vorgesehene Lagerfächer adressierbar; wichtige Prozesszustände speicherbar.  
**Qualitativ:** modular, erweiterbar, realistisch in TIA Portal V20 und Factory I/O testbar.

## Factory — Repository-Struktur

Die Anlage wird **nicht in einem einzigen Repo** entwickelt, sondern als Factory aus mehreren Repositories:

| Subsystem | Repository | Rolle in der Factory |
|---|---|---|
| Two-Axis Pick & Place | `PickPlace-2Axis-SCL` | Montage Base/Deckel |
| Palettierer | `PickPlace-2Axis-SCL` | Palettierung fertiger Produkte |
| Hochregallager | `Hochregallager-SCL` | Ein-/Auslagerung, Fachverwaltung, Suche |
| Weitere Stationen | *weitere Repos / später* | Bearbeitung, RFID, Fördertechnik |

Dieses Repository (`PickPlace-2Axis-SCL`) ist der **Integrationspunkt für die Projektdokumentation** der Gesamtanlage und enthält die Subsysteme Palettierer und Pick & Place.

## Vorgehensweise

1. Anlagenlayout, Signal- und Variablenstruktur, Betriebsarten  
2. SPS-Bausteine je Subsystem (Förder, Bearbeitung, RFID, PnP, Palettierung, HRL)  
3. Lagerverwaltung (Datenbausteine, Suche, Ein-/Auslagerung, Löschen)  
4. HMI (Fachauswahl, Status, Manual/Auto, Meldungen)  
5. Simulation Factory I/O  
6. Tests, Sicherheitsmaßnahmen, Fehlerreaktionen, Dokumentation (EN ISO 12100 / CE)

## Zugehörige Dokumente

- [Kapitel 1 — Projektgrundlagen](README.md)
- [Maschinengrenzen](Maschinengrenzen.md)
- [Bestimmungsgemäße Verwendung](Bestimmungsgemaesse_Verwendung.md)
- [Freigabe-Zusammenfassung](Freigabe_Zusammenfassung.md)
- [Gesamtindex](../README.md)
