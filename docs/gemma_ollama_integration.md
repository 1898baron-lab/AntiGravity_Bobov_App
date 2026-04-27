# Gemma + Ollama Integration

Это простая связка, чтобы локально запустить Gemma и подключить модель к вашей системе.

## 1. Самый быстрый путь

1. Установите `LM Studio` и откройте вкладку `Models`.
2. Найдите `gemma-4-31b-it` или `gemma-4-e2b-it`.
3. Скачайте `quantized (GGUF)` версию.
4. В `LM Studio` нажмите `Chat` и проверьте, что модель отвечает.

> Это самый быстрый способ проверить, что Gemma у вас работает.

## 2. Где лучше начинать

- Если у вас ноут с малым GPU или без GPU → `gemma-4-e2b-it`
- Если есть 16–24 ГБ VRAM → `gemma-4-31b-it` в квантованной версии
- Ошибка новичка: сразу брать 31B без ресурсов

## 3. Проверка через Ollama API

### 3.1 Установите Ollama

Перейдите на https://ollama.com и установите клиент.

### 3.2 Скачайте модель

```bash
ollama pull gemma-4-e2b-it
# или
ollama pull gemma-4-31b-it
```

### 3.3 Запустите сервер

```bash
ollama serve
```

По умолчанию сервер доступен на `http://localhost:11434`.

## 4. Локальный скрипт для запуска и теста

В репозитории добавлен скрипт:

```bash
python scripts/gemma_ollama.py status
python scripts/gemma_ollama.py list
python scripts/gemma_ollama.py chat --model gemma-4-e2b-it --prompt "Привет от Gemma"
```

Если хотите, сохраните вывод в файл:

```bash
python scripts/gemma_ollama.py chat --model gemma-4-e2b-it --prompt "Тест" --output response.json
```

## 5. Как встроить в вашу систему

1. Запустите `ollama serve`.
2. Используйте `http://localhost:11434/api/generate` для запросов.
3. Если нужно, опирайтесь на `scripts/gemma_ollama.py` как на простой клиент.

### Пример запроса через curl

```bash
curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{"model":"gemma-4-e2b-it","prompt":"Напиши короткий план интеграции", "stream": false}'
```

## 6. Мини-архитектура

```
[Whisper / голос] → [Gemma E2B] → быстрые ответы
                     [Gemma 31B] → сложные задачи
                     [твоя логика / Antigravity / репозиторий]
```

## 7. Что теперь сделано в репозитории

- Добавлен `scripts/gemma_ollama.py` — локальный помощник для Ollama+Gemma
- Добавлена документация `docs/gemma_ollama_integration.md`
- Обновлён дашборд `MASTADONT_DASHBOARD.md`

## 8. Что дальше

- Если надо, я могу сделать: `Gemma → RAG → Obsidian / Antigravity`.
- Или подготовить `Gemma` как ещё один источник для вашего `ChatGPT Bridge`.
