"""
Claude Connector for Antigravity IDE
=====================================
Поднимает локальный HTTP-сервер, совместимый с Anthropic API,
используя Playwright для взаимодействия с claude.ai.

Запуск:
    pip install playwright fastapi uvicorn
    playwright install chromium
    python claude_connector.py

После запуска добавь в mcp_config.json:
    "claude": { "serverUrl": "http://localhost:8765" }
"""

import asyncio
import json
import time
import uuid
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, StreamingResponse
from playwright.async_api import async_playwright, Browser, Page
from playwright_stealth import stealth_async

# ──────────────────────────────────────────────
# Конфиг
# ──────────────────────────────────────────────
PORT = 8765
SESSION_FILE = "claude_session.json"   # сохранённая сессия браузера
HEADLESS = True                         # False — для отладки (видно браузер)
CLAUDE_URL = "https://claude.ai/new"

# CSS-селекторы (актуальны на апрель 2026, могут меняться)
INPUT_SELECTOR = '[contenteditable="true"][data-testid="composer-input"], \
                  [contenteditable="true"].ProseMirror, \
                  div[contenteditable="true"]'
RESPONSE_SELECTOR = '[data-testid="chat-message-content"]:last-child, \
                     .font-claude-message:last-child'
STOP_INDICATOR = '[data-testid="stop-button"]'   # кнопка «стоп» = генерация идёт

# ──────────────────────────────────────────────
# Глобальный браузер
# ──────────────────────────────────────────────
_browser: Browser | None = None
_page: Page | None = None


async def get_page() -> Page:
    global _browser, _page
    if _page is None or _page.is_closed():
        pw = await async_playwright().start()
        launch_args = {
            "executable_path": r"C:\Users\Sasha  Baron\AppData\Local\Yandex\YandexBrowser\Application\browser.exe",
            "args": ["--disable-blink-features=AutomationControlled"],
            "ignore_default_args": ["--enable-automation"]
        }
        try:
            _browser = await pw.chromium.launch(headless=HEADLESS, **launch_args)
            context = await _browser.new_context(storage_state=SESSION_FILE)
        except Exception:
            # Если файла сессии нет — открываем без него (нужен ручной логин)
            _browser = await pw.chromium.launch(headless=False, **launch_args)
            context = await _browser.new_context()
        _page = await context.new_page()
        await stealth_async(_page)
        await _page.goto(CLAUDE_URL)
        await _page.wait_for_load_state("networkidle")
    return _page


async def send_message(prompt: str) -> str:
    """Отправляет промпт в claude.ai и возвращает ответ."""
    page = await get_page()

    # Открываем новый чат
    await page.goto(CLAUDE_URL)
    await page.wait_for_load_state("networkidle")
    await asyncio.sleep(1)

    # Находим поле ввода
    input_box = await page.wait_for_selector(INPUT_SELECTOR, timeout=15000)
    await input_box.click()
    await input_box.fill(prompt)
    await page.keyboard.press("Enter")

    # Ждём начала генерации
    await asyncio.sleep(2)

    # Ждём завершения (кнопка «стоп» исчезает)
    for _ in range(120):   # максимум 120 секунд
        stop_visible = await page.query_selector(STOP_INDICATOR)
        if stop_visible is None:
            break
        await asyncio.sleep(1)

    await asyncio.sleep(1)  # финальный буфер

    # Читаем ответ
    response_el = await page.query_selector(RESPONSE_SELECTOR)
    if response_el:
        return await response_el.inner_text()
    return "Ошибка: не удалось получить ответ от Claude."


async def save_session():
    """Сохраняет куки/сессию в файл (вызови один раз после ручного логина)."""
    page = await get_page()
    await page.context.storage_state(path=SESSION_FILE)
    print(f"Сессия сохранена в {SESSION_FILE}")


# ──────────────────────────────────────────────
# FastAPI — совместимый с Anthropic API формат
# ──────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    # прогрев браузера при старте
    await get_page()
    yield
    if _browser:
        await _browser.close()

app = FastAPI(title="Claude Connector", lifespan=lifespan)


@app.post("/v1/messages")
async def messages(request: Request):
    """Эмулирует Anthropic Messages API."""
    body = await request.json()
    messages_list = body.get("messages", [])
    stream = body.get("stream", False)

    # Собираем промпт из последнего user-сообщения
    prompt = ""
    for msg in reversed(messages_list):
        if msg.get("role") == "user":
            content = msg.get("content", "")
            if isinstance(content, list):
                prompt = " ".join(
                    c.get("text", "") for c in content if c.get("type") == "text"
                )
            else:
                prompt = str(content)
            break

    if not prompt:
        return JSONResponse({"error": "No user message found"}, status_code=400)

    response_text = await send_message(prompt)

    # Формат ответа Anthropic API
    response = {
        "id": f"msg_{uuid.uuid4().hex[:24]}",
        "type": "message",
        "role": "assistant",
        "content": [{"type": "text", "text": response_text}],
        "model": "claude-via-web",
        "stop_reason": "end_turn",
        "stop_sequence": None,
        "usage": {"input_tokens": len(prompt) // 4, "output_tokens": len(response_text) // 4},
    }

    if stream:
        async def event_stream():
            chunk = {
                "type": "content_block_delta",
                "delta": {"type": "text_delta", "text": response_text},
            }
            yield f"data: {json.dumps(chunk)}\n\n"
            yield "data: [DONE]\n\n"
        return StreamingResponse(event_stream(), media_type="text/event-stream")

    return JSONResponse(response)


@app.get("/health")
async def health():
    return {"status": "ok", "timestamp": time.time()}


@app.post("/save-session")
async def save_session_endpoint():
    """Сохраняет текущую сессию браузера."""
    await save_session()
    return {"status": "saved", "file": SESSION_FILE}


# ──────────────────────────────────────────────
# Точка входа
# ──────────────────────────────────────────────
if __name__ == "__main__":
    print(f"Claude Connector запущен на http://localhost:{PORT}")
    print(f"Добавь в mcp_config.json: \"serverUrl\": \"http://localhost:{PORT}\"")
    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="info")
