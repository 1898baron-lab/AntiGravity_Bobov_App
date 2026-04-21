# Скрипт остановки Master-Sync Daemon
$ProcessName = "powershell"
$DaemonFile = "master_sync_daemon.ps1"

# Поиск процессов powershell, которые выполняют наш скрипт
$Processes = Get-WmiObject Win32_Process -Filter "Name = 'powershell.exe'" | Where-Object { $_.CommandLine -like "*$DaemonFile*" }

if ($Processes) {
    foreach ($P in $Processes) {
        Write-Host "Остановка процесса Master-Sync (PID: $($P.ProcessId))..."
        Stop-Process -Id $P.ProcessId -Force
    }
    Write-Host "Авто-синхронизация отключена."
}
else {
    Write-Host "Процесс Master-Sync не найден."
}
