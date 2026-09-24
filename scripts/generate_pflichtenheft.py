# -*- coding: utf-8 -*-
"""Generate Pflichtenheft (how / implementation) as Word .docx — Lastenheft codes → SCL."""
from pathlib import Path
import sys
from collections import defaultdict
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

OUT = Path(__file__).resolve().parents[1] / "docs" / "01_Projektgrundlagen" / "Pflichtenheft_Abschlussprojekt.docx"
sys.path.insert(0, str(Path(__file__).resolve().parent))
from export_plctags3_stations import (  # noqa: E402
    CSV_OUT,
    SCL_SHORT,
    STATION_FUP,
    STATION_ORDER,
    STATION_SCL,
)


def set_run_font(run, name="Calibri", size=11, bold=False):
    run.font.name = name
    run.font.size = Pt(size)
    run.bold = bold
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.append(rFonts)
    rFonts.set(qn("w:ascii"), name)
    rFonts.set(qn("w:hAnsi"), name)
    rFonts.set(qn("w:cs"), name)
    rFonts.set(qn("w:eastAsia"), name)
    lang = rPr.find(qn("w:lang"))
    if lang is None:
        lang = OxmlElement("w:lang")
        rPr.append(lang)
    lang.set(qn("w:val"), "de-DE")
    lang.set(qn("w:eastAsia"), "de-DE")
    lang.set(qn("w:bidi"), "de-DE")


def add_heading_styled(doc, text, level=1):
    p = doc.add_heading(text, level=level)
    for run in p.runs:
        set_run_font(run, size=16 if level == 1 else 13 if level == 2 else 12, bold=True)
    return p


def add_para(doc, text, bold=False, size=11, space_after=8):
    p = doc.add_paragraph()
    run = p.add_run(text)
    set_run_font(run, size=size, bold=bold)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.space_before = Pt(0)
    return p


def add_bullet(doc, text, level=0):
    p = doc.add_paragraph(text, style="List Bullet")
    if level:
        p.paragraph_format.left_indent = Cm(1.25 * level)
    for run in p.runs:
        set_run_font(run)
    return p


def set_cell_shading(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), hex_color)
    shd.set(qn("w:val"), "clear")
    tcPr.append(shd)


def add_table(doc, headers, rows, col_widths=None):
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = table.rows[0].cells
    for i, h in enumerate(headers):
        hdr[i].text = ""
        p = hdr[i].paragraphs[0]
        run = p.add_run(h)
        set_run_font(run, size=9, bold=True)
        set_cell_shading(hdr[i], "1F4E79")
        run.font.color.rgb = RGBColor(255, 255, 255)
    for r_idx, row in enumerate(rows):
        cells = table.rows[r_idx + 1].cells
        for c_idx, val in enumerate(row):
            cells[c_idx].text = ""
            p = cells[c_idx].paragraphs[0]
            run = p.add_run(str(val))
            set_run_font(run, size=8)
            if r_idx % 2 == 1:
                set_cell_shading(cells[c_idx], "F2F2F2")
    if col_widths:
        for row in table.rows:
            for i, w in enumerate(col_widths):
                row.cells[i].width = Cm(w)
    doc.add_paragraph()
    return table


def setup_doc():
    doc = Document()
    section = doc.sections[0]
    section.top_margin = Cm(2.2)
    section.bottom_margin = Cm(2.2)
    section.left_margin = Cm(2.0)
    section.right_margin = Cm(2.0)
    normal = doc.styles["Normal"]
    normal.font.name = "Calibri"
    normal.font.size = Pt(11)
    n_rPr = normal.element.get_or_add_rPr()
    n_fonts = n_rPr.find(qn("w:rFonts"))
    if n_fonts is None:
        n_fonts = OxmlElement("w:rFonts")
        n_rPr.append(n_fonts)
    n_fonts.set(qn("w:ascii"), "Calibri")
    n_fonts.set(qn("w:hAnsi"), "Calibri")
    n_lang = n_rPr.find(qn("w:lang"))
    if n_lang is None:
        n_lang = OxmlElement("w:lang")
        n_rPr.append(n_lang)
    n_lang.set(qn("w:val"), "de-DE")
    return doc


def load_csv_tags():
    tags = []
    if not CSV_OUT.exists():
        return tags
    for i, line in enumerate(CSV_OUT.read_text(encoding="utf-8").splitlines()):
        if i == 0 or not line.strip():
            continue
        parts = line.split(";")
        if len(parts) < 7:
            continue
        tags.append(
            {
                "Name": parts[0],
                "Path": parts[1],
                "DataType": parts[2],
                "Address": parts[3],
                "Comment": parts[4],
                "FIO": parts[5],
                "Station": parts[6],
            }
        )
    return tags


def build():
    doc = setup_doc()

    for _ in range(2):
        doc.add_paragraph()
    t = doc.add_paragraph()
    t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = t.add_run("PFLICHTENHEFT")
    set_run_font(r, size=28, bold=True)

    st = doc.add_paragraph()
    st.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = st.add_run("Umsetzung der Lastenheft-Anforderungen\nin TIA Portal / SCL / Factory I/O")
    set_run_font(r, size=16, bold=True)

    doc.add_paragraph()
    meta = [
        ("Projekttitel", "Entwicklung einer automatisierten Produktions-, Montage- und Lagerverwaltungsanlage"),
        ("Bezug", "Lastenheft Abschlussprojekt Version 1.6 (Was)"),
        ("Dieses Dokument", "Pflichtenheft Version 1.3 (Wie) — Stationen × FUP × SCL × alle PLCTags3 FIO/SPS"),
        ("Autor / Teilnehmer", "Dereje Hailemariam"),
        ("Ort", "Berlin"),
        ("Dokumentstand", "September 2026"),
        ("Werkzeuge", "TIA Portal V20, SCL, Factory I/O, PLCSIM, TP2200, Streamlit"),
        ("Repository", "scl/ … Zone_1a … Zone_5b; docs/; nodered/; Lagerverwaltung Online"),
        ("Status-Spalte", "U = umgesetzt · T = teilweise · P = geplant"),
    ]
    for label, value in meta:
        p = doc.add_paragraph()
        r1 = p.add_run(f"{label}: ")
        set_run_font(r1, bold=True)
        r2 = p.add_run(value)
        set_run_font(r2)

    doc.add_page_break()

    add_heading_styled(doc, "Inhaltsverzeichnis", 1)
    for item in [
        "1  Zweck und Abgrenzung zum Lastenheft",
        "2  Traceability: Lastenheft-Code → SCL / FUP",
        "3  Sprachen: SCL und FUP",
        "4  FUP-Codes (OB1-Netzwerke NW 1–29)",
        "4.1  Stationen — Übersicht SCL / FUP / Tags",
        "4.2  Stationen — alle Factory-I/O- und SPS-Tags",
        "5  SCL-Codes (Quelldateien im Repository)",
        "6  Produktcodes (Artikelnummer, RFID_CODE)",
        "7  Lager-Info_Code 0–17",
        "8  Automatik-State (HMI_State)",
        "9  RFID Status_Code",
        "10  HMI- und Testcodes",
        "11  Verweise",
    ]:
        add_para(doc, item, space_after=4)
    doc.add_page_break()

    add_heading_styled(doc, "1  Zweck und Abgrenzung zum Lastenheft", 1)
    add_para(
        doc,
        "Das Lastenheft beschreibt, was die Anlage leisten muss (Anforderungscodes AF, NF, HW, "
        "OB, SW, HM, SI, T). Dieses Pflichtenheft beschreibt, wie das im Repository und in TIA "
        "umgesetzt ist: SCL-Quelldateien, FUP-Netzwerke in OB1, Tags, DBs und numerische Codes "
        "(Info_Code, State, RFID Status_Code, Produktcodierung).",
    )
    add_table(
        doc,
        ["Dokument", "Frage", "Inhalt"],
        [
            ("Lastenheft v1.6", "Was?", "Anforderungen, Scope, Abnahme T-01…T-09"),
            ("Pflichtenheft v1.3", "Wie?", "SCL-Dateien, FUP-NW, alle PLCTags3 je Station"),
            ("Gesamtanlage.md", "Kontext", "Materialfluss, Zonen, Stand"),
        ],
        col_widths=[4.5, 2.5, 9],
    )
    add_para(
        doc,
        "Abweichung zum Lastenheft AF-32a (W2 Phase1 Sensor-only): Warehouse_2-Gate ist "
        "umgesetzt als Sensor UND (2a_VisionData_Combo_Done ODER 4a_RFID_Done). Automatik W2 "
        "überspringt State 10 (Reader 0) und übernimmt Produktdaten von 4a / Vision.",
    )

    add_heading_styled(doc, "2  Traceability: Lastenheft-Code → SCL / FUP", 1)
    add_heading_styled(doc, "2.1  Allgemein / Querschnitt", 2)
    add_table(
        doc,
        ["Code", "Umsetzung (SCL / TIA)", "St."],
        [
            ("AF-01", "TIA V20 · CPU 1518F · FUP OB1 NW 1–29 · SCL-FBs", "U"),
            ("AF-02", "Factory I/O Driver-Mapping; Tags in PLC_Tags_*.csv", "U"),
            ("AF-03", "Ein TP2200 HMI_1; docs/03_Technik/HMI_Gesamtanlage.md", "T"),
            ("AF-04", "FB_Warehouse_Mode_Select / _W2 · Einricht > Auto / Hand", "U"),
            ("AF-05", "FB_Meldung / _W2 · Info_Code 0–17 · gldb_Meldungen", "U"),
        ],
        col_widths=[2.2, 12.3, 1.5],
    )

    add_heading_styled(doc, "2.2  Vision (AF-10…14)", 2)
    add_table(
        doc,
        ["Code", "Umsetzung (SCL / TIA)", "St."],
        [
            ("AF-10", "FB_VisionReader · NW 7 · scl/Zone_2b_Vision_Foerderbaender/", "U"),
            ("AF-11", "Gültig 1…6; 7…9 → Lid/Base_Reject_Metal", "U"),
            ("AF-12", "Color_Code 1/2/3 · Materialart=1 · ProductTyp · Artikelnummer gelatcht", "U"),
            ("AF-13", "RFID_CODE = YYMMDD×1000 + Materialart×100 + Color_Code", "U"),
            ("AF-14", "FB_RFID_ReadWrite Job 11 · Allow_Write := 4b_Done · ein Puls", "U"),
            ("AF-52", "FB_VisionReader_Metal · NW 5 · 2a_VisionData_Combo_Done %M56.0", "U"),
        ],
        col_widths=[2.2, 12.3, 1.5],
    )

    add_heading_styled(doc, "2.3  RFID (AF-20…25)", 2)
    add_table(
        doc,
        ["Code", "Umsetzung (SCL / TIA)", "St."],
        [
            ("AF-20", "FB_RFID_ReadWrite.scl · Command/Execute/Command ID/Status · Hold ≥100 ms", "U"),
            ("AF-21", "Index 0 RFID_CODE · 1 Artikelnummer · 2 Materialart · 3 ProductTyp", "U"),
            ("AF-22", "DB_1 Reader 2 Write (4B) · DB_2 Reader 5 Read (5B) · 4a DB_103 Reader 1", "U"),
            ("AF-23", "Pallet_Tagged %M40.2 / %M22.5 · Combo_Done %M40.0 (Kunststoff)", "U"),
            ("AF-24", "NW 25 Write · NW 29 Read · Metall NW 16/21 OB1_RFID_Metal.scl", "U"),
            ("AF-25", "Status_Code 0/1/10 · HMI Reset %M30.5 / %M61.5 / %M71.5", "U"),
        ],
        col_widths=[2.2, 12.3, 1.5],
    )

    add_heading_styled(doc, "2.4  Hochregallager (AF-30…38)", 2)
    add_table(
        doc,
        ["Code", "Umsetzung (SCL / TIA)", "St."],
        [
            ("AF-30", "W1 NW 29 · gldb_LagerverwaltungData.Fach[1..54] · UDT_Fach", "U"),
            ("AF-30a", "W2 NW 28 · *_W2 DBs/Tags · Stacker Crane 1 · %M70+", "U"),
            ("AF-31", "UDT_Fach: Materialart, Color, Artikel, Typ, RFID, Pos X/Z, Belegt, Gesperrt", "U"),
            ("AF-32", "FB_Freies_Fach_Suchen · Automatik States 20–60 · FB_Einlagern", "U"),
            ("AF-32a", "FB_Warehouse_Gate / _W2 · Vor_Regal UND (Combo ODER Tagged/4a_Done)", "U"),
            ("AF-33", "FB_Auslagern / _W2 · FB_Suchen (RFID→Artikel→Fach) · Sequenz Automatik begrenzt", "T"),
            ("AF-34", "FB_Loeschen · FB_Suchen · HMI_Loeschen / HMI_Suchen (+ _W2)", "U"),
            ("AF-34a", "Streamlit app.py · SQLite · ohne SPS-Änderung · HM-07 / T-09", "U"),
            ("AF-35", "FB_Berechn_Offset · HMI_Raster_Berechnen · Manual Soll / Jog", "U"),
            ("AF-36", "W1 State 10 Reader 5 · W2 State 10 Durchlauf, Daten von 4a/Vision", "U"),
            ("AF-37", "Gate sperrt Auto-Einlagern ohne Write-OK / Combo", "U"),
            ("AF-38", "Mode_Auto + Paket_Fuer_Hochregal → Start ohne HMI_Start_Einlagern", "U"),
        ],
        col_widths=[2.2, 12.3, 1.5],
    )

    add_heading_styled(doc, "2.5  Montage, Förderer, HMI, Sicherheit", 2)
    add_table(
        doc,
        ["Code", "Umsetzung (SCL / TIA)", "St."],
        [
            ("AF-40", "PickPlace_DigitalAnalog.scl · NW 10 Metall · NW 18 Kunststoff", "U"),
            ("AF-41", "NW 11 Waage 1 · NW 19 Waage 2", "T"),
            ("AF-42", "FB_GantryPickPlace · NW 15 · OB1_GantryPickPlace.scl", "U"),
            ("AF-43", "FB_Palletizer · NW 24 · OB1_Palletizer.scl · RFID NW 25", "U"),
            ("AF-50", "scl/Zone_1a_Metall · Zone_1b_Kunststoff · NW 1–2, 4, 6", "P"),
            ("AF-51", "NW 3 Metallband · NW 8 Kunststoffband · NW 26/27 Lagerbänder", "T"),
            ("NF-01", "Getrennte FBs je Zone / Querschnitt (Vision, RFID, Lager, P&P)", "U"),
            ("NF-07", "Web schreibt nicht gldb_LagerverwaltungData · HMI_Suchen bleibt SPS", "U"),
            ("HW-01", "Hardware_SPS.md · CPU 1518F · TP2200", "U"),
            ("HW-02 / OB-01", "OB100 vorgesehen, noch nicht im Sweep — SI-05 Soll", "P"),
            ("SW-01", "FUP OB1 NW 1–29 sequenziell · SCL nur in FBs · PLC_Networks.md", "U"),
            ("HM-01…07", "HMI_Tags_*.csv · Übersicht Prod/Tag · Web Streamlit (HM-07)", "T"),
            ("SI-01", "HMI_Stop / Not_Aus · Automatik unterbricht", "U"),
            ("SI-02", "FB_Warehouse_Mode_Select: Einricht räumt Auto/Hand", "U"),
        ],
        col_widths=[2.8, 11.7, 1.5],
    )

    add_heading_styled(doc, "3  Sprachen: SCL und FUP", 1)
    add_para(
        doc,
        "Zwei Programmiersprachen in TIA Portal: Die Ablauf- und Rechenlogik liegt in SCL "
        "(Structured Control Language, Quelle im Git). Das zyklische Hauptprogramm OB1 ist in "
        "FUP (Funktionsplan / FBD) verdrahtet: jedes Netzwerk ruft die zugehörigen SCL-FBs auf "
        "und verbindet Ein-/Ausgänge. Keine doppelte Logik in FUP — nur Aufrufe und Glue.",
    )
    add_table(
        doc,
        ["Sprache", "TIA-Name", "Wo", "Inhalt"],
        [
            ("SCL", "SCL / ST", "scl/**/*.scl  (Git)", "FBs, Sequenzen, Formeln, States"),
            ("FUP", "FBD / Funktionsplan", "TIA OB1 NW 1–29", "FB-Aufrufe, I/O-Verdrahtung"),
            ("UDT", "PLC-Datentyp", "scl/**/*.udt.txt", "Fach, Raster, HMI, RFID-Produkt"),
        ],
        col_widths=[2.2, 3.5, 5, 5.3],
    )

    add_heading_styled(doc, "4  FUP-Codes (OB1-Netzwerke NW 1–29)", 1)
    add_para(
        doc,
        "FUP-Code = Netzwerknummer in Main OB1. Titel laut TIA (PLC_Networks.md). "
        "Zone 1 CNC ohne SCL-FB (P). Legacy-Ordner scl/Zone3_PickPlace und scl/Zone4_Palettierer nicht in OB1 verdrahten.",
    )
    add_table(
        doc,
        ["FUP", "Zone", "TIA-Netzwerktitel (kurz)", "SCL-Aufruf"],
        [
            ("NW 1", "1A", "Metal Raw Material input", "— (P)"),
            ("NW 2", "1A", "Metal Robot (CNC) station", "— (P)"),
            ("NW 3", "2A", "Metal Conveyor Belts after CNC", "— (T)"),
            ("NW 4", "1B", "Plastic Raw Material input", "— (P)"),
            ("NW 5", "2A", "VisionData Sensors (Metall)", "FB_VisionReader_Metal · OB1_NW5_Metal_Vision.scl"),
            ("NW 6", "1B", "Plastic Robot (CNC) station", "— (P)"),
            ("NW 7", "2B", "VisionData Sensors (Kunststoff)", "FB_VisionReader.scl (FB17)"),
            ("NW 8", "2B", "Plastic Conveyor Belts after CNC", "— (T)"),
            ("NW 9", "3A", "Metal belts before P&P", "— (T)"),
            ("NW 10", "3A", "Metal Pick And Place 1", "PickPlace_DigitalAnalog.scl"),
            ("NW 11", "3A", "Metal Waage 1", "— (T)"),
            ("NW 12", "3A", "Metal belts after scale", "— (T)"),
            ("NW 13–14", "4A", "Belts / roller before palletizer", "— (T)"),
            ("NW 15", "4A", "Metal Assembly Palletizer", "FB_GantryPickPlace · OB1_GantryPickPlace.scl"),
            ("NW 16", "4A", "Metal Components RFID", "OB1_RFID_Metal.scl · FB_RFID_ReadWrite"),
            ("NW 17", "3B", "Plastic belts before P&P", "— (T)"),
            ("NW 18", "3B", "Plastic Pick and Place 2", "PickPlace_DigitalAnalog.scl (2. Instanz)"),
            ("NW 19", "3B", "Plastic scale 2", "— (T)"),
            ("NW 20", "3B", "Plastic belts after scale", "— (T)"),
            ("NW 21", "4A", "Metal RFID (zusätzlich)", "wie NW 16"),
            ("NW 22–23", "4B", "Belts / roller before palletizer", "— (T)"),
            ("NW 24", "4B", "Plastic Assembly Palletizer", "FB_Palletizer · OB1_Palletizer.scl"),
            ("NW 25", "4B", "Plastic RFID Write Reader 2", "FB_RFID_ReadWrite · OB1_RFID_at_PickPlace.scl"),
            ("NW 26", "5A", "Belts to plastic warehouse", "Zone_5a_Foerderband_Lager (T)"),
            ("NW 27", "5B", "Belts to metal warehouse", "OB1_NW27_Belts_to_Metal_Warehouse.scl"),
            ("NW 28", "5A", "Metal Components Warehouse W2", "OB1_NW28_Metal_Warehouse.scl + FBs *_W2"),
            ("NW 29", "5B", "Plastic Components Warehouse W1", "FUP-Aufrufe laut WAREHOUSE_1_SETUP.md §3"),
        ],
        col_widths=[2.2, 1.5, 5.3, 7],
    )

    add_heading_styled(doc, "4.1  Stationen — Übersicht SCL / FUP / Tags", 2)
    add_para(
        doc,
        "TIA-Export PLCTags3.xlsx. FIO = Prozessabbild %E/%A/%ED/%AD ↔ Factory I/O Driver. "
        "PLC = Merker %M. Alle Tags stehen in Abschnitt 4.2 (eine Tabelle Factory I/O und "
        "eine Tabelle SPS je Station) sowie in Station_PLC_FIO_Tags.md / PLCTags3_live.csv.",
    )
    add_table(
        doc,
        ["Station", "FUP", "SCL (Dateien)", "Factory I/O (Kennwerte)", "SPS (Kennwerte)"],
        [
            (
                "1A Metall Roh",
                "NW 1–2",
                "kein FB — scl/Zone_1a_Metall/ (P)",
                "Emitter %A0.0/.1 · Sensor %E0.0/.1 · Band %A0.2/.3",
                "—",
            ),
            (
                "1B Kunststoff Roh",
                "NW 4, 6",
                "kein FB — scl/Zone_1b_Kunststoff/ (P)",
                "Emitter %A1.1/.2 · Sensor %E1.0/.1 · Band %A1.0/.3",
                "—",
            ),
            (
                "2A Band + Vision Metall",
                "NW 3, 5",
                "FB_VisionReader_Metal.scl · OB1_NW5_Metal_Vision.scl",
                "Bänder %A2.x/%E2.x · Vision Lid/Base %ED170/%ED174",
                "Combo_Done %M56.0 · RFID_CODE %MD276",
            ),
            (
                "2B Band + Vision Kunststoff",
                "NW 7–8",
                "FB_VisionReader.scl",
                "Bänder %A3.x/%E3.x · Vision Lid/Base %ED142/%ED146",
                "Combo_Done %M40.0 · Color %MW50",
            ),
            (
                "3A 2-axis P&P + Waage 1",
                "NW 9–12",
                "PickPlace_DigitalAnalog.scl",
                "P&P Moving/Grab %E5/%A4–5 · Ist X/Z %ED30/%ED34 · Soll %AD16/%AD20 · Waage %ED38",
                "3a_Material_Placed %M0.2",
            ),
            (
                "3B 2-axis P&P + Waage 2",
                "NW 17–20",
                "PickPlace_DigitalAnalog.scl (2. Instanz)",
                "Ist X/Z %ED54/%ED58 · Soll %AD28/%AD32 · Waage 2 %ED62",
                "3b_Pick_and_Place_Done %M0.3",
            ),
            (
                "4A 3-axis P&P + RFID Reader 1",
                "NW 13–16, 21",
                "FB_GantryPickPlace.scl · OB1_GantryPickPlace.scl · OB1_RFID_Metal.scl",
                "P&P Ist X/Y/Z %ED42/46/50 · Soll %AD40/44/48 · Reader 1 Status %ED102 Execute %A9.0",
                "4a_HMI_* %M8 · 4a_RFID_Code_Out %MD236",
            ),
            (
                "4B Palettierer + RFID Reader 2",
                "NW 22–25",
                "FB_Palletizer.scl · FB_RFID_ReadWrite.scl · OB1_Palletizer.scl",
                "P&P Ist %ED86/90/94 · Soll %AD60/64/68 · Reader 2 Status %ED130 Execute %A11.1",
                "Pallet_Tagged / Vision %M40",
            ),
            (
                "5A Band + Warehouse_2 Crane 1",
                "NW 26, 28",
                "Hochregal_Automatik_Betrieb_W2.scl · OB1_NW28_Metal_Warehouse.scl · FB_*_W2.scl",
                "Bänder %A12/%E12 · Crane 1 Ist %ED178/%ED182 Soll %AD144/%AD148 · Reader 0 %ED114 %A15.4",
                "Mode/HMI %M70+ · HMI_State_W2 %MW228",
            ),
            (
                "5B Band + Warehouse_1 Crane 0",
                "NW 27, 29",
                "Hochregal_Automatik_Betrieb.scl · FB_Warehouse_*.scl · OB1_NW27_….scl",
                "Bänder %A13/%E13 · Crane 0 Ist %ED162/%ED166 Soll %AD136/%AD140 · Reader 5 %ED150 %A13.7",
                "Mode/HMI %M60+ · HMI_State %MW128",
            ),
        ],
        col_widths=[3.2, 2.2, 3.4, 4.2, 3],
    )

    add_heading_styled(doc, "4.2  Stationen — alle Factory-I/O- und SPS-Tags", 2)
    csv_tags = load_csv_tags()
    by_st = defaultdict(list)
    for t in csv_tags:
        by_st[t["Station"]].append(t)
    extra = sorted(k for k in by_st if k not in STATION_ORDER)
    add_para(
        doc,
        f"{len(csv_tags)} Tags aus PLCTags3_live.csv. Je Station: SCL-Dateien, dann vollständige "
        "Factory-I/O-Tabelle (%E/%A/%ED/%AD) und SPS-Tabelle (%M).",
    )
    for st in STATION_ORDER + extra:
        items = by_st.get(st, [])
        if not items:
            continue
        fio_items = sorted(
            [t for t in items if t["FIO"] == "FIO"],
            key=lambda t: (t["Address"], t["Name"]),
        )
        plc_items = sorted(
            [t for t in items if t["FIO"] == "PLC"],
            key=lambda t: (t["Address"], t["Name"]),
        )
        add_heading_styled(
            doc,
            f"Station {st} — {STATION_FUP.get(st, '—')} — {len(items)} Tags "
            f"(FIO {len(fio_items)} / SPS {len(plc_items)})",
            3,
        )
        scls = STATION_SCL.get(st) or [SCL_SHORT.get(st, "—")]
        add_para(doc, "SCL: " + " · ".join(scls), size=9)
        add_table(
            doc,
            ["Factory I/O Tag", "Adresse", "Typ", "Tabelle", "Kommentar"],
            [
                (t["Name"], t["Address"], t["DataType"], t["Path"], t["Comment"])
                for t in fio_items
            ]
            or [("—", "—", "—", "keine FIO-Tags", "")],
            col_widths=[5.2, 2.2, 1.6, 3.2, 3.8],
        )
        add_table(
            doc,
            ["SPS / PLC-Merker", "Adresse", "Typ", "Tabelle", "Kommentar"],
            [
                (t["Name"], t["Address"], t["DataType"], t["Path"], t["Comment"])
                for t in plc_items
            ]
            or [("—", "—", "—", "keine SPS-Merker", "")],
            col_widths=[5.2, 2.2, 1.6, 3.2, 3.8],
        )

    add_heading_styled(doc, "5  SCL-Codes (Quelldateien im Repository)", 1)
    add_heading_styled(doc, "5.1  Vision, RFID, Handling", 2)
    add_table(
        doc,
        ["SCL-Datei", "Lastenheft", "FUP"],
        [
            ("Zone_2a_Foerderbaender/FB_VisionReader_Metal.scl", "AF-52", "NW 5"),
            ("Zone_2a_Foerderbaender/OB1_NW5_Metal_Vision.scl", "AF-52", "NW 5 Glue"),
            ("Zone_2b_Vision_Foerderbaender/FB_VisionReader.scl", "AF-10…13", "NW 7"),
            ("Zone_3a_Metall_PickPlace/PickPlace_DigitalAnalog.scl", "AF-40", "NW 10 / 18"),
            ("Zone_4a_Metall_Palletizer_RFID/FB_GantryPickPlace.scl", "AF-42", "NW 15"),
            ("Zone_4a_Metall_Palletizer_RFID/OB1_GantryPickPlace.scl", "AF-42", "NW 15"),
            ("Zone_4a_Metall_Palletizer_RFID/OB1_RFID_Metal.scl", "AF-24", "NW 16/21"),
            ("Zone_4b_Kunststoff_Palletizer_RFID/FB_Palletizer.scl", "AF-43", "NW 24"),
            ("Zone_4b_Kunststoff_Palletizer_RFID/OB1_Palletizer.scl", "AF-43", "NW 24"),
            ("Zone_4b_Kunststoff_Palletizer_RFID/FB_RFID_ReadWrite.scl", "AF-20…25", "NW 25 / 16"),
            ("Zone_4b_Kunststoff_Palletizer_RFID/OB1_RFID_at_PickPlace.scl", "AF-14, AF-22", "NW 25"),
            ("Zone_4b_Kunststoff_Palletizer_RFID/OB1_Vision_RFID_before_Pallet.scl", "AF-14", "Glue 4B"),
            ("HMI_Plant/OB1_Prod_PerDay.scl", "HM-01", "Übersicht"),
        ],
        col_widths=[9.5, 3.3, 3.2],
    )
    add_heading_styled(doc, "5.2  Warehouse_1 Kunststoff (FUP NW 29)", 2)
    add_table(
        doc,
        ["SCL-Datei", "Lastenheft", "Rolle"],
        [
            ("Hochregal_Automatik_Betrieb.scl", "AF-32, 36–38", "Sequenz Einlagern"),
            ("FB_Warehouse_Mode_Select.scl", "AF-04, SI-02", "Einricht / Auto / Hand"),
            ("FB_Warehouse_Gate.scl", "AF-32a, 37", "Paket_Fuer_Hochregal"),
            ("FB_Warehouse_Stacker_IO.scl", "AF-32", "Kran Ist/Soll FIO"),
            ("FB_Warehouse_Manual_Soll.scl", "AF-35", "Einricht Jog / Band"),
            ("FB_Warehouse_Actuators.scl", "SI-01", "Leuchte / Sirene"),
            ("FB_Einlagern.scl / FB_Auslagern.scl", "AF-32 / 33", "DB belegen / freigeben"),
            ("FB_Suchen.scl / FB_Loeschen.scl", "AF-34", "RFID→Artikel→Fach / löschen"),
            ("FB_Freies_Fach_Suchen.scl", "AF-32", "nächstes freies Fach"),
            ("FB_Datenverwaltung_Lager.scl", "AF-31, HM-04", "HMI-Spiegel, Zählung"),
            ("FB_Berechn_Offset.scl", "AF-35", "Raster Fach → X/Z"),
            ("FB_Meldung.scl", "AF-05", "Info_Code 0–17"),
            ("FB_Lagerstatus.scl", "AF-05", "Belegt/Frei-Text"),
            ("FB_Hochregallager.scl", "—", "Optional Wrapper, nicht in OB1"),
            ("Zone_5a_Foerderband_Lager/OB1_NW27_….scl", "AF-51", "FUP NW 27 Band → W2"),
        ],
        col_widths=[7.5, 3.5, 5],
    )
    add_heading_styled(doc, "5.3  Warehouse_2 Metall (FUP NW 28)", 2)
    add_table(
        doc,
        ["SCL-Datei", "Lastenheft", "Rolle"],
        [
            ("Hochregal_Automatik_Betrieb_W2.scl", "AF-30a, 36", "Sequenz; State 10 Skip"),
            ("OB1_NW28_Metal_Warehouse.scl", "AF-30a", "FUP-Glue NW 28"),
            ("OB1_RFID_5a_DB4.scl", "AF-24", "Reader 0 optional"),
            ("FB_*_W2.scl (Gate, Mode, Stacker, Manual, Actuators)", "AF-04, 32a", "Mirror W1"),
            ("FB_Einlagern_W2 / Auslagern_W2 / Suchen_W2 / Loeschen_W2", "AF-32…34", "Lagerdaten W2"),
            ("FB_Freies_Fach_Suchen_W2 / Datenverwaltung_W2 / Offset_W2", "AF-32, 35", "Fach / Raster"),
            ("FB_Meldung_W2 / FB_Lagerstatus_W2", "AF-05", "Info_Code W2"),
        ],
        col_widths=[8.2, 3.3, 4.5],
    )
    add_para(
        doc,
        "DBs: gldb_LagerverwaltungData / _W2, gldb_AktuellerFach_HMI / _W2, gldb_Meldungen. "
        "UDTs: UDT_Fach, UDT_Lager_Raster, UDT_RFID_Product, HMI-UDTs (siehe scl/.../UDT_README.md). "
        "Nicht in OB1: Ordner legacy/ und scl/Zone3_PickPlace, scl/Zone4_Palettierer (Kopien).",
    )

    add_heading_styled(doc, "6  Produktcodes", 1)
    add_para(doc, "Artikelnummer = YY × 1000 + Materialart × 100 + Color_Code  →  Beispiel 2026 / Kunststoff / Blau = 26101")
    add_para(doc, "RFID_CODE = YYMMDD × 1000 + Materialart × 100 + Color_Code  →  Beispiel 20.08.2026 / Kunststoff / Blau = 260820101")
    add_table(
        doc,
        ["Feld", "Code / Werte", "SCL / Tag"],
        [
            ("Materialart", "1 Kunststoff · 2 Metall", "UDT_Fach · Vision / RFID Out"),
            ("Color_Code", "1 Blau · 2 Grün · 3 Mixed", "2b_VisionData_Color_Code"),
            ("ProductTyp", "Lid×10 + Base (z. B. 23)", "2b_VisionData_ProductType"),
            ("RFID Tag Index", "0 CODE · 1 Artikel · 2 Material · 3 Typ", "FB_RFID_ReadWrite Job 11"),
        ],
        col_widths=[3.5, 6.5, 6],
    )

    add_heading_styled(doc, "7  Lager-Info_Code 0–17", 1)
    add_para(doc, "Quelle: FB_Meldung / FB_Meldung_W2 → gldb_AktuellerFach_HMI(.W2).Meldung.Info_Text")
    add_table(
        doc,
        ["Code", "Info_Text", "OK"],
        [
            ("0", "Keine Meldung", "—"),
            ("1", "Einlagerung erfolgreich", "ja"),
            ("2", "Fach ist bereits belegt", "nein"),
            ("3", "Fachnummer ungültig", "nein"),
            ("4", "Auslagerung erfolgreich", "ja"),
            ("5", "Fach ist bereits frei", "nein"),
            ("6", "Datensatz gelöscht", "ja"),
            ("7", "RFID-Code fehlt", "nein"),
            ("8", "Kein passendes Fach gefunden", "nein"),
            ("9", "Produkt gefunden / Gefunden | Fach: …", "ja"),
            ("10", "Lager voll", "nein"),
            ("11", "Factory I/O Zielposition geladen", "ja"),
            ("12", "Factory I/O Ziel erreicht", "ja"),
            ("13", "Not-Aus aktiv", "nein"),
            ("14", "Freies Fach gefunden", "ja"),
            ("15", "Fach ist gesperrt", "nein"),
            ("16", "Fachposition gespeichert", "ja"),
            ("17", "Raster: alle Positionen berechnet", "ja"),
        ],
        col_widths=[2, 12, 2],
    )

    add_heading_styled(doc, "8  Automatik-State (HMI_State / HMI_State_W2)", 1)
    add_para(doc, "W1 %MW128 · W2 %MW228 · Hochregal_Automatik_Betrieb / _W2")
    add_table(
        doc,
        ["State", "Bedeutung (HMI-Beschriftung)", "Typische Aktion"],
        [
            ("0", "Bereit — warte auf Palette", "Gate / Produkt"),
            ("10", "RFID lesen… (W1 Reader 5; W2 Durchlauf)", "AF-36"),
            ("20", "Freies Fach suchen…", "FB_Freies_Fach_Suchen"),
            ("30", "Fahre zum Band…", "Soll = Band"),
            ("40–42", "Gabel Band: aus / heben / ein", "Pick"),
            ("50", "Fahre zum Fach…", "Soll = Fach X/Z"),
            ("55–58", "Gabel Regal: aus / senken / ein", "Place"),
            ("60", "Lagerdaten aktualisieren…", "FB_Einlagern · Info_Code 1"),
            ("70", "Fahre zur Home-Position…", "Home_X/Z"),
            ("80", "Fertig", "Done-Impuls · Zähler"),
            ("900", "Störung — siehe Meldung", "Reset"),
        ],
        col_widths=[2.4, 7.6, 6],
    )

    add_heading_styled(doc, "9  RFID Status_Code", 1)
    add_table(
        doc,
        ["Code", "Bedeutung", "Tag / Quittung"],
        [
            ("0", "OK / bereit", "2b_RFID_Status_Code %MW44"),
            ("1", "Kein Tag / ungültig", "Tag_Present FALSE"),
            ("10", "Handshake-Timeout Factory I/O", "HMI Reset; Command ID muss steigen"),
        ],
        col_widths=[2.2, 7.3, 6.5],
    )

    add_heading_styled(doc, "10  HMI- und Testcodes", 1)
    add_heading_styled(doc, "10.1  HMI (HM-01…07)", 2)
    add_table(
        doc,
        ["Code", "Umsetzung"],
        [
            ("HM-01", "Übersicht · Geplante/Ist-Produktion %MD320/%MD324 · HMI_Tags_Prod_PerDay.csv"),
            ("HM-02", "HMI_Tags_RFID_Vision.csv · Schreiben/Lesen/Prüfen/Löschen/Zurücksetzen"),
            ("HM-03", "Setup W1/W2: Raster, Pos speichern, Soll-Jog"),
            ("HM-04", "Operate: Suchen, Freies Fach, Löschen, Start Ein-/Auslagern (Hand)"),
            ("HM-05", "Header Einricht/Auto/Hand, STOP, Busy/Done/Error"),
            ("HM-06", "P&P- und Palettierer-Screens (Soll)"),
            ("HM-07", "Lagerverwaltung Online Streamlit · nicht TP"),
        ],
        col_widths=[2.2, 13.8],
    )
    add_heading_styled(doc, "10.2  Abnahmetests T-01…T-09", 2)
    add_table(
        doc,
        ["Test", "Code-Bezug", "Wo prüfen"],
        [
            ("T-01", "AF-10…13", "2b_VisionData_* Both_Ready"),
            ("T-02", "AF-14, AF-21", "Reader 2 · Pallet_Tagged"),
            ("T-03", "AF-32a, AF-37", "Paket_Fuer_Hochregal %M62.1 / %M72.1"),
            ("T-04", "AF-36, AF-38", "HMI_State 10→20→…→80 W1"),
            ("T-05", "AF-22, AF-36", "RFID_5b_Gueltig · Fachaktuell"),
            ("T-06", "AF-32, AF-34", "Hand Start · Belegt · Info_Code 1"),
            ("T-07", "AF-35", "Info_Code 17 · Kran folgt Soll"),
            ("T-08", "AF-25, SI-03", "Status_Code 10 → Reset → 0"),
            ("T-09", "AF-34a, HM-07", "Browser Suche RFID→Artikel→Fach"),
        ],
        col_widths=[2, 4, 10],
    )

    add_heading_styled(doc, "11  Verweise", 1)
    for b in [
        "Lastenheft_Abschlussprojekt.docx — Anforderungen (Was), Version 1.6",
        "PLC_Networks.md / Main_Program_Sweep.md — FUP-Codes NW 1–29",
        "Station_PLC_FIO_Tags.md · PLCTags3_live.csv — 485 Tags nach Station (FIO vs SPS)",
        "docs/03_Technik/Hardware_SPS.md · HMI_Gesamtanlage.md · Lagerverwaltung_Online.md",
        "scl/README.md — Ordner ↔ Netzwerke",
        "scl/Zone_5b_Hochregallager/ · Zone_5a_Metall_Hochregallager/",
        "docs/04_Anlagenbereiche/Zone_5b_Hochregallager/INFO_CODES.md",
        "Generator: scripts/generate_pflichtenheft.py",
    ]:
        add_bullet(doc, b)

    add_para(
        doc,
        "Ende des Pflichtenhefts — Version 1.3 — Dereje Hailemariam — September 2026",
        bold=True,
    )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    versioned = OUT.with_name("Pflichtenheft_Abschlussprojekt_v1.3.docx")
    try:
        doc.save(str(OUT))
        print(f"Written: {OUT}")
        try:
            doc.save(str(versioned))
            print(f"Written: {versioned}")
        except PermissionError:
            print(f"Versioned copy locked, skipped: {versioned}")
    except PermissionError:
        doc.save(str(versioned))
        print(f"Original locked — written: {versioned}")


if __name__ == "__main__":
    build()
