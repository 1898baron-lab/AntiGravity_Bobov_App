"""
chatgpt_first_login.py — однократный скрипт для сохранения сессии chatgpt.com
"""

import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

SESSION_FILE = "chatgpt_session.json"

async def main():
    async with async_playwright() as p:
        # Используем отдельную папку для профиля, чтобы не конфликтовать с основным Яндексом
        user_data_dir = r"C:\ANTIGRAVITY\1\.yandex_chatgpt_profile"
        
        context = await p.chromium.launch_persistent_context(
            user_data_dir,
            executable_path=r"C:\Users\Sasha  Baron\AppData\Local\Yandex\YandexBrowser\Application\browser.exe",
            headless=False,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-infobars",
                "--use-fake-ui-for-media-stream",
                "--use-fake-device-for-media-stream",
                "--disable-features=IsolateOrigins,site-per-process"
            ],
            ignore_default_args=["--enable-automation"]
        )
        
        page = context.pages[0] if context.pages else await context.new_page()
        await Stealth().apply_stealth_async(page)
        
        # Маскировка под реальный браузер через JS
        await page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        await page.goto("https://chatgpt.com")
        
        print("="*50)
        print("1. ЗАЛОГИНЬСЯ в ChatGPT (через Google или Email).")
        print("2. Если Google все еще ругается, попробуй зайти через Email/Password.")
        print("3. Как увидишь поле ввода чата — нажми Enter здесь.")
        print("="*50)
        
        input("Нажми Enter после успешного входа...")
        
        await context.storage_state(path=SESSION_FILE)
        print(f"Сессия ChatGPT сохранена в {SESSION_FILE}")
        await context.close()

if __name__ == "__main__":
    asyncio.run(main())
