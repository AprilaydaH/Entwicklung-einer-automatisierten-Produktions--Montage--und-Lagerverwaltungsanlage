# Phase 2 — Grenzen der Maschine

Dieser Abschnitt definiert, was zur Maschine (Factory-Gesamtanlage) gehört und was nicht. Grundlage für Risikobeurteilung und CE-Dokumentation.

## Zur Maschine gehören

- Bearbeitungszentren (Kunststoff / Metall; Base und Deckel) — geplant
- Montagezellen / Two-Axis Pick & Place — Repo `PickPlace-2Axis-SCL`
- KUKA-Roboter (soweit in der Szene / Planung vorgesehen) — geplant
- Fördertechnik — geplant / szenenabhängig
- RFID-Stationen — geplant
- Palettierer — Repo `PickPlace-2Axis-SCL`
- Hochregallager inkl. Lagerverwaltung — Repo `Hochregallager-SCL`
- HMI (Touch Panel)
- SPS (TIA Portal V20)
- Schaltschrank (konzeptionell / dokumentiert)
- Sicherheitssteuerung / Sicherheitskreise (konzeptionell nach EN ISO 12100 / ISO 13849)

## Nicht Bestandteil der Maschine

- externe Energieversorgung (Übergabepunkt)
- Gabelstapler und innerbetrieblicher Transport außerhalb der Anlage
- Bedienpersonal (Mensch ist Nutzer, nicht Bestandteil der Maschine)
- übergeordnetes ERP-System (Schnittstelle kann später beschrieben werden, ist aber nicht Gegenstand der Steuerung)

## Schnittstellen (Systemgrenze)

| Schnittstelle | Beschreibung |
|---|---|
| Energie | Übergabe an Schaltschrank |
| Material | Rohteile in / Fertigprodukte bzw. Paletten aus |
| Information | HMI-Bedienung; optional später ERP |
| Simulation | Factory I/O als Abbild der Maschinengrenzen |

## Hinweis Repositories

Die Software der Maschinengrenzen ist auf die Factory-Repos verteilt. Die **funktionale Grenze der Maschine** bleibt die Gesamtanlage; die **Entwicklungseinheiten** sind die genannten Git-Repositories.
