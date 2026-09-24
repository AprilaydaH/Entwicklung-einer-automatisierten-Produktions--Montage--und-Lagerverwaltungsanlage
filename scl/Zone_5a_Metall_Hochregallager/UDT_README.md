# Warehouse_2 (Metal) — UDTs (TIA Portal)

Mirror of Warehouse_1 UDT structure. **Same member layouts** — create types once
in a shared UDT folder **or** duplicate under `Warehouse_2` if you prefer isolation.

## Rule

Nested UDT members only work if the referenced type already exists.

## Create order (same as W1)

| # | File | PLC data type |
|---|---|---|
| 1 | `UDT_Fach.udt.txt` | `UDT_Fach` |
| 2 | `UDT_Lager_Raster.udt.txt` | `UDT_Lager_Raster` |
| 3 | `UDT_Lager.udt.txt` | `UDT_LagerverwaltungData` |
| 4 | `UDT_Meldungen_Status.udt.txt` | `UDT_Meldungen_Status` |
| 5 | `UDT_Meldungen_Fehler.udt.txt` | `UDT_Meldungen_Fehler` |
| 6 | `UDT_Meldungen.udt.txt` | `UDT_Meldungen` |
| 7 | `UDT_HMI_Auswahl.udt.txt` | `UDT_HMI_Auswahl` |
| 8 | `UDT_HMI_Lagerstatus.udt.txt` | `UDT_HMI_Lagerstatus` |
| 9 | `UDT_HMI_Meldung.udt.txt` | `UDT_HMI_Meldung` |
| 10 | `UDT_AktuellerFach_HMI.udt.txt` | `UDT_AktuellerFach_HMI` |
| 11 | `UDT_HMI_Regal.udt.txt` | `UDT_HMI_Regal` |
| 12 | `UDT_RFID_Product.udt.txt` | optional |

If W1 already has these types in the PLC, **reuse them** — only create new **global DBs**.

## Global DBs (Warehouse_2 — must be unique)

| DB name | Type |
|---|---|
| `gldb_LagerverwaltungData_W2` | `UDT_LagerverwaltungData` |
| `gldb_AktuellerFach_HMI_W2` | `UDT_AktuellerFach_HMI` (Lagerstatus occupancy arrays) |
| `gldb_Meldungen_W2` | `UDT_Meldungen` |

Do **not** share plastic DBs (`gldb_LagerverwaltungData` without `_W2`).

## Tip

Copy members from `STRUCT … END_STRUCT` only. Nested fields → pick existing UDT type.
