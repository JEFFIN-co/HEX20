$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$env:PYTHONPATH = Join-Path $Root "src"
Set-Location $Root
python -m streamlit run app/hex20_live_dashboard.py
