# Master-Sync Daemon v1.2
# Automated project synchronization with GitHub

$SyncInterval = 600
$ProjectRoot = "C:\ANTIGRAVITY\1"
$LogFilePath = "$ProjectRoot\.agents\scripts\sync_log.txt"

function Write-LogEntry {
    param($LogMessage)
    $TimeStamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "[$TimeStamp] $LogMessage" | Out-File -FilePath $LogFilePath -Append -Encoding UTF8
}

Write-LogEntry "Master-Sync Daemon started. Monitoring active."

while($true) {
    try {
        Set-Location $ProjectRoot
        $GitStatus = git status --short
        
        if ($GitStatus) {
            Write-LogEntry "Changes detected. Starting synchronization..."
            git add -A
            $CommitMessage = "auto-save: $(Get-Date -Format 'yyyy-MM-dd HH:mm') [Mastodont AI]"
            git commit -m $CommitMessage
            
            $PushOutput = git push origin main 2>&1
            if ($LASTEXITCODE -eq 0) {
                Write-LogEntry "Sync successful: $PushOutput"
            } else {
                Write-LogEntry "WARNING: Push failed: $PushOutput"
            }
        }
    }
    catch {
        $ErrorDetail = $_.Exception.Message
        Write-LogEntry "CRITICAL ERROR: $ErrorDetail"
    }
    
    Start-Sleep -Seconds $SyncInterval
}
