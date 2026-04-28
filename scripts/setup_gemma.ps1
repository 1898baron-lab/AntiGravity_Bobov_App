# ============================================================
# MASTODONT — Gemma Local Setup Script
# Запускает Ollama + Gemma-4 E2B (лёгкая модель, ~2GB)
# Совместим с RTX 5060 Laptop GPU
# ============================================================

param(
    [string]$Model = "gemma2:2b",
    [switch]$SkipInstall,
    [switch]$TestOnly
)

$ErrorActionPreference = "Stop"
$OllamaPath = "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe"
$InstallerPath = "$env:TEMP\OllamaSetup.exe"

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  MASTODONT Gemma Setup" -ForegroundColor Cyan
Write-Host "  Model: $Model" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# --- STEP 1: Check / Install Ollama ---
if (-not $SkipInstall) {
    if (Test-Path $OllamaPath) {
        Write-Host "[OK] Ollama already installed at $OllamaPath" -ForegroundColor Green
    } else {
        Write-Host "[...] Installing Ollama..." -ForegroundColor Yellow
        if (-not (Test-Path $InstallerPath)) {
            Write-Host "[...] Downloading installer..." -ForegroundColor Yellow
            Invoke-WebRequest -Uri "https://ollama.com/download/OllamaSetup.exe" `
                -OutFile $InstallerPath -UseBasicParsing
        }
        Write-Host "[...] Running installer silently..." -ForegroundColor Yellow
        Start-Process -FilePath $InstallerPath -ArgumentList "/S" -Wait
        Write-Host "[OK] Ollama installed!" -ForegroundColor Green
    }
}

# --- STEP 2: Start Ollama server ---
$running = $false
try {
    $resp = Invoke-WebRequest -Uri "http://localhost:11434" -UseBasicParsing -TimeoutSec 3
    if ($resp.StatusCode -eq 200) { $running = $true }
} catch {}

if (-not $running) {
    Write-Host "[...] Starting Ollama server..." -ForegroundColor Yellow
    Start-Process -FilePath $OllamaPath -ArgumentList "serve" -WindowStyle Hidden
    Start-Sleep -Seconds 3
    Write-Host "[OK] Ollama server started on http://localhost:11434" -ForegroundColor Green
} else {
    Write-Host "[OK] Ollama server already running" -ForegroundColor Green
}

if ($TestOnly) {
    Write-Host "[OK] Server is up. Skipping model pull." -ForegroundColor Green
    exit 0
}

# --- STEP 3: Pull model ---
Write-Host ""
Write-Host "[...] Pulling model '$Model' (may take a few minutes)..." -ForegroundColor Yellow
& $OllamaPath pull $Model
Write-Host "[OK] Model '$Model' ready!" -ForegroundColor Green

# --- STEP 4: Quick test ---
Write-Host ""
Write-Host "[...] Running quick test..." -ForegroundColor Yellow
$testResult = & python scripts\gemma_ollama.py chat --model $Model --prompt "Скажи 'Mastodont online' одной строкой."
Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host "  TEST RESULT:" -ForegroundColor Green
Write-Host "  $testResult" -ForegroundColor White
Write-Host "============================================" -ForegroundColor Green
Write-Host ""
Write-Host "[DONE] Gemma is live! Use:" -ForegroundColor Cyan
Write-Host "  python scripts\gemma_ollama.py status" -ForegroundColor White
Write-Host "  python scripts\gemma_ollama.py chat --model $Model --prompt 'ваш вопрос'" -ForegroundColor White
Write-Host ""
