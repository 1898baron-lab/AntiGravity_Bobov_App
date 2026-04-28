import asyncio
from playwright.async_api import async_playwright
import os
import re

async def gemini_u1_robust():
    async with async_playwright() as p:
        try:
            # Подключаемся к уже запущенному браузеру
            browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
            
            # Вместо создания новой страницы, попробуем использовать существующий контекст
            if not browser.contexts:
                print("No contexts found. Browser might be closed.")
                return
                
            context = browser.contexts[0]
            page = await context.new_page()
            
            url = "https://gemini.google.com/u/1/app?pageId=none"
            print(f"Navigating to {url}...")
            await page.goto(url, wait_until="networkidle", timeout=60000)
            await page.wait_for_timeout(5000)

            # Собираем чаты
            links = await page.eval_on_selector_all("a[href*='/u/1/app/']", "links => links.map(a => ({text: a.innerText, href: a.href}))")
            print(f"Found {len(links)} chats.")

            os.makedirs("obsidian_brain/Archive/Gemini", exist_ok=True)

            for chat in links[:5]: # Для начала возьмем 5 самых важных
                title = chat['text'].split('\n')[0].strip()
                if not title or "Gemini" == title: continue
                
                print(f"--- Processing: {title} ---")
                try:
                    await page.goto(chat['href'], wait_until="networkidle", timeout=60000)
                    await page.wait_for_timeout(5000)
                    
                    # Пытаемся вытащить весь контент
                    content = await page.inner_text("body") # Берем все тело, если специфичные селекторы не сработают
                    
                    safe_name = re.sub(r'[^\w\s-]', '', title).replace(' ', '_')[:50]
                    with open(f"obsidian_brain/Archive/Gemini/{safe_name}.md", "w", encoding="utf-8") as f:
                        f.write(f"# {title}\n\nURL: {chat['href']}\n\n{content}")
                    print(f"Saved: {title}")
                except Exception as e:
                    print(f"Error processing {title}: {e}")

            await page.close()
            print("Gemini /u/1/ robust export finished.")
        except Exception as e:
            print(f"Global Error: {e}")

if __name__ == "__main__":
    asyncio.run(gemini_u1_robust())
