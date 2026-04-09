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
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse, StreamingResponse, FileResponse
from playwright.async_api import async_playwright, Browser, Page
from playwright_stealth import Stealth

# ──────────────────────────────────────────────
# Конфиг
# ──────────────────────────────────────────────
PORT = 8765
SESSION_FILE = r"C:\ANTIGRAVITY\1\claude_session.json"   # сохранённая сессия браузера
HEADLESS = False                        # Включаем видимый режим для отладки
CLAUDE_URL = "https://claude.ai/new"

# CSS-селекторы (улучшенные и расширенные)
INPUT_SELECTOR = '[contenteditable="true"][data-testid="composer-input"], \
                  [contenteditable="true"].ProseMirror, \
                  [aria-label*="Write a message"], \
                  div[contenteditable="true"]'

RESPONSE_SELECTOR = '[data-testid="ai-message"], \
                     .font-claude-response, \
                     .font-claude-message, \
                     [data-testid="chat-message-content"]'

STOP_INDICATOR = '[data-testid="stop-button"], [aria-label="Stop generating"]'

# Кнопки закрытия поп-апов
POPUP_CLOSE_BUTTONS = [
    'button:has-text("Got it")',
    'button:has-text("Close")',
    'button:has-text("Remind me later")',
    '[aria-label="Close modal"]',
    'button:has-text("Skip")'
]

SEND_BUTTON_SELECTOR = '[aria-label="Send Message"], [data-testid="send-button"], button:has(svg[viewBox*="0 0 24 24"])'

# ──────────────────────────────────────────────
# Глобальный браузер
# ──────────────────────────────────────────────
_browser: Browser | None = None
_page: Page | None = None


async def get_page() -> Page:
    global _browser, _page
    if _page is None or _page.is_closed():
        pw = await async_playwright().start()
        try:
            _browser = await pw.chromium.launch(
                headless=HEADLESS,
                executable_path=r"C:\Users\Sasha  Baron\AppData\Local\Yandex\YandexBrowser\Application\browser.exe",
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    "--disable-infobars",
                    "--window-position=0,0",
                    "--ignore-certifcate-errors",
                    "--ignore-certifcate-errors-spki-list",
                    "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
                ],
                ignore_default_args=["--enable-automation"]
            )
            context = await _browser.new_context(storage_state=SESSION_FILE)
        except Exception:
            # Если файла сессии нет — открываем без него (нужен ручной логин)
            _browser = await pw.chromium.launch(
                headless=False,
                executable_path=r"C:\Users\Sasha  Baron\AppData\Local\Yandex\YandexBrowser\Application\browser.exe",
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    "--disable-infobars",
                    "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
                ],
                ignore_default_args=["--enable-automation"]
            )
            context = await _browser.new_context()
        _page = await context.new_page()
        await Stealth().apply_stealth_async(_page)
        await _page.goto(CLAUDE_URL)
        await _page.wait_for_load_state("load")
        await asyncio.sleep(2)  # Даём время JS-фреймворку
    return _page


async def close_popups(page: Page):
    """Пытается закрыть мешающие всплывающие окна."""
    for selector in POPUP_CLOSE_BUTTONS:
        try:
            btn = await page.query_selector(selector)
            if btn and await btn.is_visible():
                await btn.click()
                print(f"Closed popup with selector: {selector}")
        except Exception:
            pass

async def send_message(prompt: str) -> str:
    """Отправляет промпт в claude.ai (V3 - имитация человека)."""
    page = await get_page()

    # Попытка навигации с ретраями
    for i in range(3):
        try:
            print(f"[DEBUG] Navigating (Attempt {i+1})...")
            await page.goto(CLAUDE_URL, wait_until="load", timeout=30000)
            break
        except Exception as e:
            await asyncio.sleep(2)
            if i == 2: return f"Ошибка навигации: {str(e)}"

    await asyncio.sleep(2)
    await close_popups(page)

    # Находим поле ввода и имитируем набор текста
    try:
        input_box = await page.wait_for_selector(INPUT_SELECTOR, timeout=15000)
        await input_box.click()
        # Посимвольный ввод для обхода защиты (delay 10ms)
        await page.keyboard.type(prompt, delay=10)
        await asyncio.sleep(1)
        
        # Пробуем нажать Enter
        await page.keyboard.press("Enter")
        
        # Если кнопка "Send" всё еще видна и активна через 1 сек — нажимаем её принудительно
        await asyncio.sleep(1)
        send_btn = await page.query_selector(SEND_BUTTON_SELECTOR)
        if send_btn and await send_btn.is_visible():
            await send_btn.click()
            print("[DEBUG] Forced click on Send button")
            
    except Exception as e:
        return f"Ошибка ввода: {str(e)}"

    # Ждём начала генерации (Stop button)
    print("[DEBUG] Waiting for generation...")
    try:
        await page.wait_for_selector(STOP_INDICATOR, timeout=10000)
    except:
        print("[DEBUG] Stop button not found, checking for text growth anyway")

    # Цикл ожидания завершения и роста текста
    last_text = ""
    for _ in range(120): # до 2 минут
        stop_btn = await page.query_selector(STOP_INDICATOR)
        
        # Получаем все блоки ответов
        resp_elements = await page.query_selector_all(RESPONSE_SELECTOR)
        if resp_elements:
            current_text = (await resp_elements[-1].inner_text()).strip()
            # Если текст перестал расти и кнопка стоп пропала — готово
            if stop_btn is None and current_text and current_text == last_text:
                return current_text
            last_text = current_text
        
        await asyncio.sleep(1)

    if last_text:
        return last_text
            
    return "Ошибка: Claude не начал генерацию или селекторы не нашли текст. Попробуйте обновить страницу в браузере."


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
    print(f"Claude Connector запущен на http://127.0.0.1:{PORT}")
    print(f"Добавь в mcp_config.json: \"serverUrl\": \"http://127.0.0.1:{PORT}\"")
    uvicorn.run(app, host="127.0.0.1", port=PORT, log_level="info")
