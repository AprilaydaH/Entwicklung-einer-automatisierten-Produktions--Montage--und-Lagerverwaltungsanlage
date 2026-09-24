# Zone 4B — Palettierer + RFID Kunststoff

**TIA:** NW 20–21 Bänder · NW 22 `Zone_4b_Plastic_Assembly_Palletizer` · NW 23 `Zone_4b_Plastic_RFID`

Vision-Daten kommen aus [Zone 2B](../Zone_2b_Vision_Foerderbaender/) (NW 6). Hier wird auf die Palette geschrieben.

| Datei | Rolle |
|---|---|
| `FB_Palletizer.scl` | Palettierer Kunststoff |
| `FB_RFID_ReadWrite.scl` | RFID Handshake v1.4 (auto: Write clears Error) |
| `FB_VisionReader.scl` | in Zone 2B — v2.3 auto Write on `4b_Done` |
| `OB1_Vision_RFID_before_Pallet.scl` | Vision + Reader 2 write (automatic) |
| `RFID_AUTOMATIC.md` | Auto sequence + tags (no new FB) |
| `RFID_LIVE_2608.md` | Live TIA map from PLCTags26.08 |
| `PLC_Tags_RFID.csv` | RFID + Vision-Handshake-Tags |
| `HMI_RFID_Vision.md` | HMI-Screen (Reset only in production) |
| `OB1_Palletizer.scl` | Palettierer isoliert |

Go-live mit Lager: [`../Zone_5b_Hochregallager/OB1_Plastic_Warehouse.scl`](../Zone_5b_Hochregallager/OB1_Plastic_Warehouse.scl)  
Auto RFID: [`RFID_AUTOMATIC.md`](RFID_AUTOMATIC.md)
