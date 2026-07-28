# Factory I/O — Tag-Mapping (Digital + Analog)

Ziel-Szene: **Pick & Place** (Two Axis). Driver: Siemens S7-1500 / S7-PLCSIM / NetToPLCSim.

PLC-DB: `gldb_FactoryIO_IO` (siehe `scl/gldb_FactoryIO_IO.udt.txt`)

Umschalten in `gldb_Config.Achs_Modus`:

| Wert | Modus | Genutzte Tags |
|---|---|---|
| **0** | Analog | `Pos_X/Z`, `Target_X/Z`, optional `Moving_X/Z` |
| **1** | Digital | `X_At_*`, `Z_At_*`, `X_Plus/Minus`, `Z_Plus/Minus` |

Gemeinsam in beiden Modi: `Sensor_Entry`, `Sensor_Exit`, `Item_Detected`, `Gripper`, `Conv_Entry`, `Conv_Exit`, `Not_Aus`.

---

## 1. Digitale Eingänge (Factory I/O → PLC)

| Factory I/O Tag (typisch) | PLC (`gldb_FactoryIO_IO.Input`) | Typ | Hinweis |
|---|---|---|---|
| `At Entry` / `Entry sensor` | `Sensor_Entry` | Bool | Teil bereit zum Pick |
| `At Exit` / `Exit sensor` | `Sensor_Exit` | Bool | Optional |
| `Item detected` / `Grabbed` | `Item_Detected` | Bool | Greifer-Sensor |
| `Moving X` | `Moving_X` | Bool | Nur Analog-Szene |
| `Moving Z` | `Moving_Z` | Bool | Nur Analog-Szene |
| `X at Home` / Limit / Pos bit | `X_At_Home` | Bool | Digital-Modus |
| `X at Pick` | `X_At_Pick` | Bool | Digital-Modus |
| `X at Place` | `X_At_Place` | Bool | Digital-Modus |
| `Z at Up` / `Z raised` | `Z_At_Up` | Bool | Digital-Modus |
| `Z at Down` / `Z lowered` | `Z_At_Down` | Bool | Digital-Modus |
| `Emergency stop` (falls vorhanden) | `Not_Aus` | Bool | TRUE = Not-Aus |

Exact Tag-Namen hängen von der Factory-I/O-Szene und dem Driver ab — im Driver-Panel die Namen anpassen.

---

## 2. Digitale Ausgänge (PLC → Factory I/O)

| PLC (`gldb_FactoryIO_IO.Output`) | Factory I/O Tag (typisch) | Typ |
|---|---|---|
| `Conv_Entry` | `Entry conveyor` | Bool |
| `Conv_Exit` | `Exit conveyor` | Bool |
| `Gripper` | `Gripper` / `Magnet` | Bool |
| `X_Plus` | `Move X+` / `X+` | Bool (Digital) |
| `X_Minus` | `Move X-` / `X-` | Bool (Digital) |
| `Z_Plus` | `Move Z+` / `Z+` | Bool (Digital) |
| `Z_Minus` | `Move Z-` / `Z-` | Bool (Digital) |

---

## 3. Analoge Signale

Factory I/O Analog oft **0…10 V**. In TIA skalieren (z.B. NORM_X / SCALE_X) auf dieselbe Einheit wie Teach-Punkte (hier: `Real`, oft 0.0…10.0 oder mm).

| Richtung | PLC | Factory I/O (typisch) | Typ |
|---|---|---|---|
| Input | `Input.Pos_X` | `Pos X` / `Position X` | Real (skaliert) |
| Input | `Input.Pos_Z` | `Pos Z` / `Position Z` | Real (skaliert) |
| Output | `Output.Target_X` | `Target X` / `Setpoint X` | Real |
| Output | `Output.Target_Z` | `Target Z` / `Setpoint Z` | Real |

### Skalierungsbeispiel (Rohwert INT → Real 0…10)

```scl
"gldb_FactoryIO_IO".Input.Pos_X :=
    NORM_X(MIN := 0, VALUE := "IW_Pos_X", MAX := 27648)
    * 10.0;   // oder * max_mm
```

Analog-Output entsprechend zurück skalieren, wenn der Driver INT erwartet.

---

## 4. Empfohlene Start-Config

```
gldb_Config.Achs_Modus = 0        // zuerst Analog testen
gldb_Config.Tol_X      = 0.05
gldb_Config.Tol_Z      = 0.05
Pos.*                  = nach Einricht teachen
```

### Digital-Modus Checkliste

1. `Achs_Modus := 1`
2. Drei X-Positionssensoren (Home/Pick/Place) verdrahten
3. Zwei Z-Sensoren (Up/Down) verdrahten
4. `X+/X-` und `Z+/Z-` Outputs mappen
5. Analog-Targets können unverdrahtet bleiben

### Analog-Modus Checkliste

1. `Achs_Modus := 0`
2. `Pos_X/Z` und `Target_X/Z` skalieren
3. Optional `Moving_X/Z` für sauberes In-Position
4. Digital-Jog-Outputs bleiben FALSE

---

## 5. Driver-Hinweise

- **Official Siemens S7-1500 Driver** (Factory I/O): Tags in Driver Configuration an DB-Offsets binden
- **NetToPLCSim**: PLCSim Advanced / Classic + Factory I/O S7 driver
- Zykluszeit PLC ≤ 10–50 ms empfohlen, damit Analog-Nachführung ruhig bleibt
