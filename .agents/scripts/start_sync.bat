@echo off
REM Master-Sync Startup Script
echo Starting Master-Sync Daemon in background...
powershell.exe -WindowStyle Hidden -ExecutionPolicy Bypass -File "C:\ANTIGRAVITY\1\.agents\scripts\master_sync_daemon.ps1"
echo Master-Sync started. Check sync_log.txt for status.
timeout /t 5
