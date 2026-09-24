# Raster teach — one pallet slot → all 54

**Gesamtanlage:** [Gesamtanlage.md](../../docs/01_Projektgrundlagen/Gesamtanlage.md)

Same idea as Fanuc `BERECHN_OFFSET`: measure **one** rest pose + bay/level pitch, then apply MOD/DIV to every Fach.

## Formula

```
Mult_X = (Fachnummer - 1) MOD Spalten
Mult_Z = (Fachnummer - 1) DIV Spalten
Pos_X  = Basis_X + Pitch_X * Mult_X
Pos_Z  = Basis_Z + Pitch_Z * Mult_Z
```

Default: **Spalten = 6** → 9 levels × 6 columns = **54**. Change `Spalten` if your Factory I/O numbering is different.

## Manual Soll X/Z (Setup screen)

In **Mode Einricht**, when Automatik is **not Busy**, type exact targets on HMI:

| Field | Tag | Address |
|---|---|---|
| Soll X | `HMI_Soll_X` | `%MD152` |
| Soll Z | `HMI_Soll_Z` | `%MD156` |
| Ist → Soll | `HMI_Copy_Ist_to_Soll` | `%M61.7` (momentary) |

PLC network: [`FB_Warehouse_Manual_Soll.scl`](FB_Warehouse_Manual_Soll.scl) — must run **after** Automatik, **before** Stacker IO.

Crane follows `%MD152/156` → `Soll_X/Z` → Factory I/O setpoints. Use **Ist → Soll** to snap current pose, nudge values, then **Teach** (Pos speichern).

## Einricht steps

1. **Mode Einricht**
2. Jog with **Soll X/Z** (or Factory I/O) to **Fach 1** (pallet rest) → **Teach** / `HMI_Pos_Speichern`  
   → stores `Fach[1]` and `Raster.Basis_X/Z`
3. Get pitch (pick one):
   - **A)** Drive to **Fach 2** → Pos speichern → auto `Pitch_X`  
      Drive to **Fach (1+Spalten)** e.g. Fach 7 if Spalten=6 → Pos speichern → auto `Pitch_Z`  
   - **B)** Enter `Pitch_X` / `Pitch_Z` on HMI (distance between bays / levels)
4. Pulse **`HMI_Raster_Berechnen`** → all `Fach[1..54].Position_X/Z` (+ `RegalSeite`)

## Files

| File | Role |
|---|---|
| `FB_Datenverwaltung_Lager.scl` | Teach + fill loop (**inline** raster math, no `instOffset`) |
| `FB_Berechn_Offset.scl` | Optional standalone FB — not required if you use V1.4 Datenverwaltung |
| `UDT_Lager.udt.txt` | `Raster` struct in `gldb_LagerverwaltungData` |

## TIA checklist

1. Import `FB_Berechn_Offset`
2. Add `Raster` to `UDT_LagerverwaltungData` / update DB
3. On `FB_Datenverwaltung_Lager`: add inputs per `FB_Datenverwaltung_Lager_LocalVars.csv`
4. On `FB_Hochregallager`: wire `HMI_Raster_Berechnen` (+ optional pitch tags)
5. Import `PLC_Tags_Hochregallager.csv` — HMI button: Raster berechnen (Einricht only)

Info_Code **17** = raster applied. Fehlercode **103** = raster denied (not Einricht).
