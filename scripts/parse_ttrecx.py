"""Quick probe of TIA Portal .ttrecx trace recording."""
import re
import sys
import zipfile
from pathlib import Path

path = Path(sys.argv[1] if len(sys.argv) > 1 else r"c:\Users\derej\OneDrive\Desktop\Weiterbildung\Abschlussprojekt\Trace_1.ttrecx")
data = path.read_bytes()
print(f"FILE: {path}")
print(f"SIZE: {len(data)} bytes")
print(f"HEAD: {data[:32].hex()}")

# ZIP / OPC package?
if data[:2] == b"PK":
    print("FORMAT: ZIP/OPC")
    with zipfile.ZipFile(path) as z:
        for n in sorted(z.namelist()):
            info = z.getinfo(n)
            print(f"  {n} ({info.file_size} bytes)")
else:
    print("FORMAT: not ZIP at start")

for enc in ("utf-16-le", "utf-8", "latin-1"):
    text = data.decode(enc, errors="ignore")
    hits = sorted(set(re.findall(r"Trace_1|Command ID|Execute|Pallet|Write|%[QMI][A-Za-z0-9.]+|ConfigurationName|CreationTime|Recording", text)))
    if hits:
        print(f"\nSTRINGS ({enc}):")
        for h in hits[:60]:
            print(f"  {h}")
