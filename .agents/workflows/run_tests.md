---
description: Запуск всех тестов проекта через pytest
---

# /run_tests — Запуск тестов

## Шаги

// turbo-all

1. Запустить все тесты с подробным выводом:
```powershell
& "C:\ANTIGRAVITY\1\.venv\Scripts\python.exe" -m pytest -v
```

2. Если тесты упали — запустить конкретный файл для отладки:
```powershell
& "C:\ANTIGRAVITY\1\.venv\Scripts\python.exe" -m pytest tests/test_pdf_logic.py -v
```

3. Для тестов бота:
```powershell
& "C:\ANTIGRAVITY\1\.venv\Scripts\python.exe" -m pytest tests/test_bot_handlers.py -v
```
