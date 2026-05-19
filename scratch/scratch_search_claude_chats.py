import asyncio
import sys
import os
import json
sys.stdout.reconfigure(encoding='utf-8')
from playwright.async_api import async_playwright

SESSION_FILE = r"C:\ANTIGRAVITY\1\claude_session.json"
YANDEX_PATH = r"C:\Users\Sasha  Baron\AppData\Local\Yandex\YandexBrowser\Application\browser.exe"

async def main():
    print("🚀 Запуск Playwright с сессией Claude...")
    async with async_playwright() as p:
        # Запускаем Яндекс.Браузер с сохраненной сессией
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
        
        print("🔍 Переход на https://claude.ai/chats...")
        await page.goto("https://claude.ai/chats", wait_until="load", timeout=60000)
        await asyncio.sleep(5)  # Ждем загрузки JS
        
        # Делаем скриншот для отладки
        screenshot_path = r"C:\ANTIGRAVITY\1\scratch\claude_chats_debug.png"
        await page.screenshot(path=screenshot_path)
        print(f"📸 Скриншот сохранен в {screenshot_path}")
        
        # Собираем ссылки на чаты
        print("📂 Поиск ссылок на чаты в DOM...")
        links = await page.query_selector_all("a")
        
        chats = []
        for link in links:
            href = await link.get_attribute("href")
            text = await link.inner_text()
            if href and "/chat/" in href:
                href_clean = href.strip()
                text_clean = text.strip().replace("\n", " ")
                if href_clean not in [c['url'] for c in chats]:
                    chats.append({
                        "title": text_clean if text_clean else "Без названия",
                        "url": f"https://claude.ai{href_clean}" if href_clean.startswith("/") else href_clean
                    })
        
        print(f"📊 Всего найдено чатов: {len(chats)}")
        
        # Фильтруем чаты по ключевым словам
        keywords = ["бобов", "юр", "legal", "зевс", "zeus", "мастодонт", "mastodont", "дело"]
        filtered_chats = []
        
        for chat in chats:
            title_lower = chat['title'].lower()
            if any(kw in title_lower for kw in keywords):
                filtered_chats.append(chat)
                
        print(f"🎯 Найдено подходящих чатов: {len(filtered_chats)}")
        
        # Выводим все чаты и подходящие отдельно
        result = {
            "filtered": filtered_chats,
            "all": chats
        }
        
        with open(r"C:\ANTIGRAVITY\1\scratch\claude_chats_result.json", "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
            
        print("\n=== НАЙДЕННЫЕ ЮРИДИЧЕСКИЕ ЧАТЫ ===")
        if filtered_chats:
            for idx, chat in enumerate(filtered_chats, 1):
                print(f"{idx}. [{chat['title']}] -> {chat['url']}")
        else:
            print("Чаты с упоминанием 'Бобов', 'юр' не найдены.")
            print("\nСписок всех последних чатов для сверки:")
            for idx, chat in enumerate(chats[:15], 1):
                print(f"{idx}. [{chat['title']}] -> {chat['url']}")
                
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
