# Palettierer — Fertigstellung & Test (Factory I/O)

## Ist-Stand

| Element | Status |
|---|---|
| `FB_Palletizer` v2.1 | Sequenz + Auto/Manual HMI |
| PLC-Tags CSV/XLSX | `%I6.1+` / `%Q6.1+` / `%M…` |
| HMI-Organisation | Screens Auto / Manual / Recipe / Diagnostics |
| `OB1_Palletizer.scl` | Aufruf mit Tag-Verdrahtung |
| Factory I/O Mapping | **vom Anwender prüfen / anpassen** |

## TIA-Import (Reihenfolge)

1. PLC-Tags importieren: `scl/PLC_Tags_Palletizer.csv`
2. External Source: `FB_Palletizer.scl` → generieren
3. Instanz-DB anlegen: `FB_Palletizer_DB`
4. External Source / übernehmen: `OB1_Palletizer.scl` (oder Call manuell in OB1)
5. Factory I/O Driver: Sensoren/Aktoren auf dieselben `%I`/`%Q` legen
6. HMI (TP): Tags laut [HMI_Organisation.md](HMI_Organisation.md)

## Sequenz (Kurz)

`0 Idle` → `10 Emit/Roller` → `12 Chain (Lichtschrank ↓)` → `20 Elevator up` →  
`30–50` Belt / Push / Clamp (**×2**) → `60 Open plate` → `70–72` Elevator down / Unload

## Test-Checkliste Manual

- [ ] `HMI_Auto = 0`
- [ ] Emit + Roller bringen Box zur Station
- [ ] Chain Fwd → `Elev_Front_Limit` TRUE dann FALSE
- [ ] Elevator Up/Down + Move to Limit
- [ ] Belt / Push / Clamp / Open Plate einzeln
- [ ] Sensor-Lampen auf HMI folgen den Inputs

## Test-Checkliste Automatik

- [ ] `HMI_Auto = 1`, `HMI_SingleCycle = 1`
- [ ] Ready-Lampe → **Start**
- [ ] Steps in `State` / Textliste durchlaufen
- [ ] 2× Assembly (Belt→Push→Clamp)
- [ ] Open plate → Unload → **Done**
- [ ] **Stop** bricht ab, Aktoren aus
- [ ] Continuous: `SingleCycle = 0` → nächste Box ab Step 10

## Typische Stuck-Punkte

| Step | Prüfen |
|---|---|
| 10 | Emitter, `Stackable_Box_Present`, `Stackable_Box_At_Palletizer` |
| 12 | Chain +, Lichtschrank-Flanke |
| 20 / 70 | `Elevator_Moving` fallende Flanke + Move to Limit |
| 30 | `Assembled_Part_Present` + `Stackable_Box_Ready` |
| 40 | `Pusher_Limit` steigende Flanke |
| 50 | `Clamped` |

## Nächste Feinschritte (wenn Simulation läuft)

1. Adressen an echte Factory-I/O-Belegung anpassen (falls Konflikt mit Pick & Place)
2. `Belt_Run_Time` / `Unload_Time` tunen
3. HMI-Screens im TP anlegen (laut HMI_Organisation)
4. Danach: Pick & Place HMI angleichen → später **ein** Gesamt-HMI
