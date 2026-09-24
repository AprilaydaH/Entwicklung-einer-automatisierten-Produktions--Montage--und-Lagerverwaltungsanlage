# Subsystem â€” Hochregallager

**Code:** [`scl/Zone_5b_Hochregallager/`](../../../scl/Zone_5b_Hochregallager/)  
**Gesamtanlage:** [Gesamtanlage.md](../../01_Projektgrundlagen/Gesamtanlage.md)  
**Lastenheft:** [Lastenheft_Abschlussprojekt.docx](../../01_Projektgrundlagen/Lastenheft_Abschlussprojekt.docx) (v1.4)

## Use this in OB1 â€” **plastic warehouse first**

| Datei | Rolle |
|---|---|
| **`SYSTEM_AUDIT.md`** | **Inconsistency checklist (TIA wiring)** |
| **`WAREHOUSE_AUTO_START.md`** | Auto-Einlagern ohne Start-Taste |
| **`WAREHOUSE_1_SETUP.md`** | FIO + Automatik pin wiring |
| **`WAREHOUSE_FIRST_PALLET.md`** | Hand then Auto commissioning |
| **`OB1_Warehouse_1_IO.scl`** | Gate Â· Manual Soll Â· Stacker Â· DB_2 |
| **`PLASTIC_WAREHOUSE_GOLIVE.md`** | Checklist + test |
| **`RASTER_TEACH.md`** | Teach + Manual Soll X/Z |
| **`PLC_Tags_*.csv`** | Warehouse / FIO / RFID 5b tags |

### Bausteine (NW 29 Warehouse_1)

| FB | Rolle |
|---|---|
| `FB_Warehouse_Gate` | Sensor + Combo_Done/Pallet_Tagged â†’ `Paket_Fuer_Hochregal` |
| `FB_Warehouse_Stacker_IO` | FIO â†” Ist/Soll/Gabel |
| `FB_Warehouse_Manual_Soll` | Einricht HMI Soll X/Z + Jog |
| `Hochregal_Automatik_Betrieb` V1.4 | Sequencer; **IN `RFID_Busy`** â†’ `%M65.1` |
| `FB_Datenverwaltung_Lager` | Raster / Pos speichern |
| `RFID_Read_Write_DB_2` | Reader **5** read only |

### OB1-Reihenfolge

```
Vision â†’ DB_1 Write â†’ Gate â†’ Datenverwaltung â†’ Automatik
      â†’ Manual Soll â†’ Stacker â†’ DB_2 Read
```

Metal warehouse = **Zone 5A / Warehouse_2** Â· **NW 28**: [`scl/Zone_5a_Metall_Hochregallager/`](../../../scl/Zone_5a_Metall_Hochregallager/)  
Plastic warehouse = **Warehouse_1** Â· **NW 29**: this folder.

| Doku | |
|---|---|
| [Hochregallager_Dokumentation.md](Hochregallager_Dokumentation.md) | Gesamtdoku |
| [VARIABLES.md](VARIABLES.md) | Variablen |
| [INFO_CODES.md](INFO_CODES.md) | Codes |
| [Metal Warehouse_2](../Zone_5a_Metall_Hochregallager/) | Zone **5A** Metall-Hochregal (NW 28) |
| [Lagerverwaltung Online](../../03_Technik/Lagerverwaltung_Online.md) | Web-Suche W1+W2 (Streamlit) |

ZurÃ¼ck: [04_Anlagenbereiche](../README.md)
