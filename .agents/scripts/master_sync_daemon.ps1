# Master-Sync Daemon v1.1
# Автоматическая синхронизация проекта с GitHub

$IntervalSeconds = 600
$ProjectRoot = "C:\ANTIGRAVITY\1"
$LogFile = "$ProjectRoot\.agents\scripts\sync_log.txt"

function Write-Log {
    param($Message)
    $TimeStamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "[$TimeStamp] $Message" | Out-File -FilePath $LogFile -Append
}

Write-Log "Master-Sync перезапущен. Мониторинг активен."

while($true) {
    try {
        Set-Location $ProjectRoot
        $Status = git status --short
        
        if ($Status) {
            Write-Log "Обнаружены изменения. Начинаю синхронизацию..."
            git add -A
            $CommitMsg = "auto-save: $(Get-Date -Format 'yyyy-MM-dd HH:mm') [Mastodont AI]"
            git commit -m $CommitMsg
            
            $PushResult = git push origin main 2>&1
            if ($LASTEXITCODE -eq 0) {
                Write-Log "Синхронизация завершена успешно: $PushResult"
            } else {
                Write-Log "ПРЕДУПРЕЖДЕНИЕ: Ошибка при отправке на GitHub: $PushResult"
            }
        }
    }
    catch {
        $ErrorMessage = $_.Exception.Message
        Write-Log "ОШИБКА ЦИКЛА: $ErrorMessage"
    }
    
    Start-Sleep -Seconds $IntervalSeconds
}
