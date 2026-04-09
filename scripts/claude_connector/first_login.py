"""
first_login.py — однократный скрипт для сохранения сессии claude.ai

Запусти один раз:
    python first_login.py

Откроется браузер → залогинься в claude.ai вручную →
нажми Enter в терминале → сессия сохранится в claude_session.json
"""

import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

SESSION_FILE = "claude_session.json"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False, 
            executable_path=r"C:\Users\Sasha  Baron\AppData\Local\Yandex\YandexBrowser\Application\browser.exe",
            args=["--disable-blink-features=AutomationControlled"],
            ignore_default_args=["--enable-automation"]
        )
        context = await browser.new_context()
        page = await context.new_page()
        await Stealth().apply_stealth_async(page)
        await page.goto("https://claude.ai")
        print("="*50)
        print("Залогинься в claude.ai в открывшемся браузере.")
        print("После входа нажми Enter здесь...")
        input()
        await context.storage_state(path=SESSION_FILE)
        print(f"Сессия сохранена: {SESSION_FILE}")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
