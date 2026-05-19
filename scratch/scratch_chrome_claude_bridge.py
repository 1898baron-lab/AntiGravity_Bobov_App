import asyncio
import sys
import os
import shutil
sys.stdout.reconfigure(encoding='utf-8')
from playwright.async_api import async_playwright

CHROME_USER_DATA = r"C:\Users\Sasha  Baron\AppData\Local\Google\Chrome\User Data"
TEMP_PROFILE = r"C:\ANTIGRAVITY\1\scratch\temp_chrome_profile"

def prepare_temp_profile():
    print("🧹 Подготовка временного профиля из Google Chrome...")
    if os.path.exists(TEMP_PROFILE):
        try:
            shutil.rmtree(TEMP_PROFILE)
        except Exception as e:
            print(f"Предупреждение при очистке темп-профиля: {e}")
            
    os.makedirs(os.path.join(TEMP_PROFILE, "Default", "Network"), exist_ok=True)
    os.makedirs(os.path.join(TEMP_PROFILE, "Default", "Local Storage"), exist_ok=True)
    
    # Копируем куки из Chrome
    src_cookies = os.path.join(CHROME_USER_DATA, "Default", "Network", "Cookies")
    dst_cookies = os.path.join(TEMP_PROFILE, "Default", "Network", "Cookies")
    if os.path.exists(src_cookies):
        try:
            shutil.copy2(src_cookies, dst_cookies)
            print("✅ Файл Cookies Chrome скопирован.")
        except Exception as e:
            print(f"Ошибка копирования Cookies Chrome: {e}")
    else:
        print("ℹ️ Файл Cookies Chrome не найден по стандартному пути Default\\Network\\Cookies")
            
    # Копируем Local Storage из Chrome
    src_ls = os.path.join(CHROME_USER_DATA, "Default", "Local Storage")
    dst_ls = os.path.join(TEMP_PROFILE, "Default", "Local Storage")
    if os.path.exists(src_ls):
        try:
            shutil.copytree(src_ls, dst_ls, dirs_exist_ok=True)
            print("✅ Папка Local Storage Chrome скопирована.")
        except Exception as e:
            print(f"Ошибка копирования Local Storage Chrome: {e}")

async def main():
    prepare_temp_profile()
    
    print("🚀 Запуск Playwright с временным профилем Google Chrome...")
    async with async_playwright() as p:
        try:
            # Запускаем системный Chrome
            context = await p.chromium.launch_persistent_context(
                user_data_dir=TEMP_PROFILE,
                headless=True,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    "--disable-infobars"
                ]
            )
        except Exception as e:
            print(f"❌ Не удалось запустить браузер: {e}")
            return
            
        page = await context.new_page()
        
        print("🔍 Переход на https://claude.ai/chats...")
        await page.goto("https://claude.ai/chats", wait_until="load", timeout=60000)
        await asyncio.sleep(5)
        
        print(f"Current URL: {page.url}")
        print(f"Page Title: {await page.title()}")
        
        # Делаем скриншот для проверки
        screenshot_path = r"C:\ANTIGRAVITY\1\scratch\claude_chrome_debug.png"
        await page.screenshot(path=screenshot_path)
        print(f"📸 Скриншот сохранен в {screenshot_path}")
        
        content = await page.content()
        if "Sign in" in content or "Continue with Google" in content:
            print("❌ Авторизация через Google Chrome не удалась. Claude требует войти в аккаунт.")
        else:
            print("✅ Авторизация успешна!")
            
            # Сохраняем свежую сессию в claude_session.json, чтобы обновить её
            await context.storage_state(path=r"C:\ANTIGRAVITY\1\claude_session.json")
            print("💾 Свежая сессия успешно сохранена в C:\\ANTIGRAVITY\\1\\claude_session.json!")
            
            # Ищем чаты
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
            
            print(f"📊 Найдено чатов: {len(chats)}")
            keywords = ["бобов", "юр", "legal", "зевс", "zeus", "мастодонт", "mastodont", "дело"]
            filtered_chats = []
            for chat in chats:
                title_lower = chat['title'].lower()
                if any(kw in title_lower for kw in keywords):
                    filtered_chats.append(chat)
            
            print(f"🎯 Найдено подходящих юридических чатов: {len(filtered_chats)}")
            for idx, chat in enumerate(filtered_chats, 1):
                print(f"{idx}. [{chat['title']}] -> {chat['url']}")
                
            if not filtered_chats:
                print("\nСписок всех последних чатов:")
                for idx, chat in enumerate(chats[:15], 1):
                    print(f"{idx}. [{chat['title']}] -> {chat['url']}")
                    
        await context.close()

if __name__ == "__main__":
    asyncio.run(main())
