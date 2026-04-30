"""
ChatGPT Connector for Antigravity IDE (Yandex Edition)
======================================================
Uses Playwright to interact with chatgpt.com via Yandex Browser.
"""

import asyncio
import os
import json
import time
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from playwright.async_api import async_playwright, Browser, Page
from playwright_stealth import Stealth

PORT = 8001
SESSION_FILE = r"C:\ANTIGRAVITY\1\chatgpt_session.json"
YANDEX_PATH = r"C:\Users\Sasha  Baron\AppData\Local\Yandex\YandexBrowser\Application\browser.exe"
CHATGPT_URL = "https://chatgpt.com/"

# Selectors for ChatGPT
INPUT_SELECTOR = '#prompt-textarea'
RESPONSE_SELECTOR = '[data-message-author-role="assistant"]'
SEND_BUTTON_SELECTOR = '[data-testid="send-button"]'

_browser: Browser | None = None
_page: Page | None = None

async def get_page() -> Page:
    global _browser, _page
    if _page is None or _page.is_closed():
        pw = await async_playwright().start()
        try:
            # Пытаемся подключиться к уже запущенному Яндексу через CDP
            print("[DEBUG] Attempting to connect via CDP (port 9222)...")
            _browser = await pw.chromium.connect_over_cdp("http://localhost:9222")
            context = _browser.contexts[0]
            # Ищем вкладку с ChatGPT или создаем новую
            for p in context.pages:
                if "chatgpt.com" in p.url:
                    _page = p
                    print(f"[DEBUG] Found existing ChatGPT tab: {p.url}")
                    break
            if not _page:
                _page = await context.new_page()
                await _page.goto(CHATGPT_URL)
        except Exception as e:
            print(f"[DEBUG] CDP connection failed: {e}. Falling back to standalone launch.")
            try:
                _browser = await pw.chromium.launch(
                    headless=False,
                    executable_path=YANDEX_PATH,
                    args=["--disable-blink-features=AutomationControlled", "--no-sandbox"],
                    ignore_default_args=["--enable-automation"]
                )
                if os.path.exists(SESSION_FILE):
                    context = await _browser.new_context(storage_state=SESSION_FILE)
                else:
                    context = await _browser.new_context()
                _page = await context.new_page()
                await Stealth().apply_stealth_async(_page)
                await _page.goto(CHATGPT_URL)
            except Exception as e2:
                print(f"[DEBUG] Standalone launch failed: {e2}")
                return None
    return _page

async def send_message(prompt: str, chat_url: str | None = None) -> tuple[str, str]:
    page = await get_page()
    if chat_url and page.url != chat_url:
        await page.goto(chat_url)
        await asyncio.sleep(2)
    try:
        input_box = await page.wait_for_selector(INPUT_SELECTOR, timeout=15000)
        await input_box.click()
        await page.keyboard.type(prompt, delay=10)
        await asyncio.sleep(1)
        await page.keyboard.press("Enter")
        
        # Wait for response
        await asyncio.sleep(10)
        responses = await page.query_selector_all(RESPONSE_SELECTOR)
        if responses:
            return (await responses[-1].inner_text()).strip(), page.url
        return "Ошибка: ответ не найден.", page.url
    except Exception as e:
        return f"Ошибка: {str(e)}", page.url

app = FastAPI(title="ChatGPT Connector")

@app.post("/v1/messages")
async def messages(request: Request):
    body = await request.json()
    prompt = body.get("messages", [{}])[-1].get("content", "")
    chat_url = body.get("chat_url")
    response_text, final_url = await send_message(prompt, chat_url=chat_url)
    return JSONResponse({
        "id": final_url,
        "content": [{"type": "text", "text": response_text}]
    })

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=PORT)
