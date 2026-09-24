# Hardware — Vision at 2-axis P&P, RFID at pallet

## Layout

```
  [Lid camera]     [Base camera]          ← Detects All (Numerical)
         \             /
          \           /
       2-axis Pick & Place (Zone 3B)      ← BEFORE assembly
                |
           assembled pallet
                |
         [RFID Reader 2]                  ← tag write (4b)
```

## Vision cameras (must)

| Setting | Value |
|---|---|
| Operating mode | **Detects All (Numerical)** — not “Blue Bases” Bool |
| Lid Value | `%ID142` / `%ED142` |
| Base Value | `%ID146` / `%ED146` |
| Position | Lid lane + Base lane **before** P&P gripper merges them |
| Codes | Plastic **1…6**; metal 7…9 rejected |

## RFID Reader 2 (must)

| Signal | Address |
|---|---|
| Execute | `%Q11.1` / `%A11.1` |
| Command ID | `%ID138` / `%ED138` (must increment) |
| Status / Read | `%ID130` / `%ID134` |
| Command / Write / Index | `%QD104` / `%QD108` / `%QD112` |

## PLC gate

| Step | Signal |
|---|---|
| Sense | Vision at P&P → `Both_Ready` + product fields (State **4**) |
| Write | `Allow_Write` = `4b_Done(1)` → `Write_Req` → tag |

## Limitations

- Bool vision mode → PLC never gets 1…6 → **no Both_Ready**  
- Write before `4b_Done` → do not set `Allow_Write := TRUE` at P&P  
- Command ID stuck → Status 10 (driver / range / Execute hold)  
- Latches hold data after cameras go idle until write finishes  

See also: [`RFID_AUTOMATIC.md`](RFID_AUTOMATIC.md)
