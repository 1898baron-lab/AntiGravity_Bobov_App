# AntiGravity: GitHub Exclusive Synchronization Engine 🐙🦾
# --------------------------------------------------------
# Version: 1.0 (Git Edition)
# Path: scripts/sync_project.ps1

# Используем глобальный git, так как он установлен в системе
$git = "git"
# Автоматически определяем директорию проекта (на уровень выше от папки scripts)
$projectDir = Split-Path -Parent $PSScriptRoot

Clear-Host
Write-Host "--- AntiGravity: GitHub Exclusive Sync ---" -ForegroundColor Cyan
Write-Host "Mode: Git Pull/Push (Cloud Mirror)" -ForegroundColor Gray

# 1. Проверка Git
if (-not (Test-Path $git)) {
    Write-Host "ERROR: Portable Git not found at $git" -ForegroundColor Red
    exit 1
}

cd $projectDir

# 2. Подготовка (Stage everything)
Write-Host "`n[1/4] Indexing Project Files..." -ForegroundColor Yellow
& $git add .

# 3. Коммит локальных изменений
Write-Host "[2/4] Capturing Local Context (Commit)..." -ForegroundColor Yellow
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$commitMsg = "Session Sync: $timestamp"
& $git commit -m $commitMsg

# 4. Подтягивание изменений (Pull)
Write-Host "[3/4] Fetching Cloud Updates (Pull/Rebase)..." -ForegroundColor Yellow
& $git pull --rebase origin main

# 5. Выгрузка в облако (Push)
Write-Host "[4/4] Synchronizing with GitHub (Push)..." -ForegroundColor Yellow
& $git push origin main

Write-Host "`n--- Sync Complete ---" -ForegroundColor Green
Write-Host "Project is live on GitHub Mirror." -ForegroundColor Gray
