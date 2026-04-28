import asyncio
from playwright.async_api import async_playwright
import os
import re

async def gemini_u1_export():
    async with async_playwright() as p:
        try:
            browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
            context = browser.contexts[0]
            page = await context.new_page()
            
            # Используем твою конкретную ссылку
            url = "https://gemini.google.com/u/1/app?pageId=none"
            print(f"Navigating to Gemini Profile /u/1/...")
            await page.goto(url)
            await page.wait_for_timeout(7000)

            # Собираем чаты из сайдбара
            # В Gemini /u/1/ селекторы могут быть такими же, но контент другой
            history_links = await page.eval_on_selector_all("a[href*='/u/1/app/']", "links => links.map(a => ({text: a.innerText, href: a.href}))")
            
            print(f"Detected {len(history_links)} chats in profile /u/1/.")

            os.makedirs("obsidian_brain/Archive/Gemini", exist_ok=True)

            for chat in history_links[:10]:
                name = chat['text'].split('\n')[0].strip()
                if not name or name == "Gemini": continue
                
                target_url = chat['href']
                print(f"--- Exporting from /u/1/: {name} ---")
                
                await page.goto(target_url)
                await page.wait_for_timeout(5000)
                
                # Извлекаем текст
                try:
                    content = await page.inner_text("main")
                    safe_name = re.sub(r'[^\w\s-]', '', name).replace(' ', '_')[:50]
                    file_path = f"obsidian_brain/Archive/Gemini/{safe_name}.md"
                    
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(f"# {name}\n\nSource: {target_url}\n\n{content}")
                    print(f"Saved: {file_path}")
                except:
                    print(f"Failed to extract content for {name}")

            await page.close()
            await browser.close()
            print("Gemini /u/1/ export complete.")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(gemini_u1_export())
