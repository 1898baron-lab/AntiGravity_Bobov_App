import asyncio
from playwright.async_api import async_playwright
import os

async def crawl_all_chats():
    async with async_playwright() as p:
        try:
            browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
            context = browser.contexts[0]
            
            target_url = "tekhnologiia-mashinostroeniia"
            page = None
            for pg in context.pages:
                if target_url in pg.url:
                    page = pg
                    break
            
            if not page:
                print("Engineering GPT page not found.")
                return

            os.makedirs("obsidian_brain/Context", exist_ok=True)
            
            # Список ключевых слов для поиска чатов
            targets = [
                "Изучение файлов", 
                "Сравнение планов", 
                "Список литературы", 
                "Хомут быстросъёмный", 
                "05_План освоения", 
                "Разработка технологических", 
                "Цифровая модель",
                "Требования руководителя"
            ]

            for target in targets:
                print(f"--- Processing: {target} ---")
                try:
                    # Находим ссылку
                    chat_link = page.get_by_text(target, exact=False)
                    if await chat_link.count() > 0:
                        await chat_link.first.click()
                        await page.wait_for_timeout(4000) # Даем время на загрузку
                        
                        # Извлекаем контент
                        content = await page.inner_text("main")
                        
                        safe_name = target.replace(" ", "_").replace("/", "-")[:50]
                        file_path = f"obsidian_brain/Context/{safe_name}.md"
                        
                        with open(file_path, "w", encoding="utf-8") as f:
                            f.write(f"# {target}\n\n")
                            f.write(content)
                        print(f"Saved to {file_path}")
                        
                        # Возвращаемся в список (опционально, если клик уводит со страницы)
                        # Но в ChatGPT обычно это просто смена контента в main, сайдбар остается.
                    else:
                        print(f"Could not find link for: {target}")
                except Exception as e:
                    print(f"Failed to process {target}: {e}")
            
            await browser.close()
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(crawl_all_chats())
