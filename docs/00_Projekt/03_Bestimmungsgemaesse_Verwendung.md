# Phase 3 — Bestimmungsgemäße Verwendung

## Bestimmungsgemäße Verwendung

Die Maschine dient ausschließlich zum:

- Bearbeiten von Kunststoffteilen (Base / Deckel)
- Bearbeiten von Metallteilen (Base / Deckel)
- Zusammenbauen der Produkte (Pick & Place)
- RFID-Kontrolle und Produktverfolgung
- Palettieren fertiger Produkte
- Einlagern in das Hochregallager
- Auslagern nach Auftrag / Anforderung
- Bedienung und Visualisierung über HMI in Automatik- und Handbetrieb

## Vernünftigerweise vorhersehbare Fehlanwendung — nicht erlaubt

- Bearbeitung anderer Materialien als vorgesehen
- Arbeiten bei geöffneter Schutztür / umgangenem Sicherheitskreis
- Betrieb ohne intakten Sicherheitskreis
- Eingriff in Roboter- oder Pick-&-Place-Bereich während Automatik
- manuelles Entfernen von Teilen aus laufender Förder-/Palettier-/Regalmechanik
- Überbrücken von Not-Halt, Türzuhaltung oder Lichtgittern

## Betriebsarten (geplant)

| Betriebsart | Verwendung |
|---|---|
| Automatik | bestimmungsgemäße Produktion |
| Hand / Einrichten | Setup, Störungsbeseitigung mit reduzierten Risiken |
| Service / Wartung | nur nach Freischalten, Lockout/Tagout |

## Bezug zu den Subsystemen

| Verwendung | Subsystem / Repo |
|---|---|
| Montage | Two-Axis Pick & Place — `PickPlace-2Axis-SCL` |
| Palettieren | Palettierer — `PickPlace-2Axis-SCL` |
| Ein-/Auslagern | Hochregallager — `Hochregallager-SCL` |
