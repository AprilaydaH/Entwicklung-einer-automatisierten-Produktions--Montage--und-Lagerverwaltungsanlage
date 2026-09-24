# -*- coding: utf-8 -*-
"""Export PLCTags3.xlsx grouped by station / FIO vs merker."""
from collections import defaultdict
from pathlib import Path

import openpyxl

SRC = Path(r"c:\Users\derej\Downloads\PLCTags3.xlsx")
OUT_DIR = Path(__file__).resolve().parents[1] / "docs" / "01_Projektgrundlagen"
CSV_OUT = OUT_DIR / "PLCTags3_live.csv"
MD_OUT = OUT_DIR / "Station_PLC_FIO_Tags.md"


def is_fio(addr: str) -> bool:
    if not addr:
        return False
    a = addr.replace(" ", "")
    return a.startswith(("%E", "%A", "%I", "%Q"))


def station_of(name: str, path: str) -> str:
    n = (name or "").strip()
    p = (path or "").strip()
    low = n.lower()
    if n.startswith("1a_") or n.startswith("1A_"):
        return "1A"
    if n.startswith("1b_") or n.startswith("1B_"):
        return "1B"
    if n.startswith("2a_") or n.startswith("2A_") or "2a_Vision" in n:
        return "2A"
    if n.startswith("2b_") or n.startswith("2B_") or p == "2b_VisionDataSensors":
        return "2B"
    if n.startswith("3a_") or n.startswith("3A_"):
        return "3A"
    if n.startswith("3b_") or n.startswith("3B_"):
        return "3B"
    if n.startswith("4a_") or n.startswith("4A_") or p in ("Gantry", "Gantry_2"):
        return "4A"
    if n.startswith("4b_") or n.startswith("4B_") or p == "4b_Palletizer":
        return "4B"
    if n.startswith("5a_") or n.startswith("5A_") or "_W2" in n or n.startswith("HRL2"):
        return "5A"
    if n.startswith("5b_") or n.startswith("5B_") or p in ("5b_RFID", "Warehouse"):
        if n.startswith("5a_") or "_W2" in n:
            return "5A"
        return "5B"
    if p == "4a_4b_RFID_Readers":
        if "4a" in low or "reader 0" in low or "reader 1" in low:
            return "4A" if "4a" in low or "reader 1" in low else "RFID"
        if "reader 2" in low or "4b" in low:
            return "4B"
        if "reader 5" in low or "5b" in low:
            return "5B"
        return "RFID"
    if p == "Forderband":
        return "2A/2B Band"
    if "HMI_Prod" in n:
        return "HMI Übersicht"
    if n.startswith("HMI_") or n.startswith("HRL_") or n.startswith("Mode_") or n.startswith("Paket_"):
        return "5B"
    return p or "Sonstige"


STATION_SCL = {
    "1A": ["(kein FB — geplant) scl/Zone_1a_Metall/"],
    "1B": ["(kein FB — geplant) scl/Zone_1b_Kunststoff/"],
    "2A": [
        "scl/Zone_2a_Foerderbaender/FB_VisionReader_Metal.scl",
        "scl/Zone_2a_Foerderbaender/OB1_NW5_Metal_Vision.scl",
    ],
    "2B": ["scl/Zone_2b_Vision_Foerderbaender/FB_VisionReader.scl"],
    "2A/2B Band": ["(FUP-Bänder; SCL in der jeweiligen Zone)"],
    "3A": ["scl/Zone_3a_Metall_PickPlace/PickPlace_DigitalAnalog.scl"],
    "3B": [
        "scl/Zone_3a_Metall_PickPlace/PickPlace_DigitalAnalog.scl (2. Instanz, NW 18)",
    ],
    "4A": [
        "scl/Zone_4a_Metall_Palletizer_RFID/FB_GantryPickPlace.scl",
        "scl/Zone_4a_Metall_Palletizer_RFID/OB1_GantryPickPlace.scl",
        "scl/Zone_4a_Metall_Palletizer_RFID/OB1_RFID_Metal.scl",
        "scl/Zone_4b_Kunststoff_Palletizer_RFID/FB_RFID_ReadWrite.scl (Instanz Metall)",
    ],
    "4B": [
        "scl/Zone_4b_Kunststoff_Palletizer_RFID/FB_Palletizer.scl",
        "scl/Zone_4b_Kunststoff_Palletizer_RFID/OB1_Palletizer.scl",
        "scl/Zone_4b_Kunststoff_Palletizer_RFID/UDT_Palletizer.scl",
        "scl/Zone_4b_Kunststoff_Palletizer_RFID/FB_RFID_ReadWrite.scl",
        "scl/Zone_4b_Kunststoff_Palletizer_RFID/OB1_RFID_at_PickPlace.scl",
        "scl/Zone_4b_Kunststoff_Palletizer_RFID/OB1_Vision_RFID_before_Pallet.scl",
    ],
    "5A": [
        "scl/Zone_5a_Metall_Hochregallager/Hochregal_Automatik_Betrieb_W2.scl",
        "scl/Zone_5a_Metall_Hochregallager/OB1_NW28_Metal_Warehouse.scl",
        "scl/Zone_5a_Metall_Hochregallager/OB1_RFID_5a_DB4.scl",
        "scl/Zone_5a_Metall_Hochregallager/FB_Warehouse_Mode_Select_W2.scl",
        "scl/Zone_5a_Metall_Hochregallager/FB_Warehouse_Gate_W2.scl",
        "scl/Zone_5a_Metall_Hochregallager/FB_Warehouse_Stacker_IO_W2.scl",
        "scl/Zone_5a_Metall_Hochregallager/FB_Warehouse_Manual_Soll_W2.scl",
        "scl/Zone_5a_Metall_Hochregallager/FB_Warehouse_Actuators_W2.scl",
        "scl/Zone_5a_Metall_Hochregallager/FB_Einlagern_W2.scl",
        "scl/Zone_5a_Metall_Hochregallager/FB_Auslagern_W2.scl",
        "scl/Zone_5a_Metall_Hochregallager/FB_Suchen_W2.scl",
        "scl/Zone_5a_Metall_Hochregallager/FB_Loeschen_W2.scl",
        "scl/Zone_5a_Metall_Hochregallager/FB_Freies_Fach_Suchen_W2.scl",
        "scl/Zone_5a_Metall_Hochregallager/FB_Datenverwaltung_Lager_W2.scl",
        "scl/Zone_5a_Metall_Hochregallager/FB_Berechn_Offset_W2.scl",
        "scl/Zone_5a_Metall_Hochregallager/FB_Meldung_W2.scl",
        "scl/Zone_5a_Metall_Hochregallager/FB_Lagerstatus_W2.scl",
        "(NW 26 Bänder → W1: kein eigenes SCL, nur FUP)",
    ],
    "5B": [
        "scl/Zone_5b_Hochregallager/Hochregal_Automatik_Betrieb.scl",
        "scl/Zone_5b_Hochregallager/FB_Warehouse_Mode_Select.scl",
        "scl/Zone_5b_Hochregallager/FB_Warehouse_Gate.scl",
        "scl/Zone_5b_Hochregallager/FB_Warehouse_Stacker_IO.scl",
        "scl/Zone_5b_Hochregallager/FB_Warehouse_Manual_Soll.scl",
        "scl/Zone_5b_Hochregallager/FB_Warehouse_Actuators.scl",
        "scl/Zone_5b_Hochregallager/FB_Einlagern.scl",
        "scl/Zone_5b_Hochregallager/FB_Auslagern.scl",
        "scl/Zone_5b_Hochregallager/FB_Suchen.scl",
        "scl/Zone_5b_Hochregallager/FB_Loeschen.scl",
        "scl/Zone_5b_Hochregallager/FB_Freies_Fach_Suchen.scl",
        "scl/Zone_5b_Hochregallager/FB_Datenverwaltung_Lager.scl",
        "scl/Zone_5b_Hochregallager/FB_Berechn_Offset.scl",
        "scl/Zone_5b_Hochregallager/FB_Meldung.scl",
        "scl/Zone_5b_Hochregallager/FB_Lagerstatus.scl",
        "scl/Zone_5b_Hochregallager/FB_Hochregallager.scl (optional, nicht in OB1)",
        "scl/Zone_5a_Foerderband_Lager/OB1_NW27_Belts_to_Metal_Warehouse.scl",
    ],
    "RFID": [
        "scl/Zone_4b_Kunststoff_Palletizer_RFID/FB_RFID_ReadWrite.scl",
        "scl/Zone_4a_Metall_Palletizer_RFID/OB1_RFID_Metal.scl",
        "scl/Zone_4b_Kunststoff_Palletizer_RFID/OB1_RFID_at_PickPlace.scl",
        "scl/Zone_5a_Metall_Hochregallager/OB1_RFID_5a_DB4.scl",
    ],
    "HMI Übersicht": ["scl/HMI_Plant/OB1_Prod_PerDay.scl"],
    "Standard-Variablentabelle": ["(Querschnitt, z. B. Clock_Byte)"],
}

STATION_FUP = {
    "1A": "NW 1–2",
    "1B": "NW 4, 6",
    "2A": "NW 3, 5",
    "2B": "NW 7–8",
    "2A/2B Band": "NW 3 / 8 / 26 / 27",
    "3A": "NW 9–12",
    "3B": "NW 17–20",
    "4A": "NW 13–16, 21",
    "4B": "NW 22–25",
    "5A": "NW 26, 28 Warehouse_2",
    "5B": "NW 27, 29 Warehouse_1",
    "RFID": "Reader 0–5 FIO",
    "HMI Übersicht": "TP Header",
    "Sonstige": "—",
    "Standard-Variablentabelle": "—",
}

SCL_SHORT = {
    "1A": "— (P)",
    "1B": "— (P)",
    "2A": "FB_VisionReader_Metal.scl",
    "2B": "FB_VisionReader.scl",
    "2A/2B Band": "—",
    "3A": "PickPlace_DigitalAnalog.scl",
    "3B": "PickPlace_DigitalAnalog.scl (2.)",
    "4A": "FB_GantryPickPlace.scl · RFID",
    "4B": "FB_Palletizer.scl · FB_RFID_ReadWrite.scl",
    "5A": "Hochregal_Automatik_Betrieb_W2.scl · FB_*_W2",
    "5B": "Hochregal_Automatik_Betrieb.scl · Warehouse_1 FBs",
    "RFID": "FB_RFID_ReadWrite.scl",
    "HMI Übersicht": "OB1_Prod_PerDay.scl",
    "Standard-Variablentabelle": "—",
}

STATION_ORDER = [
    "1A",
    "1B",
    "2A",
    "2B",
    "2A/2B Band",
    "3A",
    "3B",
    "4A",
    "4B",
    "5A",
    "5B",
    "RFID",
    "HMI Übersicht",
    "Standard-Variablentabelle",
    "Sonstige",
]


def main() -> None:
    wb = openpyxl.load_workbook(SRC, data_only=True)
    ws = wb["PLC Tags"]
    rows = list(ws.iter_rows(min_row=2, values_only=True))
    tags = []
    for r in rows:
        name, path, dtype, addr, comment = r[0], r[1], r[2], r[3], r[4]
        if not name:
            continue
        tags.append(
            {
                "Name": name,
                "Path": path or "",
                "DataType": dtype or "",
                "Address": addr or "",
                "Comment": comment or "",
                "FIO": "FIO" if is_fio(str(addr or "")) else "PLC",
                "Station": station_of(str(name), str(path or "")),
            }
        )

    lines = ["Name;Path;Data Type;Logical Address;Comment;Kind;Station"]
    for t in tags:
        c = str(t["Comment"]).replace(";", ",")
        lines.append(
            f"{t['Name']};{t['Path']};{t['DataType']};{t['Address']};{c};{t['FIO']};{t['Station']}"
        )
    CSV_OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    by_st = defaultdict(list)
    for t in tags:
        by_st[t["Station"]].append(t)

    extra = sorted(k for k in by_st if k not in STATION_ORDER)

    md = []
    md.append("# Stationen — SCL, FUP, SPS-Tags und Factory I/O")
    md.append("")
    md.append("Quelle Tags: `PLCTags3.xlsx`. SCL: `scl/` im Repository.")
    md.append("CSV: [`PLCTags3_live.csv`](PLCTags3_live.csv).")
    md.append("")
    md.append("**FIO** = Prozessabbild (`%E` / `%A` / `%ED` / `%AD` …) ↔ Factory I/O Driver.")
    md.append("**PLC** = Merker/DB (`%M` …) in der SPS.")
    md.append("")
    md.append(f"Gesamt: **{len(tags)}** Tags.")
    md.append("")

    md.append("| Station | FUP | SCL | Tags | FIO | PLC |")
    md.append("|---|---|---|---:|---:|---:|")
    for st in STATION_ORDER + extra:
        items = by_st.get(st, [])
        if not items:
            continue
        fio = sum(1 for t in items if t["FIO"] == "FIO")
        plc = len(items) - fio
        md.append(
            f"| **{st}** | {STATION_FUP.get(st, '—')} | `{SCL_SHORT.get(st, '—')}` | {len(items)} | {fio} | {plc} |"
        )
    md.append("")

    def tag_rows(items, kind):
        sel = [t for t in items if t["FIO"] == kind]
        return sorted(sel, key=lambda t: (t["Address"] or "", t["Name"]))

    def md_tag_table(title, rows):
        md.append(f"### {title}")
        md.append("")
        if not rows:
            md.append("*(keine)*")
            md.append("")
            return
        md.append("| Tag | Adresse | Typ | Tabelle | Kommentar |")
        md.append("|---|---|---|---|---|")
        for t in rows:
            c = str(t["Comment"]).replace("|", "\\|").replace("\n", " ")
            md.append(
                f"| `{t['Name']}` | `{t['Address']}` | {t['DataType']} | {t['Path']} | {c} |"
            )
        md.append("")

    for st in STATION_ORDER + extra:
        items = by_st.get(st, [])
        if not items:
            continue
        fio_items = tag_rows(items, "FIO")
        plc_items = tag_rows(items, "PLC")
        md.append(f"## {st}")
        md.append("")
        md.append(
            f"FUP: {STATION_FUP.get(st, '—')} · Tags: {len(items)} "
            f"(Factory I/O {len(fio_items)} · SPS {len(plc_items)})"
        )
        md.append("")
        scls = STATION_SCL.get(st)
        if scls:
            md.append("### SCL")
            md.append("")
            for f in scls:
                if f.startswith("scl/") or ".scl" in f:
                    md.append(f"- `{f}`")
                else:
                    md.append(f"- {f}")
            md.append("")
        md_tag_table(f"Factory I/O ({len(fio_items)})", fio_items)
        md_tag_table(f"SPS / PLC-Merker ({len(plc_items)})", plc_items)

    md.append("Zurück: [Pflichtenheft.md](Pflichtenheft.md) · [PLC_Networks.md](PLC_Networks.md)")
    md.append("")
    MD_OUT.write_text("\n".join(md), encoding="utf-8")
    print(f"Wrote {CSV_OUT} ({len(tags)} tags)")
    print(f"Wrote {MD_OUT}")
    print("stations", {k: len(v) for k, v in sorted(by_st.items())})


if __name__ == "__main__":
    main()
