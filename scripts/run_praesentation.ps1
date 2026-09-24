# Build and open the 15-minute Abschlussprojekt PowerPoint.
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
python "$Root\scripts\generate_praesentation.py"
$Pptx = Join-Path $Root "docs\01_Projektgrundlagen\Praesentation_Abschlussprojekt_15min.pptx"
Start-Process $Pptx
