# Zone 2B — Vision data + Transportband Kunststoff

**TIA:** NW 6 `Zone_2b_VisionData_Sensors` · NW 7 Band

**Hardware placement:** Vision cameras sit at **Zone 3B 2-axis Pick & Place** (lid + base **before** assembly).  
NW 6 only holds the Vision FB / tags; physical sensors are at the P&P infeed.

| Schritt | Wo | Baustein |
|---|---|---|
| Sense Lid + Base | 3B 2-axis P&P infeed | `FB_VisionReader` v2.8 |
| Assemble | 3B 2-axis P&P | `PickPlace_DigitalAnalog` |
| RFID Write | 4B Reader 2 | `FB_RFID_ReadWrite` when `4b_Done` |

| Datei | Rolle |
|---|---|
| [`FB_VisionReader.scl`](FB_VisionReader.scl) | Pre-assembly latch; write gated by `Allow_Write` |
| [`TAGS_VisionSensorData.md`](TAGS_VisionSensorData.md) | Tag map |

RFID: [Zone 4B](../Zone_4b_Kunststoff_Palletizer_RFID/) · [`RFID_AUTOMATIC.md`](../Zone_4b_Kunststoff_Palletizer_RFID/RFID_AUTOMATIC.md)
