# organize-local.ps1 — Abschlussprojekt auf diesem PC
# Ausführen: .\scripts\organize-local.ps1

$ErrorActionPreference = 'Stop'

$proj = 'C:\Users\derej\Projects\PickPlace-2Axis-SCL'
$od   = 'C:\Users\derej\OneDrive\Desktop\Weiterbildung\Abschlussprojekt'
$docs = Join-Path $proj 'docs\01_Projektgrundlagen'

# --- simulation/FactoryIO ---
$simFio = Join-Path $proj 'simulation\FactoryIO'
$simTia = Join-Path $proj 'simulation\TIA'
New-Item -ItemType Directory -Force -Path $simFio, $simTia | Out-Null

$scenes = @(
    'aBSCHLUSSPROJEKT.factoryio',
    'Automated Warehouse.factoryio',
    'Automated Warehouse2w.factoryio',
    'Sortieranlage_mit_Pick_and_Place.factoryio'
)
foreach ($s in $scenes) {
    $src = Join-Path $od $s
    if (Test-Path -LiteralPath $src) {
        Copy-Item -LiteralPath $src -Destination (Join-Path $simFio $s) -Force
        Write-Host "simulation: $s"
    }
}
$rfid = Get-ChildItem -Path $od -Recurse -Filter 'Warenlager_RFID.factoryio' -ErrorAction SilentlyContinue | Select-Object -First 1
if ($rfid) {
    Copy-Item -LiteralPath $rfid.FullName -Destination (Join-Path $simFio 'Warenlager_RFID.factoryio') -Force
    Write-Host 'simulation: Warenlager_RFID.factoryio'
}

@(
    '# TIA Portal Projekt',
    '',
    'Lokaler Pfad auf diesem PC:',
    '',
    "`$od\Abschlussprojekt\Abschlussprojekt.ap20`",
    '',
    'Nicht ins Git kopiert (binär / groß). In TIA öffnen und SCL aus `scl/` importieren.'
) | Set-Content -Encoding utf8 (Join-Path $simTia 'README.md')

# --- OneDrive Ordner ---
@(
    (Join-Path $od '01_Dokumente'),
    (Join-Path $od '02_TIA_Portal'),
    (Join-Path $od '03_FactoryIO'),
    (Join-Path $od '04_Git_Repository_Hinweis')
) | ForEach-Object { New-Item -ItemType Directory -Force -Path $_ | Out-Null }

# 01_Dokumente
foreach ($f in @(
    'Lageplan.pdf',
    'Freigabedokument_Abschlussarbeit_Dereje_Hailemariam.pdf',
    'Freigabedokument_Abschlussarbeit_Dereje_Hailemariam.docx'
)) {
    $src = Join-Path $docs $f
    if (Test-Path -LiteralPath $src) {
        Copy-Item -LiteralPath $src -Destination (Join-Path $od "01_Dokumente\$f") -Force
        Write-Host "01_Dokumente: $f"
    }
}

# 03_FactoryIO (ohne waage)
Get-ChildItem $od -File -Filter '*.factoryio' -ErrorAction SilentlyContinue |
    Where-Object { $_.Name -ne 'waage.factoryio' } |
    ForEach-Object {
        Copy-Item $_.FullName (Join-Path $od "03_FactoryIO\$($_.Name)") -Force
    }
if ($rfid) {
    Copy-Item -LiteralPath $rfid.FullName -Destination (Join-Path $od '03_FactoryIO\Warenlager_RFID.factoryio') -Force
}
$waageOd = Join-Path $od '03_FactoryIO\waage.factoryio'
if (Test-Path -LiteralPath $waageOd) { Remove-Item -LiteralPath $waageOd -Force }

# Hinweise
@(
    "TIA-Projektordner: `$od\Abschlussprojekt\",
    'Projektdatei: Abschlussprojekt.ap20'
) | Set-Content -Encoding utf8 (Join-Path $od '02_TIA_Portal\PFAD.txt')

@(
    'Git-Repository (einzige Code-/Doku-Quelle):',
    '',
    $proj,
    '',
    'GitHub:',
    'https://github.com/AprilaydaH/Entwicklung-einer-automatisierten-Produktions--Montage--und-Lagerverwaltungsanlage',
    '',
    'Titel: Entwicklung einer automatisierten Produktions-, Montage- und Lagerverwaltungsanlage',
    '',
    'Struktur:',
    '  docs/   Dokumentation (Lageplan-Zonen)',
    '  scl/    Zone1..5, Foerderbaender, Hochregallager',
    '  simulation/FactoryIO/  Szenen-Kopien'
) | Set-Content -Encoding utf8 (Join-Path $od '04_Git_Repository_Hinweis\README.txt')

Write-Host ''
Write-Host '=== OneDrive ==='
Get-ChildItem $od -Directory | ForEach-Object { $_.Name }
Write-Host ''
Write-Host '=== 01_Dokumente ==='
Get-ChildItem (Join-Path $od '01_Dokumente') -File | ForEach-Object { $_.Name }
Write-Host ''
Write-Host '=== simulation/FactoryIO ==='
Get-ChildItem $simFio -File | ForEach-Object {
    '{0}  ({1:N2} MB)' -f $_.Name, ($_.Length / 1MB)
}
Write-Host 'Done.'
