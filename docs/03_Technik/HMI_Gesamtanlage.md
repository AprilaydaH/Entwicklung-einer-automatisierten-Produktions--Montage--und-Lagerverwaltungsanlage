# HMI Gesamtanlage — ein Touch Panel für die Factory

**Prinzip:** Es gibt **eine** HMI (Siemens TP / WinCC) für **alle** Maschinen der Abschlussarbeit.

Kein separates Panel pro Station. Navigation über Bereiche / Tabs; gemeinsame Betriebsarten und Meldungen.

---

## Abgedeckte Bereiche

| Bereich | Maschinen / Technik | SPS-Logik (Ziel) |
|---|---|---|
| **Hochregallager** | Ein-/Auslagern, Fachverwaltung, Suche | `scl/Hochregallager/` |
| **Pick & Place** | Montage Base/Deckel | `scl/PickPlace_DigitalAnalog.scl` |
| **Palettierer** | Box laden, Assembly, Platte, Unload | `scl/FB_Palletizer.scl` |
| **CNC / Bearbeitungsstationen** | Kunststoff + Metall (Base/Deckel) | *folgt* |
| **Förderbänder** | Verbindung zwischen den Stationen | *folgt* |
| **RFID** (wo vorhanden) | Identifikation / Verfolgung | *folgt* |

**Nicht im Scope:** Wasserverbrauch / Wasserwirtschaft.

---

## Bildschirm-Struktur (ein TP)

```
┌─────────────────────────────────────────────────────────────┐
│  HEADER (immer sichtbar)                                    │
│  Betriebsart Auto/Hand · Anlagen-Start/Stop · Reset         │
│  Sammelmeldung · Zone-Statuslampen · Not-Halt-Anzeige       │
├──────────┬──────────┬──────────┬──────────┬─────────────────┤
│ Übersicht│ Hochregal│ PickPlace│ Palettier│ CNC / Förder    │
└──────────┴──────────┴──────────┴──────────┴─────────────────┘
```

| Screen | Inhalt |
|---|---|
| **Übersicht** | Materialfluss, welche Zone busy/ready/fault; Schnellzugriff |
| **Hochregal** | Fachauswahl, Ein/Aus/Löschen/Suche, Lagerstatus, Meldetexte |
| **Pick & Place** | Auto/Hand, Positionen, Grab, Status |
| **Palettierer** | laut [Palettierer/HMI_Organisation.md](../04_Subsysteme/Palettierer/HMI_Organisation.md) |
| **CNC** | Start/Stop/Reset Stationen, Busy/Error, Materialwahl |
| **Förderbänder** | Band ± je Segment, Stausensoren, Verriegelung zu Zonen |
| **Rezept / Parameter** | Zeiten, Offsets, Assemblies (schreibgeschützt je User-Level) |
| **Diagnose** | Roh-I/O, Step/State je FB, Alarmliste |

---

## Gemeinsame HMI → SPS Signale (Konvention)

| Signal | Bedeutung |
|---|---|
| `HMI_Auto` | Gesamt oder je Zone (Empfehlung: **je Zone** + Master Auto) |
| `HMI_Start` / `HMI_Stop` / `HMI_Reset` | je Zone oder zentral mit Freigabe-Logik |
| `HMI_Lamp_*` | Ready / Running / Done / Fault je Zone auf Übersicht |
| Manual-Jog `Man_*` | nur auf dem jeweiligen Zonen-Screen, nur wenn Hand |

**Empfehlung für die Factory:**  
- Header: zentraler **Stop** (alle Zonen)  
- Pro Zone: eigener Start / Hand-Jog (wie bereits beim Palettierer)

---

## Zuordnung zu bestehenden Tags

| Zone | Bestehende Tag-/DB-Basis |
|---|---|
| Palettierer | `PLC_Tags_Palletizer.csv` (`HMI_*`, `Man_*`, Status) |
| Hochregal | `gldb_AktuellerFach_HMI`, `gldb_Meldungen`, … (siehe VARIABLES.md) |
| Pick & Place | FB-Pins + spätere PLC-Tags analog Palettierer |
| CNC / Förder | neue Tag-Tabelle (noch anzulegen) |

Später: **eine** HMI-Tag-Tabelle oder ein gemeinsamer DB `gldb_HMI_Factory` mit Unterstrukturen je Zone.

---

## Umsetzungsreihenfolge

1. Palettierer-HMI (Screen fertig, Tags vorhanden)  
2. Hochregal-HMI (bestehende DBs anbinden)  
3. Pick & Place-HMI  
4. CNC + Förderbänder  
5. Übersicht + zentraler Stop + Alarmseite  

Zurück: [docs/README.md](../README.md)
