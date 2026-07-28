# Pick & Place 2-Axis — SCL (Factory I/O)

Zwei-Achs-Pick-and-Place-Steuerung in SCL für **Factory I/O** (S7-1500 / S7-PLCSIM).

Unterstützt **Analog**- und **Digital**-Achsansteuerung über eine gemeinsame Konfiguration.

## Szene (Factory I/O)

Empfohlen: **Pick & Place** (Two Axis Pick and Place) mit Förderband-Eingang/-Ausgang und Greifer.

```
  [Entry Conveyor] → Pick-Position → Z-Hub → X-Fahrt → Place-Position → [Exit Conveyor]
                              ↑
                         Gripper (DO)
```

## Inhalt (`scl/`)

| Datei | Baustein | Beschreibung |
|---|---|---|
| `OB1_Main.scl` | Main | Zyklusaufruf, Modi, I/O-Verdrahtung |
| `FB_PickPlace_2Axis.scl` | FB_PickPlace_2Axis | Automatik-Sequenz Pick → Place |
| `FB_Axis_Analog.scl` | FB_Axis_Analog | Achse per Analog-Sollwert + Istwert |
| `FB_Axis_Digital.scl` | FB_Axis_Digital | Achse per Digital +/- und Endlagen |
| `FB_Gripper.scl` | FB_Gripper | Greifer aufnehmen / ablegen |
| `gldb_FactoryIO_IO.udt.txt` | UDT / DB-Vorlage | Digitale + analoge Tags |

Siehe auch:

- `VARIABLES.md` — Interfaces und globale Tags
- `FACTORY_IO_IO.md` — Tag-Mapping Factory I/O ↔ PLC
- `docs/PickPlace_2Axis_Dokumentation.md` — Sequenz, States, Inbetriebnahme

## Betriebsmodi

| Modus | Bedeutung |
|---|---|
| **Auto** | Zyklus: Band → Pick → Place → Band |
| **Hand** | Einzelne Achsen / Greifer per HMI |
| **Einricht** | Positionen speichern, Achsen freigeben |

## Achs-Konfiguration

In `gldb_Config.Achs_Modus`:

| Wert | Bedeutung |
|---|---|
| `0` | **Analog** — `AO_Target_*` / `AI_Pos_*` (0…10 V → mm/Position) |
| `1` | **Digital** — `DO_Move_*_Plus/Minus` + Endlagen / Positionssensoren |

Beide Modi nutzen dieselbe Sequenz in `FB_PickPlace_2Axis`; nur die Achs-FBs wechseln.

## Aufrufreihenfolge (OB1)

1. I/O → Prozessabbild / `gldb_FactoryIO_IO` spiegeln (Driver)
2. Modi (Einricht > Auto > Hand)
3. `FB_PickPlace_2Axis` (intern: Achsen + Greifer)
4. Prozessabbild → Factory I/O Outputs

## Schnellstart TIA

1. SCL-Bausteine aus `scl/` importieren / anlegen
2. `gldb_FactoryIO_IO` und `gldb_Config` anlegen (siehe `VARIABLES.md`)
3. Factory I/O Driver (S7-1500 / NetToPLCSim / Official) Tags laut `FACTORY_IO_IO.md` mappen
4. `Achs_Modus` auf `0` (Analog) oder `1` (Digital) setzen
5. Teach-Punkte: Home, Pick, Place (X/Z) in Einricht speichern
6. Auto starten
