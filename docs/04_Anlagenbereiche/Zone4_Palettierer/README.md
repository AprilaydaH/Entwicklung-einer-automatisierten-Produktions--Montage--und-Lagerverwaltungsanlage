# Zone 4 — Palettierer

**Lageplan:** Zone **4A** Palletizer Metal Parts · Zone **4B** Palletizer Plastic Parts  

**Maschinenlogik:** Function Block **`FB_Palletizer`**  
Zwei Instanzen: `FB_Palletizer_4A` (Metal), `FB_Palletizer_4B` (Plastic)

## Code (`scl/Zone4_Palettierer/`)

| Datei | Beschreibung |
|---|---|
| `FB_Palletizer.scl` | Sequenz + HMI Auto/Manual |
| `OB1_Palletizer.scl` | Beispiel-Aufruf (eine Instanz, für 4A/4B duplizieren) |
| `UDT_Palletizer.scl` | optionale UDT |
| `PLC_Tags_Palletizer.csv` / `.xlsx` | Tag-Vorlage (je Linie eigene Adressen) |

## Dokumentation

| Dokument | Inhalt |
|---|---|
| [Palletizer_Dokumentation.md](Palletizer_Dokumentation.md) | Sequenz, I/O |
| [HMI_Organisation.md](HMI_Organisation.md) | Zonen-Screen inkl. 4A/4B Instanzkonzept |
| [Test_und_Inbetriebnahme.md](Test_und_Inbetriebnahme.md) | Import + Tests |

Zurück: [04_Anlagenbereiche](../README.md)
