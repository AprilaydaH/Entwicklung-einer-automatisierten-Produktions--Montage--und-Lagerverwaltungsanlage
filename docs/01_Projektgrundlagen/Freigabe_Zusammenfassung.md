# Freigabedokument — Zusammenfassung

**Quelle:** [`Freigabedokument_Abschlussarbeit_Dereje_Hailemariam.pdf`](Freigabedokument_Abschlussarbeit_Dereje_Hailemariam.pdf)  
**Teilnehmer:** Dereje Hailemariam  
**Ort / Datum (Teilnehmer):** Berlin, 29.06.2026  

**Projekttitel:** Entwicklung einer automatisierten Produktions-, Montage- und Lagerverwaltungsanlage  

**Thema der Abschlussarbeit (Freigabe):**  
Entwicklung und Simulation einer automatisierten Fertigungs- und Lageranlage mit RFID-gestützter Produktverfolgung in TIA Portal und Factory I/O

---

## 1. Ausgangslage (Ist-Zustand)

Automatisierte Fertigungs- und Lageranlage in **TIA Portal V20** und **Factory I/O**:

- Rohteile aus dem Lager
- Transport über Fördertechnik zu Bearbeitungsstationen
- Verarbeitung nach Materialart (Metall / Kunststoff)
- jeweils Base- und Deckel-Komponenten
- RFID-Identifikation
- Montage (zusammengeführte Base/Deckel)
- Palettierung
- automatische Ein- und Auslagerung

## 2. Problemstellung / Ansatzpunkte

Teilprozesse zu einer durchgängigen, sicheren Automatisierung verbinden:

- Materialerkennung
- Förderstrecken
- Bearbeitungszentren
- RFID-gestützte Produktverfolgung
- Pick-and-Place-Montage
- Palettierung
- Lagerverwaltung (Fachnummer, Artikelnummer, Materialart, Produkttyp, RFID, Belegung)
- Manual / Automatik, HMI, Fehler-/Statusmeldungen, grundlegende Sicherheit

## 3. Zielsetzung

- Funktionsfähige **SPS-Steuerung** mit übersichtlicher **HMI**
- Rohprodukte bereitstellen, Metall/Kunststoff getrennt bearbeiten
- Base und Deckel korrekt zuordnen, fertige Produkte palettieren
- Ein-/Auslagerung über Lagerverwaltung
- **Quantitativ:** alle vorgesehenen Lagerfächer adressierbar; wichtige Prozesszustände speicherbar
- **Qualitativ:** modular, erweiterbar, realistisch in TIA + Factory I/O test- und dokumentierbar

## 4. Vorgehensweise

1. Anlagenlayout, Signal-/Variablenstruktur, Betriebsarten  
2. SPS-Bausteine: Fördertechnik, Bearbeitung, RFID, Pick-and-Place, Palettierung, Hochregallager  
3. Lagerverwaltung: DBs, Suche, Einlagern, Auslagern, Löschen  
4. HMI: Fachauswahl, Status, Manual, Automatik, Meldungen  
5. Factory I/O: Bewegungsabläufe und Sensor/Aktor-Signale prüfen  
6. Testfälle, Sicherheitsmaßnahmen, Fehlerreaktionen, Projektdokumentation  

## 5. Bedeutung (fiktives Unternehmen)

- digitale Abbildung und Optimierung von Produktion und Lager
- weniger Verwechslungen durch RFID
- bessere Übersicht Roh-/Fertigprodukte
- kürzere Durchlaufzeiten, weniger manuelle Eingriffe und Fehler
- Prozesssicherheit, Qualität, Nachverfolgbarkeit, Erweiterbarkeit

## 6. Bewertung (Experten-Seite)

| Kriterium | Max. Punkte |
|---|---|
| Ausgangslage | 6 |
| Ansatzpunkte | 6 |
| Zielsetzung | 6 |
| Vorgehensweise | 6 |
| Bedeutung für Unternehmen | 6 |
| **Gesamt** | **30** (mind. 15 erforderlich) |

Freigabe-Felder im PDF: Formularseite für ExpertIn (ja/nein, Anmerkungen, Unterschrift).

---

**Nicht Bestandteil dieses Projekts:** u. a. Wasserverbrauch / Wasserwirtschaft (siehe [Maschinengrenzen.md](Maschinengrenzen.md)).
