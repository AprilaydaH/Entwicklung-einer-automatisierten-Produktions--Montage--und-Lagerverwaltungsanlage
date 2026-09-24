# Hardware — PLC_1 und HMI_1

**Quelle:** TIA Geräteübersicht, Netzsicht, Belegungsplan, Speicherauslastung · **Stand 19.09.2026**

## Steuerung

| Gerät | Typ / Bestellnr. | Firmware | Bemerkung |
|---|---|---|---|
| **PLC_1** | CPU **1518F-4 PN/DP** · `6ES7 518-4FX00-1AB0` | V3.1 | Failsafe S7-1500; Schnittstellen X1–X3 PROFINET, X4 PROFIBUS DP |
| **PS** Slot 0 | PS 60W 24/48/60VDC · `6ES7 505-0RA00-0AB0` | V1.1 | 24 V DC Versorgung |
| **HMI_1** | **TP2200 Comfort** | — | Ein Touch Panel, Netz `PN/IE_1`, X1 **`192.168.0.2`** (X3 anderes Subnetz) |

OB1 = zyklisches Hauptprogramm (Zonen-NW **1–29**, danach **`FB_Plant_Start_Stop`**, zuletzt `"OB100_Startup_Init" := FALSE`). **OB100 (Startup)** läuft **einmal** bei STOP → RUN: Modi und Kran-/Gabel-Kommandos aus, Automatik-Reset über `OB100_Startup_Init` `%M59.0`, Produktion nicht selbststartend. Lager-DBs (`gldb_LagerverwaltungData`) werden **nicht** gelöscht. SCL: [`scl/HMI_Plant/OB100_Startup.scl`](../../scl/HMI_Plant/OB100_Startup.scl). FUP Start/Stop: [`scl/HMI_Plant/FB_Plant_Start_Stop.md`](../../scl/HMI_Plant/FB_Plant_Start_Stop.md). F-Programm bleibt getrennt.

**OPC UA Server** (CPU-Eigenschaft, Port **4840**): Schnittstelle [`Si_Lagerverwaltung_Online`](OPC_UA_Server_Schnittstelle.md) für die Web-App. **Live getestet** gegen Streamlit (`192.168.0.1`). Kein Connector-`gldb`. Classic PLCSIM spricht OPC UA nicht; **PLCSIM Advanced** (TCP/IP Single Adapter, Siemens Virtual Ethernet Adapter) oder echte CPU. CPU-Typ bleibt **1518F** — kein Tausch auf 1518T.

## Peripherie Rack 0

| Slot | Baugruppe | Adressen | Bestellnr. |
|---:|---|---|---|
| 2 | DI 32×24VDC BA_1 | E 4.0 … E 7.7 | 6ES7 521-1BL10-0AA0 |
| 3 | DI 32×24VDC BA_2 | E 0.0 … E 3.7 | 6ES7 521-1BL10-0AA0 |
| 4 | DI 32×24VDC BA_3 | E 8.0 … E 11.7 | 6ES7 521-1BL10-0AA0 |
| 5 | DI 32×24VDC BA_4 | E 12.0 … E 15.7 | 6ES7 521-1BL10-0AA0 |
| 6 | DQ 64×24VDC/0,3A BA_1 | A 8.0 … A 15.7 | 6ES7 522-1BP00-0AA0 |
| 7 | DQ 64×24VDC/0,3A BA_2 | A 16.0 … A 23.7 | 6ES7 522-1BP00-0AA0 |
| 8 | DQ 64×24VDC/0,3A BA_3 | A 24.0 … A 31.7 | 6ES7 522-1BP00-0AA0 |
| 9 | AI 16×I BA_1 (Strom) | EW/ED ab E 16 (… E 47) | 6ES7 531-7MH00-0AB0 |
| 10 | AI 16×U BA_1 (Spannung) | ab E 48 (… E 79) | 6ES7 531-7LH00-0AB0 |
| 11 | AQ 2×U/I ST_2 | A 0 … A 3 | 6ES7 532-5NB00-0AB0 |
| 12 | AQ 2×U/I ST_1 | A 4 … A 7 | 6ES7 532-5NB00-0AB0 |

Konfiguriert laut Speicherauslastung: **128 DE** (58 genutzt, 45 %), **192 DA** (157 genutzt, 82 %), **32 AE** (18 genutzt, 56 %), **4 AA** (0 genutzt). DA ist der knappste Kanal.

## Belegungsplan (Auszug)

Digitale Eingänge u. a. **EB0…EB13** (Sensorik). Analoge/Prozess-DWORDs u. a. **EB30…EB50**, weitere Blöcke **EB50…EB65**, **EB86…EB109**, **EB140…EB149**.  
Digitale Ausgänge dicht belegt **AB0…AB13**; weiterer Block **AB16…AB22**.  
Merker u. a. MB0–MB51 (Flags, Words, DWORDs; MB20 Taktmerker).

## Pick & Place — Namenskonvention

| Bezeichnung (Lastenheft / HMI) | Zone / NW | TIA-Objekt (aktuell) |
|---|---|---|
| **2-axis Pick and Place** | 3A NW 9, 3B NW 17 | `PickPlace_DigitalAnalog.scl` (2 Instanzen) |
| **3-axis Pick and Place** | 4A Handling (X/Y/Z) | bisher „Gantry“: `FB_GantryPickPlace` / Tags `Gantry_*` |

„Gantry“ wird in der Dokumentation nicht mehr verwendet. PLC-Tag-Umbenennung `Gantry_*` → `Pnp3Axis_*` erfolgt in TIA, wenn die Adressen stehen bleiben.

Zurück: [03_Technik](README.md) · [Lastenheft](../01_Projektgrundlagen/Lastenheft_Abschlussprojekt.docx)
