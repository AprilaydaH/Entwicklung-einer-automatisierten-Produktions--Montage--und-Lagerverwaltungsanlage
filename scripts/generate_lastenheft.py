# -*- coding: utf-8 -*-
"""Generate Lastenheft (requirements specification) as Word .docx"""
from pathlib import Path
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

OUT = Path(__file__).resolve().parents[1] / "docs" / "01_Projektgrundlagen" / "Lastenheft_Abschlussprojekt.docx"


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
        set_run_font(run, size=10, bold=True)
        set_cell_shading(hdr[i], "1F4E79")
        run.font.color.rgb = RGBColor(255, 255, 255)
    for r_idx, row in enumerate(rows):
        cells = table.rows[r_idx + 1].cells
        for c_idx, val in enumerate(row):
            cells[c_idx].text = ""
            p = cells[c_idx].paragraphs[0]
            run = p.add_run(str(val))
            set_run_font(run, size=10)
            if r_idx % 2 == 1:
                set_cell_shading(cells[c_idx], "F2F2F2")
    if col_widths:
        for row in table.rows:
            for i, w in enumerate(col_widths):
                row.cells[i].width = Cm(w)
    doc.add_paragraph()
    return table


def req(doc, rid, text, prio="Muss"):
    p = doc.add_paragraph()
    r1 = p.add_run(f"{rid}  [{prio}]  ")
    set_run_font(r1, size=11, bold=True)
    r2 = p.add_run(text)
    set_run_font(r2, size=11)
    p.paragraph_format.space_after = Pt(4)
    return p


def build():
    doc = Document()
    section = doc.sections[0]
    section.top_margin = Cm(2.5)
    section.bottom_margin = Cm(2.5)
    section.left_margin = Cm(2.5)
    section.right_margin = Cm(2.5)
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
    n_fonts.set(qn("w:cs"), "Calibri")
    n_lang = n_rPr.find(qn("w:lang"))
    if n_lang is None:
        n_lang = OxmlElement("w:lang")
        n_rPr.append(n_lang)
    n_lang.set(qn("w:val"), "de-DE")

    # ----- Title page -----
    for _ in range(3):
        doc.add_paragraph()
    t = doc.add_paragraph()
    t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = t.add_run("LASTENHEFT")
    set_run_font(r, size=28, bold=True)

    st = doc.add_paragraph()
    st.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = st.add_run("Anforderungen an die automatisierte\nFertigungs- und Lageranlage")
    set_run_font(r, size=16, bold=True)

    doc.add_paragraph()
    meta = [
        ("Projekttitel", "Entwicklung einer automatisierten Produktions-, Montage- und Lagerverwaltungsanlage"),
        ("Thema (Freigabe)", "Entwicklung und Simulation einer automatisierten Fertigungs- und Lageranlage mit RFID-gestützter Produktverfolgung in TIA Portal und Factory I/O"),
        ("Autor / Teilnehmer", "Dereje Hailemariam"),
        ("Ort", "Berlin"),
        ("Dokumentstand", "September 2026"),
        ("Werkzeuge", "TIA Portal V20, Factory I/O, Siemens S7-1500 / PLCSIM, HMI (Touch Panel), Streamlit (Lagerverwaltung Online)"),
        ("Dokumentart", "Lastenheft (Auftraggeber-Sicht / Anforderungsspezifikation)"),
        ("Version", "1.6"),
        ("SPS-Gliederung", "29 OB1-Netzwerke (Main Program Sweep v1.4); Hardware CPU 1518F-4 PN/DP + TP2200 Comfort"),
        ("Änderung v1.6", "Lagerverwaltung Online: Streamlit-Suche W1/W2 (RFID→Artikel→Fach), SQLite, ohne SPS-Änderung; TP-HMI bleibt führend"),
        ("Änderung v1.5", "OB1 29 NW; Warehouse_1 Kunststoff NW 29; Warehouse_2 Metall NW 28 Mirror-Scaffold; Vision FB17; P&P-NW angepasst"),
        ("Änderung v1.4", "Kunststoff-E2E: Vision an 3B P&P, RFID Write Reader 2 / Read Reader 5, Warehouse Gate + Auto-Einlagern, Einricht Manual Soll"),
    ]
    for label, value in meta:
        p = doc.add_paragraph()
        r1 = p.add_run(f"{label}: ")
        set_run_font(r1, bold=True)
        r2 = p.add_run(value)
        set_run_font(r2)

    doc.add_page_break()

    # ----- TOC placeholder -----
    add_heading_styled(doc, "Inhaltsverzeichnis", 1)
    toc_items = [
        "1  Einleitung und Zweck",
        "2  Ausgangslage und Problemstellung",
        "3  Geltungsbereich und Abgrenzung",
        "4  Ziele und Nutzen",
        "5  Anlagenübersicht und Materialfluss",
        "6  Funktionale Anforderungen",
        "7  Nichtfunktionale Anforderungen",
        "8  Hardware und SPS-Konfiguration",
        "9  Main Program Sweep (OB1-Netzwerke)",
        "10  Schnittstellen",
        "11  HMI-Anforderungen",
        "12  Lagerverwaltung und Produktcodierung",
        "13  Sicherheit, Betriebsarten und OB100",
        "14  Abnahmekriterien und Testfälle",
        "15  Lieferumfang und Prioritäten",
        "16  Glossar und Verweise",
    ]
    for item in toc_items:
        add_para(doc, item, space_after=4)
    doc.add_page_break()

    # ----- 1 -----
    add_heading_styled(doc, "1  Einleitung und Zweck", 1)
    add_para(
        doc,
        "Dieses Lastenheft beschreibt die Anforderungen an die Entwicklung und Simulation "
        "einer automatisierten Fertigungs-, Montage- und Lagerverwaltungsanlage. Es formuliert "
        "die Erwartungen aus Auftraggeber- bzw. Projektziel-Sicht und dient als Grundlage für "
        "das Pflichtenheft, die SPS-/HMI-Implementierung in TIA Portal sowie die Simulation in Factory I/O.",
    )
    add_para(
        doc,
        "Das Dokument leitet sich aus dem freigegebenen Abschlussarbeitsthema, dem Anlagenlageplan, "
        "den 29 TIA-OB1-Netzwerken sowie der bestehenden Projektdokumentation ab und legt fest, "
        "was die Anlage leisten muss — nicht im Detail, wie die Software intern aufgebaut wird.",
    )

    # ----- 2 -----
    add_heading_styled(doc, "2  Ausgangslage und Problemstellung", 1)
    add_heading_styled(doc, "2.1  Ausgangslage", 2)
    add_para(
        doc,
        "Es soll eine automatisierte Fertigungs- und Lageranlage in TIA Portal V20 und Factory I/O "
        "abgebildet werden. Rohteile verlassen das Lager, werden über Fördertechnik zu "
        "Bearbeitungsstationen transportiert, nach Materialart (Metall / Kunststoff) verarbeitet "
        "(Base und Deckel), per RFID identifiziert, montiert, ggf. palettiert und automatisch "
        "ein- bzw. ausgelagert.",
    )
    add_heading_styled(doc, "2.2  Problemstellung", 2)
    add_para(doc, "Die Teilprozesse müssen zu einer durchgängigen, sicheren Automatisierung verbunden werden:")
    for b in [
        "Materialerkennung und getrennte Bearbeitung Metall / Kunststoff",
        "Förderstrecken und Zonenübergänge",
        "RFID-gestützte Produktverfolgung",
        "Pick-and-Place-Montage (2-axis, Base + Deckel)",
        "3-axis Pick and Place und Palettierung",
        "Lagerverwaltung (Fachnummer, Artikelnummer, Materialart, Produkttyp, RFID, Belegung)",
        "Betriebsarten Manual / Automatik, HMI, Fehler- und Statusmeldungen",
        "Grundlegende Sicherheitsbetrachtung",
    ]:
        add_bullet(doc, b)

    # ----- 3 -----
    add_heading_styled(doc, "3  Geltungsbereich und Abgrenzung", 1)
    add_para(
        doc,
        "Die SPS-Gliederung folgt dem Main Program Sweep (OB1) mit 29 Netzwerken "
        "(Main_Program_Sweep.md v1.4 / PLC_Networks.md). Linie A = Metall, Linie B = Kunststoff.",
    )
    add_heading_styled(doc, "3.1  Zur Anlage gehören (In-Scope)", 2)
    for b in [
        "Zone 1A (NW 1–2): Rohmaterial-Annahme Metall, Bearbeitungszentren (Roboter + CNC, Base und Deckel)",
        "Zone 1B (NW 4, 6): Rohmaterial-Annahme Kunststoff, Bearbeitungszentren (Roboter + CNC, Base und Deckel)",
        "Zone 2A (NW 3, 5): Transportband Metall; VisionData Sensors (NW 5)",
        "Zone 2B (NW 7–8): VisionSensorData FB17 (Lid/Base, Color, Combo_Done, Reject Metal); Band Kunststoff",
        "Zone 3A (NW 9–12): Bänder, 2-axis Pick and Place Metall (NW 10), Waage 1",
        "Zone 3B (NW 17–20): Bänder, 2-axis Pick and Place Kunststoff (NW 18), Waage 2",
        "Zone 4A (NW 13–16, 21): Band/Rollenbahn, 3-axis Pick and Place / Palettierer Metall (NW 15), RFID Metall",
        "Zone 4B (NW 22–25): Band/Rollenbahn, Palettierer Kunststoff, RFID Write Reader 2 (NW 25)",
        "Zone 5A (NW 26, 28): Band zum Kunststoff-Hochregal (NW 26); Metal Components Warehouse Warehouse_2 (NW 28)",
        "Zone 5B (NW 27, 29): Band zum Metall-Hochregal (NW 27); Plastic Components Warehouse Warehouse_1 (NW 29) inkl. RFID Read Reader 5",
        "Hochregallager Warehouse_1 (Kunststoff, NW 29) mit 54 Fächern, Gate, Auto-Einlagern, Raster-Teach",
        "Hochregallager Warehouse_2 (Metall, NW 28) als Mirror von Warehouse_1 (eigene DBs/Tags *_W2, Stacker Crane 1)",
        "Ein gemeinsames Touch Panel (HMI) für alle Zonen",
        "Optionale Web-Suche Lagerverwaltung Online (Streamlit, je 54 Fächer W1/W2) — ergänzt das TP, ersetzt es nicht",
        "SPS-Steuerung (S7-1500 / PLCSIM) in TIA Portal V20",
        "Simulation der Bewegungsabläufe in Factory I/O",
    ]:
        add_bullet(doc, b)

    add_heading_styled(doc, "3.2  Nicht Bestandteil (Out-of-Scope)", 2)
    for b in [
        "Externe Energieversorgung",
        "Gabelstapler / Transport außerhalb der Anlage",
        "Bedienpersonal als Systemteil",
        "ERP-System / übergeordnete MES-Anbindung",
        "Wasserverbrauch / Wasserwirtschaft",
        "Live-Anbindung der Web-Lagerverwaltung an SPS-DBs (gldb_LagerverwaltungData / _W2); Web nutzt SQLite-Kopie",
        "Serienreife CE-Zertifizierung einer realen Maschine (nur konzeptionelle Sicherheitsdokumentation)",
    ]:
        add_bullet(doc, b)

    # ----- 4 -----
    add_heading_styled(doc, "4  Ziele und Nutzen", 1)
    add_heading_styled(doc, "4.1  Projektziele", 2)
    for b in [
        "Funktionsfähige SPS-Steuerung mit übersichtlicher HMI",
        "Rohprodukte bereitstellen, Metall und Kunststoff getrennt bearbeiten",
        "Base und Deckel korrekt zuordnen und montieren",
        "Fertige Produkte palettieren bzw. dem Lager zuführen",
        "Ein- und Auslagerung über eine nachvollziehbare Lagerverwaltung",
        "RFID-gestützte Rückverfolgbarkeit der Produkte / Paletten",
        "Realistische Test- und Dokumentierbarkeit in TIA Portal und Factory I/O",
        "Modularer, erweiterbarer Aufbau der Softwarebausteine",
    ]:
        add_bullet(doc, b)

    add_heading_styled(doc, "4.2  Quantitative / qualitative Ziele", 2)
    add_table(
        doc,
        ["Art", "Anforderung"],
        [
            ("Quantitativ", "Alle 54 vorgesehenen Lagerfächer adressierbar"),
            ("Quantitativ", "Wichtige Prozesszustände speicherbar (Fach belegt, Produktfelder, Meldungen)"),
            ("Qualitativ", "Modular, erweiterbar, nachvollziehbar dokumentiert"),
            ("Qualitativ", "Kunststofflinie End-to-End vor Metalllinie"),
        ],
        col_widths=[3.5, 12],
    )

    add_heading_styled(doc, "4.3  Nutzen (fiktives Unternehmen)", 2)
    for b in [
        "Digitale Abbildung und Optimierung von Produktion und Lager",
        "Weniger Verwechslungen durch RFID",
        "Bessere Übersicht über Roh- und Fertigprodukte",
        "Kürzere Durchlaufzeiten, weniger manuelle Eingriffe",
        "Prozesssicherheit, Qualität, Nachverfolgbarkeit, Erweiterbarkeit",
    ]:
        add_bullet(doc, b)

    # ----- 5 -----
    add_heading_styled(doc, "5  Anlagenübersicht und Materialfluss", 1)
    add_heading_styled(doc, "5.1  Zonenübersicht", 2)
    add_table(
        doc,
        ["Zone", "Bezeichnung", "Aufgabe"],
        [
            ("1A", "Metall Roh + CNC", "NW 1–2: Annahme, Roboter, Bearbeitungszentren"),
            ("1B", "Kunststoff Roh + CNC", "NW 4, 6: Annahme, Roboter, Bearbeitungszentren"),
            ("2A", "Band Metall + Vision NW5", "NW 3 Band; NW 5 VisionData"),
            ("2B", "Band + Vision FB17", "NW 7 VisionSensorData; NW 8 Band Kunststoff"),
            ("3A", "2-axis Pick and Place Metall", "NW 9–12: Band, Montage NW 10, Waage 1"),
            ("3B", "2-axis P&P Kunststoff", "NW 17–20: Montage NW 18, Waage 2"),
            ("4A", "3-axis P&P + RFID Metall", "NW 13–16, 21"),
            ("4B", "Palettierer + RFID Write", "NW 22–25, Reader 2"),
            ("5A", "Band Plastik + Metall-Lager W2", "NW 26 Band; NW 28 Warehouse_2 Metall"),
            ("5B", "Band Metall + Kunststoff-Lager W1", "NW 27 Band; NW 29 Warehouse_1 + Reader 5"),
        ],
        col_widths=[2.2, 5, 8.5],
    )

    add_heading_styled(doc, "5.2  Materialfluss Kunststoff (Priorität)", 2)
    add_para(
        doc,
        "Zone 1B Roh + CNC (NW 4–5) → Zone 2B Transportband (NW 6–7) → "
        "Zone 3B Vision latch (Lid/Base) + Montage und Waage (NW 16–19) → "
        "Zone 4B Palettierer und RFID-Write Reader 2 bei 4b_Done (NW 20–23) → "
        "Zone 5A Band zum Kunststoff-Lager (NW 26) → Zone 5B Gate + RFID-Read Reader 5 + Auto-Einlagern (NW 29).",
    )
    add_para(
        doc,
        "Freigabe für das Hochregallager erst nach erfolgreichem RFID-Schreiben: "
        "Paket_Fuer_Hochregal = Paket_Vor_Regal UND (Vision_Combo_Done ODER Pallet_Tagged).",
        bold=False,
    )

    add_heading_styled(doc, "5.3  Materialfluss Metall (nachrangig)", 2)
    add_para(
        doc,
        "Zone 1A Roh + CNC (NW 1–2) → Zone 2A Transportband (NW 3, ohne Vision) → "
        "Zone 3A Montage und Waage (NW 8–11) → Zone 4A Palettierer und RFID (NW 12–15) → "
        "Band zum Metall-Lager (NW 27) → Hochregal Metall Warehouse_2 (NW 28) — Mirror von Warehouse_1, Phase1 Hand/Sensor-Gate.",
    )

    # ----- 6 -----
    add_heading_styled(doc, "6  Funktionale Anforderungen", 1)
    add_para(
        doc,
        "Kennzeichnung: [Muss] = verpflichtend für Abnahme der Prioritätslinie Kunststoff; "
        "[Soll] = vorgesehen, kann nachgelagert werden; [Kann] = optional.",
    )

    add_heading_styled(doc, "6.1  Allgemein / Querschnitt", 2)
    req(doc, "AF-01", "Die Anlage wird mit einer SPS (S7-1500 / PLCSIM) in TIA Portal V20 gesteuert.")
    req(doc, "AF-02", "Die Bewegungsabläufe und Sensorik werden in Factory I/O simuliert und getestet.")
    req(doc, "AF-03", "Ein gemeinsames HMI (Touch Panel) bedient alle Zonen.")
    req(doc, "AF-04", "Betriebsarten Einricht, Automatik und Hand sind unterscheidbar; Einricht hat Priorität.")
    req(doc, "AF-05", "Fehler- und Statusmeldungen sind über HMI und/oder Meldungs-DB abrufbar.")

    add_heading_styled(doc, "6.2  Vision (Kunststoff)", 2)
    req(doc, "AF-10", "Zwei Vision-Sensoren (Lid und Base) an Zone 3B 2-axis P&P (vor Montage) liefern numerische Werte (Detects All Numerical); SPS-Baustein/Tags unter Zone 2B (NW 6).")
    req(doc, "AF-11", "Werte 1…6 gelten als gültige Kunststoffteile; 7…9 führen zu Metall-Reject.")
    req(doc, "AF-12", "Aus Lid und Base werden Color_Code (1 Blau / 2 Grün / 3 Mixed), Materialart=1, ProductTyp und Artikelnummer gebildet und gelatcht.")
    req(doc, "AF-13", "RFID_CODE wird als Datums-/Material-/Farbstempel erzeugt und für den Paletten-Tag bereitgestellt.")
    req(doc, "AF-14", "Ein Schreibauftrag an RFID Reader 2 (Zone 4B) erfolgt erst nach Palettierer-Done (Allow_Write := 4b_Done); ein Write-Puls pro Auftrag.")

    add_heading_styled(doc, "6.3  RFID", 2)
    req(doc, "AF-20", "Der RFID-Baustein unterstützt Prüfen, Lesen und Schreiben gemäß Factory-I/O-Handshake (Command, Execute, Command ID, Status); Execute_Hold mind. 100 ms.")
    req(doc, "AF-21", "Produkt-Schreiben (Job 11) belegt Tag-Speicher Index 0…3 mit RFID_CODE, Artikelnummer, Materialart, ProductTyp.")
    req(doc, "AF-22", "Zwei getrennte Instanzen: DB_1 Reader 2 = Write an der Palettenstation; DB_2 Reader 5 = Read am Hochregal (kein Write).")
    req(doc, "AF-23", "Nach erfolgreichem Schreiben ist die Palette für das Lager freigebbar (Pallet_Tagged und/oder Combo_Done).")
    req(doc, "AF-24", "Kunststoff-RFID Write Zone 4B (NW 25); Read Zone 5B Reader 5 (NW 29); Metall-RFID Zone 4A (NW 16/21).", "Soll")
    req(doc, "AF-25", "Timeout und Fehlerzustände (z. B. kein Tag, Handshake-Timeout Status 10) sind am HMI sichtbar und per Reset quittierbar.")

    add_heading_styled(doc, "6.4  Hochregallager", 2)
    req(doc, "AF-30", "Das Hochregallager Warehouse_1 (Kunststoff, NW 29) umfasst 54 adressierbare Fächer.")
    req(doc, "AF-30a", "Warehouse_2 (Metall, NW 28) ist Mirror von Warehouse_1 mit getrennten DBs/Tags (*_W2) und Stacker Crane 1.", "Soll")
    req(doc, "AF-31", "Jedes Fach speichert mindestens Materialart, Color_Code, Artikelnummer, ProductTyp, RFID_CODE, Position X/Z, Belegt/Gesperrt.")
    req(doc, "AF-32", "Einlagern: freies Fach suchen, Regalbediengerät anfahren, Fach belegen.")
    req(doc, "AF-32a", "Gate Warehouse_1: Paket_Fuer_Hochregal = Paket_Vor_Regal UND (Combo_Done ODER Pallet_Tagged). Gate Warehouse_2 Phase1: Sensor-only.", "Soll")
    req(doc, "AF-33", "Auslagern: Suche nach Artikel/RFID/Fach, Entnahme, Fach freigeben.")
    req(doc, "AF-34", "Löschen und Suchfunktionen für die Lagerverwaltung sind vorhanden.")
    req(
        doc,
        "AF-34a",
        "Lagerverwaltung Online (Web): Suche je Warehouse (W1 Kunststoff, W2 Metall) über 54 Fächer in der Reihenfolge RFID → Artikelnummer → Fachnummer, ohne Änderung des SPS-Programms. Demo Einlagern/Löschen nur in SQLite. Das TP-HMI bleibt führend für Betrieb.",
        "Soll",
    )
    req(doc, "AF-35", "Raster-Teach: Basis Fach 1 + Pitch_X/Pitch_Z (+ Spalten) berechnet alle Fachpositionen; Einricht mit manuellen Soll-X/Z und Jog möglich.")
    req(doc, "AF-36", "Automatik Warehouse_1 liest vor dem Einlagern den RFID-Tag an Reader 5 (State 10) und übernimmt gültige Produktdaten.")
    req(doc, "AF-37", "Einlagern der Kunststofflinie erst nach RFID-Write-OK (Gate).")
    req(doc, "AF-38", "Im Betriebsmodus Auto startet Einlagern automatisch bei geöffnetem Gate — ohne Start-Einlagern-Taste.")

    add_heading_styled(doc, "6.5  Montage und Handling", 2)
    req(doc, "AF-40", "Zone 3A/3B: 2-axis Pick and Place montiert Base und Deckel (NW 10 Metall, NW 18 Kunststoff).")
    req(doc, "AF-41", "Zone 3A/3B enthalten je eine Waage (NW 11 / NW 19) nach der Montage.", "Soll")
    req(doc, "AF-42", "Zone 4A NW 15: 3-axis Pick and Place (X/Y/Z) führt die Metall-Palettiersequenz; RFID Metall in NW 16/21.", "Soll")
    req(doc, "AF-43", "Zone 4B palettiert Kunststoffprodukte (NW 24) und schreibt RFID (NW 25).", "Soll")

    add_heading_styled(doc, "6.6  Bearbeitung und Fördertechnik", 2)
    req(doc, "AF-50", "Zone 1A und 1B nehmen Rohmaterial an und bearbeiten Base/Deckel mit Roboter und CNC (NW 1–2, 4, 6).", "Soll")
    req(doc, "AF-51", "Zone 2A ist das Metall-Transportband (NW 3); Zone 2B das Kunststoff-Transportband (NW 8).", "Soll")
    req(doc, "AF-52", "Vision FB17 (NW 5/7) registriert Farbe/Typ, stellt RFID-Produktdaten bereit und kann Metall-Reject setzen.")

    # ----- 7 -----
    add_heading_styled(doc, "7  Nichtfunktionale Anforderungen", 1)
    req(doc, "NF-01", "Softwarebausteine sind modular (getrennte FBs für Vision, RFID, Lager, Zonen).")
    req(doc, "NF-02", "Code und Variablen sind in Deutsch/Englisch konsistent und dokumentiert (README, Tags-CSV).")
    req(doc, "NF-03", "Die Kunststoff-E2E-Kette hat Entwicklungsvorrang vor der Metalllinie.")
    req(doc, "NF-04", "Simulation und SPS-Test müssen ohne reale Hardware (PLCSIM + Factory I/O) durchführbar sein.")
    req(doc, "NF-05", "Timeouts und Fehler dürfen die Anlage in einen sicheren, quittierbaren Zustand führen.")
    req(doc, "NF-06", "HMI-Bedienung muss für Inbetriebnahme (Reset, Check, Write, Read, Raster) ohne TIA-Online-Zwang nutzbar sein.", "Soll")
    req(doc, "NF-07", "Die Web-Lagerverwaltung darf das SPS-Programm nicht ändern; Suchen am TP (HMI_Suchen / HMI_Suchen_W2) bleibt maßgeblich.", "Soll")

    # ----- 8 Hardware -----
    add_heading_styled(doc, "8  Hardware und SPS-Konfiguration", 1)
    add_para(
        doc,
        "Die reale TIA-Konfiguration (Geräteübersicht PLC_1, Netzsicht, Belegungsplan, Speicherauslastung) "
        "ist verbindlich. Detail: docs/03_Technik/Hardware_SPS.md.",
    )
    add_heading_styled(doc, "8.1  Steuerung und HMI", 2)
    add_table(
        doc,
        ["Gerät", "Typ / Bestellnr.", "Hinweis"],
        [
            ("PLC_1", "CPU 1518F-4 PN/DP · 6ES7 518-4FX00-1AB0 · FW V3.1", "Failsafe S7-1500; PN X1–X3, DP X4"),
            ("Netzteil Slot 0", "PS 60W 24/48/60VDC · 6ES7 505-0RA00-0AB0 · V1.1", "24 V DC"),
            ("HMI_1", "TP2200 Comfort", "Ein Panel, Netz PN/IE_1"),
        ],
        col_widths=[3.5, 8, 4.5],
    )
    req(doc, "HW-01", "Die Anlage wird auf CPU 1518F-4 PN/DP (TIA-Gerät PLC_1) und einem TP2200 Comfort (HMI_1) abgebildet.")
    req(doc, "HW-02", "OB1 enthält die 27 Zonen-Netzwerke; OB100 (Startup) wird am Projektende für Initialisierung STOP→RUN ergänzt.")

    add_heading_styled(doc, "8.2  E/A-Baugruppen (Rack 0)", 2)
    add_table(
        doc,
        ["Slot", "Baugruppe", "Adressen", "Bestellnr."],
        [
            ("2", "DI 32×24VDC BA", "E 4.0 … 7.7", "6ES7 521-1BL10-0AA0"),
            ("3", "DI 32×24VDC BA", "E 0.0 … 3.7", "6ES7 521-1BL10-0AA0"),
            ("4", "DI 32×24VDC BA", "E 8.0 … 11.7", "6ES7 521-1BL10-0AA0"),
            ("5", "DI 32×24VDC BA", "E 12.0 … 15.7", "6ES7 521-1BL10-0AA0"),
            ("6", "DQ 64×24VDC/0,3A BA", "A 8.0 … 15.7", "6ES7 522-1BP00-0AA0"),
            ("7", "DQ 64×24VDC/0,3A BA", "A 16.0 … 23.7", "6ES7 522-1BP00-0AA0"),
            ("8", "DQ 64×24VDC/0,3A BA", "A 24.0 … 31.7", "6ES7 522-1BP00-0AA0"),
            ("9", "AI 16×I (Strom)", "E 16 … 47", "6ES7 531-7MH00-0AB0"),
            ("10", "AI 16×U (Spannung)", "E 48 … 79", "6ES7 531-7LH00-0AB0"),
            ("11", "AQ 2×U/I ST", "A 0 … 3", "6ES7 532-5NB00-0AB0"),
            ("12", "AQ 2×U/I ST", "A 4 … 7", "6ES7 532-5NB00-0AB0"),
        ],
        col_widths=[1.5, 5, 4, 5.5],
    )
    add_para(
        doc,
        "Konfigurierte Kanäle (TIA Speicherauslastung): 128 DE (58 genutzt), 192 DA (157 genutzt), "
        "32 AE (18 genutzt), 4 AA (noch 0 genutzt). Digitale Ausgänge sind der knappste Bereich.",
    )

    add_heading_styled(doc, "8.3  Adressbereiche (Belegungsplan)", 2)
    add_para(
        doc,
        "Digitale Eingänge u. a. EB0…EB13; Prozess-DWORDs u. a. EB30…EB50 sowie Blöcke EB50…EB65, "
        "EB86…EB109, EB140…EB149. Digitale Ausgänge u. a. AB0…AB13 und AB16…AB22. "
        "Merker u. a. MB0…MB51 (Zustände, Words/DWORDs).",
    )

    add_heading_styled(doc, "8.4  OB100 Startup (geplant)", 2)
    req(doc, "OB-01", "OB100 setzt Ausgänge in einen sicheren Zustand (Greifer, Bänder, Kran) beim Übergang STOP → RUN.")
    req(doc, "OB-02", "OB100 initialisiert bzw. prüft Sequenz-States und Handshake-Flags (RFID Error/Busy, Vision Latch), ohne Produkt-Retain ungewollt zu löschen.")
    req(doc, "OB-03", "OB100 wird erst nach stabilem OB1-Ablauf (Kunststoff-E2E) eingefügt — nicht vor Go-live der Einlagerung.", "Soll")

    # ----- 9 Main Program Sweep -----
    add_heading_styled(doc, "9  Main Program Sweep (OB1-Netzwerke)", 1)
    add_para(
        doc,
        "Der Main Program Sweep (Cycle) ist das zyklische Hauptprogramm (OB1). Er koordiniert alle "
        "Produktionsbereiche der Factory-I/O-Anlage. Die 29 Netzwerke entsprechen den physikalischen "
        "Zonen (Stand TIA Sep 2026). Detaillierte Maschinenabläufe liegen in FBs/FCs; OB1 ist der zentrale Koordinator. "
        "Quelle: Main_Program_Sweep.md v1.4.",
    )
    req(doc, "SW-01", "OB1 verarbeitet in jedem Zyklus Netzwerk 1 bis 29 sequenziell (Main Program Sweep).")
    req(doc, "SW-02", "Jedes Netzwerk steuert den zugeordneten Anlagenbereich (Roh, CNC, Band, Vision, 2-axis/3-axis P&P, Waage, Palettierer, RFID, Lager).")
    req(doc, "SW-03", "Materialfluss: Rohmaterial → CNC → Fördertechnik → Identifikation → Pick & Place → Waage → Palettieren → RFID → Lagertransport → Einlagerung.")

    add_heading_styled(doc, "9.1  Netzwerkübersicht", 2)
    add_table(
        doc,
        ["NW", "Zone", "Funktion"],
        [
            ("1", "1A", "Metal raw material input"),
            ("2", "1A", "Metal robot (CNC) station"),
            ("3", "2A", "Metal conveyors after CNC"),
            ("4", "1B", "Plastic raw material input"),
            ("5", "2A", "VisionData Sensors"),
            ("6", "1B", "Plastic robot (CNC) station"),
            ("7", "2B", "VisionData Sensors (FB17)"),
            ("8", "2B", "Plastic conveyors after CNC"),
            ("9", "3A", "Metal conveyors before 2-axis P&P"),
            ("10", "3A", "Metal Pick & Place 1 — 2-axis"),
            ("11", "3A", "Metal scale 1"),
            ("12", "3A", "Metal conveyors after scale"),
            ("13", "4A", "Conveyors before metal palletizer"),
            ("14", "4A", "Roller conveyors before palletizer"),
            ("15", "4A", "Metal assembly palletizer — 3-axis"),
            ("16", "4A", "Metal components RFID"),
            ("17", "3B", "Plastic conveyors before 2-axis P&P"),
            ("18", "3B", "Plastic Pick & Place 2 — 2-axis"),
            ("19", "3B", "Plastic scale 2"),
            ("20", "3B", "Plastic conveyors after scale"),
            ("21", "4A", "Metal RFID"),
            ("22", "4B", "Conveyors before plastic palletizer"),
            ("23", "4B", "Roller conveyors before palletizer"),
            ("24", "4B", "Plastic assembly palletizer"),
            ("25", "4B", "Plastic RFID Write/Read"),
            ("26", "5A", "Conveyors to plastic warehouse"),
            ("27", "5B", "Conveyors to metal warehouse"),
            ("28", "5A", "Metal Components Warehouse (Warehouse_2)"),
            ("29", "5B", "Plastic Components Warehouse (Warehouse_1)"),
        ],
        col_widths=[1.5, 2, 12],
    )
    add_para(
        doc,
        "Bezeichnung: 2-axis Pick and Place = NW 10 und NW 18; 3-axis Pick and Place = NW 15 "
        "(ehem. „Gantry“, nur noch als TIA-Alias Gantry_* / FB_GantryPickPlace). "
        "Warehouse_2 Metall = NW 28; Warehouse_1 Kunststoff = NW 29.",
    )

    # ----- 10 -----
    add_heading_styled(doc, "10  Schnittstellen", 1)
    add_heading_styled(doc, "10.1  Factory I/O → SPS", 2)
    add_para(doc, "Digitale und analoge Signale gemäß Driver-Mapping, u. a.:")
    for b in [
        "Vision Lid/Base Value (numerisch) an Zone 3B P&P",
        "RFID Reader 2 (4b Write): Command, Execute, Memory Index, Write Data, Command ID, Status, Read Data",
        "RFID Reader 5 (5b Read): gleiche FIO-Schnittstelle, eigene Adressen",
        "Hochregal / Stackercrane: Ist/Soll X/Z, Gabel-Limits, Moving-X/Z",
        "Anwesenheitssensoren (z. B. 5b_Pallet_vor_Regal)",
    ]:
        add_bullet(doc, b)

    add_heading_styled(doc, "10.2  Interne SPS-Schnittstellen", 2)
    for b in [
        "Vision → RFID DB_1: Artikelnummer, Materialart, ProductTyp, RFID_CODE, Write_Req (= HMI_Write)",
        "RFID DB_1 → Vision: Bereit, Busy, Done, Reset (Handshake %M30.x)",
        "RFID DB_1 → Gate: Pallet_Tagged (%M40.2); Vision Combo_Done (%M40.0)",
        "Gate → Automatik: Paket_Fuer_Hochregal (%M62.1)",
        "Automatik → RFID DB_2: RFID_Lesen, RFID_Busy, RFID_Bereit, RFID_Gueltig, RFID_Fehler, Produkt-Out",
        "Automatik → Stacker: Soll_X/Z (%MD104/108), Gabel-/Palette-Befehle; Stacker → FIO",
        "Einricht Manual Soll → Soll_X/Z (nur wenn Mode_Einricht und nicht HRL_Busy)",
        "Globale DBs: Lagerverwaltung, aktueller Fach/HMI, Meldungen",
    ]:
        add_bullet(doc, b)

    add_heading_styled(doc, "10.3  HMI → SPS", 2)
    add_para(
        doc,
        "Betriebsarten Einricht/Auto/Hand als latched Radio-Buttons; Momentary-Befehle "
        "(Reset, Start Ein-/Auslagern Hand, Pos speichern, Raster, Soll-Jog ±); "
        "Setup: Ist/Soll X/Z, Home, Pitch, Fachnummer; Statuslampen Gate und RFID_5b.",
    )

    add_heading_styled(doc, "10.4  Web-Lagerverwaltung (ohne SPS-Änderung)", 2)
    add_para(
        doc,
        "Lagerverwaltung Online ist eine optionale Browser-Anwendung (Streamlit) mit getrennten SQLite-Dateien "
        "für Warehouse_1 und Warehouse_2. Sie dient der Suche und Demonstration, nicht der Maschinenbedienung. "
        "Live-Merkers (Node-RED PUT/GET) sind davon unabhängig.",
    )
    for b in [
        "Tabs: Kunststoff (W1) und Metall (W2), je 54 Fächer",
        "Suchreihenfolge wie FB_Suchen: RFID_CODE → Artikelnummer → Fachnummer",
        "Keine Schreibzugriffe auf gldb_LagerverwaltungData / _W2",
        "Dokumentation: docs/03_Technik/Lagerverwaltung_Online.md",
    ]:
        add_bullet(doc, b)

    # ----- 11 -----
    add_heading_styled(doc, "11  HMI-Anforderungen", 1)
    req(doc, "HM-01", "Übersichtsscreen mit Materialfluss / Zonenstatus.", "Soll")
    req(doc, "HM-02", "Screen Vision/RFID Kunststoff: Produktwerte, Write/Reset, Status_Code, Lampen; Auto-Write über Vision Write_Req.")
    req(doc, "HM-03", "Screen Hochregallager Setup: Einricht, Fachwahl, Pos speichern, Raster, manuelle Soll-X/Z und Jog-Step.")
    req(doc, "HM-04", "Screen Operate: Auto/Hand, Start Ein-/Auslagern (Hand), Gate-/RFID-Lampen, State, Belegt/Frei.")
    req(doc, "HM-05", "Header mit Betriebsart (latched), Stop und Sammelmeldung.", "Soll")
    req(doc, "HM-06", "Screens 2-axis/3-axis P&P und Palettierer für Auto, Manual, Diagnose.", "Soll")
    req(
        doc,
        "HM-07",
        "Optionale Web-Oberfläche Lagerverwaltung Online: Tabs W1/W2, Suche RFID/Artikel/Fach, Belegt-Anzeige; kein Ersatz für das TP2200.",
        "Soll",
    )

    add_heading_styled(doc, "12  Lagerverwaltung und Produktcodierung", 1)
    add_heading_styled(doc, "12.1  Artikelnummer", 2)
    add_para(doc, "Artikelnummer = YY × 1000 + Materialart × 100 + Color_Code")
    add_para(doc, "Beispiel: Jahr 2026, Kunststoff, Blau → 26101")

    add_heading_styled(doc, "12.2  RFID_CODE", 2)
    add_para(doc, "RFID_CODE = YYMMDD × 1000 + Materialart × 100 + Color_Code")
    add_para(doc, "Beispiel: 20.08.2026, Kunststoff, Blau → 260820101")

    add_heading_styled(doc, "12.3  ProductTyp / Color", 2)
    add_para(doc, "ProductTyp = Lid × 10 + Base (z. B. 23). Color_Code: 1 Blau, 2 Grün, 3 Mixed.")

    add_heading_styled(doc, "12.4  Fachdaten", 2)
    add_para(
        doc,
        "Jedes Fach der 54 Positionen hält die Produktfelder plus Position und Belegungsstatus. "
        "Raster: Standard 6 Spalten × 9 Ebenen.",
    )

    add_heading_styled(doc, "12.5  Lagerverwaltung Online (Web)", 2)
    add_para(
        doc,
        "Ergänzend zum TP: Streamlit-App mit SQLite (lagerverwaltung.db / lagerverwaltung_w2.db). "
        "Gleiche Fachfelder wie UDT_Fach (RFID_CODE, Artikelnummer, Materialart, Color_Code, ProductTyp, Belegt). "
        "SPS-Suchen bleibt HMI_Suchen / HMI_Suchen_W2.",
    )

    add_heading_styled(doc, "13  Sicherheit, Betriebsarten und OB100", 1)
    req(doc, "SI-01", "Not-Aus / Stop muss laufende Automatik unterbrechen bzw. Bewegung stoppen.")
    req(doc, "SI-02", "Einricht-Modus hat Vorrang vor Automatik und Hand.")
    req(doc, "SI-03", "Fehler (RFID, Lager, Timeout) sind quittierbar; Neustart ohne undefinierten Zustand.", "Soll")
    req(doc, "SI-04", "Sicherheitskonzept wird dokumentiert (konzeptionell); volle CE-Abnahme realer Hardware ist Out-of-Scope.", "Soll")
    req(doc, "SI-05", "Nach STOP→RUN übernimmt OB100 die sichere Initialisierung (siehe HW-02 / OB-01).", "Soll")

    add_heading_styled(doc, "14  Abnahmekriterien und Testfälle", 1)
    add_heading_styled(doc, "14.1  Prioritätsabnahme Kunststoff-Warehouse E2E", 2)
    add_table(
        doc,
        ["Nr.", "Testfall", "Erwartetes Ergebnis"],
        [
            ("T-01", "Vision Lid + Base an 3B P&P", "Both_Ready; Artikelnummer / RFID_CODE / ProductTyp gelatcht"),
            ("T-02", "RFID Write Reader 2 nach 4b_Done", "Ein Write-Puls; Command ID steigt; Pallet_Tagged TRUE"),
            ("T-03", "Gate", "Paket_Fuer_Hochregal nur bei Vor_Regal UND (Combo_Done ODER Pallet_Tagged)"),
            ("T-04", "Auto-Einlagern ohne Start-Taste", "Mode_Auto + Gate → State 10 → Reader 5 Busy/Gueltig → Einlagern"),
            ("T-05", "RFID Read Reader 5", "RFID_Lesen / Busy / Gueltig; Produktdaten in Fachaktuell"),
            ("T-06", "Hand-Einlagern (Commissioning)", "RFID_CODE ≠ 0 → Start → Belegt=TRUE"),
            ("T-07", "Raster-Teach + Manual Soll", "54 Positionen; Einricht Soll X/Z bewegen Kran"),
            ("T-08", "HMI Reset bei Fehler", "Error/Status 10 löschbar; Bereit wieder TRUE"),
            ("T-09", "Web-Suche W1/W2 (Streamlit)", "RFID → Artikel → Fach findet belegtes Fach; SPS-Code unverändert"),
        ],
        col_widths=[1.5, 6, 8],
    )

    add_heading_styled(doc, "14.2  Nachgelagerte Abnahmen", 2)
    for b in [
        "2-axis P&P (3A/3B) und 3-axis P&P (4A) plus Palettierer 4B im Gesamtablauf",
        "Zone 1A/1B CNC und Zone 2A/2B Bänder",
        "Metall-RFID und Warehouse_2 (NW 28) Inbetriebnahme",
        "OB100 Startup-Tests (sichere Ausgänge nach STOP→RUN)",
        "Gesamt-HMI aller Zonen",
        "Lagerverwaltung Online: Suche W1/W2 im Browser (T-09)",
    ]:
        add_bullet(doc, b)

    add_heading_styled(doc, "15  Lieferumfang und Prioritäten", 1)
    add_heading_styled(doc, "15.1  Liefergegenstände", 2)
    for b in [
        "SPS-Quellcode (SCL) je Zone / Querschnitt im Repository",
        "TIA-Projekt (lokal) mit FBs, DBs, Tags, OB1; OB100 zum Projektabschluss",
        "Factory-I/O-Szene(n)",
        "HMI-Konzept und Tags; Screens schrittweise",
        "Projektdokumentation (docs/) inkl. dieses Lastenhefts und Main_Program_Sweep.md",
        "Go-live-Checkliste Kunststoff-Warehouse",
        "Lagerverwaltung Online (Streamlit + SQLite) gemäß AF-34a / HM-07",
    ]:
        add_bullet(doc, b)

    add_heading_styled(doc, "15.2  Umsetzungspriorität", 2)
    add_table(
        doc,
        ["Prio", "Inhalt"],
        [
            ("1", "Kunststoff E2E: Vision → RFID Write → Hochregal Read → Einlagern (NW 29)"),
            ("2", "HMI Vision/RFID + Hochregal-Einricht Warehouse_1"),
            ("3", "2-axis P&P (3A/3B) und 3-axis P&P (4A) + Palettierer 4B in Gesamt-OB1"),
            ("4", "Zone 1A/1B CNC, Bänder, Waagen, Warehouse_2 Metall (NW 28)"),
            ("5", "OB100 Startup, Gesamt-HMI, Sicherheit Doku, Lagerverwaltung Online (Web-Suche)"),
        ],
        col_widths=[2, 13.5],
    )

    add_heading_styled(doc, "16  Glossar und Verweise", 1)
    add_heading_styled(doc, "16.1  Glossar", 2)
    add_table(
        doc,
        ["Begriff", "Bedeutung"],
        [
            ("Lastenheft", "Anforderungen aus Auftraggeber-/Zielsicht (Was)"),
            ("Pflichtenheft", "Umsetzungsspezifikation (Wie) — Pflichtenheft_Abschlussprojekt.docx v1.0, Codes → SCL"),
            ("Main Program Sweep", "Zyklisches OB1 mit 27 Zonen-Netzwerken"),
            ("E2E", "End-to-End: Vision latch → RFID Write → Gate → RFID Read → Einlagern"),
            ("RFID_CODE", "Produktstempel auf dem Paletten-Tag (Index 0)"),
            ("Artikelnummer", "Kurze Produktnummer (Jahr/Material/Farbe)"),
            ("Paket_Vor_Regal", "Sensor/raw: Palette am Hochregal (%M62.0)"),
            ("Paket_Fuer_Hochregal", "Gate: Vor_Regal UND (Combo_Done ODER Pallet_Tagged) → Auto"),
            ("Pallet_Tagged", "RFID DB_1: Write Job 11 OK (%M40.2)"),
            ("Combo_Done", "Vision: Schreibsequenz abgeschlossen (%M40.0)"),
            ("DB_1 / DB_2", "RFID_Read_Write Instanzen: Writer Reader 2 / Reader Reader 5"),
            ("2-axis Pick and Place", "Zone 3A/3B Montage Base+Deckel; Vision HW an 3B"),
            ("3-axis Pick and Place", "Zone 4A Handling X/Y/Z / Palettierer Metall; NW 14"),
            ("OB100", "Startup-OB S7-1500: einmalig STOP→RUN (am Projektende)"),
            ("Raster-Teach", "Fachpositionen aus Basis + Pitch berechnen"),
            ("Manual Soll", "Einricht: HMI Soll X/Z + Jog steuern den Kran"),
            ("Lagerverwaltung Online", "Streamlit-Websuche W1/W2 über SQLite; nicht live an SPS-DBs"),
            ("HMI_Suchen / _W2", "SPS-Suche am Touch Panel (FB_Suchen / FB_Suchen_W2)"),
        ],
        col_widths=[4, 11.5],
    )

    add_heading_styled(doc, "16.2  Verweisdokumente", 2)
    for b in [
        "Main_Program_Sweep.md — OB1-Netzwerkbeschreibung",
        "PLC_Networks.md — 29 TIA-OB1-Netzwerke (Kurzübersicht)",
        "Hardware_SPS.md — CPU, HMI, E/A, Belegungsplan",
        "Gesamtanlage.md — zentrale Factory-Dokumentation",
        "Pflichtenheft_Abschlussprojekt.docx — Umsetzung (Wie), Lastenheft-Codes → SCL",
        "Lageplan.md / Maschinengrenzen.md",
        "HMI_Gesamtanlage.md · Lagerverwaltung_Online.md · scl/.../HMI_Warehouse_1.md · HMI_Warehouse_2.md",
        "PLASTIC_WAREHOUSE_GOLIVE.md · WAREHOUSE_2_SETUP.md · WAREHOUSE_1_SETUP.md",
        "SYSTEM_AUDIT.md · RASTER_TEACH.md · WAREHOUSE_FIRST_PALLET.md",
        "scl/Zone_5a_Metall_Hochregallager/ (Warehouse_2 Mirror)",
        "RFID_INSTANCE_CHECK.md · COMMISSIONING.md (Zone 4b)",
        "Repository README.md",
    ]:
        add_bullet(doc, b)

    doc.add_paragraph()
    add_para(
        doc,
        "Ende des Lastenhefts — Version 1.6 — Dereje Hailemariam — September 2026",
        bold=True,
    )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    versioned = OUT.with_name("Lastenheft_Abschlussprojekt_v1.6.docx")
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
