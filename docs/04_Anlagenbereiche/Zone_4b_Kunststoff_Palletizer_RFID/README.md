# Zone 4 — Palettierer (4B Kunststoff)

**Lageplan:** Zone **4B** — Palettierer Kunststoff  
**Hinweis:** Zone **4A** Palettierer + RFID Metall → [Zone_4a_Metall_Palletizer_RFID](../Zone_4a_Metall_Palletizer_RFID/)

**Gesamtanlage:** [Gesamtanlage.md](../../01_Projektgrundlagen/Gesamtanlage.md)

**Maschinenlogik:** Function Block **`FB_Palletizer`**  
Instanz: `FB_Palletizer_4B` (Kunststoff). Metall-Palettierer ggf. eigene Instanz — *folgt*.

## Code (`scl/Zone_4b_Kunststoff_Palletizer_RFID/`)

| Datei | Beschreibung |
|---|---|
| `FB_Palletizer.scl` | Sequenz + HMI Auto/Manual |
| `OB1_Palletizer.scl` | Beispiel-Aufruf |
| `UDT_Palletizer.scl` | optionale UDT |
| `PLC_Tags_Palletizer.csv` | Tag-Vorlage |

## Dokumentation

| Dokument | Inhalt |
|---|---|
| [Palletizer_Dokumentation.md](Palletizer_Dokumentation.md) | Sequenz, I/O |
| [HMI_Organisation.md](HMI_Organisation.md) | Zonen-Screen |
| [Test_und_Inbetriebnahme.md](Test_und_Inbetriebnahme.md) | Import + Tests |

Zurück: [04_Anlagenbereiche](../README.md)
