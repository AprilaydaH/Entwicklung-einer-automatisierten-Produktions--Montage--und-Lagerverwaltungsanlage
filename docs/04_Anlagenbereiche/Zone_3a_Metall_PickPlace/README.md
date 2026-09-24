# Zone 3 — Pick and Place

**Lageplan:** Zone **3A** / **3B**  
**Funktion:** Montage Base + Deckel (**2-axis Pick and Place**)

**Gesamtanlage:** [Gesamtanlage.md](../../01_Projektgrundlagen/Gesamtanlage.md)

## Code

| Datei | Inhalt |
|---|---|
| [`PickPlace_DigitalAnalog.scl`](../../../scl/Zone_3a_Metall_PickPlace/PickPlace_DigitalAnalog.scl) | Haupt-Sequenz (Digital + Analog Modi) |

Zwei Instanzen in TIA für **3A** und **3B** (gleicher FB, getrennte I/O-Tags).

## Anschluss im Materialfluss

```
1B CNC → 2B Vision + Band → 3B Montage + Waage → 4B Palettierer + RFID
```

Vision sitzt in **Zone 2B** (TIA NW 6), nicht in Zone 3. Siehe [RFID](../RFID/README.md).

**Zone 4A Palettierer** → [Zone_4a_Metall_Palletizer_RFID](../Zone_4a_Metall_Palletizer_RFID/)

Zurück: [04_Anlagenbereiche](../README.md)
