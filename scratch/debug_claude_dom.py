import asyncio
import json
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

CLAUDE_URL = "https://claude.ai/new"
SESSION_FILE = "claude_session.json"

async def debug_dom():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            executable_path=r"C:\Users\Sasha  Baron\AppData\Local\Yandex\YandexBrowser\Application\browser.exe",
            args=["--disable-blink-features=AutomationControlled"],
            ignore_default_args=["--enable-automation"]
        )
        context = await browser.new_context(storage_state=SESSION_FILE)
        page = await context.new_page()
        await Stealth().apply_stealth_async(page)
        
        print("Заходим на Claude...")
        await page.goto(CLAUDE_URL)
        await page.wait_for_load_state("load")
        await asyncio.sleep(5)
        
        print("Отправляем тестовый запрос...")
        input_selector = '[contenteditable="true"]'
        await page.wait_for_selector(input_selector)
        await page.fill(input_selector, "Привет! Это технический тест селекторов. Ответь парой слов.")
        await page.keyboard.press("Enter")
        
        print("Ждем ответа (10 сек)...")
        await asyncio.sleep(10)
        
        print("--- АНАЛИЗ DOM ---")
        # Ищем все элементы, которые могут быть сообщениями
        elements = await page.query_selector_all('div[data-testid], div[class*="message"], div[class*="response"]')
        for i, el in enumerate(elements[-5:]): # смотрим последние 5 элементов
            tag = await el.evaluate("el => el.tagName")
            testid = await el.get_attribute("data-testid")
            classes = await el.get_attribute("class")
            text_snippet = (await el.inner_text())[:50].replace("\n", " ")
            print(f"[{i}] {tag} | testid: {testid} | classes: {classes}")
            print(f"    Text: {text_snippet}...")
            
        print("--- ПОИСК MARKDOWN ---")
        markdowns = await page.query_selector_all('.markdown, [class*="prose"]')
        for i, m in enumerate(markdowns[-2:]):
            classes = await m.get_attribute("class")
            print(f"Markdown [{i}] classes: {classes}")
            print(f"Content: {(await m.inner_text())[:100]}...")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(debug_dom())
