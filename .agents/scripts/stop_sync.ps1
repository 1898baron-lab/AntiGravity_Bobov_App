# Master-Sync Daemon Stop Script
$DaemonFileName = "master_sync_daemon.ps1"

# Find powershell processes running our specific daemon script
$TargetProcesses = Get-WmiObject Win32_Process -Filter "Name = 'powershell.exe'" | Where-Object { $_.CommandLine -like "*$DaemonFileName*" }

if ($TargetProcesses) {
    foreach ($Process in $TargetProcesses) {
        Write-Host "Stopping Master-Sync process (PID: $($Process.ProcessId))..."
        Stop-Process -Id $Process.ProcessId -Force
    }
    Write-Host "Auto-sync disabled successfully."
}
else {
    Write-Host "Master-Sync process not found."
}
