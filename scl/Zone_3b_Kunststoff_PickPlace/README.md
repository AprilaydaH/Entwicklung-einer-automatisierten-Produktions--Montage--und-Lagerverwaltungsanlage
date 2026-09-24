# Zone 3B — Kunststoff Pick & Place + Waage

**TIA:** NW 16 Band vor P&P · NW 17 `Zone_3b_Kunststoff_Pick_and_Place_2` · NW 18 Waage 2 · NW 19 Band nach Waage

Gleicher FB wie Zone 3A, **zweite Instanz** + eigene I/O:

[`../Zone_3a_Metall_PickPlace/PickPlace_DigitalAnalog.scl`](../Zone_3a_Metall_PickPlace/PickPlace_DigitalAnalog.scl)

**Vision (plastic):** Lid + Base cameras are mounted on this **2-axis P&P infeed** (before assembly).  
Data FB: [`../Zone_2b_Vision_Foerderbaender/FB_VisionReader.scl`](../Zone_2b_Vision_Foerderbaender/FB_VisionReader.scl) — RFID write later via `4b_Done`.
