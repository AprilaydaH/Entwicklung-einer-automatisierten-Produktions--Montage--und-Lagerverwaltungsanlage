# Node-RED — live Warehouse 1 and 2

Browser page for both Hochregale. Reads **PLC merkers** (M / MW / MD / MB), not optimized DBs.

Dashboard tabs: **Lager 1** (Kunststoff 5B) and **Lager 2** (Metall 5A). Each has a **6×9 Fach table**. Yellow outline = current Ziel-Fach. Occupied cells are filled (blue W1 / steel W2). Fach **1–6 at the bottom**, level 8 at the top — same numbering as the TP.

This is **not** the Streamlit slot search (SQLite, no PLC). That app is [Lagerverwaltung Online](../docs/03_Technik/Lagerverwaltung_Online.md).

Dashboard: [http://127.0.0.1:1880/ui](http://127.0.0.1:1880/ui)  
Editor: [http://127.0.0.1:1880](http://127.0.0.1:1880)

## 1. TIA — allow PUT/GET

CPU → **Properties → Protection & Security → Connection mechanisms**

- Enable **Permit access with PUT/GET communication from remote partner**
- Download the hardware config

Merkers work with PUT/GET. Optimized `gldb_LagerverwaltungData(_W2)` does **not**. Occupancy for the table uses `HRL_Occ_0…6` (`%MB400`) and `HRL2_Occ_0…6` (`%MB410`). Counts: `HRL_Anzahl_*` / `HRL2_Anzahl_*`.

## 2. PLC IP

Open `flows.json` (or the **s7 endpoint** node in the editor) and set **Address** to the CPU:

| Runtime | Typical IP |
|---|---|
| PLCSIM Advanced | the IP you set in the virtual NIC (often `192.168.0.1`) |
| Real S7-1500 | CPU PROFINET IP |
| Classic PLCSIM | **no** TCP 102 — use Advanced or a real CPU |

This PC must ping that IP. Rack **0**, slot **1** (S7-1500 default).

## 3. Install and run

Need [Node.js LTS](https://nodejs.org/) (includes npm).

```powershell
cd c:\Users\derej\Projects\PickPlace-2Axis-SCL\nodered
npm install
npm start
```

First start: browser opens the editor. **Deploy**. Then open `/ui`.

If the s7 node is missing: menu → **Manage palette** → install `node-red-contrib-s7` and `node-red-dashboard`.

## 4. What you see

| Dashboard | W1 Kunststoff | W2 Metall |
|---|---|---|
| 6×9 table | `HRL_Occ_*` `%MB400…406` | `HRL2_Occ_*` `%MB410…416` |
| Ziel outline | `HMI_Ziel_Fach` `%MW130` | `HMI_Ziel_Fach_W2` `%MW230` |
| State | `HMI_State` `%MW128` | `HMI_State_W2` `%MW228` |
| Belegt / Frei | `%MW132` / `%MW134` | `%MW232` / `%MW234` |
| Busy / Done / Error | `HRL_*` `%M64.0…2` | `HRL2_*` `%M74.0…2` |
| RFID / Vision | — | `%MD236` / `%MD276` |

Cycle 500 ms. Status text: 0 Ready, 20 free slot, 30–58 motion, 60 DB, 70 home, 80 done, 900 fault.

S7 node addresses are **not** TIA syntax. Do not use `MW228,INT`. Use `MI228` (Int), `MW232` (Word), `MR196` (Real), `MDI324` (DInt), `MD236` (UDInt), `M70.1` (Bool). After changing `flows.json`, stop Node-RED (`Ctrl+C`) and run `npm start` again.

The 6×9 tables are drawn on startup even if the PLC is offline (all grey). Live occupancy and the yellow Ziel outline appear only when port 102 answers.
