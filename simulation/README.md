# Simulation — Factory I/O & TIA

Lokale Simulationsdateien für die Abschlussarbeit.

**Gesamtdokument:** [docs/01_Projektgrundlagen/Gesamtanlage.md](../docs/01_Projektgrundlagen/Gesamtanlage.md)

## Factory I/O (`FactoryIO/`)

| Datei | Verwendung |
|---|---|
| `aBSCHLUSSPROJEKT.factoryio` | Haupt-/Abschlussprojekt-Szene (Gesamtanlage) |
| `Automated Warehouse.factoryio` | Hochregal / Warehouse (54 Fächer) |
| `Automated Warehouse2w.factoryio` | Warehouse Variante |
| `Warenlager_RFID.factoryio` | RFID-Warenlager |
| `Sortieranlage_mit_Pick_and_Place.factoryio` | Sortierung + Pick & Place |

> `waage.factoryio` bewusst **nicht** übernommen (Wasser/Waage nicht im Scope).

## TIA Portal

Siehe [TIA/README.md](TIA/README.md) — `.ap20` bleibt lokal unter OneDrive (nicht im Git).

## Zuordnung zu Lageplan-Zonen

| Zone | Szene / SCL |
|---|---|
| 1–2 CNC | Abschlussprojekt + `scl/Zone_1a_Metall/` · `Zone_1b_Kunststoff/` |
| 3 Pick&Place | Abschlussprojekt / Sortieranlage + `scl/Zone_3a_Metall_PickPlace/` |
| 4A | 3-axis Pick and Place | Abschlussprojekt + `scl/Zone_4a_Metall_Palletizer_RFID/` |
| 4B Palettierer | Abschlussprojekt + `scl/Zone_4b_Kunststoff_Palletizer_RFID/` |
| 5 + Lager | Automated Warehouse / Warenlager_RFID + `scl/Zone_5b_Hochregallager/` · `scl/Zone_4b_Kunststoff_Palletizer_RFID/` |
| 5 Roboter | Abschlussprojekt + `scl/Zone_5a_Foerderband_Lager/` |

Driver: Siemens S7-1500 / PLCSIM / NetToPLCSim — Tag-CSV je Bereich unter `scl/*/PLC_Tags_*.csv`.
