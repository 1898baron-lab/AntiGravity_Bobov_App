import asyncio
import sys
import os
sys.stdout.reconfigure(encoding='utf-8')
from playwright.async_api import async_playwright

SESSION_FILE = r"C:\ANTIGRAVITY\1\claude_session.json"
YANDEX_PATH = r"C:\Users\Sasha  Baron\AppData\Local\Yandex\YandexBrowser\Application\browser.exe"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            executable_path=YANDEX_PATH,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-infobars"
            ]
        )
        context = await browser.new_context(storage_state=SESSION_FILE)
        page = await context.new_page()
        
        await page.goto("https://claude.ai/chats", wait_until="networkidle", timeout=60000)
        await asyncio.sleep(5)
        
        print(f"Current URL: {page.url}")
        print(f"Page Title: {await page.title()}")
        
        # Посмотрим, есть ли на странице текст "Sign in" или поле ввода логина
        content = await page.content()
        if "Sign in" in content or "Continue with Google" in content:
            print("❌ Сессия устарела или не авторизована! Claude требует логин.")
        else:
            print("✅ Сессия авторизована.")
            # Выведем список всех ссылок (A) с их текстами для отладки
            links = await page.query_selector_all("a")
            print(f"Найдено ссылок 'a': {len(links)}")
            for idx, link in enumerate(links[:30]):
                href = await link.get_attribute("href")
                text = (await link.inner_text()).strip().replace("\n", " ")
                print(f"Link {idx}: href='{href}', text='{text}'")
                
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
