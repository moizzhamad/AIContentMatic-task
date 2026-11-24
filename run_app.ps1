# QuantumTrade PowerShell Runner
Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "       QuantumTrade - Virtual Stock Trading Simulator" -ForegroundColor Cyan
Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host ""

$pythonCmd = "python"
try {
    $ver = & python --version 2>&1
    if ($LASTEXITCODE -ne 0 -or "$ver" -like "*not found*") {
        throw "not found"
    }
} catch {
    $fallback = "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe"
    if (Test-Path $fallback) {
        $pythonCmd = $fallback
    }
}

# Ensure dependencies
& $pythonCmd -m pip install -r backend\requirements.txt

# Run unified server
& $pythonCmd run.py
