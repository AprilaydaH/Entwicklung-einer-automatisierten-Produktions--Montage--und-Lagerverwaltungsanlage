# Sprechskript — 15 Minuten

**Datei:** [Praesentation_Abschlussprojekt_15min.pptx](Praesentation_Abschlussprojekt_15min.pptx)  
**Folien neu bauen:** `python scripts/generate_praesentation.py`  
**Tempo:** ruhig sprechen, Folie 10 (Hochregal) nicht hetzen.

Gesamtziel: Zuhörer verstehen den Bogen **Rohteil → Montage → RFID → Hochregal**, und dass **W1 Kunststoff** und **W2 Metall** getrennte Daten haben.

---

## Folie 1 — Titel (~45 s)

Guten Tag. Mein Name ist **Dereje Hailemariam**.

Mein Abschlussprojekt heißt: **Entwicklung einer automatisierten Produktions-, Montage- und Lagerverwaltungsanlage**.

Das genehmigte Thema ist die **Simulation einer Fertigungs- und Lageranlage mit RFID-gestützter Produktverfolgung** in **TIA Portal V20** und **Factory I/O**.

Ich steuere die gesamte Factory mit **einer SPS** und **einem Touch Panel**. Heute erkläre ich die Anlage von der Rohbearbeitung bis ins Hochregal.

---

## Folie 2 — Ablauf (~30 s)

In fünfzehn Minuten gehe ich so vor:

Zuerst Aufgabe und Hardware. Dann die zwei Linien und die Zonen. Danach der Materialfluss Kunststoff und Metall. Anschließend RFID, Palettierer und die beiden Hochregale. Zum Schluss Software, HMI, Web und der aktuelle Stand. Danach gerne Fragen.

---

## Folie 3 — Aufgabe und Ziele (~1 min)

Ausgangslage: In Factory I/O gibt es viele Stationen. Die Aufgabe war, daraus **einen durchgängigen Prozess** zu machen.

Es gibt **zwei Linien**: **Linie A Metall**, **Linie B Kunststoff**. Überall **Base und Deckel**.

Die Ziele sind: RFID-Verfolgung, Montage, Palettierung, automatische Ein- und Auslagerung, Manual und Automatik, ein Programm, ein HMI.

Im Lager merken wir Fachnummer, Artikel, Material, Produkttyp, RFID und Belegung.

**Nicht im Scope:** Wasserverbrauch. Die volle CE-Akte kommt später.

---

## Folie 4 — Hardware (~1 min)

Die CPU ist eine **1518F-4 PN/DP**, also Failsafe S7-1500. Das HMI ist ein **TP2200 Comfort** — ein Panel für alle Zonen.

Die Mechanik und Sensorik laufen in **Factory I/O**, angebunden an die SPS.

Software: TIA V20, **SCL und FUP**. **OB1** ist das zyklische Hauptprogramm mit **29 Netzwerken**. **OB100** für den Start STOP nach RUN.

Wichtig später für PC-Anbindung: Classic PLCSIM hat **kein TCP-Port 102**. Dafür braucht man PLCSIM Advanced oder die echte CPU.

---

## Folie 5 — Zwei Linien, Zonen 1–5 (~1,5 min)

Die Anlage ist **spiegelbildlich**.

**Zone 1:** Rohmaterial, Roboter, CNC — Base und Deckel.  
**Zone 2:** Förderband. Bei Kunststoff und Metall kommt **Vision** dazu, damit Farbe und Typ in die RFID-Daten gehen.  
**Zone 3:** **2-axis Pick and Place** — Montage Base plus Deckel.  
**Zone 4:** Palettierer und RFID. Metall zusätzlich **3-axis Pick and Place**.  
**Zone 5:** Hochregal.

Bitte merken: **Kunststoff lagert in Warehouse 1, Zone 5B, Netzwerk 29.**  
**Metall lagert in Warehouse 2, Zone 5A, Netzwerk 28.**  
Die Nummern 5A/5B und W1/W2 sind leicht zu verwechseln — ich komme darauf zurück.

---

## Folie 6 — Kunststofffluss (~1,5 min)

Linie B war die **Priorität**, weil sie zuerst durchgängig laufen sollte.

Rohteil und CNC in 1B, Band und Vision in 2B, Montage in 3B. Dann Palettierer 4B: wenn die Palette fertig ist, schreibt **RFID Reader 2** den Tag.

Am Hochregal gilt das **Gate**: Es liegt eine Palette vor dem Regal **und** RFID ist geschrieben — Combo_Done oder Pallet_Tagged. Sonst kein Automatik-Einlagern.

Im Automatikbetrieb Warehouse 1: State 10 liest **Reader 5**, dann freies Fach, Kran, Einlagern in die Lager-DB.

Die Instanz heißt **fb_Datenverwaltung_Lager_DB**. Merker ab **%M60**.

---

## Folie 7 — Metallfluss (~1 min)

Linie A ist dasselbe Muster, aber **eigene Daten**.

Nach 4A kommt das Produkt von **RFID Reader 1**. Warehouse 2 hat **keinen Reader 0** am Regal — deshalb **kein State 10**.

Gate: Sensor **und** Combo_Done oder 4a-RFID-Done.

Daten: `gldb_*_W2`, Ziel-Fach **%MW230**, Merker **%M70**. Instanz: **FB_Datenverwaltung_Lager_W2_DB**.

Diese Blöcke darf man **nicht** mit Warehouse 1 tauschen.

---

## Folie 8 — Zonen 1–3 (~1 min)

Zone 1 ist Roh und CNC — die Fein-FBs sind noch geplant, die Ordner existieren.

Zone 2 bringt das Teil zur Montage und speichert Vision-Daten für den RFID-Tag.

Zone 3 ist die **2-axis-Montage**, zwei Instanzen, Metall und Kunststoff. Das ist nicht der 3-axis-Kran — der sitzt erst in 4A.

---

## Folie 9 — Palettierer und RFID (~1,5 min)

Der RFID-Tag ist die Identität bis ins Fach.

Kunststoff: Write erst wenn Palettierer fertig. Metall: Handling plus RFID, Code und Artikel als Merker.

Ohne gültigen Write gibt das Gate die Palette nicht frei. So bleibt die Lagerbuchung nachvollziehbar.

---

## Folie 10 — Hochregal W1 / W2 (~2 min) — langsam

Beide Regale haben **54 Fächer**, Raster **6 mal 9**, Fach **1 bis 6 unten**.

| | W1 Kunststoff | W2 Metall |
|---|---|---|
| Zone / NW | 5B / 29 | 5A / 28 |
| Kran | Crane 0 | Crane 1 |
| Merker | %M60+ | %M70+ |
| DB | ohne `_W2` | mit `_W2` |

Ablauf Automatik: freies Fach suchen, **Ziel-Fach** setzen, Kran nach X/Z, Gabel, Einlagern.

Auf dem HMI: grau frei, Farbe belegt, **gelber Rand = Ziel-Fach**.

PUT/GET vom PC liest nicht die optimierte Lager-DB, sondern die Occupancy-Merker `HRL_Occ_*` und `HRL_2_Occ_*` (`%MB400` / `%MB407`). OPC UA veröffentlicht dieselben Tags live.

---

## Folie 11 — Software (~1 min)

Alles liegt in **einem Git-Repository**: SCL unter `scl/`, Doku unter `docs/`.

OB1 hat 29 Netzwerke. Lastenheft beschreibt das Was, Pflichtenheft das Wie mit FUP, SCL und Tags.

Für den PC: Occupancy-Merker und **OPC UA** `Si_Lagerverwaltung_Online`. Die Web-App sucht in SQLite und zeigt das Gitter **live**, wenn die CPU auf `192.168.0.1:4840` erreichbar ist (PLCSIM Advanced).

---

## Folie 12 — HMI und Web (~1 min)

Das **TP2200 bleibt führend** für den Betrieb.

Die Streamlit-App **Lagerverwaltung Online** ist Suche und Übersicht, nicht die Maschinenbedienung. Zwei Tabs, Warehouse 1 und 2. OPC UA live ist nachgewiesen.

HMI-Simulation auf dem Laptop: Verbindung **PLCSIM**. Ethernet scheitert, weil das Panel nicht wirklich `192.168.0.2` ist. Mein Laptop hängt oft im WLAN `192.168.178.x`, die CPU auf `192.168.0.1`.

---

## Folie 13 — Stand (~1 min)

**Weit:** Warehouse 1 Kunststoff Ende-zu-Ende, Warehouse 2 SCL und Netzwerk 28, Palettierer und RFID, 2-axis, Vision, Raster-Teach, **OPC UA live** Streamlit, Plant-Start-Rezept.

**Offen:** CNC-Feinsteuerung, erste Auto-Palette auf W2, HMI-Events und 54-Fach-Animation am TP, Plant-FB in TIA zeichnen, Sicherheit und CE.

Die Kunststofflinie ist der Nachweis. Metall folgt dem gleichen Muster mit eigenen DBs. CPU bleibt **1518F**.

---

## Folie 14 — Schluss (~45 s)

Vielen Dank.

Die Kernaussage: **zwei Linien, RFID bis ins Fach, Warehouse 1 Kunststoff, Warehouse 2 Metall, ein HMI.**

Ich beantworte gerne Fragen. Bei Bedarf zeige ich Factory I/O Automatik Warehouse 1 oder die Web-Oberfläche.

---

## Falls die Zeit knapp wird

Überspringen oder kürzen: Folie 8 (Zonen 1–3), Folie 12 (Web). **Folie 5, 6 und 10 nicht streichen.**

## Falls Zeit übrig ist

Kurz Demo: Auto-Zyklus W1 oder Streamlit `http://localhost:8501`.
