# Lageplan â€” Factory-Zonen

**Quelle:** [Lageplan.pdf](Lageplan.pdf)  
**Gesamtdokument:** [Gesamtanlage.md](Gesamtanlage.md)

**SPS-Netzwerke (TIA):** [PLC_Networks.md](PLC_Networks.md) â€” **29** OB1-Netzwerke  
**Konvention:** Linie **A = Metall**, Linie **B = Kunststoff**.

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚ Zone 1A â€” METALL             â”‚ Zone 1B â€” KUNSTSTOFF         â”‚
â”‚ Rohmaterial                  â”‚ Rohmaterial                  â”‚
â”‚ Robotstation A Â· Base + CNC  â”‚ Robotstation C Â· Base + CNC  â”‚
â”‚ Robotstation B Â· Deckel + CNCâ”‚ Robotstation D Â· Deckel + CNCâ”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚ Zone 2A                      â”‚ Zone 2B                      â”‚
â”‚ Transportband (Metall)       â”‚ Transportband (Kunststoff)   â”‚
â”‚                              â”‚ + Vision Farbregistrierung   â”‚
â”‚                              â”‚   fÃ¼r RFID-Daten             â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚ Zone 3A                      â”‚ Zone 3B                      â”‚
â”‚ 2-axis Pick and Place Metall â”‚ 2-axis Pick and Place Kunst. â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚ Zone 4A                      â”‚ Zone 4B                      â”‚
â”‚ 3-axis P&P + Palettierer     â”‚ Palettierer Kunststoffteile  â”‚
â”‚ Metall + RFID                â”‚ + RFID                       â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚ Zone 5A                      â”‚ Zone 5B                      â”‚
â”‚ Hochregallager Metall        â”‚ Hochregallager Kunststoff    â”‚
â”‚ RFID Metall (spÃ¤ter)         â”‚ RFID Write/Read (4b)         â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”´â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

## Zonentabelle

| Zone | Stationen | Code-Pfad | Status |
|---|---|---|---|
| **1A** | Rohmaterial Metall, Roboter A/B, CNC Base + Deckel | `scl/Zone_1a_Metall/` | geplant |
| **1B** | Rohmaterial Kunststoff, Roboter C/D, CNC Base + Deckel | `scl/Zone_1b_Kunststoff/` | geplant |
| **2A** | Transportband Metall (nach 1A) | `scl/Zone_2a_Foerderbaender/` | geplant |
| **2B** | Transportband Kunststoff + Vision (Farbregistrierung fÃ¼r RFID) | `scl/Zone_2b_Vision_Foerderbaender/` | Vision SCL |
| **3A / 3B** | 2-axis Pick and Place Metall / Kunststoff | `scl/Zone_3a_Metall_PickPlace/` Â· `scl/Zone_3b_Kunststoff_PickPlace/` | SCL vorhanden |
| **4A** | 3-axis Pick and Place + Palettierer + RFID Metall | `scl/Zone_4a_Metall_Palletizer_RFID/` | SCL vorhanden |
| **4B** | Palettierer Kunststoff + RFID | `scl/Zone_4b_Kunststoff_Palletizer_RFID/` | SCL vorhanden |
| **5A** | **Metall-Hochregal W2 (NW 28)** + Band → Kunststoff-Lager (NW 26) | scl/Zone_5a_Metall_Hochregallager/ · scl/Zone_5a_Foerderband_Lager/ | W2 scaffold |
| **5B** | **Kunststoff-Hochregal W1 (NW 29)** + Band → Metall-Lager (NW 27) | scl/Zone_5b_Hochregallager/ | W1 E2E |

Ordnernamen folgen den TIA-Zonen (`scl/Zone_1a_Metall/` â€¦). Siehe [PLC_Networks.md](PLC_Networks.md).

## Materialfluss

**Kunststoff (PrioritÃ¤t) â€” TIA NW 4, 6â€“8, 17â€“20, 22â€“26, 29:**
```
1B Roh (NW 4) + CNC (NW 6)
    â†’ 2B Vision (NW 7) + Transportband (NW 8)
    â†’ 3B Band â†’ 2-axis P&P â†’ Waage â†’ Band (NW 17â€“20)
    â†’ 4B Band/Rolle â†’ Palettierer â†’ RFID Write (NW 22â€“25)
    â†’ 5A Band zum Kunststoff-Lager (NW 26)
    â†’ 5B Plastic Components Warehouse (NW 29) â€” Warehouse_1
```

**Metall â€” TIA NW 1â€“3, 5, 9â€“16, 21, 27â€“28:**
```
1A Roh + CNC (NW 1â€“2) â†’ 2A Band (NW 3) + Vision NW 5
    â†’ 3A Band â†’ 2-axis P&P â†’ Waage â†’ Band (NW 9â€“12)
    â†’ 4A Band/Rolle â†’ 3-axis P&P â†’ RFID (NW 13â€“16, 21)
    â†’ 5B Band zum Metall-Lager (NW 27)
    â†’ 5A Metal Components Warehouse (NW 28) â€” Warehouse_2
```

Detail: [Gesamtanlage.md](Gesamtanlage.md) Abschnitt 3.

**Ein HMI (TP)** bedient alle Zonen â€” siehe [HMI_Gesamtanlage.md](../03_Technik/HMI_Gesamtanlage.md).

**Nicht im Scope:** Wasserverbrauch.
