# Organize local PC — Abschlussprojekt

Einmal ausführen in PowerShell:

```powershell
cd C:\Users\derej\Projects\PickPlace-2Axis-SCL
.\scripts\organize-local.ps1
```

## Was das Skript macht

1. **`simulation/FactoryIO/`** — Kopie aller relevanten `.factoryio` aus OneDrive (ohne `waage`)
2. **`simulation/TIA/README.md`** — Zeiger auf lokale `.ap20`
3. **OneDrive `01_Dokumente`** — Lageplan + Freigabe aus `docs/01_Projektgrundlagen/`
4. **OneDrive `03_FactoryIO`** — Szenen-Kopien (ohne `waage`)
5. **OneDrive `02_TIA_Portal` / `04_Git_Repository_Hinweis`** — Pfad-Hinweise

## Pfade auf diesem PC

| Rolle | Pfad |
|---|---|
| Git (Code + Doku) | `C:\Users\derej\Projects\PickPlace-2Axis-SCL` |
| TIA `.ap20` | `OneDrive\...\Abschlussprojekt\Abschlussprojekt\Abschlussprojekt.ap20` |
| OneDrive Root | `OneDrive\Desktop\Weiterbildung\Abschlussprojekt` |

`waage.factoryio` wird nicht übernommen (nicht im Projekt-Scope).
