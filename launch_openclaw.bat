@echo off
title OpenClaw Launcher
echo ==========================================
echo Запуск OpenClaw (AntiGravity AI)
echo ==========================================

:: Указываем полный путь к Ollama, чтобы обойти ошибку "not recognized" в PowerShell
"C:\Users\Sasha  Baron\AppData\Local\Programs\Ollama\ollama.exe" launch openclaw

pause
