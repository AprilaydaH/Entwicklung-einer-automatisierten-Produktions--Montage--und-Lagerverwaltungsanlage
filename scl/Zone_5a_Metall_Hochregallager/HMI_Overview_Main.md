# HMI — Warehouse_2 Metal · MAIN PAGE (Overview)

**Panel:** Siemens TP · start screen after login: **Overview**  
**Folder:** `Warehouse_2` (do not share objects with Warehouse_1)  
**Tags:** [`HMI_Tags_Warehouse_2.csv`](HMI_Tags_Warehouse_2.csv)

All command buttons = **momentary** (Press SetBit / Release ResetBit).

**RFID on this page = palletizer write (DB_103 / Reader 1), not warehouse Reader 0.**

```
HEADER (always)     Mode_W2 · Busy/Done/Error · Step text · STOP
NAV                 Overview * | Operate | Setup
```

---

## Header (permanent, all screens)

| Object | Type | Tag | Appearance |
|---|---|---|---|
| Einricht | Radio / Button | `Mode_Einricht_W2` `%M70.0` | SetBit on press |
| Auto | Radio / Button | `Mode_Auto_W2` `%M70.1` | |
| Hand | Radio / Button | `Mode_Hand_W2` `%M70.2` | |
| Not-Aus | Circle lamp | `Not_Aus_W2` `%M70.3` | Red when TRUE |
| Busy | Circle lamp | `HRL2_Busy` `%M74.0` | Yellow |
| Done | Circle lamp | `HRL2_Done` `%M74.1` | Green |
| Error | Circle lamp | `HRL2_Error` `%M74.2` | Red |
| Step | IOField + **text list** | `HMI_State_W2` `%MW228` | See list below |
| STOP | Button large | `HMI_Stop_W2` `%M71.6` | Red, momentary |
| Reset | Button | `HMI_Reset_W2` `%M71.5` | Momentary — leave State 900 / 10 |

Mode radios: PLC `FB_Warehouse_Mode_Select_W2` pins **IN_OUT**.

### Text list `HMI_State_W2`

| Value | Text |
|---:|---|
| 0 | Bereit — warte auf Palette |
| 10 | Warte auf RFID Hochregal (überspringen — nutze 4a) |
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
| 900 | Störung — Reset drücken |

---

## Overview layout (main page)

```
┌──────────────────────────────────────────────────────────────────────────┐
│  HEADER  Einricht Auto Hand │ Busy Done Error │ Step text │ RESET STOP  │
├────────────────────────────────────┬─────────────────────────────────────┤
│                                    │  PRODUCT (from DB_103 write)        │
│   LOADING                          │  RFID_CODE      4a_RFID_Code_Out    │
│   ▭ pallet when Paket_Vor_Regal    │  Artikel        4a_RFID_Artikel…    │
│                                    │  Materialart    2 = Metall          │
│   ┌──┬──┬──┬──┬──┬──┐              │                                     │
│   │  │  │  │  │  │  │  Ziel flash  │  PROCESS                            │
│   ├──┼──┼──┼──┼──┼──┤              │  Ziel-Fach      HMI_Ziel_Fach_W2    │
│   │  │  │  │  │  │  │              │  Belegt / Frei  HRL2_Anzahl_*       │
│   ├──┼──┼──┼──┼──┼──┤  CRANE       │  Info_Text      gldb … Info_Text    │
│   │  │  │  │  │  │  │  fork L/M/R  │                                     │
│   └──┴──┴──┴──┴──┴──┘              │  GATE                               │
│        RACK 6 × 9                  │  Pallet at rack    Paket_Vor_Regal  │
│   Ist X / Z                        │  Gate open         Paket_Fuer_HRL   │
│                                    │  4a write Done     4a_RFID_Done     │
│                                    │  Tag at 4a         4a_RFID_Tag_Pres.│
└────────────────────────────────────┴─────────────────────────────────────┘
```

No Start on Overview (use **Operate**). Header Reset/Stop stay visible.

---

## Right panel — bind these first

### Product (DB_103 / Reader 1)

| HMI object | Tag | Access |
|---|---|---|
| IO RFID_CODE | `4a_RFID_Code_Out` `%MD236` | R |
| IO Artikel | `4a_RFID_Artikelnummer` `%MW150` | R |
| IO Material | constant text **Metall** or `Fachaktuell.Materialart` | R |
| Lamp 4a Done | `4a_RFID_Done` `%M21.1` | R green |
| Lamp Tag present | `4a_RFID_Tag_Present` `%M21.3` | R |

If `RFID_CODE` = 0, pallet is **not** tagged yet — Auto will stick in State 10.

### Process

| HMI object | Tag |
|---|---|
| IO Ziel-Fach | `HMI_Ziel_Fach_W2` `%MW230` |
| IO Belegt | `HRL2_Anzahl_Belegt` `%MW232` |
| IO Frei | `HRL2_Anzahl_Frei` `%MW234` |
| IO Info_Text | `gldb_AktuellerFach_HMI_W2.Meldung.Info_Text` |
| IO Info_Code | `gldb_AktuellerFach_HMI_W2.Meldung.Info_Code` |
| IO Ist_X | `Ist_X_W2` `%MD196` format `0.00` |
| IO Ist_Z | `Ist_Z_W2` `%MD200` format `0.00` |

### Gate / crane

| HMI object | Tag | Show |
|---|---|---|
| Lamp pallet at rack | `Paket_Vor_Regal_W2` `%M72.0` | Loading pallet graphic |
| Lamp gate | `Paket_Fuer_Hochregal_W2` `%M72.1` | Gate open |
| Lamp pallet on fork | `Palette_Aufgenommen_W2` `%M72.2` | |
| Lamp fork left | `Gabel_Links_Ausgefahren_W2` `%M72.6` | |
| Lamp fork right | `Gabel_Rechts_Ausgefahren_W2` `%M72.5` | |
| Lamp fork middle | `Gabel_Eingefahren_W2` `%M72.7` | |

**Do not** put `5a_RFID_Fehler` / `5a_RFID_Gueltig` on this page (Reader 0 unused).

---

## Left — rack + crane

1. Draw rack **6 × 9** with Fach numbers as in [`HMI_Regal_Animation.md`](../../docs/03_Technik/HMI_Regal_Animation.md).  
2. Cell fill: `gldb_AktuellerFach_HMI_W2.Lagerstatus.Farbe[n]` (Range 0 grey / 4 steel for metal). Tags: [`HMI_Tags_Rack_W2.csv`](HMI_Tags_Rack_W2.csv).  
3. Ziel overlay: visibility `gldb_AktuellerFach_HMI_W2.Lagerstatus.Ziel[n]` (flashing yellow border).  
4. Crane: 4 poses by `HMI_State_W2` (no pixel motion yet):

| State | Pose |
|---|---|
| 0, 80 | Home |
| 10, 20, 30–42 | Loading |
| 50–58 | At slot |
| 70 | Travel home |
| 900 | Red overlay + Info_Text |

Fork: three graphics, visibility from `Gabel_Links_*` / `Gabel_Rechts_*` / `Gabel_Eingefahren_W2`.

---

## WinCC events (header)

| Button | Event |
|---|---|
| Einricht / Auto / Hand | SetBit that mode tag |
| STOP | Press SetBit `HMI_Stop_W2`, Release ResetBit |
| Reset | Press SetBit `HMI_Reset_W2`, Release ResetBit |
| Overview / Operate / Setup | ChangeScreen |

---

## Pass on this page (online)

| Watch | Pass |
|---|---|
| `4a_RFID_Code_Out` | 260906 (or current YYMMDD) after DB_103 write |
| `4a_RFID_Done` | TRUE |
| `HMI_State_W2` | 0 after Reset (not 10, not 900) |
| `HMI_Ziel_Fach_W2` | ≥ 1 once cycle reaches state 20 |
| Occupied cell | `gldb_AktuellerFach_HMI_W2.Lagerstatus.Farbe[n]` ≠ 0 after Einlagern |
| `HRL2_Error` | FALSE |
| `Paket_Fuer_Hochregal_W2` | TRUE when pallet at `%E15.0` and (`Combo_Done` or `4a_RFID_Done`) |

If State stays **10**: product not on `Fachaktuell` / skip not downloaded — still use this page to confirm `4a_RFID_Code_Out` ≠ 0, then Reset.

---

## Next screens (not this page)

| Screen | When |
|---|---|
| **Operate** | Hand Start Einlagern, product IO, Suchen / Freies Fach |
| **Setup** | Einricht jog, Pos speichern, Raster |

Operate / Setup field lists: same file below in [`HMI_Warehouse_2.md`](HMI_Warehouse_2.md) Operate/Setup sections — keep this Overview as the default.
