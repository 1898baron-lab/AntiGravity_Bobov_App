---
description: Принудительный перезапуск или проверка среды NotebookLM MCP
---

# /check_notebooklm — Проверка статуса NotebookLM MCP

## Шаги

// turbo-all

1. Проверить конфигурацию `mcp_config.json`:
```powershell
Get-Content -Path "C:\Users\Sasha  Baron\.gemini\antigravity\mcp_config.json"
```

2. Убедиться, что исполняемый файл сервера на месте:
```powershell
Test-Path "C:\Users\Sasha  Baron\.local\bin\notebooklm-mcp.exe"
```
