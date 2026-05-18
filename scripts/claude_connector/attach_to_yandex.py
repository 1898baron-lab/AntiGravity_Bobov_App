import asyncio
from playwright.async_api import async_playwright
import json

async def attach_and_save_cookies():
    print("Попытка подключения к Яндекс.Браузеру на порту 9222...")
    try:
        async with async_playwright() as p:
            # Подключаемся к уже запущенному браузеру
            browser = await p.chromium.connect_over_cdp("http://localhost:9222")
            context = browser.contexts[0]
            page = context.pages[0]
            
            print(f"Подключено! Текущий URL: {page.url}")
            
            # Переходим на ChatGPT, чтобы убедиться, что куки актуальны
            await page.goto("https://chatgpt.com")
            await asyncio.sleep(5)
            
            # Сохраняем куки
            cookies = await context.cookies()
            with open(r'C:/ANTIGRAVITY/1/scripts/claude_connector/chatgpt_session.json', 'w') as f:
                json.dump(cookies, f)
            
            print("Куки ChatGPT успешно сохранены в chatgpt_session.json")
            
    except Exception as e:
        print(f"Ошибка подключения: {e}")
        print("Убедись, что Яндекс запущен с флагом --remote-debugging-port=9222")

if __name__ == "__main__":
    asyncio.run(attach_and_save_cookies())
