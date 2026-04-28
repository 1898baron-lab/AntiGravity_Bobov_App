import asyncio
from playwright.async_api import async_playwright

async def get_raw_text():
    async with async_playwright() as p:
        try:
            browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
            context = browser.contexts[0]
            
            target_url = "tekhnologiia-mashinostroeniia"
            target_page = None
            
            for pg in context.pages:
                if target_url in pg.url:
                    target_page = pg
                    break
            
            if target_page:
                print(f"Extracting raw content from: {target_page.url}")
                # Ждем подгрузки контента
                await target_page.wait_for_timeout(3000)
                
                # Берем весь текст из главного контейнера чата
                content = await target_page.inner_text("main")
                
                with open("obsidian_brain/Context/Engineering_GPT_Raw.md", "w", encoding="utf-8") as f:
                    f.write("# RAW HISTORY: Технология машиностроения\n\n")
                    f.write(content)
                print(f"Raw history saved (Length: {len(content)} characters)")
            else:
                print("Tab not found.")
            await browser.close()
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(get_raw_text())
