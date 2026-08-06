# Simulation — Factory I/O & TIA

Lokale Simulationsdateien für die Abschlussarbeit  
**Titel:** Entwicklung einer automatisierten Produktions-, Montage- und Lagerverwaltungsanlage

## Factory I/O (`FactoryIO/`)

| Datei | Verwendung |
|---|---|
| `aBSCHLUSSPROJEKT.factoryio` | Haupt-/Abschlussprojekt-Szene |
| `Automated Warehouse.factoryio` | Hochregal / Warehouse |
| `Automated Warehouse2w.factoryio` | Warehouse Variante |
| `Warenlager_RFID.factoryio` | RFID-Warenlager |
| `Sortieranlage_mit_Pick_and_Place.factoryio` | Sortierung + Pick & Place |

> `waage.factoryio` bewusst **nicht** übernommen (Wasser/Waage nicht im Scope).

## TIA Portal

Siehe [TIA/README.md](TIA/README.md) — `.ap20` bleibt lokal unter OneDrive (nicht im Git).

## Zuordnung zu Lageplan-Zonen

| Zone | Typische Szene / Code |
|---|---|
| 1–2 CNC | Szene Abschlussprojekt + `scl/Zone1_*` / `Zone2_*` |
| 3 Pick&Place | Sortieranlage / Abschlussprojekt + `scl/Zone3_PickPlace/` |
| 4 Palettierer | Abschlussprojekt + `scl/Zone4_Palettierer/` |
| 5 Roboter | Abschlussprojekt + `scl/Zone5_Roboter/` |
| Hochregal | Automated Warehouse / RFID + `scl/Hochregallager/` |
