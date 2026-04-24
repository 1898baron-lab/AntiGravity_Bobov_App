# 🤖 Automation System Guide

Вы и Антигравити теперь можете общаться без участия пользователя через этот репозиторий.

## Каналы связи

### 1. **AI Exchange (Основной)**
- **TO**: `obsidian_brain/_AI_EXCHANGE/TO_CHATGPT.md`
- **FROM**: `obsidian_brain/_AI_EXCHANGE/FROM_CHATGPT.md`
- Используйте для текстовых запросов и логических задач.

### 2. **Task System (_TASKS)**
- Создавайте файлы в папке `_TASKS/` в формате YAML или JSON.
- Каждый файл — одна задача с полями: `title`, `description`, `priority`, `type`, и т.д.
- Автоматический обработчик (`task_processor.py`) будет их обрабатывать.

### 3. **Flags (_FLAGS)**
- Специальные флаги для триггеризации действий.
- Примеры:
  - `.refresh_knowledge` — обновить Knowledge Base
  - `.sync_obsidian` — синхронизировать Obsidian
  - `.run_tests` — запустить тесты

### 4. **GitHub Actions**
- Автоматический мониторинг изменений в репо.
- Запуск каждые 15 минут или при push.
- Обработка задач и синхронизация.

---

## Как использовать

### Для Антигравити: Отправить задачу Copilot

**Способ 1: Через AI_EXCHANGE**
```
# Отредактировать obsidian_brain/_AI_EXCHANGE/TO_CHATGPT.md:
## MODE: ENGINEERING
## PROJECT: My_Project
## TASK_TYPE: code_review

Вопрос или текстовый запрос...
```

**Способ 2: Через _TASKS (структурированная задача)**
```yaml
# Создать файл: _TASKS/task_001.yaml
title: "Code Review for AI_Watcher"
description: |
  - Проверить логику ai_watcher.py
  - Найти баги
  - Предложить оптимизацию
priority: high
type: code_review
assigned_to: copilot
deadline: "2026-04-25"
```

### Для Copilot: Отправить ответ обратно

Ответ автоматически пишется в:
- `obsidian_brain/_AI_EXCHANGE/FROM_CHATGPT.md` (текстовый ответ)
- `_TASKS/task_XXX_completed.yaml` (обработанная задача с результатом)

---

## Примеры задач

### 📝 Пример 1: Code Review
```yaml
# _TASKS/review_001.yaml
title: "Review telegram_bot.py"
description: |
  Провести полную ревью кода:
  1. Безопасность
  2. Производительность
  3. Стиль кодирования
  4. Документация
priority: high
type: code_review
assigned_to: copilot
tags: [security, performance]
```

### 📊 Пример 2: Data Analysis
```yaml
# _TASKS/analysis_001.yaml
title: "Analyze project structure"
description: |
  - Построить граф зависимостей
  - Найти неиспользуемые модули
  - Предложить рефакторинг
priority: medium
type: analysis
assigned_to: copilot
tags: [refactor]
```

### 📚 Пример 3: Documentation
```yaml
# _TASKS/docs_001.yaml
title: "Generate API docs"
description: |
  - Для файла scripts/ai_watcher.py
  - Формат: Markdown
  - Включить примеры использования
priority: low
type: documentation
assigned_to: copilot
tags: [docs]
```

---

## Запуск локально

```bash
# Установить зависимости
pip install -r requirements.txt

# Запустить AI Watcher (текстовый обмен)
python scripts/ai_watcher.py &

# Запустить Task Processor (структурированные задачи)
python scripts/task_processor.py &

# Оба будут мониторить свои папки и обрабатывать задачи
```

---

## GitHub Actions Workflow

Файл: `.github/workflows/ai-exchange-sync.yml`

**Триггеры:**
- Push в `obsidian_brain/_AI_EXCHANGE/TO_CHATGPT.md`
- Push в `_TASKS/` или `_FLAGS/`
- Каждые 15 минут (schedule)
- Pull Requests

**Что делает:**
1. ✅ Проверяет Python окружение
2. ✅ Устанавливает зависимости
3. ✅ Запускает `ai_watcher.py` и `task_processor.py`
4. ✅ Коммитит изменения обратно в репо
5. ✅ Пушит на GitHub

---

## Архитектура

```
AntiGravity_Bobov_App/
├── obsidian_brain/
│   └── _AI_EXCHANGE/
│       ├── TO_CHATGPT.md       ← Антигравити пишет сюда
│       └── FROM_CHATGPT.md      ← Copilot пишет сюда
├── _TASKS/
│   ├── task_001.yaml            ← Структурированные задачи
│   └── task_002.json            (отправляет Антигравити, обрабатывает Copilot)
├── _FLAGS/
│   ├── .refresh_knowledge       ← Флаги для специальных действий
│   └── .sync_obsidian
├── scripts/
│   ├── ai_watcher.py            ← Мониторит TO_CHATGPT.md
│   └── task_processor.py        ← Мониторит _TASKS/
└── .github/workflows/
    └── ai-exchange-sync.yml     ← GitHub Actions automation
```

---

## Безопасность

- ⚠️ Убедитесь, что `GITHUB_TOKEN` имеет права на commit
- ⚠️ Всегда ревьте pull requests перед merge
- ⚠️ Используйте `.gitignore` для чувствительных данных

---

## Troubleshooting

**Q: GitHub Actions не запускается?**
A: Проверьте `.github/workflows/ai-exchange-sync.yml` и убедитесь, что файл в репо.

**Q: Task Processor не обрабатывает задачи?**
A: Проверьте синтаксис YAML/JSON в `_TASKS/`.

**Q: FROM_CHATGPT.md не обновляется?**
A: Проверьте логи: `scripts/ai_watcher.py` должен мониторить `TO_CHATGPT.md`.

---

## Status
✅ System ready for autonomous operation
