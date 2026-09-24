# HMI — Warehouse_1 (efficient + visual)

**Panel:** Siemens TP · Zone 5B  
**PLC:** NW27 tags + `gldb_AktuellerFach_HMI` + `gldb_LagerverwaltungData`  
**Raster:** [`RASTER_TEACH.md`](RASTER_TEACH.md)  
**Tags:** [`HMI_Tags_Warehouse_1.csv`](HMI_Tags_Warehouse_1.csv)

All command buttons = **momentary** (Press SetBit / Release ResetBit).

---

## Recommended structure (3 screens + header)

```
┌─────────────────────────────────────────────────────────────────┐
│  HEADER (always)  Mode · Busy/Done/Error · State · STOP         │
├──────────────┬──────────────┬───────────────────────────────────┤
│  OVERVIEW    │  OPERATE     │  SETUP                            │
│  visual +    │  product /   │  teach / raster                   │
│  animation   │  Hand fields │                                   │
└──────────────┴──────────────┴───────────────────────────────────┘
```

| Screen | Purpose |
|---|---|
| **Overview** | See the warehouse: rack, crane, pallet flow, live process |
| **Operate** | Hand product entry + Start / Reset (compact) |
| **Setup** | Einricht teach only |

**Nav in header:** `Overview` | `Operate` | `Setup` → ChangeScreen.

Default start screen after login: **Overview**.

---

## Header (permanent)

| Object | Tag | Notes |
|---|---|---|
| Mode radios | `Mode_Einricht` / `Mode_Auto` / `Mode_Hand` | **SetBit on press** — PLC [`FB_Warehouse_Mode_Select`](FB_Warehouse_Mode_Select.scl) clears the other two (call **first** in OB1). Optional: also ResetBit others on press. |
| Busy / Done / Error | `HRL_Busy` / `HRL_Done` / `HRL_Error` | Yellow / Green / Red |
| State | `HMI_State` | Integer |
| Step text | Text list from `HMI_State` | See § Animation below |
| STOP | `HMI_Stop` | Large red |
| Not-Aus | `Not_Aus` | Lamp |

---

## Screen C — OVERVIEW (visual + animation)

This is the main operator picture. Keep it **symbolic** (not a 1:1 Factory I/O clone).

```
┌──────────────────────────────────────────────────────────────────────────┐
│  HEADER …                                                                │
├────────────────────────────────────┬─────────────────────────────────────┤
│                                    │  PROCESS                            │
│     [LOADING]                      │  Step: RFID / Pick / Travel / Place │
│        ▭ pallet                    │  Ziel-Fach     ##                   │
│                                    │  Belegt/Frei   ## / ##              │
│   ┌──┬──┬──┬──┬──┬──┐              │  RFID_CODE     ######               │
│   │▓▓│  │  │  │  │  │  ◄── Ziel    │  Artikel       ####                 │
│   ├──┼──┼──┼──┼──┼──┤     highlight│  Material/Color # / #               │
│   │  │  │  │  │  │  │              │                                     │
│   ├──┼──┼──┼──┼──┼──┤   CRANE      │  Gate                               │
│   │  │  │★ │  │  │  │   [≡]──fork  │  Paket vor Regal ○                  │
│   └──┴──┴──┴──┴──┴──┘              │  Paket für HRL   ○                  │
│        RACK 6×9                    │  RFID Gueltig    ○                  │
│                                    │                                     │
│   Ist X/Z  ####.# / ####.#         │  [→ Operate]  [→ Setup]             │
└────────────────────────────────────┴─────────────────────────────────────┘
```

### What to draw (WinCC objects)

| Graphic | How |
|---|---|
| **Rack grid** | 54 small rectangles (6 columns × 9 levels) — or 2 racks of 27 if RegalSeite matters |
| **Occupied slot** | Fill from `gldb_AktuellerFach_HMI.Lagerstatus.Farbe[n]` — WinCC Range animation ([HMI_Regal_Animation.md](../../docs/03_Technik/HMI_Regal_Animation.md)) |
| **Target slot** | Visibility + flash on `gldb_AktuellerFach_HMI.Lagerstatus.Ziel[n]` |
| **Crane** | Rectangle/group; position from `Ist_X` / `Ist_Z` (see animation) |
| **Fork** | 3 states: Left / Middle / Right from `Gabel_*` tags |
| **Pallet at loading** | Visible when `Paket_Vor_Regal` |
| **Pallet on fork** | Visible when `Palette_Aufgenommen` OR states 32–70 |
| **RFID reader** | Small icon near loading; blink when `HMI_State = 10` |

### Rack occupancy (Overview)

PLC fills `gldb_AktuellerFach_HMI.Lagerstatus` every scan. **Do not** bind nested `Fach[n].Belegt`.

Full WinCC steps, colours, grid numbers: [`docs/03_Technik/HMI_Regal_Animation.md`](../../docs/03_Technik/HMI_Regal_Animation.md)  
HMI tags: [`HMI_Tags_Rack_W1.csv`](HMI_Tags_Rack_W1.csv)

| Layer | Tag | Animation |
|---|---|---|
| Cell fill | `gldb_AktuellerFach_HMI.Lagerstatus.Farbe[n]` | Appearance **Range**: 0 grey (frei), 1 blue, 2 green, 3 mixed, 4 steel (metall), 5 red (gesperrt) |
| Fallback 2-colour | `gldb_AktuellerFach_HMI.Lagerstatus.Belegt[n]` | FALSE grey / TRUE occupied |
| Ziel border | `gldb_AktuellerFach_HMI.Lagerstatus.Ziel[n]` | Visibility + flashing yellow border |
| Click cell | SetValue `HMI_Fachnummer` := n | Operate shows that slot |

---

### Live info panel (right side)

| Display | Tag |
|---|---|
| Ziel-Fach | `HMI_Ziel_Fach` |
| Belegt / Frei | `HRL_Anzahl_Belegt` / `HRL_Anzahl_Frei` |
| RFID_CODE | `gldb_AktuellerFach_HMI.Auswahl.Fachaktuell.RFID_CODE` |
| Artikel / Material / Color | `…Fachaktuell.*` |
| Info_Text | `gldb_AktuellerFach_HMI.Meldung.Info_Text` |
| Gate / RFID lamps | `Paket_Vor_Regal`, `Paket_Fuer_Hochregal`, `RFID_5b_*` |
| Ist_X / Ist_Z | `Ist_X`, `Ist_Z` |

No Start buttons on Overview — use **Operate** for commands (keeps the picture clean). Optional: small Start/Stop duplicates if you prefer one-screen operation.

---

## Animation — drive everything from `HMI_State`

Use **Visibility** / **Appearance** animations (no fancy motion needed for v1).

| `HMI_State` | Prozessschritt (Kopfzeile) | Anzeige |
|---|---|---|
| 0 | Bereit — warte auf Palette | Kran in Home |
| 10 | RFID lesen… | RFID-Symbol blinkt |
| 20 | Freies Fach suchen… | Ziel-Fach aktualisiert |
| 30 | Fahre zum Band, Gabel ein | Kran an der Beladung |
| 40–42 | Ausfahren / anheben+aufnehmen / einfahren | Gabel aus → Palette auf Gabel |
| 50 | Fahre zum Fach, Gabel ein | Zielfach hervorgehoben |
| 55–58 | Ausfahren / absenken+absetzen / einfahren | Gabel an der Regalseite |
| 60 | Lagerdaten aktualisieren… | Buchung über `FB_Einlagern` |
| 70 | Fahre zur Home-Position… | Kran nach Home |
| 80 | Zyklus fertig | Done-Impuls |
| 900 | Störung | Rote Überlagerung |

**Data management + OB1 wiring:** [`HMI_DATA_MGMT.md`](HMI_DATA_MGMT.md)

### Crane motion (two options)

**A — Simple (recommended first)**  
- Do **not** move the crane pixel-by-pixel.  
- Show 4 crane “poses” (Loading / Travel / at Ziel / Home) with visibility by State ranges.  
- Fast to build, clear for operators.

**B — Smooth (later)**  
- Animate crane X/Y on screen from `Ist_X` / `Ist_Z` with linear scaling:  
  `ScreenX = Offset + Ist_X * Scale`  
- Needs known min/max of Factory I/O voltages after teach.

### Fork animation

| Tag | Show |
|---|---|
| `Gabel_Links_Ausgefahren` | Fork graphic left |
| `Gabel_Rechts_Ausgefahren` | Fork graphic right |
| `Gabel_Eingefahren` | Fork graphic middle |

### Step text list (WinCC text list)

Bind a text field to `HMI_State`:

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

## Screen A — OPERATE (controls)

Compact — product + buttons only. Open from Overview when Mode Hand.

| Object | Tag |
|---|---|
| Start Einlagern / Auslagern | `HMI_Start_Einlagern` / `HMI_Start_Auslagern` (Auslagern: sequencer not yet) |
| Reset / Reset Meldung | `HMI_Reset` / `HMI_Reset_Meldung` |
| Suchen / Freies Fach / Löschen | `HMI_Suchen` / `HMI_FreiesFach` / `HMI_Loeschen` |
| Fachnummer + product fields | `HMI_Fachnummer` + `Fachaktuell.*` |
| Lagerstatus text | `gldb_AktuellerFach_HMI.Lagerstatus.Lagerstatus_Text` |

Visibility: Hand product edit only in `Mode_Hand`.

---

## Screen B — SETUP

Fields: Ist/Home/Ausgabe, **Soll X/Z (manual)**, Pitch, Fachnummer, Teach / Raster / Initialisieren.  
Enable only when `Mode_Einricht`.

| Object | Tag | Notes |
|---|---|---|
| Soll X / Soll Z | `HMI_Soll_X` `%MD152` / `HMI_Soll_Z` `%MD156` | RW — exact crane target in Einricht |
| Ist → Soll | `HMI_Copy_Ist_to_Soll` `%M61.7` | Momentary — copy current Ist to Soll |
| Teach | `HMI_Pos_Speichern` `%M60.6` | Saves **Ist** to selected Fach |

While `Mode_Einricht` and not `HRL_Busy`, typed Soll values drive the crane (via `FB_Warehouse_Manual_Soll`).

---

## Build order (visual go-live)

1. Header + nav (`Overview` / `Operate` / `Setup`)  
2. Overview: rack outline + Ziel highlight + info panel + state text list  
3. Overview: pallet/fork/RFID visibility by State (pose-based, no smooth motion yet)  
4. Operate: Hand fields + Start  
5. Setup: raster teach  
6. **Rack occupancy** — 54 cells from `gldb_AktuellerFach_HMI.Lagerstatus` ([HMI_Regal_Animation.md](../../docs/03_Technik/HMI_Regal_Animation.md))  
7. Later: smooth crane from Ist_X/Z  

---

## What to skip

| Idea | Why skip now |
|---|---|
| Full 3D / video of Factory I/O | Heavy; panel already has FIO on PC |
| Animating every conveyor | Separate belt screen |
| Clicking each Fach to open detail | Nice later; use Operate Fachnummer |

---

## Operator flow

1. Land on **Overview** → see rack + process animation  
2. Need Hand product → **Operate** → Start Einlagern → back to Overview to watch  
3. Need teach → Mode Einricht → **Setup**  

This gives a clear animated warehouse without making the HMI hard to maintain.
