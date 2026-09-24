# HMI — Warehouse_2 (Metal)

**Panel:** Siemens TP · Zone **5A** Metal Hochregal (NW 28)  
**PLC:** W2 tags + `gldb_AktuellerFach_HMI_W2` + `gldb_LagerverwaltungData_W2`  
**Tags:** [`HMI_Tags_Warehouse_2.csv`](HMI_Tags_Warehouse_2.csv)  
**Data mgmt:** [`HMI_DATA_MGMT.md`](HMI_DATA_MGMT.md)

Mirror of Warehouse_1 screens — use a **separate HMI screen set** (or folder) so plastic and metal do not share tags.

All command buttons = **momentary**.

**Mode radios:** HMI SetBit / ResetBit on `Mode_*_W2`. PLC `FB_Warehouse_Mode_Select_W2` pins must be **IN_OUT** or `%M70.0–.2` never stay TRUE.

---

## Structure

```
HEADER  Mode_W2 · Busy/Done/Error · State · STOP
OVERVIEW | OPERATE | SETUP
```

| Screen | Purpose |
|---|---|
| **Overview** | Rack + process + counts |
| **Operate** | Hand product + Start / data cmds |
| **Setup** | Einricht teach |

Default: **Overview** = main operator page. Build spec: [`HMI_Overview_Main.md`](HMI_Overview_Main.md).

---

## Header

| Object | Tag |
|---|---|
| Mode radios | `Mode_Einricht_W2` / `Mode_Auto_W2` / `Mode_Hand_W2` |
| Busy / Done / Error | `HRL2_Busy` / `HRL2_Done` / `HRL2_Error` |
| State | `HMI_State_W2` |
| STOP | `HMI_Stop_W2` |
| Not-Aus | `Not_Aus_W2` |

### State text list (V5.6)

| Value | Text |
|---|---|
| 0 | Bereit — warte auf Palette |
| 10 | RFID lesen… |
| 20 | Freies Fach suchen… |
| 30 | Fahre zum Band… |
| 40 | Gabel ausfahren (Band) |
| 41 | Anheben + aufnehmen |
| 42 | Gabel einfahren |
| 50 | Fahre zum Fach… |
| 55 | Gabel ausfahren (Regal) |
| 56 | Absenken + absetzen |
| 58 | Gabel einfahren |
| 60 | Lagerdaten aktualisieren… |
| 70 | Fahre zur Home-Position… |
| 80 | Fertig |
| 900 | Störung — siehe Meldung |

---

## Overview

**Full layout + WinCC bindings:** [`HMI_Overview_Main.md`](HMI_Overview_Main.md)

Product on the main page is **DB_103** (`4a_RFID_Code_Out`), not warehouse Reader 0.

---

## Operate

| Object | Tag |
|---|---|
| Start Einlagern | `HMI_Start_Einlagern_W2` |
| Start Auslagern | `HMI_Start_Auslagern_W2` (no sequencer yet) |
| Reset / Reset Meldung | `HMI_Reset_W2` / `HMI_Reset_Meldung_W2` |
| Suchen / Freies Fach / Löschen | `HMI_Suchen_W2` / `HMI_FreiesFach_W2` / `HMI_Loeschen_W2` |
| Fachnummer | `HMI_Fachnummer_W2` |
| Product | `gldb_AktuellerFach_HMI_W2.Auswahl.Fachaktuell.*` |
| Materialart | default **2** (Metall) |

---

## Setup

| Object | Tag |
|---|---|
| Soll X/Z, Jog | `HMI_Soll_*_W2`, `HMI_Jog_Step_W2` |
| Ist→Soll / Band | `HMI_Copy_Ist_to_Soll_W2`, `HMI_Copy_Ist_to_Band_W2` |
| Home / Band / Pitch | `Home_*_W2`, `Band_*_W2`, `HMI_Pitch_*_W2` |
| Pos / Raster / Init | `HMI_Pos_Speichern_W2`, `HMI_Raster_Berechnen_W2`, `HMI_Initialisieren_W2` |

Enable only when `Mode_Einricht_W2`.

---

## Build order

1. Header + nav  
2. **Overview (main)** — [`HMI_Overview_Main.md`](HMI_Overview_Main.md)  
3. Operate Hand fields + Start  
4. Setup raster teach  
5. **Rack occupancy** — 54 cells from `gldb_AktuellerFach_HMI_W2.Lagerstatus` ([HMI_Regal_Animation.md](../../docs/03_Technik/HMI_Regal_Animation.md))  
