import asyncio
from playwright.async_api import async_playwright
import os
import re

async def exhaustive_claude_scan():
    async with async_playwright() as p:
        try:
            browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
            context = browser.contexts[0]
            page = await context.new_page()
            
            print("Navigating to Claude for EXHAUSTIVE scan...")
            await page.goto("https://claude.ai/chats")
            await page.wait_for_timeout(5000)

            # 1. Загружаем всю историю (у Клода может быть кнопка "Show more")
            print("Loading all Claude chats...")
            for i in range(10):
                show_more = page.get_by_text("Show more", exact=False)
                if await show_more.count() > 0:
                    await show_more.first.click()
                    await page.wait_for_timeout(2000)
                else:
                    break

            # 2. Собираем ссылки
            chats = await page.eval_on_selector_all("a[href*='/chat/']", "links => links.map(a => ({text: a.innerText, href: a.href}))")
            unique_chats = {c['href']: c['text'] for c in chats}
            print(f"Total unique Claude chats found: {len(unique_chats)}")

            os.makedirs("obsidian_brain/Archive/Claude/Full_History", exist_ok=True)

            # 3. Скрапим
            count = 0
            for href, text in unique_chats.items():
                count += 1
                name = text.split('\n')[0].strip()
                clean_name = re.sub(r'[^\w\s-]', '', name).replace(' ', '_')[:60]
                if not clean_name: clean_name = f"Chat_{count}"
                
                file_path = f"obsidian_brain/Archive/Claude/Full_History/{clean_name}.md"
                if os.path.exists(file_path): continue

                print(f"[{count}/{len(unique_chats)}] Scraping Claude: {name}")
                try:
                    await page.goto(href)
                    await page.wait_for_timeout(5000)
                    content = await page.inner_text("main, .flex-1.overflow-y-auto")
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(f"# {name}\n\nURL: {href}\n\n{content}")
                except Exception as e:
                    print(f"Failed: {name}: {e}")

            await page.close()
            await browser.close()
            print("Claude exhaustive scan complete.")
        except Exception as e:
            print(f"Global Error: {e}")

if __name__ == "__main__":
    asyncio.run(exhaustive_claude_scan())
