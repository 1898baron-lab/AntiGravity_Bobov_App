import asyncio
from playwright.async_api import async_playwright
import os
import re

async def exhaustive_gemini_final():
    async with async_playwright() as p:
        try:
            browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
            context = browser.contexts[0]
            page = await context.new_page()
            
            url = "https://gemini.google.com/u/1/app?pageId=none"
            print(f"Navigating to Gemini /u/1/...")
            await page.goto(url)
            await page.wait_for_timeout(7000)

            # Собираем ссылки по классу 'conversation'
            # В Gemini они могут подгружаться динамически
            print("Collecting chats...")
            chat_elements = await page.query_selector_all("a.conversation")
            
            chats = []
            for el in chat_elements:
                href = await el.get_attribute("href")
                # Текст может быть во вложенном элементе или всплывающей подсказке
                text = await el.inner_text()
                if not text:
                    text = await el.get_attribute("aria-label") or "Untitled_Gemini_Chat"
                chats.append({'text': text.split('\n')[0].strip(), 'href': href})
            
            print(f"Found {len(chats)} Gemini chats.")

            os.makedirs("obsidian_brain/Archive/Gemini/Full_History", exist_ok=True)

            count = 0
            for chat in chats:
                count += 1
                name = chat['text']
                target_url = chat['href']
                if not target_url.startswith("http"):
                    target_url = "https://gemini.google.com" + target_url
                
                # Принудительно добавляем /u/1/ если его нет
                if "/u/1/" not in target_url:
                    target_url = target_url.replace("gemini.google.com/app", "gemini.google.com/u/1/app")

                clean_name = re.sub(r'[^\w\s-]', '', name).replace(' ', '_')[:60]
                file_path = f"obsidian_brain/Archive/Gemini/Full_History/{clean_name}.md"
                
                print(f"[{count}/{len(chats)}] Scraping Gemini: {name}")
                try:
                    await page.goto(target_url)
                    await page.wait_for_timeout(6000)
                    content = await page.inner_text("main, .chat-window")
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(f"# {name}\n\nURL: {target_url}\n\n{content}")
                except Exception as e:
                    print(f"Failed: {name}: {e}")

            await page.close()
            await browser.close()
            print("Gemini exhaustive scan complete.")
        except Exception as e:
            print(f"Global Error: {e}")

if __name__ == "__main__":
    asyncio.run(exhaustive_gemini_final())
