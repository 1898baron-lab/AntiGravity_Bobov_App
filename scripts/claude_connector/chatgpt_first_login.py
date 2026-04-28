"""
chatgpt_first_login.py — однократный скрипт для сохранения сессии chatgpt.com
"""

import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

SESSION_FILE = "chatgpt_session.json"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            executable_path=r"C:\Users\Sasha  Baron\AppData\Local\Yandex\YandexBrowser\Application\browser.exe",
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-infobars"
            ],
            ignore_default_args=["--enable-automation"]
        )
        context = await browser.new_context()
        page = await context.new_page()
        await Stealth().apply_stealth_async(page)
        await page.goto("https://chatgpt.com")
        
        print("="*50)
        print("1. ЗАЛОГИНЬСЯ в ChatGPT в открывшемся окне Яндекса.")
        print("2. Пройди все капчи вручную.")
        print("3. Как увидишь поле ввода чата — вернись сюда и нажми Enter.")
        print("="*50)
        
        input("Нажми Enter после успешного входа...")
        
        await context.storage_state(path=SESSION_FILE)
        print(f"Сессия ChatGPT сохранена в {SESSION_FILE}")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
