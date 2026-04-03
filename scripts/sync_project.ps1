# AntiGravity Sync Script (v1.0)
# Bidirectional sync between C: and G:

$localPath = "C:\ANTIGRAVITY\1\AI_Project_Backup"
$cloudPath = "G:\Мой диск\AntiGravity\AI_Project_Backup"

Write-Host "--- AntiGravity Sync Starting ---" -ForegroundColor Cyan

# 1. Push: Local -> Cloud (Only newer files)
Write-Host "[1/2] Синхронизация: Локальный -> Облако..." -ForegroundColor Yellow
robocopy $localPath $cloudPath /E /XO /XJ /R:3 /W:5 /MT:32 /NP /LOG+:sync_push.log
# Добавляем синхронизацию .cursor настроек (если есть)
if (Test-Path "$localPath\.cursor") { robocopy "$localPath\.cursor" "$cloudPath\.cursor" /E /XO /XJ /R:3 /W:5 /NP /LOG+:sync_cursor_push.log }

# 2. Pull: Cloud -> Local (Only newer files)
Write-Host "[2/2] Синхронизация: Облако -> Локальный..." -ForegroundColor Yellow
robocopy $cloudPath $localPath /E /XO /XJ /R:3 /W:5 /MT:32 /NP /LOG+:sync_pull.log
# Затягиваем .cursor настройки
if (Test-Path "$cloudPath\.cursor") { robocopy "$cloudPath\.cursor" "$localPath\.cursor" /E /XO /XJ /R:3 /W:5 /NP /LOG+:sync_cursor_pull.log }

Write-Host "--- Синхронизация завершена! ---" -ForegroundColor Green
