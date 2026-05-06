@echo off
title Claude Code + Gemma4 (Local Proxy)

echo ====================================================
echo Запуск локального прокси-сервера (LiteLLM)
echo Модель: gemma4:26b-lite
echo ====================================================

:: Проверяем, запущен ли Ollama
echo Проверка статуса Ollama...
curl -s http://localhost:11434/api/tags >nul
if %errorlevel% neq 0 (
    echo [ОШИБКА] Ollama не запущена! Пожалуйста, запустите приложение Ollama.
    pause
    exit /b
)

:: Запускаем LiteLLM в фоновом режиме на порту 4000
echo Запускаем LiteLLM на порту 4000...
start "LiteLLM Proxy" cmd /c "C:\ANTIGRAVITY\1\.venv\Scripts\litellm.exe --model openai/gemma4:26b-lite --api_base http://127.0.0.1:1234/v1 --port 4000"

:: Ждем пару секунд, чтобы сервер успел подняться
timeout /t 3 /nobreak >nul

echo ====================================================
echo Запуск Claude Code
echo ====================================================

:: Настраиваем переменные окружения для подмены API
set ANTHROPIC_API_KEY=sk-ant-fake-local-key
set ANTHROPIC_BASE_URL=http://localhost:4000

:: Запускаем сам Claude Code
claude

echo.
echo Сессия завершена.
pause
