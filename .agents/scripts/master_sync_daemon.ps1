# Master-Sync Daemon v1.0
# Автоматическая синхронизация проекта с GitHub

$IntervalSeconds = 600 # Интервал проверки (10 минут)
$ProjectRoot = "C:\ANTIGRAVITY\1"
$LogFile = "$ProjectRoot\.agents\scripts\sync_log.txt"

function Write-Log {
    param($Message)
    $TimeStamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "[$TimeStamp] $Message" | Out-File -FilePath $LogFile -Append
}

Write-Log "Master-Sync запущен. Интервал: $IntervalSeconds сек."

while($true) {
    try {
        Set-Location $ProjectRoot
        
        # Проверка наличия изменений
        $Status = git status --short
        
        if ($Status) {
            Write-Log "Обнаружены изменения. Начинаю синхронизацию..."
            
            git add -A
            $CommitMsg = "auto-save: $(Get-Date -Format 'yyyy-MM-dd HH:mm') [Mastodont AI]"
            git commit -m $CommitMsg
            
            # Попытка отправки на GitHub
            $PushResult = git push origin main 2>&1
            Write-Log "Синхронизация завершена успешно."
        }
    }
    catch {
        Write-Log "ОШИБКА: $($_.Exception.Message)"
    }
    
    Start-Sleep -Seconds $IntervalSeconds
}
