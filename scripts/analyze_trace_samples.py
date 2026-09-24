"""Extract edge statistics from TIA Portal Trace_1 Samples blob."""
from __future__ import annotations

import struct
import zipfile
from datetime import datetime, timezone
from pathlib import Path

TRACE = Path(r"c:\Users\derej\OneDrive\Desktop\Weiterbildung\Abschlussprojekt\Trace_1.ttrecx")
EXTRACT = Path(r"c:\Users\derej\Projects\PickPlace-2Axis-SCL\Trace_1_extract")

SIGNALS = {
    0: "Execute",
    1: "Write",
    2: "CommandID",
    35: "Pallet_Tagged",
}


def read_general(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    import re

    def tag(name: str) -> str:
        m = re.search(rf"<{name}>([^<]+)</{name}>", text)
        return m.group(1) if m else ""

    return {
        "first": tag("FirstSampleTime"),
        "last": tag("LastSampleTime"),
        "duration_ns": int(tag("RecordingDuration") or "0"),
        "samples": int(tag("ActualSamples") or "0"),
    }


def parse_tssbl(data: bytes) -> tuple[int, int]:
    pos = data.find(b"TSSBL:1.0")
    if pos < 0:
        raise ValueError("TSSBL block not found")
    p = pos + 9
    sample_count, _zero = struct.unpack_from("<II", data, p)
    p += 8
    while p + 4 <= len(data):
        v = struct.unpack_from("<I", data, p)[0]
        if v != (p - (pos + 17)) // 4 + 1:
            # heuristic break: sequential list ended
            break
        p += 4
    return sample_count, p


def try_parse_as_bitstream(data: bytes, start: int, sample_count: int, n_signals: int = 4):
    """Brute-force: assume packed bits/bools after metadata."""
    best = None
    for offset in range(start, min(start + 4096, len(data) - sample_count)):
        series = []
        ok = True
        for s in range(n_signals):
            vals = []
            for i in range(min(sample_count, 5000)):
                byte_i = offset + i * n_signals + s
                if byte_i >= len(data):
                    ok = False
                    break
                vals.append(data[byte_i] & 1)
            if not ok:
                break
            series.append(vals)
        if ok and len(series) == n_signals:
            transitions = sum(sum(1 for a, b in zip(v, v[1:]) if a != b) for v in series)
            if best is None or transitions > best[0]:
                best = (transitions, offset, series)
    return best


def decode_signal_changes(data: bytes, meta_end: int, sample_count: int, duration_s: float):
    """Scan for plausible DInt CommandID stream + bool edges."""
    # Search for monotonic CommandID segments (DInt LE every N bytes)
    results = {}

    # Heuristic scan: 4-byte aligned DInt values 0..100 in plausible runs
    cmd_candidates = []
    for off in range(meta_end, min(meta_end + 65536, len(data) - 4 * sample_count), 4):
        vals = [struct.unpack_from("<i", data, off + 4 * i)[0] for i in range(min(sample_count, 2000))]
        if vals[0] != 0:
            continue
        inc = sum(1 for a, b in zip(vals, vals[1:]) if b == a + 1 or b == a)
        if inc > len(vals) * 0.7 and max(vals) <= 200:
            cmd_candidates.append((inc, off, vals))

    cmd_candidates.sort(reverse=True)
    if cmd_candidates:
        inc, off, vals = cmd_candidates[0]
        results["cmd_off"] = off
        results["cmd_start"] = vals[0]
        results["cmd_end"] = vals[-1]
        results["cmd_max"] = max(vals)
        # first increase
        for i in range(1, len(vals)):
            if vals[i] > vals[i - 1]:
                results["cmd_first_inc_sample"] = i
                results["cmd_first_inc_time_s"] = i / sample_count * duration_s
                break
        # count distinct steps
        steps = sum(1 for a, b in zip(vals, vals[1:]) if b > a)
        results["cmd_steps_in_window"] = steps

    return results


def main() -> None:
    if not EXTRACT.exists():
        with zipfile.ZipFile(TRACE) as z:
            z.extractall(EXTRACT)

    general = read_general(EXTRACT / "General")
    duration_s = general["duration_ns"] / 1e9
    sample_count = general["samples"]
    t0 = datetime.fromisoformat(general["first"].replace("Z", "+00:00"))

    data = (EXTRACT / "Samples").read_bytes()
    sc, meta_end = parse_tssbl(data)
    print(f"Recording: {general['first']} .. {general['last']}")
    print(f"Duration: {duration_s:.2f} s | Samples: {sample_count} | Rate: {sample_count/duration_s:.0f} Hz")
    print(f"TSSBL sample_count={sc}, metadata ends ~@{meta_end}")
    print()

    # Parse Presentation-17 for signal sample layout hints
    pres = (EXTRACT / "Presentation-17.0").read_bytes()
    if b"Command ID" in pres:
        print("Signals confirmed in presentation: Execute, Write, Command ID, Pallet_Tagged")
    print()

    stats = decode_signal_changes(data, meta_end, sample_count, duration_s)
    for k, v in stats.items():
        print(f"{k}: {v}")

    # Brute scan bool patterns - look for region with sparse 0/1
    print("\nScanning binary for bool edge regions...")
    best_regions = []
    chunk = 2000
    for off in range(meta_end, len(data) - chunk, 97):
        window = data[off : off + chunk]
        ones = sum(b & 1 for b in window)
        if 10 < ones < chunk * 0.4:
            edges = sum(1 for a, b in zip(window, window[1:]) if (a & 1) != (b & 1))
            if edges > 20:
                best_regions.append((edges, off, ones / chunk))

    best_regions.sort(reverse=True)
    for edges, off, density in best_regions[:5]:
        w = data[off : off + min(sample_count, 5000)]
        rising = sum(1 for a, b in zip(w, w[1:]) if (a & 1) == 0 and (b & 1) == 1)
        print(f"  off={off}: edges={edges}, rising={rising}, density={density:.3f}")

    # Direct search: find Execute pulse count by looking for 0x01 bytes with spacing ~sample rate
    print("\nCommand ID dword scan (full recording)...")
    for off in range(meta_end, min(meta_end + 200000, len(data) - 4 * sc), 1):
        try:
            vals = [struct.unpack_from("<i", data, off + 4 * i)[0] for i in range(sc)]
        except struct.error:
            continue
        if vals[0] != 0 or vals[-1] < 50 or vals[-1] > 90:
            continue
        mono = sum(1 for a, b in zip(vals, vals[1:]) if b >= a)
        if mono < sc * 0.95:
            continue
        steps = sum(1 for a, b in zip(vals, vals[1:]) if b > a)
        flat0 = next((i for i, v in enumerate(vals) if v > 0), None)
        print(f"MATCH off={off}: start={vals[0]} end={vals[-1]} max={max(vals)} steps={steps} first_nonzero@{flat0} ({flat0/sc*duration_s:.1f}s)")
        # sample times for key values
        for target in [1, 10, 50, vals[-1]]:
            idx = next((i for i, v in enumerate(vals) if v >= target), None)
            if idx is not None:
                print(f"  CommandID>={target} at sample {idx} (~{idx/sc*duration_s:.1f}s)")
        break


if __name__ == "__main__":
    main()
