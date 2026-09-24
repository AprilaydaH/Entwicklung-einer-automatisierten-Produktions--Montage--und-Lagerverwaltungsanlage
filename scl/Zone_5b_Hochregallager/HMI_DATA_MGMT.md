# Data management + HMI — post Einlagern

Mechanical **Auto Einlagern** works (V5.6). This guide wires **DB bookkeeping**, **operator messages**, and **WinCC screens**.

**Related:** [`HMI_Warehouse_1.md`](HMI_Warehouse_1.md) · [`HMI_Tags_Warehouse_1.csv`](HMI_Tags_Warehouse_1.csv) · [`WAREHOUSE_1_SETUP.md`](WAREHOUSE_1_SETUP.md) · [`INFO_CODES.md`](../../docs/04_Anlagenbereiche/Zone_5b_Hochregallager/INFO_CODES.md)

---

## 1) What happens today (PLC)

```
Automatik state 60
  → fill gldb_AktuellerFach_HMI.Auswahl.Fachaktuell (RFID + product + position)
  → instEinlagern (FB_Einlagern) → gldb_LagerverwaltungData.Fach[n].Belegt := TRUE
  → instLagerstatus → counts + Lagerstatus_Text in DB
```

| FB | Called from | Purpose |
|---|---|---|
| `FB_Datenverwaltung_Lager` | OB1 NW4 | Slot mirror, teach, raster, live counts |
| `FB_Einlagern` | Automatik `instEinlagern` @ state **60** | Persist pallet to `Fach[n]` |
| `FB_Lagerstatus` | Automatik after Einlagern | Refresh `Anzahl_Belegt/Frei` in DB |
| `FB_Meldung` | OB1 (after Lager FBs) | `Info_Code` → `Info_Text` |
| `FB_Suchen` | OB1 `instSuchen` | Find slot by RFID / Artikel / Fach |
| `FB_Freies_Fach_Suchen` | OB1 `instFreiesFach` | Next free slot → `Fachaktuell` |
| `FB_Loeschen` | OB1 `instLoeschen` | Clear DB record (Hand/Einricht) |

---

## 2) OB1 — add these networks (TIA)

Place **after** NW4 Datenverwaltung, **before or after** Automatik as noted.

### NW 4 — Datenverwaltung (extend wiring)

| Pin | Tag |
|---|---|
| OUT `Anzahl_Belegt` | `HRL_Anzahl_Belegt` `%MW132` |
| OUT `Anzahl_Frei` | `HRL_Anzahl_Frei` `%MW134` |
| IN `Raster_Berechnen` | `HMI_Raster_Berechnen` |
| IN `Pitch_X/Z`, `Spalten`, `Spalten_Rechts` | `%MD84`, `%MD88`, `%MW92`, `%MW94` |

Counts are also written to `gldb_AktuellerFach_HMI.Lagerstatus` every scan.

### NW 4b — HMI data commands (multi-instances in Datenverwaltung DB or OB1)

```scl
"instLoeschen"(Execute := "HMI_Loeschen" AND ("Mode_Hand" OR "Mode_Einricht"));

IF "HMI_Suchen" THEN
    "instSuchen"();
END_IF;

"instFreiesFach"(Start := "HMI_FreiesFach");
```

| Button | Tag | Mode | Effect |
|---|---|---|---|
| Löschen | `HMI_Loeschen` `%M61.0` | Hand / Einricht | Clears selected slot in DB |
| Suchen | `HMI_Suchen` `%M61.1` | Any | Search using `Fachaktuell` RFID / Artikel / Fach |
| Freies Fach | `HMI_FreiesFach` `%M61.2` | Any | Puts next free slot into `Fachaktuell` |

After **Loeschen** or **Auslagern**, call `instLagerstatus()` once (legacy pattern) or rely on Datenverwaltung counts next scan.

### NW 10 — Messages (last among Lager blocks)

```scl
"instMeldung"();
```

`FB_Meldung` reads `gldb_AktuellerFach_HMI.Meldung.Info_Code` and fills `Info_Text`.

**Success after Auto Einlagern:** `Info_Code = 1` → *Einlagerung erfolgreich*

---

## 3) Verify DB after one Auto cycle

| Check | Expected |
|---|---|
| `gldb_LagerverwaltungData.Fach[n].Belegt` | `TRUE` for stored slot |
| `…Fach[n].RFID_CODE` | Matches pallet |
| `HRL_Anzahl_Belegt` / `HRL_Anzahl_Frei` | e.g. `1` / `53` |
| `HMI_Ziel_Fach` `%MW130` | Same `n` as booked slot |
| `Info_Code` / `Info_Text` | `1` / Einlagerung erfolgreich |
| `HRL_Done` | Brief pulse at state **80** |

Online: open `gldb_LagerverwaltungData` → Fach array → find `Belegt = true`.

---

## 4) HMI build order (after Einlagern works)

### Phase 1 — confirm data (1–2 h)

1. **Header** — modes, Busy/Done/Error, `HMI_State`, STOP  
2. **Overview — info panel** — `HMI_Ziel_Fach`, `HRL_Anzahl_Belegt/Frei`, `Info_Text`  
3. **Operate — read-only** — show booked `Fachaktuell.*` after cycle  

### Phase 2 — data tools

4. **Operate — Fachnummer** `%MW80` — browse slots (Datenverwaltung mirrors DB → `Fachaktuell`)  
5. **Suchen / Freies Fach / Löschen** buttons (momentary)  
6. **Reset Meldung** `%M60.5` — clear message line  

### Phase 3 — visual rack

7. 54 cells: fill `gldb_AktuellerFach_HMI.Lagerstatus.Farbe[n]`, Ziel `gldb_AktuellerFach_HMI.Lagerstatus.Ziel[n]`  
   Guide: [`docs/03_Technik/HMI_Regal_Animation.md`](../../docs/03_Technik/HMI_Regal_Animation.md)  

### Defer

- **Start Auslagern** — no Auslagern sequencer in Automatik V5.6 yet  
- Smooth crane animation from `Ist_X/Z`  

---

## Web search (no PLC change)

Browser search of 54 slots (SQLite copy, not live `gldb_LagerverwaltungData`):  
[`docs/03_Technik/Lagerverwaltung_Online.md`](../../docs/03_Technik/Lagerverwaltung_Online.md)  

---

## 5) WinCC state text list (V5.6)

Bind header text field to `HMI_State` `%MW128`:

| State | Text |
|---:|---|
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

## 6) Operator workflows

### Auto (production)

1. Mode **Auto** → pallet at gate → cycle runs  
2. Watch **Overview** — state text + Ziel-Fach  
3. On Done — check `Info_Text`, Belegt count +1  

### Hand (test without Vision)

1. Mode **Hand** → Operate: fill `RFID_CODE`, Artikel, Material, Color  
2. Optional: **Freies Fach** or set `HMI_Fachnummer`  
3. **Start Einlagern**  

### Einricht (teach only)

1. Mode **Einricht** → **Setup** screen  
2. Jog crane, **Pos speichern**, **Raster berechnen**  
3. See [`RASTER_TEACH.md`](RASTER_TEACH.md)  

### Fix wrong DB entry (no crane move)

1. Mode **Hand** or **Einricht**  
2. Set `HMI_Fachnummer` to slot  
3. **Löschen** → verify `Belegt = FALSE`, counts update  

---

## 7) Common issues

| Symptom | Cause | Fix |
|---|---|---|
| `Info_Text` always empty | `FB_Meldung` not called | Add NW10 |
| Counts stay 0/54 | OUT not wired, **or** Einlagern never books | Wire Datenverwaltung OUT; check Info_Code 7 (RFID wiped) |
| Fachaktuell always empty online | Datenverwaltung copied empty `Fach[n]` every scan | V1.5 copies **only when `HMI_Fachnummer` changes**. Add STAT `Last_HMI_Fach`. |
| Occupancy all grey | `UDT_HMI_Lagerstatus` arrays not downloaded | Update UDT, download HMI DB; watch `LagerverwaltungData.Fach[n].Belegt` |
| Einlagern OK but no message | `Info_Code` set, Meldung missing | Call `instMeldung` |
| Search finds nothing | RFID/Artikel = 0 in Operate | Fill search fields first |
| Löschen no effect | Wrong mode or invalid Fach | Hand/Einricht + Fach 1..54 |
