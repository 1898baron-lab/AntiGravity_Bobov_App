import asyncio
from playwright.async_api import async_playwright
import os
import re

async def exhaustive_gemini_scan():
    async with async_playwright() as p:
        try:
            browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
            context = browser.contexts[0]
            page = await context.new_page()
            
            url = "https://gemini.google.com/u/1/app?pageId=none"
            print(f"Navigating to Gemini /u/1/ for EXHAUSTIVE scan...")
            await page.goto(url)
            await page.wait_for_timeout(7000)

            # 1. Прогружаем историю в сайдбаре
            print("Loading all Gemini chats...")
            for i in range(10):
                # В Gemini история подгружается при скролле или есть кнопка
                await page.mouse.move(100, 500)
                await page.mouse.wheel(0, 5000)
                await page.wait_for_timeout(2000)

            # 2. Собираем ссылки
            # Ссылки в Gemini часто в <a> с определенными атрибутами
            chats = await page.eval_on_selector_all("a[href*='/u/1/app/']", "links => links.map(a => ({text: a.innerText, href: a.href}))")
            unique_chats = {c['href']: c['text'] for c in chats}
            print(f"Total unique Gemini chats found: {len(unique_chats)}")

            os.makedirs("obsidian_brain/Archive/Gemini/Full_History", exist_ok=True)

            # 3. Скрапим
            count = 0
            for href, text in unique_chats.items():
                count += 1
                name = text.split('\n')[0].strip()
                if not name or name == "Gemini": continue
                
                clean_name = re.sub(r'[^\w\s-]', '', name).replace(' ', '_')[:60]
                if not clean_name: clean_name = f"Chat_{count}"
                
                file_path = f"obsidian_brain/Archive/Gemini/Full_History/{clean_name}.md"
                if os.path.exists(file_path): continue

                print(f"[{count}/{len(unique_chats)}] Scraping Gemini: {name}")
                try:
                    await page.goto(href)
                    await page.wait_for_timeout(6000)
                    content = await page.inner_text("main, .chat-window")
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(f"# {name}\n\nURL: {href}\n\n{content}")
                except Exception as e:
                    print(f"Failed: {name}: {e}")

            await page.close()
            await browser.close()
            print("Gemini exhaustive scan complete.")
        except Exception as e:
            print(f"Global Error: {e}")

if __name__ == "__main__":
    asyncio.run(exhaustive_gemini_scan())
