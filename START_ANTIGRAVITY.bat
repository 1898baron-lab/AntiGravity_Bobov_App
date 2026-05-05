@echo off
:: AntiGravity Master Launch Script
:: Sets UTF-8 encoding for clear Russian text in console
chcp 65001 > nul

echo [1/4] Синхронизация с GitHub...
git pull origin main

echo [2/4] Запуск AntiGravity Hub (Порт 8766)...
start /min "AntiGravity Hub" cmd /c ".\.venv\Scripts\python.exe scripts/mcp_server_sse.py"

echo [3/4] Запуск Claude Connector (Порт 8765)...
start /min "Claude Connector" cmd /c ".\.venv\Scripts\python.exe scripts/claude_connector/claude_connector.py"

echo [4/4] Проверка статуса Obsidian...
:: Проверка, запущен ли Obsidian (опционально)
tasklist /nh /fi "imagename eq Obsidian.exe" | find /i "Obsidian.exe" > nul
if %errorlevel% neq 0 (
    echo [!] ПРЕДУПРЕЖДЕНИЕ: Obsidian не запущен. Инструменты могут не работать.
) else (
    echo [OK] Obsidian запущен.
)

echo.
echo ===================================================
echo ИНФРАСТРУКТУРА ANTIGRAVITY ГОТОВА
echo ===================================================
echo [8765] - Claude Connector
echo [8766] - AntiGravity Hub (Obsidian/Ollama)
echo.
echo Ты можешь использовать свой "Gateway" интерфейс.
echo Не закрывай это окно, если хочешь видеть логи синхронизации.
pause
