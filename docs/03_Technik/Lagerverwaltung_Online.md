# Lagerverwaltung Online (Web)

**Stand 19.09.2026:** OPC UA **verbunden** — Streamlit liest `Si_Lagerverwaltung_Online` auf `opc.tcp://192.168.0.1:4840` (PLCSIM Advanced, CPU 1518F). SQLite bleibt für RFID-Suche. Kein Live-Sync der Lager-DBs.

Browser search and **live occupancy** for Warehouse 1 (plastic) and Warehouse 2 (metal).

**Location (PC):**  
`C:\Users\derej\OneDrive\Desktop\Weiterbildung\Abschlussprojekt\Lagerverwaltung Online\`

This is **not** the Siemens TP. The Touch Panel stays the operator HMI. Node-RED is not used for this page.

---

## What you see

| Quelle | Inhalt |
|---|---|
| **SPS live** (sidebar, off by default) | 6×9 Gitter belegt/frei + **Ziel-Fach** (yellow border) + Zähler |
| SQLite | RFID / Artikel-Suche und Demo-Einlagern (nicht die Lager-DB der SPS) |

PUT/GET cannot read optimized `gldb_LagerverwaltungData`. Occupancy bits are therefore copied to merkers:

| Warehouse | Bytes | Address |
|---|---|---|
| W1 | `HRL_Occ_0` … `HRL_Occ_6` | `%MB400` … `%MB406` |
| W2 | `HRL_2_Occ_0` … `HRL_2_Occ_6` | `%MB407` … `%MB413` |

Filled every scan by the instance DBs (do not mix):

| Warehouse | FB | Instance DB | Occupancy merkers |
|---|---|---|---|
| 1 Kunststoff 5B | `FB_Datenverwaltung_Lager` | `fb_Datenverwaltung_Lager_DB` | `HRL_Occ_*` `%MB400` |
| 2 Metall 5A | `FB_Datenverwaltung_Lager_W2` | `FB_Datenverwaltung_Lager_W2_DB` | `HRL_2_Occ_*` `%MB407` |

---

## TIA — OPC UA (preferred)

Create server interface **`Si_Lagerverwaltung_Online`** (folders Warehouse_1 / Warehouse_2).  
Steps: [`OPC_UA_Server_Schnittstelle.md`](OPC_UA_Server_Schnittstelle.md).  
Tag list: [`scl/HMI_Plant/OPC_UA_Si_Lagerverwaltung_Online.csv`](../../scl/HMI_Plant/OPC_UA_Si_Lagerverwaltung_Online.csv).

Streamlit sidebar: **Live-Quelle = OPC UA**. Test: `python opc_test.py`.

## TIA — PUT/GET (fallback)

1. Enable **Permit access with PUT/GET communication from remote partner**.
2. Import tags `HRL_Occ_0`…`6` and `HRL_2_Occ_0`…`6`.
3. Paste Datenverwaltung V1.5 (writes the occupancy bytes).
4. Download. CPU IP in Streamlit sidebar (PLCSIM Advanced or real CPU). Classic PLCSIM has no TCP 102.

---

## Run

```powershell
cd "C:\Users\derej\OneDrive\Desktop\Weiterbildung\Abschlussprojekt\Lagerverwaltung Online"
.\venv\Scripts\python.exe -m streamlit run app.py --server.headless true
```

(`streamlit.exe` kann unter Windows Application Control blockiert sein.)

Browser: `http://localhost:8501`

Tabs **Lager 1** / **Lager 2**. **Demo Ziel 7** marks Fach 7 without a CPU.

Sidebar: CPU-IP, **Live-Quelle = OPC UA**. Fallback PUT/GET. Classic PLCSIM has neither port 4840 nor 102.

---

## Lastenheft

AF-34a / HM-07: web search RFID → Artikel → Fach. TP remains leading for operation.
