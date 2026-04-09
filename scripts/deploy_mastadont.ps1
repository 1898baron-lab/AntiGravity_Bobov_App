# deploy_mastadont.ps1
# Скрипт для стабильного развертывания проекта MASTADONT AI

$ROOT = "C:\ANTIGRAVITY\1"
$VENV_PYTHON = "$ROOT\.venv\Scripts\python.exe"
$CONNECTOR_PATH = "$ROOT\scripts\claude_connector\claude_connector.py"
$BOT_PATH = "$ROOT\pdf_funnel_output\telegram_bot.py"
$LOG_DIR = "$ROOT\logs"

Write-Host "--- [DEPLOY] Starting Cleanup ---" -ForegroundColor Cyan

# 1. Kill all related processes
Write-Host "Killing existing project processes..."
Get-WmiObject Win32_Process | Where-Object { 
    $_.CommandLine -like "*telegram_bot.py*" -or 
    $_.CommandLine -like "*claude_connector.py*" 
} | ForEach-Object { 
    Write-Host "Stopping PID $($_.ProcessId): $($_.Name)"
    Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue
}

# 2. Kill anyone on port 8765
$portProcess = netstat -ano | findstr :8765
if ($portProcess) {
    $pidToKill = $portProcess.Split(" ", [System.StringSplitOptions]::RemoveEmptyEntries)[-1]
    Write-Host "Releasing port 8765 (Killing PID $pidToKill)..."
    Stop-Process -Id $pidToKill -Force -ErrorAction SilentlyContinue
}

Start-Sleep -s 2

# 3. Clean logs
if (Test-Path $LOG_DIR) {
    Write-Host "Cleaning logs..."
    Remove-Item -Path "$LOG_DIR\*" -Force -ErrorAction SilentlyContinue
} else {
    New-Item -ItemType Directory -Path $LOG_DIR -Force
}

Write-Host "--- [DEPLOY] Starting Services ---" -ForegroundColor Green

# 4. Start Connector
Write-Host "Starting Claude Connector..."
$connectorProc = Start-Process -FilePath $VENV_PYTHON -ArgumentList $CONNECTOR_PATH -WindowStyle Normal -PassThru
Write-Host "Connector PID: $($connectorProc.Id)"

Start-Sleep -s 5

# 5. Start Bot
Write-Host "Starting Telegram Bot..."
$botProc = Start-Process -FilePath $VENV_PYTHON -ArgumentList $BOT_PATH -WindowStyle Normal -PassThru
Write-Host "Bot PID: $($botProc.Id)"

Write-Host "--- [DEPLOY] Verification ---" -ForegroundColor Yellow
Start-Sleep -s 2

$procs = Get-WmiObject Win32_Process | Where-Object { 
    $_.CommandLine -like "*telegram_bot.py*" -or 
    $_.CommandLine -like "*claude_connector.py*" 
}
Write-Host "Active processes found: $($procs.Count)"
foreach ($p in $procs) {
    Write-Host "[$($p.ProcessId)] $($p.CommandLine)"
}

Write-Host "--- [DEPLOY] Done! Check Telegram and the open windows. ---" -ForegroundColor White
