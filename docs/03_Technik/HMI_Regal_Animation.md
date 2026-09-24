# HMI — Hochregal occupancy animation (54 Fächer)

**WinCC Comfort · TP2200 · Overview Warehouse_1 and Warehouse_2**

PLC copies occupancy every scan in `FB_Datenverwaltung_Lager` / `_W2` into the **HMI DB you already have** (`gldb_AktuellerFach_HMI.Lagerstatus`). No extra occupancy DB.

| Warehouse | Bind these | Filled by |
|---|---|---|
| **1** Kunststoff 5B | `gldb_AktuellerFach_HMI.Lagerstatus.Farbe[n]` | `FB_Datenverwaltung_Lager` |
| **2** Metall 5A | `gldb_AktuellerFach_HMI_W2.Lagerstatus.Farbe[n]` | `FB_Datenverwaltung_Lager_W2` |

TIA: add `Belegt` / `Ziel` / `Farbe` arrays to **`UDT_HMI_Lagerstatus`** (see `UDT_HMI_Lagerstatus.udt.txt`), compile, download the HMI DB.

Watch **online** after a booking: `gldb_LagerverwaltungData(_W2).Fach[n].Belegt` and `Lagerstatus.Anzahl_Belegt` — not `Fachaktuell` (that is only the selected slot).

---

## What the operator sees

| Cell | Meaning |
|---|---|
| Light grey | **Frei** (`Farbe = 0`) |
| Blue / green / amber | **Belegt** Kunststoff (`Farbe` 1 / 2 / 3) |
| Steel blue | **Belegt** Metall or no colour (`Farbe = 4`) |
| Red | **Gesperrt** (`Farbe = 5`) |
| Yellow flashing border | Cycle **Ziel-Fach** (`Ziel[n] = TRUE`) |

Counts on the right panel stay `HRL_Anzahl_Belegt` / `HRL_Anzahl_Frei` (W2: **`HRL_2_Anzahl_*`**, not `HRL2_*`). Occupancy bytes: W1 `%MB400`, W2 **`HRL_2_Occ_*` `%MB407`**.

---

## Grid numbering (6 columns × 9 levels)

Same formula as raster teach: `Fach = 1 + col + level × 6` with `col` 0…5, `level` 0…8. Draw **level 8 at the top**, **level 0 at the bottom**.

```
 Z↑  49 50 51 52 53 54     level 8
     43 44 45 46 47 48     level 7
     37 38 39 40 41 42
     31 32 33 34 35 36
     25 26 27 28 29 30
     19 20 21 22 23 24
     13 14 15 16 17 18
      7  8  9 10 11 12     level 1
      1  2  3  4  5  6     level 0  (loading)
         col →
```

Object names: `Fach_01` … `Fach_54` (two digits). Overlay: `Fach_01_Ziel` … (copy of the same rectangle, no fill, thick border).

---

## WinCC — build one cell, then duplicate

### 1) Rectangle `Fach_01`

1. Draw a small rectangle (e.g. 28 × 18 px).
2. **Animations → Appearance → Fill color** (or *Background color*).
3. Tag: `gldb_AktuellerFach_HMI.Lagerstatus.Farbe[1]` (W2: `gldb_AktuellerFach_HMI_W2.Lagerstatus.Farbe[1]`).
4. Type: **Range** / *Value table* (not Bool).

| Value | Fill | Name |
|---:|---|---|
| 0 | `#E6E6E6` | Frei |
| 1 | `#4A90D9` | Blau |
| 2 | `#2E8B57` | Grün |
| 3 | `#E6A817` | Mixed |
| 4 | `#5B7C99` | Metall |
| 5 | `#C0392B` | Gesperrt |

5. Optional **Click → SetValue**: `HMI_Fachnummer` := `1` (W2: `HMI_Fachnummer_W2`). Then Operate shows that slot.

**Simple 2-colour fallback** (if Range is awkward): Appearance on `gldb_AktuellerFach_HMI.Lagerstatus.Belegt[1]` — FALSE grey, TRUE steel blue. Skip `Farbe`.

### 2) Overlay `Fach_01_Ziel`

1. Copy the rectangle, send to front, fill **transparent**, border **3 px yellow**.
2. **Animations → Visibility** → `gldb_AktuellerFach_HMI.Lagerstatus.Ziel[1]`.
3. Enable **Flashing** when visible (Properties → Flashing).

### 3) Duplicate 53 times

1. Copy `Fach_01` + `Fach_01_Ziel`.
2. Place according to the grid (or copy a whole row of 6, then 8 more rows).
3. For each copy: change `[1]` → `[n]` in **both** animations, and SetValue to `n`.
4. Tag list to import: [`HMI_Tags_Rack_W1.csv`](../../scl/Zone_5b_Hochregallager/HMI_Tags_Rack_W1.csv) / [`HMI_Tags_Rack_W2.csv`](../../scl/Zone_5a_Metall_Hochregallager/HMI_Tags_Rack_W2.csv).

Do **not** bind `gldb_LagerverwaltungData.Fach[n].Belegt` on the 54 cells.

---

## PLC (already in Datenverwaltung)

Each scan:

- `Belegt[n]` ← `Fach[n].Belegt`
- `Farbe[n]` ← 0 if free, else Color_Code 1…3, else 4, or 5 if `Gesperrt`
- `Ziel[n]` ← `n = HMI_Ziel_Fach` (`_W2` on metal)

No extra OB1 call. After Einlagern / Löschen / Suchen the map updates on the next cycle.

### TIA import

1. Update `UDT_HMI_Lagerstatus` with the three arrays (Belegt, Ziel, Farbe).
2. Compile / download `gldb_AktuellerFach_HMI` and `_W2`.
3. Paste **Datenverwaltung V1.5** (occupancy loop + copy only when `HMI_Fachnummer` changes).
4. Add STAT `Last_HMI_Fach : UInt` on W1 if missing.
5. Online: `gldb_LagerverwaltungData(_W2).Fach[n].Belegt` = TRUE after Einlagern; `Lagerstatus.Anzahl_Belegt` ≥ 1.

---

## Check on the panel

| Action | Expected |
|---|---|
| Empty warehouse | All cells grey, Frei = 54 |
| Hand Einlagern Fach 7 | `Fach_07` coloured, Belegt = 1 |
| Auto cycle | Target border flashes on `HMI_Ziel_Fach`, then that cell fills at State 60 |
| Löschen Fach 7 | Cell grey again |
| Click `Fach_12` | `HMI_Fachnummer` = 12, Operate shows that record |
