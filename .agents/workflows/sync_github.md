---
description: Синхронизация всего проекта на GitHub (git add, commit, push)
---

# /sync_github — Полная синхронизация проекта

## Шаги

// turbo-all

1. Перейти в папку проекта:
```powershell
cd C:\ANTIGRAVITY\1
```

2. Проверить статус изменений:
```powershell
git status --short
```

3. Добавить все изменения:
```powershell
git add -A
```

4. Зафиксировать коммит (сообщение генерируется автоматически на основе изменений):
```powershell
git commit -m "sync: автоматическая синхронизация $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
```

5. Отправить на GitHub:
```powershell
git push origin main
```

6. Если пуш отклонён — использовать принудительную отправку:
```powershell
git push origin main --force-with-lease
```
