"""
first_login.py — однократный скрипт для сохранения сессии claude.ai

Запусти один раз:
    python first_login.py

Откроется браузер → залогинься в claude.ai вручную →
нажми Enter в терминале → сессия сохранится в claude_session.json
"""

import asyncio
from playwright.async_api import async_playwright

SESSION_FILE = "claude_session.json"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
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
