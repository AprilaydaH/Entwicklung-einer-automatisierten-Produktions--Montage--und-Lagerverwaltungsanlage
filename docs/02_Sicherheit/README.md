# Sicherheit — Index (Phasen 4–11)

Stub-Ordner für EN ISO 12100 / EN ISO 13849-1. Inhalte werden ergänzt, sobald Dokumente geliefert werden.

Zurück: [docs/README.md](../README.md)

## Sicherheitszonen der Factory

| Zone | Bereich | Repo / Subsystem | Status |
|---|---|---|---|
| 1 | Kunststoffbearbeitung | *folgt* | Stub |
| 2 | Metallbearbeitung | *folgt* | Stub |
| 3 | Montage (Pick & Place) | `PickPlace-2Axis-SCL` | Technik vorhanden, Sicherheit folgt |
| 4 | Palettierung | `PickPlace-2Axis-SCL` | Technik vorhanden, Sicherheit folgt |
| 5 | Hochregallager | `Hochregallager-SCL` | Technik vorhanden, Sicherheit folgt |

Jede Zone soll später besitzen: Not-Halt, Schutztüren / Zuhaltung, Sicherheitsfreigabe, Statusleuchte, Wiederanlaufsperre, HMI-Sicherheitsstatus.

## Phasen-Stubs

| Phase | Datei | Inhalt (später) |
|---|---|---|
| 4 Lebensphasen | [04_Lebensphasen.md](04_Lebensphasen.md) | Transport … Außerbetriebnahme |
| 5 Gefährdungsanalyse | [05_Gefaehrdungsanalyse.md](05_Gefaehrdungsanalyse.md) | je Station |
| 6 Risikoeinschätzung | [06_Risikoeinschaetzung.md](06_Risikoeinschaetzung.md) | S/F/P → PL |
| 7 Sicherheitsstrategie | [07_Sicherheitsstrategie.md](07_Sicherheitsstrategie.md) | Zonenkonzept |
| 8 Schutzziele | [08_Schutzziele.md](08_Schutzziele.md) | — |
| 9 Schutzmaßnahmen | [09_Schutzmassnahmen.md](09_Schutzmassnahmen.md) | mech./elektr./SW |
| 10 Restrisiken | [10_Restrisiken.md](10_Restrisiken.md) | Betriebsanleitung |
| 11 Sicherheitskontrollen | [11_Sicherheitskontrollen.md](11_Sicherheitskontrollen.md) | Prüfprotokolle |

## Vorläufige PL-Hinweise (aus Projektbrief, zu verifizieren)

| Gefährdung | S | F | P | Ergebnis (Entwurf) |
|---|---|---|---|---|
| Roboter | S2 | F2 | P2 | PL e |
| Bearbeitungszentrum | S2 | F2 | P2 | PL e |
| Förderband | S1 | F2 | P1 | PL c |
| RFID | S1 | F1 | P1 | PL a |
| Hochregal | S2 | F2 | P2 | PL d/e |
| Palettierer | — | — | — | *folgt* |
| Pick & Place | — | — | — | *folgt* |
