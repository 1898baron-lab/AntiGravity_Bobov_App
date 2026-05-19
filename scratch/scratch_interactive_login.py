import asyncio
import sys
import os
sys.stdout.reconfigure(encoding='utf-8')
from playwright.async_api import async_playwright

SESSION_FILE = r"C:\ANTIGRAVITY\1\claude_session.json"
YANDEX_PATH = r"C:\Users\Sasha  Baron\AppData\Local\Yandex\YandexBrowser\Application\browser.exe"

INPUT_SELECTOR = '[contenteditable="true"][data-testid="composer-input"], [contenteditable="true"].ProseMirror'

async def main():
    print("====================================================")
    print("🔑 ИНТЕРАКТИВНАЯ АВТОРИЗАЦИЯ В CLAUDE.AI")
    print("====================================================")
    print("Сейчас на твоем экране откроется видимое окно браузера.")
    print("Пожалуйста, войди в свой аккаунт Claude (через Google или Email).")
    print("Как только ты войдешь и откроется главная страница чатов,")
    print("скрипт автоматически сохранит свежую сессию и продолжит работу!")
    print("У тебя есть 5 минут на авторизацию.")
    print("====================================================\n")
    
    async with async_playwright() as p:
        # Запускаем браузер в видимом режиме (headless=False)
        try:
            browser = await p.chromium.launch(
                headless=False,
                executable_path=YANDEX_PATH,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    "--disable-infobars"
                ]
            )
        except Exception as e:
            print(f"❌ Не удалось запустить Яндекс.Браузер: {e}")
            print("Пробуем запустить стандартный Chromium...")
            browser = await p.chromium.launch(headless=False)
            
        # Пытаемся загрузить старую сессию как базу
        try:
            context = await browser.new_context(storage_state=SESSION_FILE)
            print("Loaded existing session state.")
        except:
            context = await browser.new_context()
            print("Started with fresh session context.")
            
        page = await context.new_page()
        await page.goto("https://claude.ai/new", wait_until="load")
        
        print("\n⏳ Ожидание успешного входа (до 300 секунд)...")
        authenticated = False
        
        for seconds in range(300):
            current_url = page.url
            # Проверяем, залогинился ли пользователь (появилось ли поле ввода сообщения или URL изменился)
            try:
                composer = await page.query_selector(INPUT_SELECTOR)
                if composer and await composer.is_visible():
                    authenticated = True
                    break
            except:
                pass
                
            if "/chats" in current_url or "/chat/" in current_url:
                authenticated = True
                break
                
            await asyncio.sleep(1)
            if seconds % 10 == 0:
                print(f"[{seconds}s] Ожидаем авторизацию... Текущий адрес: {current_url}")
                
        if authenticated:
            print("\n🎉 Авторизация успешна! Сохраняем свежую сессию...")
            await context.storage_state(path=SESSION_FILE)
            print(f"💾 Сессия сохранена в {SESSION_FILE}!")
            
            # Извлекаем чаты
            print("🔍 Собираем список чатов...")
            await page.goto("https://claude.ai/chats", wait_until="load")
            await asyncio.sleep(5)
            
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
            keywords = ["бобов", "юр", "legal", "зевс", "zeus", "мастодонт", "mastodont", "дело"]
            filtered_chats = []
            for chat in chats:
                title_lower = chat['title'].lower()
                if any(kw in title_lower for kw in keywords):
                    filtered_chats.append(chat)
            
            print(f"\n🎯 НАЙДЕННЫЕ ЮРИДИЧЕСКИЕ ЧАТЫ:")
            if filtered_chats:
                for idx, chat in enumerate(filtered_chats, 1):
                    print(f"{idx}. [{chat['title']}] -> {chat['url']}")
            else:
                print("Чаты с упоминанием 'Бобов', 'юр' не найдены.")
                print("\nСписок последних чатов:")
                for idx, chat in enumerate(chats[:15], 1):
                    print(f"{idx}. [{chat['title']}] -> {chat['url']}")
        else:
            print("\n❌ Время ожидания авторизации истекло.")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
