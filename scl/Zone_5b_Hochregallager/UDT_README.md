# Hochregallager — UDTs (TIA Portal)

## Rule

In TIA, a member of type **another UDT** only works if that UDT already exists.
**One file = one type** (or create them one by one in this order).

## Create order

| # | File | PLC data type | Nested members |
|---|---|---|---|
| 1 | `UDT_Fach.udt.txt` | `UDT_Fach` | — |
| 2 | `UDT_Lager_Raster.udt.txt` | `UDT_Lager_Raster` | — |
| 3 | `UDT_Lager.udt.txt` | `UDT_LagerverwaltungData` | `Raster` → `UDT_Lager_Raster` |
| 4 | `UDT_Meldungen_Status.udt.txt` | `UDT_Meldungen_Status` | — |
| 5 | `UDT_Meldungen_Fehler.udt.txt` | `UDT_Meldungen_Fehler` | — |
| 6 | `UDT_Meldungen.udt.txt` | `UDT_Meldungen` | `Status` → Status, `Fehler` → Fehler |
| 7 | `UDT_HMI_Auswahl.udt.txt` | `UDT_HMI_Auswahl` | `Fachaktuell` → `UDT_Fach` |
| 8 | `UDT_HMI_Lagerstatus.udt.txt` | `UDT_HMI_Lagerstatus` | — |
| 9 | `UDT_HMI_Meldung.udt.txt` | `UDT_HMI_Meldung` | — |
| 10 | `UDT_AktuellerFach_HMI.udt.txt` | `UDT_AktuellerFach_HMI` | Auswahl / Lagerstatus / Meldung → the three above |
| 11 | `UDT_HMI_Regal.udt.txt` | `UDT_HMI_Regal` | ARRAY 1..54 Belegt / Ziel / Farbe — **HMI occupancy map** |
| 12 | `UDT_RFID_Product.udt.txt` | optional | — |

## HMI (same nesting pattern)

1. `UDT_HMI_Auswahl` — `Fachaktuell` type = **`UDT_Fach`**
2. `UDT_HMI_Lagerstatus`
3. `UDT_HMI_Meldung`
4. `UDT_AktuellerFach_HMI` — pick the three existing types for Auswahl / Lagerstatus / Meldung
5. DB `gldb_AktuellerFach_HMI`

## Meldungen (same pattern as Raster)

1. Create **`UDT_Meldungen_Status`** (Meldecode, Meldung)
2. Create **`UDT_Meldungen_Fehler`** (Fehlercode, Fehler_Aktiv)
3. Create **`UDT_Meldungen`**
4. Members:
   - **Status** → type **`UDT_Meldungen_Status`**
   - **Fehler** → type **`UDT_Meldungen_Fehler`**
5. DB `gldb_Meldungen` of type `UDT_Meldungen`

Paths:

```
gldb_Meldungen.Status.Meldecode
gldb_Meldungen.Status.Meldung
gldb_Meldungen.Fehler.Fehlercode
gldb_Meldungen.Fehler.Fehler_Aktiv
```

## Raster in LagerverwaltungData

1. Create **`UDT_Lager_Raster`** alone
2. Create **`UDT_LagerverwaltungData`**
3. Member **Raster** → type **`UDT_Lager_Raster`**
4. DB `gldb_LagerverwaltungData`

```
gldb_LagerverwaltungData.Raster.Basis_X
gldb_LagerverwaltungData.Raster.Pitch_X
…
```

## Global DBs

| DB name | Type |
|---|---|
| `gldb_LagerverwaltungData` | `UDT_LagerverwaltungData` |
| `gldb_AktuellerFach_HMI` | `UDT_AktuellerFach_HMI` (Lagerstatus.Belegt/Farbe/Ziel[1..54] = occupancy) |
| `gldb_Meldungen` | `UDT_Meldungen` |

## Tip

In TIA structure editor: copy only members inside `STRUCT … END_STRUCT`.  
For nested members, click **Data type** → pick the **existing** UDT — do not paste another STRUCT inside.
