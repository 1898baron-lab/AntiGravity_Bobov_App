import json
import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

COOKIE_STRING = """anthropic-device-id=5eb2f8b7-b381-42d7-9a73-dca788e570fc; cookie_seed_done=1; __ssid=2b3a8b82-c93d-4cb4-acec-a9f1433dca90; anthropic-consent-preferences=%7B%22analytics%22%3Atrue%2C%22marketing%22%3Atrue%7D; _fbp=fb.1.1771929498071.89397106544917070; hubspotutk=079cc7d3de92294dd3455a48b939612e; intercom-device-id-lupk8zyo=c29ed3fc-122c-4196-8255-af61c4569da2; __hstc=215430600.079cc7d3de92294dd3455a48b939612e.1771929501177.1771999334127.1772003469713.7; app-shell-mode=gate-disabled; __stripe_mid=cc03ad28-1684-43a8-919a-ce7b2845223e8c855e; lastActiveOrg=5ec64782-f2cb-4bda-b3a4-6c9e4b046a27; ajs_user_id=1ef627fd-1d93-4c23-8971-fd4e9325d064; _gcl_au=1.1.1070545603.1773369892.1741983711.1773824334.1773824334; g_state={"i_l":0,"i_ll":1774329849647,"i_b":"MGlWsy6AZZ6S0kBhDaR6/9i7Mp5k4ZP+fxCrzcuds1g","i_e":{"enable_itp_optimization":0}}; sessionKey=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; ajs_anonymous_id=21e09512-4763-4a23-abc3-79a85f669e58; sessionKeyLC=1776139594038; CH-prefers-color-scheme=dark; _cfuvid=NVB5LdB73tK.C1Abll_f_M08kWK4W0Vm3D7VpvxYdiU-1779083998.5558658-1.0.1.1-yTe87XewYIOAH1jpuFWuZ_38eKEeulrYIQ5VHfA8ews; activitySessionId=02f3f932-3de5-450d-9295-8f39c26c6d4a; user-sidebar-pinned=true; cf_clearance=QlTj6ryaLSYXwKNGoiHNlUIuQaaE.pzwVcwM4ERJ83o-1779168780-1.2.1.1-uPiI_v4THZPzcBAa_GfKrF.V.qpGsfglq8NJ.f86Tk5diSTX_rgf6cUyzs0MbNRdjVZD2noAb2XqiuExpe5jAepPSvkcgznprVQCycK9zmqcD.W52kWijbF0PhNj_szBUMxBhBYz0tJ3OjiXh_Cg8wq4gw.XvxTHK8SBZj_wwQ0EfA7mhXeTwYa.ur8hoLiQ6.8zzvJqADR_hsoFH402FjZ99wb8S4HYRElV2OGfHV2mN2rWScqQWmya7osCDFt1FFP4jhORi4Cg_HMZIlt3UHYQ8XJRG1tMvfgM7x4CkrOdKhOw_Z_gVPE0xlkMWPxmpCFPrwwT5oweiI8qNVKURy4YTUeFYecgj.WkUehXpyKs.xARuJ3B5kzFlx6jJzLP.Tx3skZz5GEbpRDPTU8YvCky88GOA52G83piVzDKdzs; __cf_bm=PKTqteL5u5ZHFEgDfDe_oL7l7X0_Y_P0SXtExC1IFKg-1779168780.2192585-1.0.1.1-hJReqsAr4kiEgAUtqVzs7rcAzGCObKTX7DYy7vyMkbE8oV4wGW8Z6fwYdfp4eXexTl8_xXCVWxIVhAvYesWGhyLqdc0OecBjQopKIgyC9xlapwjs5uL3rQDU6Skiuz89; user-sidebar-visible-on-load=false; _dd_s=aid=c942d44d-bf85-4be0-8ab5-4a1bc5f81240&rum=2&id=ebbfef33-e98a-43e1-a821-97fab3b3f758&created=1779168761548&expire=1779170001855"""

SESSION_FILE = r"C:\ANTIGRAVITY\1\claude_session.json"
YANDEX_PATH = r"C:\Users\Sasha  Baron\AppData\Local\Yandex\YandexBrowser\Application\browser.exe"

def parse_cookies(cookie_str):
    cookies = []
    # Разделяем строку кук
    pairs = cookie_str.split("; ")
    for pair in pairs:
        if "=" in pair:
            name, value = pair.split("=", 1)
            # Формируем объект для Playwright
            cookie_obj = {
                "name": name,
                "value": value,
                "domain": ".claude.ai" if "cf" in name or "stripe" in name or "anthropic" in name or "sessionKey" in name else "claude.ai",
                "path": "/",
                "expires": -1,
                "httpOnly": name in ["sessionKey", "cf_clearance", "__cf_bm", "_cfuvid"],
                "secure": True,
                "sameSite": "Lax"
            }
            # Специфические домены
            if name.startswith("__cf") or name.startswith("_cf") or name == "cf_clearance":
                cookie_obj["domain"] = ".claude.ai"
            cookies.append(cookie_obj)
    return cookies

async def main():
    print("🧹 Парсинг сырых кук...")
    playwright_cookies = parse_cookies(COOKIE_STRING)
    
    # Формируем структуру storage_state
    storage_state = {
        "cookies": playwright_cookies,
        "origins": [
            {
                "origin": "https://claude.ai",
                "localStorage": []
            }
        ]
    }
    
    # Записываем в файл сессии
    with open(SESSION_FILE, "w", encoding="utf-8") as f:
        json.dump(storage_state, f, ensure_ascii=False, indent=2)
    print(f"✅ Файл сессии сохранен в {SESSION_FILE}")
    
    # Запускаем браузер для проверки и перехода в чат
    print("🚀 Запуск Playwright для проверки сессии и сбора данных...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            executable_path=YANDEX_PATH,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-setuid-sandbox"
            ]
        )
        
        context = await browser.new_context(storage_state=SESSION_FILE)
        page = await context.new_page()
        
        # Переходим на конкретный чат, предоставленный пользователем
        target_chat = "https://claude.ai/chat/cac6f2cc-2dcb-4ad2-882d-a40a34169545"
        print(f"🔍 Открываем чат {target_chat}...")
        await page.goto(target_chat, wait_until="load", timeout=60000)
        await asyncio.sleep(6)
        
        print(f"Current URL: {page.url}")
        print(f"Page Title: {await page.title()}")
        
        # Скриншот для подтверждения авторизации
        screenshot_path = r"C:\ANTIGRAVITY\1\scratch\claude_shared_chat_debug.png"
        await page.screenshot(path=screenshot_path)
        print(f"📸 Скриншот чата сохранен в {screenshot_path}")
        
        content = await page.content()
        if "Sign in" in content or "Continue with Google" in content:
            print("❌ Авторизация по кукам не удалась. Убедитесь, что строка кук полная и свежая.")
        else:
            print("✅ Авторизация успешна! Мы внутри чата.")
            
            # Сохраняем свежую сессию после успешного входа
            await context.storage_state(path=SESSION_FILE)
            print("💾 Свежие куки пересохранены!")
            
            # Извлекаем название и последние сообщения чата
            title_element = await page.query_selector("h1, [data-testid='chat-title'], title")
            chat_title = await title_element.inner_text() if title_element else "Без названия"
            print(f"\n📌 Название чата: {chat_title.strip()}")
            
            # Попробуем вытащить текст сообщений из этого чата
            messages = await page.query_selector_all('[data-testid="user-message"], [data-testid="ai-message"]')
            print(f"📝 Найдено сообщений в чате: {len(messages)}")
            for idx, msg in enumerate(messages[:4]):
                role = "User" if "user-message" in str(await msg.get_attribute("data-testid")) else "AI"
                text = (await msg.inner_text()).strip()[:200]
                print(f"[{role}]: {text}...")
                
            # Теперь перейдем в раздел всех чатов и соберем список
            print("\n📂 Переходим в историю всех чатов...")
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
            
            print(f"📊 Всего найдено чатов в истории: {len(chats)}")
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
                for idx, chat in enumerate(chats[:20], 1):
                    print(f"{idx}. [{chat['title']}] -> {chat['url']}")
                    
        await context.close()

if __name__ == "__main__":
    asyncio.run(main())
