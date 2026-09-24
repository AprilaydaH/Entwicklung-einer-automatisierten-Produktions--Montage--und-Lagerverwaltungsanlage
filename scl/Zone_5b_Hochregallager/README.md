# Hochregallager â€” SCL

**Doku:** [docs/04_Anlagenbereiche/Zone_5b_Hochregallager/](../../docs/04_Anlagenbereiche/Zone_5b_Hochregallager/)

**TIA:** NW 26 Band → Kunststoff-Lager · NW 27 Band → Metall-Lager · **NW 28 Zone 5A Metall-Hochregal (W2)** · **NW 29 Zone 5B Kunststoff-Hochregal (W1)**  

**TIA tree:** Warehouse_Management → **Warehouse_1** = plastic Zone **5B** (NW 29) · **Warehouse_2** = metal Zone **5A** (NW 28)  

**Metal mirror (Zone 5A):** [../Zone_5a_Metall_Hochregallager/](../Zone_5a_Metall_Hochregallager/) (NW 28)

## Start here

| | |
|---|---|
| **Audit (TIA wiring)** | [`SYSTEM_AUDIT.md`](SYSTEM_AUDIT.md) |
| **Auto-Einlagern** | [`WAREHOUSE_AUTO_START.md`](WAREHOUSE_AUTO_START.md) |
| **Setup (FIO + pins)** | [`WAREHOUSE_1_SETUP.md`](WAREHOUSE_1_SETUP.md) |
| **First pallet** | [`WAREHOUSE_FIRST_PALLET.md`](WAREHOUSE_FIRST_PALLET.md) |
| **HMI Warehouse_1** | [`HMI_Warehouse_1.md`](HMI_Warehouse_1.md) Â· [`HMI_DATA_MGMT.md`](HMI_DATA_MGMT.md) Â· [`HMI_Tags_Warehouse_1.csv`](HMI_Tags_Warehouse_1.csv) Â· occupancy [`HMI_Tags_Rack_W1.csv`](HMI_Tags_Rack_W1.csv) Â· [Regal animation](../../docs/03_Technik/HMI_Regal_Animation.md) |
| **Main OB1 wiring** | [`WAREHOUSE_1_SETUP.md`](WAREHOUSE_1_SETUP.md) Â§3 (FB calls in TIA â€” no OB paste files) |
| **Checkliste** | [`PLASTIC_WAREHOUSE_GOLIVE.md`](PLASTIC_WAREHOUSE_GOLIVE.md) |
| **UDTs (TIA)** | [`UDT_README.md`](UDT_README.md) |
| **Raster teach** | [`RASTER_TEACH.md`](RASTER_TEACH.md) |
| **Tags** | [`PLC_Tags_Hochregallager.csv`](PLC_Tags_Hochregallager.csv) Â· [`PLC_Tags_Warehouse_1_FIO.csv`](PLC_Tags_Warehouse_1_FIO.csv) Â· [`PLC_Tags_RFID_5b.csv`](PLC_Tags_RFID_5b.csv) |
| **TIA export snapshot** | [`PLC_Tags_from_TIA_export.csv`](PLC_Tags_from_TIA_export.csv) |
| **Lastenheft** | [`docs/.../Lastenheft_Abschlussprojekt.docx`](../../docs/01_Projektgrundlagen/Lastenheft_Abschlussprojekt.docx) v1.6 |
| **Web-Suche** | [`docs/03_Technik/Lagerverwaltung_Online.md`](../../docs/03_Technik/Lagerverwaltung_Online.md) (Streamlit, SQLite) |

## Bausteine

| Baustein | Rolle |
|---|---|
| `FB_Warehouse_Gate.scl` | NW27 gate: pallet + tagged â†’ `Paket_Fuer_Hochregal` |
| `FB_Warehouse_Stacker_IO.scl` | NW27 stacker: FIO â†” Ist/Soll/Gabel/Palette feedback |
| `FB_Warehouse_Manual_Soll.scl` | Einricht: jog + Band teach â†’ Soll / Band_X/Z |
| `FB_Warehouse_Actuators.scl` | Warning Light 5 + Alarm Siren 2 |
| `FB_Warehouse_Mode_Select.scl` | Exclusive Einricht / Auto / Hand |
| `Hochregal_Automatik_Betrieb.scl` | Sequencer (your TIA folder `03_Automatik_Betrieb`) |
| `FB_Hochregallager.scl` | Optional one-call wrapper â€” skip if Warehouse_1 already uses separate FBs |
| `FB_Datenverwaltung_Lager.scl` | HMI, ZÃ¤hlung, Pos speichern, Raster |
| `FB_Berechn_Offset.scl` | MOD/DIV pro Fachnummer |
| `Hochregal_Automatik_Betrieb.scl` | State machine Mechanik |
| `FB_Einlagern` / `FB_Auslagern` / â€¦ | Lagerdaten |

## UDTs â€” Kurz

**`UDT_Fach` ist Pflicht** â€” ein Regalfach (Produkt + Position + Belegt).  
**`UDT_Lager_Raster`** â€” einmal pro Lager (Basis + Pitch fÃ¼r 54 FÃ¤cher).  
Siehe [`UDT_README.md`](UDT_README.md) fÃ¼r die exakte TIA-Anlege-Reihenfolge.

## OB1

Wire **Main OB1 in TIA** â€” [`WAREHOUSE_1_SETUP.md`](WAREHOUSE_1_SETUP.md) Â§3 (FB order + pin tables).  
**No OB `.scl` files** in this repo; old examples in [`legacy/`](legacy/) only.
