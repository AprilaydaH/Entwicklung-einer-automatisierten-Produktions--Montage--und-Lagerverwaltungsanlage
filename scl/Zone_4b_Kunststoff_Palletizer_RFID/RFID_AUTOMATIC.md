# Automatic RFID — Vision at 2-axis P&P (pre-assembly)

## Sequence

```
Zone 3B 2-axis Pick & Place (BEFORE assembly)
  Lid camera + Base camera  →  FB_VisionReader latch + stamp
        ↓
  2-axis P&P assembles lid+base on pallet
        ↓
  4b_Done(1)  →  Allow_Write
        ↓
  Write_Req → Reader 2 tags pallet
        ↓
  Combo_Done / Pallet_Tagged → warehouse
```

Vision **senses early**; RFID **writes later**. Latches keep product data while parts leave the cameras.

## Hardware placement

| Device | Where |
|---|---|
| Vision Lid | 2-axis P&P lid infeed (Zone 3B) |
| Vision Base | 2-axis P&P base infeed (Zone 3B) |
| Mode | **Detects All (Numerical)** → `%ED142` / `%ED146` |
| RFID Reader 2 | Pallet write station (4b) |

## TIA wiring

| Pin | Value |
|---|---|
| Vision `Allow_Write` | **`4b_Done(1)`** `%M10.0` |
| Vision `Write_Req` | `%M20.0` |
| RFID `HMI_Write` | `%M20.0` |
| RFID `Tag_Wait_Time` | `T#3M` (travel after Done if needed) |

## States (Vision)

| State | Meaning |
|---|---|
| 1 | Waiting for lid+base at P&P |
| 4 | Both sensed — **Waiting_For_Write** (assembly / convey) |
| 2 | RFID write running |
| 3 | Combo_Done / tagged |

Paste FB **v2.7** + [`OB1_Vision_RFID_before_Pallet.scl`](OB1_Vision_RFID_before_Pallet.scl)
