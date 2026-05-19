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
            executable_path=YANDEX_PATH
        )
        context = await browser.new_context(storage_state=SESSION_FILE)
        page = await context.new_page()
        
        url = "https://claude.ai/chat/cac6f2cc-2dcb-4ad2-882d-a40a34169545"
        await page.goto(url, wait_until="networkidle", timeout=60000)
        await asyncio.sleep(5)
        
        # Сохраняем полный HTML для детального анализа
        html = await page.content()
        with open(r"C:\ANTIGRAVITY\1\scratch\claude_chat_dom.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("💾 Полный HTML-код страницы сохранен в C:\\ANTIGRAVITY\\1\\scratch\\claude_chat_dom.html")
        
        # Исследуем текстовые элементы на странице
        print("\n🔍 Анализ элементов страницы:")
        
        # Попробуем найти все div-элементы, содержащие текст
        # В Claude сообщения обычно лежат в элементах с классами, содержащими 'grid' или 'flex', или внутри 'p'
        # Давай найдем элементы по ключевым словам
        all_divs = await page.query_selector_all("div")
        print(f"Всего div-элементов: {len(all_divs)}")
        
        # Ищем элементы с атрибутами data-testid
        all_testids = []
        for div in all_divs[:200]: # ограничимся первыми 200 для скорости
            testid = await div.get_attribute("data-testid")
            if testid:
                all_testids.append(testid)
        print(f"Атрибуты data-testid (первые 200 div): {set(all_testids)}")
        
        # Попробуем селекторы для сообщений:
        # Обычно в Claude ответы лежат в div с классом font-claude-response или grid
        claude_responses = await page.query_selector_all(".font-claude-message, [data-testid='chat-message-content']")
        print(f"Найдено ответов Claude по селекторам: {len(claude_responses)}")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
