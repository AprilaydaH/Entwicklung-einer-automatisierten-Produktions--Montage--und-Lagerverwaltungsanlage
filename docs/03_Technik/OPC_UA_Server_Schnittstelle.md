# OPC UA Server-Schnittstelle — Lagerverwaltung Online

**Stand 19.09.2026:** Schnittstelle geladen, Streamlit **live** auf `opc.tcp://192.168.0.1:4840`. Dialog „Lokale Daten erzeugen“ = **Abbrechen** (kein Connector-DB). Classic PLCSIM: Port 4840 tot. F-CPU nur auf **neue** PLCSIM-Advanced-Instanz (nicht Standard-CPU-Karte).

CPU **1518F-4 PN/DP** (TIA V20) stellt den **OPC UA Server** bereit.  
Die Web-App ist nur **Client**. Kein extra Connector-`gldb`. Die Lager-DBs bleiben intern.

**Schnittstelle:** `Si_Lagerverwaltung_Online`  
**Endpoint:** `opc.tcp://<CPU-IP>:4840`  
**Checkliste Tags:** [`scl/HMI_Plant/OPC_UA_Si_Lagerverwaltung_Online.csv`](../../scl/HMI_Plant/OPC_UA_Si_Lagerverwaltung_Online.csv)

Zwei Ordner, nicht mischen:

| Ordner | Lager | Occupancy | Ziel |
|---|---|---|---|
| `Warehouse_1` | Kunststoff 5B | `HRL_Occ_0…6` | `HMI_Ziel_Fach` |
| `Warehouse_2` | Metall 5A | `HRL_2_Occ_0…6` | `HMI_Ziel_Fach_W2` |

Access nur **Read**. Das Touch Panel bleibt die Bedienung.

---

## 1. OPC UA Server auf der CPU (einmal)

1. Gerätekonfiguration → CPU **PLC_1** → Eigenschaften.
2. **OPC UA → Server**.
3. **Activate OPC UA server** einschalten.
4. **Security policies:** nur **Keine Security**.
5. **Benutzer (Firmware V3.1):** es gibt **kein** Gast-Häkchen unter Server → Einstellungen.
   Projektnavigation → **Security-Einstellungen → Benutzer und Rollen**.
   Benutzer **Anonymous** aktivieren und Funktionsrecht **OPC UA-Server-Zugriff** (nur Lesen).
   Änderung an Anonymous nur im CPU-Zustand **STOP** laden.
6. Hardware übersetzen und laden.

Echte CPU: OPC UA Runtime-Lizenz der 1518F prüfen.  
**Classic PLCSIM:** kein OPC UA. **PLCSIM Advanced** oder echte CPU.

---

## 2. Server-Schnittstelle anlegen

1. CPU → **OPC UA → Server interfaces**.
2. **Add new server interface**.
3. Name: **`Si_Lagerverwaltung_Online`**.
4. Im Interface zwei Ordner anlegen: **`Warehouse_1`**, **`Warehouse_2`**.
5. Aus der PLC-Tag-Tabelle **ziehen** (nicht `gldb_LagerverwaltungData` als Ganzes):

### Warehouse_1 — Pflicht

- `HMI_Ziel_Fach`
- `HRL_Anzahl_Belegt`, `HRL_Anzahl_Frei`
- `HMI_State`
- `HRL_Busy`, `HRL_Done`, `HRL_Error`
- `HRL_Occ_0` … `HRL_Occ_6`

### Warehouse_2 — Pflicht

- `HMI_Ziel_Fach_W2`
- `HRL_2_Anzahl_Belegt`, `HRL_2_Anzahl_Frei`
- `HMI_State_W2`
- `HRL_2_Busy`, `HRL_2_Done`, `HRL_2_Error`
- `HRL_2_Occ_0` … `HRL_2_Occ_6`

### Optional (statt vieler Einzel-Merker)

Ganze Arrays aus der **HMI-DB** (OPC UA kann optimized DBs, PUT/GET nicht):

- `gldb_AktuellerFach_HMI.Lagerstatus.Belegt`
- `gldb_AktuellerFach_HMI.Lagerstatus.Farbe`
- W2: `gldb_AktuellerFach_HMI_W2.Lagerstatus.Belegt` / `Farbe`

Nicht in die Schnittstelle: `gldb_LagerverwaltungData`, `gldb_LagerverwaltungData_W2` (Prozessdaten, kein PC-Schreiben).

6. Alle Elemente **Read**.
7. Übersetzen → **Download** (Hardware + Bausteine).

Keine 57 Extra-Merker nötig. Occupancy liegt schon auf `%MB400` / `%MB407`; OPC UA veröffentlicht genau diese Tags.

---

## 3. Test vom PC

```powershell
cd "C:\Users\derej\OneDrive\Desktop\Weiterbildung\Abschlussprojekt\Lagerverwaltung Online"
.\venv\Scripts\python.exe opc_test.py
```

Erwartung: Verbindung, Liste der Nodes unter `Si_Lagerverwaltung_Online`, Werte für Ziel-Fach und Occ-Bytes.

Wenn Port 4840 nicht antwortet: Server aktiv? Download Hardware? IP = CPU (PLCSIM Advanced), nicht Laptop-WLAN `192.168.178.x`.

---

## 4. Streamlit

Sidebar: **Live-Quelle = OPC UA**. URL `opc.tcp://<IP>:4840`.

PUT/GET (Port 102) bleibt als Alternative, wenn OPC UA noch nicht geladen ist.

---

## NodeId (nach Download)

Typisch:

`ns=3;s="Si_Lagerverwaltung_Online"."Warehouse_1"."HMI_Ziel_Fach"`

Der Namespace-Index kann 3 oder 4 sein. `opc_test.py` sucht nach Browse-Name, nicht nach fester Nummer.
