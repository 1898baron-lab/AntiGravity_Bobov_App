@echo off
:: AntiGravity Master Launch Script v2.0
chcp 65001 > nul

echo [1/5] Syncing with GitHub (Pull)...
git pull origin main

echo [2/5] Starting AntiGravity Hub (Port 8766)...
start "AntiGravity_Hub" /min cmd /c ".\.venv\Scripts\python.exe scripts/mcp_server_sse.py"

echo [3/5] Starting Claude Connector (Port 8765)...
start "Claude_Connector" /min cmd /c ".\.venv\Scripts\python.exe scripts/claude_connector/claude_connector.py"

echo [4/5] Starting Auto-Commit Watcher...
start "Auto_Sync" /min cmd /c ".\.venv\Scripts\python.exe scripts/auto_sync.py"

echo [5/5] Checking Obsidian status...
tasklist /nh /fi "imagename eq Obsidian.exe" | find /i "Obsidian.exe" > nul
if %errorlevel% neq 0 (
    echo [!] WARNING: Obsidian is not running.
) else (
    echo [OK] Obsidian is active.
)

echo.
echo ===================================================
echo   ANTIGRAVITY INFRASTRUCTURE IS LIVE (AUTOPILOT)
echo ===================================================
echo [8765] - Claude Connector
echo [8766] - AntiGravity Hub
echo [SYNC] - Auto-Commit Enabled
echo.
echo You can now focus on your work. Commits are automatic.
echo.
pause
