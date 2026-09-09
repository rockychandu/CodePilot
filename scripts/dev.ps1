# CodePilot Unified Development Launcher (PowerShell)
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "   CodePilot Enterprise Development Platform              " -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Cyan

$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCmd) {
    Write-Error "Python 3 is required but not found on PATH."
    exit 1
}

$nodeCmd = Get-Command node -ErrorAction SilentlyContinue
if (-not $nodeCmd) {
    Write-Error "Node.js is required but not found on PATH."
    exit 1
}

Write-Host "[1/2] Launching CodePilot Backend on http://127.0.0.1:5000..." -ForegroundColor Yellow
$backendJob = Start-Job -ScriptBlock {
    Set-Location $using:PWD
    python -m backend.app
}

Start-Sleep -Seconds 2

Write-Host "[2/2] Launching Frontend Development Server (Vite) on http://127.0.0.1:5173..." -ForegroundColor Yellow
Write-Host "Access Web Application at: http://127.0.0.1:5173" -ForegroundColor Green
Write-Host "Press Ctrl+C to shutdown servers." -ForegroundColor Gray

try {
    npm run dev
} finally {
    Write-Host "Stopping backend service..." -ForegroundColor Yellow
    Stop-Job $backendJob -ErrorAction SilentlyContinue
    Remove-Job $backendJob -ErrorAction SilentlyContinue
    Write-Host "Shutdown complete." -ForegroundColor Green
}
