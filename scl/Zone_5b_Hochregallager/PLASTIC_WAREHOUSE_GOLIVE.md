# Plastic warehouse — go-live (finish this first)

**Gesamtanlage:** [Gesamtanlage.md](../../docs/01_Projektgrundlagen/Gesamtanlage.md)  
**SCL index:** [scl/README.md](../../scl/README.md)

Metal warehouse comes **later**. Use **Warehouse_1** only. Leave **Warehouse_2** collapsed.

## TIA folder map (your project tree)

```
Warehouse_Management
├── Warehouse_1     ← PLASTIC go-live (NW 29)
├── Warehouse_2     ← METAL scaffold (NW 28)
│   ├── 01_Daten
│   ├── 02_Lagerverwaltung
│   └── 03_Automatik_Betrieb
└── Warehouse_2     ← METAL later — do not change yet
```

| TIA (Warehouse_1) | Repo / role |
|---|---|
| `01_Daten` / `gldb_LagerverwaltungData` | 54 Fächer + Raster |
| `01_Daten` / `gldb_AktuellerFach_HMI` | HMI current slot |
| `01_Daten` / `gldb_Meldungen` | Status / error codes |
| `01_Daten` / `gldb_FactoryIO_IO` | **Legacy I/O DB — do not use for RFID** |
| `02_Lagerverwaltung` / `FB_Einlagern` … `FB_Suchen` | Keep; Automatik calls these as instances |
| `02_Lagerverwaltung` / `FC_Berechn_Offset` **[FB30]** | Same as repo `FB_Berechn_Offset` |
| `03_Automatik_Betrieb` / `Hochregal_Automatik_Betrieb` | **Paste V1.4 here** (main sequencer) |
| Instance DBs next to FBs (`FB_Loeschen_DB`, Automatik DB, …) | Keep your instances — no need for `FB_Hochregallager` wrapper |

You already call **Datenverwaltung + Automatik as separate FBs**. That is valid. `FB_Hochregallager.scl` is only an optional one-call wrapper; do **not** add it if Warehouse_1 already runs that way.

## End-to-end flow

**Automatic warehouse (no Start button):** [`WAREHOUSE_AUTO_START.md`](WAREHOUSE_AUTO_START.md)

```
Lid MC Vision ──┐
                ├→ FB_VisionReader_Plastic → Artikelnummer / Material / Color / RFID_CODE
Base MC Vision ─┘              │
                               ▼  when **4b Done** (palletizer finished)
                    RFID WRITE on pallet (4b Reader 2)
                               │
                               ▼  Vision_Combo_Done OR RFID_Pallet_Tagged
                    … convey to warehouse …
                               ▼
                    Gate: Paket_Vor_Regal AND tagged
                               ▼
                    Automatik → optional Reader 5 READ → Einlagern
```

Start signal: palletizer tag **`4b_Done(1)`** (`%M10.0`) → Vision `Allow_Write`.  
Example: [`OB1_RFID_at_PickPlace.scl`](../Zone_4b_Kunststoff_Palletizer_RFID/OB1_RFID_at_PickPlace.scl)


## OB1

In **Main OB1**, keep your existing Warehouse_1 calls (Datenverwaltung + `Hochregal_Automatik_Betrieb` instance). Add **in front** of them:

1. `FB_VisionReader_Plastic`
2. `RFID_Read_Write_DB_1`
3. Gate: `Paket_Fuer_Hochregal := Paket_Vor_Regal AND (Vision_Combo_Done OR RFID_Pallet_Tagged)`
4. Existing Warehouse_1 Automatik — wire `Paket_Vor_Regal` **from the gate**, RFID pins from the RFID FB (`RFID_Lesen` out → `RFID_Lesen` in)

Full example (wrapper style): [`OB1_Plastic_Warehouse.scl`](OB1_Plastic_Warehouse.scl) — if you do **not** use `FB_Hochregallager_DB`, copy only the Vision + RFID + gate networks and keep your current Automatik call.

## TIA updates (v1.4 Automatik / RFID v1.3)

| Task | Detail |
|---|---|
| `Hochregal_Automatik_Betrieb` | Paste **V4.1**; STAT: `RFID_Read_Armed`, `Akt_*`, `i`; multi-inst. `instEinlagern` … |
| `FB_RFID_ReadWrite` | Paste v1.3 (write copies In→Out; `Pallet_Tagged`) |
| Wire `Pallet_Tagged` | → tag `RFID_Pallet_Tagged` |
| Wire `Write_Preview` | → tag `RFID_Write_Preview` (optional HMI) |

## TIA checklist

**Setup guide (connections):** [`WAREHOUSE_1_SETUP.md`](WAREHOUSE_1_SETUP.md) — pin wiring from your TIA export  
**Tags:** `PLC_Tags_Hochregallager.csv` (M60+) + `PLC_Tags_Warehouse_1_FIO.csv` + `PLC_Tags_RFID_5b.csv`  
**I/O glue:** [`OB1_Warehouse_1_IO.scl`](OB1_Warehouse_1_IO.scl)  
**UDTs:** follow [`UDT_README.md`](UDT_README.md) — **`UDT_Fach` is required**

| # | Task | Done |
|---|---|---|
| 1 | Create UDTs in order (Fach → Raster → Lager → Meldungen → HMI) | ☐ |
| 2 | Global DBs: `gldb_LagerverwaltungData`, `gldb_AktuellerFach_HMI`, `gldb_Meldungen` | ☐ |
| 3 | Import FBs: `FB_Berechn_Offset` → child FBs → `FB_Hochregallager` | ☐ |
| 4 | Instance `FB_Hochregallager_DB` + Vision/RFID instances | ☐ |
| 5 | Paste `OB1_Plastic_Warehouse.scl` | ☐ |
| 6 | Vision both = **All Numerical** → `Vision_Lid_Value`, `Vision_Base_Value` | ☐ |
| 7 | RFID 4b write: `%ED130/134/138`, Exec `%A11.1`, `%AD104/108/112` | ☐ |
| 8 | Import stacker + Reader 5 FIO tags; paste `OB1_Warehouse_1_IO.scl` | ☐ |
| 9 | Automatik: RFID from Reader 5 FB; `Ziel_Fachnummer_Out` → `%MW130` | ☐ |
| 10 | Fix `5b_RFID_Lesen` `%M0.0` → `%M65.0`; Datenverwaltung `Einricht_Mode` → `%M60.0` | ☐ |
| 11 | Factory I/O: crane setpoints, fork limits, Home/Ausgabe teach | ☐ |
| 12 | Raster: Fach 1 + pitch → `HMI_Raster_Berechnen` ([`RASTER_TEACH.md`](RASTER_TEACH.md)) | ☐ |
| 13 | Mode Auto + Not_Aus OFF → test Einlagern | ☐ |

## Commissioning order (make warehouse move first)

### A — Crane + DB only (no Vision)

1. Mode **Einricht** → teach Fach 1 + pitch → **Raster berechnen**  
2. Set `gldb_AktuellerFach_HMI.Auswahl.Fachaktuell`: `RFID_CODE`, `Artikelnummer`, `Materialart=1`, `ProductTyp`, `Color_Code`  
3. Mode **Hand** → **Start Einlagern** (skips RFID if `RFID_CODE <> 0`)  
4. Confirm crane sequence and `Fach[n].Belegt = TRUE`

### B — Full plastic E2E

1. Vision: lid + base → `Vision_Both_Ready`  
2. Pallet at reader → write → `Vision_Combo_Done` / `RFID_Pallet_Tagged`  
3. If `Status_Code = 10`: HMI Reset; check FIO Execute/Command_ID addresses (CmdID must increment)  
4. Mode **Auto** → State 10 read → free Fach → Einlagern → Home  
5. Verify `gldb_LagerverwaltungData.Fach[n]`: `Materialart=1`, `Color_Code`, `Artikelnummer`, `RFID_CODE`, `Belegt=TRUE`

## Watch online

| Tag / value | Meaning |
|---|---|
| `HMI_State` | 10=RFID, 20=search, 22–90=motion, 300=home, 900=error |
| `RFID_Status_Code` | 0=OK, 1=no tag, **10=timeout** (Command ID stuck) |
| `RFID_Pallet_Tagged` | Write OK — gate may open |
| `Paket_Fuer_Hochregal` | Auto start condition |
| `HRL_Anzahl_Belegt` / `Frei` | After Einlagern |

## Do not do yet

- Second warehouse / metal DBs  
- `OB1_RFID_Metal.scl`  
- Files under `legacy/` folders
