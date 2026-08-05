# Abschlussprojekt — Fertigungs- und Lageranlage (Factory)

**Thema:** Entwicklung und Simulation einer automatisierten Fertigungs- und Lageranlage mit RFID-gestützter Produktverfolgung in **TIA Portal V20** und **Factory I/O**

**Master-Dokumentation:** [`docs/00_Projekt/README.md`](docs/00_Projekt/README.md)

---

## Factory — Repositories

| Zone | Subsystem | Repository |
|---|---|---|
| 3 | Two-Axis Pick & Place | **dieses Repo** → `scl/PickPlace_DigitalAnalog.scl` |
| 4 | Palettierer | **dieses Repo** → `scl/FB_Palletizer.scl` |
| 5 | Hochregallager | [`Hochregallager-SCL`](../Hochregallager-SCL) |

Dieses Repo dient zusätzlich als **Dokumentations-Hub** der Gesamtanlage (`docs/00_Projekt` … `04_CE_Dokumentation`).

---

## Inhalt dieses Repos (Code)

| Pfad | Beschreibung |
|---|---|
| `scl/FB_Palletizer.scl` | Palettierer FB v2.1 + HMI |
| `scl/PickPlace_DigitalAnalog.scl` | Two-Axis Pick & Place FB v1.3 |
| `scl/PLC_Tags_Palletizer.*` | PLC-Tags |
| `scl/UDT_Palletizer.scl` | optionale UDT |
| `docs/Palletizer_Dokumentation.md` | Palettierer-Technikdoku |
| `docs/HMI_Palletizer_Organization.md` | HMI-Organisation Palettierer |
| `docs/03_Subsysteme/` | Verweise Zone 3 / 4 / 5 |

---

## Nächster Schritt

Weitere Dokumente (Lastenheft, Anlagenübersicht, RFID, Sicherheit …) einzeln liefern — sie werden unter `docs/` eingeordnet und die Checkliste aktualisiert.
