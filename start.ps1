$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$python = Join-Path $projectRoot "venv\Scripts\python.exe"
$appDir = Join-Path $projectRoot "quiz\src"

if (-not (Test-Path -LiteralPath $python)) {
    throw "Ambiente virtual não encontrado em '$python'. Crie a venv e instale requirements.txt antes de iniciar a API."
}

Set-Location -LiteralPath $projectRoot
& $python -m uvicorn presentation.http.main:app `
    --app-dir $appDir `
    --reload
