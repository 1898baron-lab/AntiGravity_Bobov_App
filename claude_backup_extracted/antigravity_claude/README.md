# Claude Connector для Antigravity

Локальный HTTP-сервер, который превращает сессию **claude.ai** в Anthropic-совместимый API endpoint.
Antigravity подключается к нему как к обычному MCP-серверу.

---

## Быстрый старт

### 1. Установка зависимостей

```bash
pip install playwright fastapi uvicorn
playwright install chromium
```

### 2. Первый вход (один раз)

```bash
python first_login.py
```

Откроется браузер → залогинься → нажми Enter.
Создастся файл `claude_session.json`.

### 3. Запуск коннектора

```bash
python claude_connector.py
```

Сервер поднимется на `http://localhost:8765`.

### 4. Подключение в Antigravity

Открой файл:
```
C:\Users\<USER>\.gemini\antigravity\mcp_config.json
```

Добавь (или замени содержимое):
```json
{
  "mcpServers": {
    "claude-web": {
      "serverUrl": "http://localhost:8765"
    }
  }
}
```

Перезапусти Antigravity → в MCP Servers появится `claude-web`.

---

## Структура файлов

```
antigravity_claude/
├── claude_connector.py    # основной сервер
├── first_login.py         # однократный логин
├── mcp_config_claude.json # готовый конфиг для Antigravity
├── claude_session.json    # создаётся автоматически после логина
└── README.md
```

---

## Важно

- Сессия хранится в `claude_session.json` — не коммить в публичный репо
- Добавь в `.gitignore`: `claude_session.json`
- Коннектор использует бесплатный аккаунт claude.ai (лимиты как в браузере)
- При изменении верстки claude.ai — обнови CSS-селекторы в `claude_connector.py`

---

## .gitignore

```
claude_session.json
__pycache__/
*.pyc
```
