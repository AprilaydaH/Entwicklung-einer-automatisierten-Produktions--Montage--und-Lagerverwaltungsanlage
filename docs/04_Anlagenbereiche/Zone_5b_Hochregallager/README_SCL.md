# Hochregallager — SCL

## Plastic warehouse go-live (use this first)

| File | Role |
|---|---|
| **`OB1_Plastic_Warehouse.scl`** | Vision → RFID → Hochregal (complete OB1) |
| **`PLASTIC_WAREHOUSE_GOLIVE.md`** | Checklist + test |
| **`RASTER_TEACH.md`** | Teach Fach 1 + pitch → all 54 slots |
| `PLC_Tags_Hochregallager.csv` | HMI + crane tags (import to TIA) |
| `../RFID/PLC_Tags_RFID.csv` | Vision + RFID tags |

Metal warehouse = later (second instance + DB set).

## Main FB (Hochregal only OB1)

| File | Role |
|---|---|
| **`FB_Hochregallager.scl`** | One FB — modes, HMI, Automatik, RFID, raster |
| `OB1_Hochregallager.scl` | Thin OB1 → instance `FB_Hochregallager_DB` |

### Inside `FB_Hochregallager` (multi-instance)

1. `FB_Datenverwaltung_Lager` (+ `FB_Berechn_Offset` as child STAT)
2. `FB_Loeschen` / `FB_Suchen` / `FB_Freies_Fach_Suchen` (HMI)
3. `Hochregal_Automatik_Betrieb` (Einlagern / Auslagern / …)
4. `FB_Meldung` (last)

### TIA import order

1. `UDT_Fach`, `UDT_Lager_Raster`, `UDT_LagerverwaltungData` — see [`UDT_README.md`](../../../scl/Zone_5b_Hochregallager/UDT_README.md)
2. Global DBs: `gldb_LagerverwaltungData`, `gldb_AktuellerFach_HMI`, `gldb_Meldungen`
3. **`FB_Berechn_Offset`**
4. Child FBs (`FB_Einlagern`, `FB_Auslagern`, …)
5. `Hochregal_Automatik_Betrieb`
6. **`FB_Datenverwaltung_Lager`** — add V1.3 pins per `FB_Datenverwaltung_Lager_LocalVars.csv`
7. **`FB_Hochregallager`**
8. Instance DB `FB_Hochregallager_DB`
9. Paste OB1 (`OB1_Plastic_Warehouse.scl` or `OB1_Hochregallager.scl`)

### RFID

Wire `FB_RFID_ReadWrite` into:

`RFID_Bereit`, `RFID_Gueltig`, `RFID_Fehler`, `RFID_Artikelnummer`, `RFID_Materialart`, `RFID_ProduktTyp`, `RFID_Code`

Output `RFID_Lesen` → RFID reader request.

### Raster teach (Einricht)

1. Pos speichern at **Fach 1** (basis), **Fach 2** (Pitch_X), **Fach 7** if Spalten=6 (Pitch_Z)
2. Pulse **`HMI_Raster_Berechnen`** → all `Fach[1..54].Position_X/Z`

See [`RASTER_TEACH.md`](../../../scl/Zone_5b_Hochregallager/RASTER_TEACH.md).

## Other files

| File | Baustein |
|---|---|
| `FB_Berechn_Offset.scl` | Fanuc-style MOD/DIV offset |
| `UDT_*.udt.txt` | Fach / HMI / Lager |
| `FB_Auslagern.scl` / `FB_Einlagern.scl` / … | Sub-FBs |
| `Hochregal_Automatik_Betrieb.scl` | State machine |
| `legacy/OB1_Main_LEGACY.scl` | **Archiv** — flat OB1 (replaced) |

Globals: `gldb_LagerverwaltungData`, `gldb_AktuellerFach_HMI`, `gldb_Meldungen`.  
Folder index: [`README.md`](../../../scl/Zone_5b_Hochregallager/README.md) · [`scl/README.md`](../../../scl/README.md)
