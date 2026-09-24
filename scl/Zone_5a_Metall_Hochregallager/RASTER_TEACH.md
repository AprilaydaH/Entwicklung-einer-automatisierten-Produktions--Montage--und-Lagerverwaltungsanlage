# Raster teach — Warehouse_2 (Metal)

Same formula as Warehouse_1. Tags use `_W2` suffix.

```
Mult_X = (Fachnummer - 1) MOD Spalten
Mult_Z = (Fachnummer - 1) DIV Spalten
Pos_X  = Basis_X + Pitch_X * Mult_X
Pos_Z  = Basis_Z + Pitch_Z * Mult_Z
```

Default: **Spalten = 6** → 54 Fächer. Stored in `gldb_LagerverwaltungData_W2.Raster`.

## Manual Soll (Einricht)

| Field | Tag | Address |
|---|---|---|
| Soll X / Z | `HMI_Soll_X_W2` / `HMI_Soll_Z_W2` | `%MD252` / `%MD256` |
| Ist → Soll | `HMI_Copy_Ist_to_Soll_W2` | `%M71.7` |
| Jog step | `HMI_Jog_Step_W2` | `%MD260` |

FB: [`FB_Warehouse_Manual_Soll_W2.scl`](FB_Warehouse_Manual_Soll_W2.scl) — after Automatik, before Stacker.

## Steps

1. Mode **Einricht** (`%M70.0`)
2. Jog to Fach 1 → `HMI_Pos_Speichern_W2` → Basis
3. Fach 2 → Pitch_X · Fach (1+Spalten) → Pitch_Z  
   **or** type `HMI_Pitch_X_W2` / `HMI_Pitch_Z_W2`
4. `HMI_Raster_Berechnen_W2` → all 54 positions + `RegalSeite`
5. Confirm online in `gldb_LagerverwaltungData_W2.Fach[n].Position_*`

Plastic reference: [`../Zone_5b_Hochregallager/RASTER_TEACH.md`](../Zone_5b_Hochregallager/RASTER_TEACH.md)
