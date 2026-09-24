# Data management + HMI — Warehouse_2 Metal

Mechanical sequencer = W1 V5.6 mirror. This guide is the metal data path.

**Related:** [`HMI_Warehouse_2.md`](HMI_Warehouse_2.md) · [`WAREHOUSE_2_SETUP.md`](WAREHOUSE_2_SETUP.md)

---

## 1) PLC data path

```
Automatik_W2 state 60
  → fill gldb_AktuellerFach_HMI_W2.Auswahl.Fachaktuell
  → instEinlagern (FB_Einlagern_W2) → gldb_LagerverwaltungData_W2.Fach[n]
  → instLagerstatus → counts in DB
```

| FB | Call | Purpose |
|---|---|---|
| `FB_Datenverwaltung_Lager_W2` | OB1 | Slot mirror, teach, raster, counts |
| `FB_Einlagern_W2` | Automatik @ 60 | Persist pallet |
| `FB_Lagerstatus_W2` | After Einlagern | Refresh counts text |
| `FB_Meldung_W2` | OB1 last | Info_Code → Info_Text |
| `FB_Suchen_W2` / `Freies_Fach` / `Loeschen_W2` | OB1 2b | HMI data tools |

---

## 2) OB1 data networks

### Datenverwaltung OUT

| Pin | Tag |
|---|---|
| `Anzahl_Belegt` | `HRL2_Anzahl_Belegt` `%MW232` |
| `Anzahl_Frei` | `HRL2_Anzahl_Frei` `%MW234` |

### Data commands

```scl
"instLoeschen_W2"(Execute := "HMI_Loeschen_W2" AND ("Mode_Hand_W2" OR "Mode_Einricht_W2"));
"instSuchen_W2"(Execute := "HMI_Suchen_W2");
"instFreiesFach_W2"(Start := "HMI_FreiesFach_W2");
```

`FB_Suchen_W2` needs INPUT **`Execute`** (Bool) and STAT **`R_Go`** (R_TRIG).

| Button | Tag |
|---|---|
| Löschen | `HMI_Loeschen_W2` `%M71.0` |
| Suchen | `HMI_Suchen_W2` `%M71.1` |
| Freies Fach | `HMI_FreiesFach_W2` `%M71.2` |

### Suchen (Hand / Einricht)

Mode **Hand**. Type **one** key into `Fachaktuell`, then pulse **Suchen**:

| You type | Looks for |
|---|---|
| `RFID_CODE` ≠ 0 | First occupied slot with that code |
| else `Artikelnummer` ≠ 0 | First occupied slot with that article |
| else `Fachnummer` 1…54 | That slot (empty is OK) |

Result stays on the Operate IO fields. Info_Text: `Gefunden | Fach: n | Artikel: … | RFID: …` (`Info_Code` **9**) or `Kein passendes Fach gefunden` (**8**).

Do **not** leave Mode Auto while searching — Auto still copies 4a onto `Fachaktuell`.

Success after Einlagern: `Info_Code = 1` → *Einlagerung erfolgreich*

---

## 3) Verify after one Hand cycle

| Check | Expected |
|---|---|
| `gldb_LagerverwaltungData_W2.Fach[n].Belegt` | TRUE |
| `…Materialart` | 2 (Metall) if set on HMI |
| `HRL2_Anzahl_Belegt` | ≥ 1 |
| `HMI_Ziel_Fach_W2` | booked `n` |
| `Info_Text` | Einlagerung erfolgreich |

If **online Datenverwaltung shows empty product / Belegt stays 0**: the block was copying empty `Fach[HMI_Fachnummer]` onto `Fachaktuell` every scan (RFID → 0 → Einlagern Info_Code 7). V1.5 copies **only when Fachnummer changes**. Watch `gldb_LagerverwaltungData_W2.Fach[n].Belegt`, not only `Fachaktuell`.

---

## 4) HMI phase order

1. Header + Overview counts / Info_Text / State  
2. Operate product + Start + Fach browse  
3. Suchen / Freies Fach / Löschen  
4. Rack occupancy map — `gldb_AktuellerFach_HMI_W2.Lagerstatus` ([HMI_Regal_Animation.md](../../docs/03_Technik/HMI_Regal_Animation.md))  

Defer Auslagern until sequencer exists.

---

## Web search (no PLC change)

Browser search of 54 slots (SQLite copy, not live `gldb_LagerverwaltungData_W2`):  
[`docs/03_Technik/Lagerverwaltung_Online.md`](../../docs/03_Technik/Lagerverwaltung_Online.md)
