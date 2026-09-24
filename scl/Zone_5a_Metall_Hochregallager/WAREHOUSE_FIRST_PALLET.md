# Warehouse_2 metal — make it store a pallet (now)

DB_103 already writes the tag. **Do not use DB_4 / Reader 0.** Automatik must skip State 10.

---

## 1) TIA — paste (required)

1. Open `FB_Hochregal_Automatik_Betrieb_W2` → paste body from [`Hochregal_Automatik_Betrieb_W2.scl`](Hochregal_Automatik_Betrieb_W2.scl)  
   State 0/10 must contain `ELSIF "4a_RFID_Code_Out" <> UDINT#0 THEN … #State := 20`.  
   If TIA still has `#RFID_Read_Armed AND #RFID_Gueltig` only → you will stay in **10**.
2. `RFID_Read_Write_DB_4`: `RFID_Lesen` := **FALSE**. `HMI_Reset` := `HMI_Reset_W2`.
3. Automatik call:
   - `RFID_Fehler` := **FALSE** (not `5a_RFID_Fehler`)
   - `RFID_Code` := `4a_RFID_Code_Out`
   - `RFID_Lesen` **out** → unwire
4. Gate: `RFID_Pallet_Tagged` := `4a_RFID_Done`
5. After Datenverwaltung, before Automatik:

```scl
IF "4a_RFID_Code_Out" <> UDINT#0 THEN
    "gldb_AktuellerFach_HMI_W2".Auswahl.Fachaktuell.RFID_CODE := "4a_RFID_Code_Out";
    "gldb_AktuellerFach_HMI_W2".Auswahl.Fachaktuell.Artikelnummer := "4a_RFID_Artikelnummer";
    "gldb_AktuellerFach_HMI_W2".Auswahl.Fachaktuell.Materialart := USINT#2;
END_IF;
```

Download. Pulse **`HMI_Reset_W2`**. State must be **0**, Error **FALSE**.

---

## 2) Teach (if Home/Band are 0.0)

Mode **Einricht** `%M70.0`:

| Teach | Tag |
|---|---|
| Loading pose → Fach 1 Pos speichern | `HMI_Fachnummer_W2` = 1, `HMI_Pos_Speichern_W2` |
| Pitch | Fach 2 (X), Fach 7 (Z) if Spalten = 6 |
| Raster | `HMI_Raster_Berechnen_W2` → Info_Code **17** |
| Home / Band / Lift | `Home_*_W2`, `Band_X/Z_W2`, `Band_Z_Lift_W2` ≈ 0.5 |
| Offset_Z | **0.2** (live was 0.4 — OK if taught) |

`gldb_LagerverwaltungData_W2.Fach[1].Position_X/Z` must be **≠ 0**.

---

## 3) First pallet — Hand (safest)

1. Pallet tagged at 4A: `4a_RFID_Code_Out` ≠ 0 (e.g. 260906), `4a_RFID_Done` TRUE.  
2. Pallet at metal rack: `5a_Metal_Pallet_vor_Regal` TRUE.  
3. Mode **Hand** `%M70.2`.  
4. If `Fachaktuell.RFID_CODE` is still 0, type the 4a code (or rely on the OB1 copy). Materialart **2**.  
5. Pulse **Start Einlagern** `%M71.3`.

| Watch | Pass |
|---|---|
| `HMI_State_W2` | **0 → 20 → 30 … → 80 → 0** (never 10, never 900) |
| `HMI_Ziel_Fach_W2` | ≥ 1 |
| `Fach[n].Belegt` | TRUE |
| `HRL2_Anzahl_Belegt` | +1 |
| `Info_Code` | 1 |

---

## 4) Then Auto

Mode **Auto**. Gate: sensor AND (`2a_VisionData_Combo_Done` OR `4a_RFID_Done`). Cycle starts without Start button.

---

## If it fails

| Symptom | Cause |
|---|---|
| State **10** | Old Automatik body not pasted, or `4a_RFID_Code_Out` = 0 |
| State **900** | `RFID_Fehler` still `5a_RFID_Fehler`, or warehouse full |
| Ziel = 0 in 20 | All 54 Belegt/Gesperrt — Initialisieren / Loeschen |
| Crane does not move | Home/Band/Fach positions still 0 — teach |
| Gate stays FALSE | No `4a_RFID_Done` and Combo_Done already FALSE |
