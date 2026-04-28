import asyncio
from playwright.async_api import async_playwright
import os
import re

async def exhaustive_chatgpt_scan():
    async with async_playwright() as p:
        try:
            browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
            context = browser.contexts[0]
            page = await context.new_page()
            
            print("Navigating to ChatGPT for EXHAUSTIVE scan...")
            await page.goto("https://chatgpt.com/")
            await page.wait_for_timeout(5000)

            # 1. Скроллим сайдбар до упора
            print("Scrolling sidebar to the end of time...")
            sidebar_selector = "nav div[role='navigation']" # Уточненный селектор сайдбара
            last_height = 0
            for i in range(20): # 20 попыток прокрутки
                await page.mouse.move(100, 500) # Наводим на сайдбар
                await page.mouse.wheel(0, 5000)
                await page.wait_for_timeout(2000)
                print(f"Scroll step {i+1}...")

            # 2. Собираем ВСЕ ссылки на чаты
            # Чаты в ChatGPT обычно имеют ссылки типа /c/[uuid]
            chats = await page.eval_on_selector_all("a[href*='/c/']", "links => links.map(a => ({text: a.innerText, href: a.href}))")
            
            # Убираем дубликаты по href
            unique_chats = {c['href']: c['text'] for c in chats}
            print(f"Total unique chats found: {len(unique_chats)}")

            os.makedirs("obsidian_brain/Archive/ChatGPT/Full_History", exist_ok=True)

            # 3. Проходим по каждому
            count = 0
            for href, text in unique_chats.items():
                count += 1
                clean_name = re.sub(r'[^\w\s-]', '', text).replace(' ', '_')[:60]
                if not clean_name: clean_name = f"Chat_{count}"
                
                file_path = f"obsidian_brain/Archive/ChatGPT/Full_History/{clean_name}.md"
                if os.path.exists(file_path):
                    print(f"Skipping (already exists): {clean_name}")
                    continue

                print(f"[{count}/{len(unique_chats)}] Scraping: {text}")
                try:
                    await page.goto(href)
                    await page.wait_for_timeout(4000)
                    
                    # Извлекаем контент
                    content = await page.inner_text("main")
                    
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(f"# {text}\n\nURL: {href}\n\n{content}")
                except Exception as e:
                    print(f"Failed to scrape {text}: {e}")

            await page.close()
            await browser.close()
            print("Exhaustive scan complete.")
        except Exception as e:
            print(f"Global Error: {e}")

if __name__ == "__main__":
    asyncio.run(exhaustive_chatgpt_scan())
