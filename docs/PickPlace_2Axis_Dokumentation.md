# Dokumentation — Pick & Place 2-Axis (Factory I/O)

## Überblick

SCL-Steuerung für eine zweiachsige Pick-and-Place-Station (X horizontal, Z vertikal) mit Greifer und Ein-/Ausgangsförderband. Die gleiche Sequenz arbeitet mit **Analog**- oder **Digital**-Achsansteuerung (`gldb_Config.Achs_Modus`).

## Architektur

```
OB1_Main
 └── FB_PickPlace_2Axis
      ├── FB_Axis_Analog   (Achs_Modus = 0)
      ├── FB_Axis_Digital  (Achs_Modus = 1)
      └── FB_Gripper
```

I/O gebündelt in `gldb_FactoryIO_IO`. Teach-Punkte und Modus in `gldb_Config`.

## Sequenz (Auto)

1. Start (HMI)
2. Entry-Conveyor bis `Sensor_Entry`
3. Verfahren nach Pick (X) bei Z oben
4. Absenken → Greifen → Anheben
5. Verfahren nach Place (X)
6. Absenken → Ablegen → Anheben
7. Exit-Conveyor + Rückfahrt Home
8. `Done_Cycle`, zurück Idle

Zwischen X-Fahrten immer **Z oben**, analog zum klassischen Pick-and-Place.

## Inbetriebnahme

1. TIA-Projekt: Bausteine aus `scl/` anlegen, Multiinstanzen in `FB_PickPlace_2Axis`
2. DBs `gldb_FactoryIO_IO`, `gldb_Config` erzeugen
3. Factory I/O Driver Tags laut `FACTORY_IO_IO.md` mappen
4. `Achs_Modus` wählen (0 empfohlen zum ersten Test)
5. Einricht: Jog → Teach Home / Pick / Place
6. Auto: `Mode_Auto` + `HMI_Start`

## Hand / Einricht

- Jog über HMI +/- (Analog: Soft-Jog am Target; Digital: direkte DO)
- Goto Home / Pick / Place (Analog)
- Teach schreibt aktuelle Istwerte in Config (über OB1 zurück)

## Sicherheit

- `Not_Aus` setzt Outputs zurück und State → 0 (Error 9001)
- `HMI_Stop` bricht Zyklus ab ohne Teach-Verlust
- `HMI_Reset` quittiert Fehler

## Erweiterungsideen

- Mehrere Pick-/Place-Koordinaten (Rezept)
- Palettier-Muster (Raster)
- Analog-Skalierung als eigener FB
- Separates FB für Conveyor-Handshake mit Stauüberwachung
