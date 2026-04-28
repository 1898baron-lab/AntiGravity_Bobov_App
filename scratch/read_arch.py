import asyncio
from playwright.async_api import async_playwright
import os

async def read_arch_chat():
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

            print("Searching for ARCH_ HR chat link...")
            # Пытаемся найти ссылку по тексту
            chat_link = await page.get_by_text("ARCH_ HR", exact=False)
            if await chat_link.count() > 0:
                print("Clicking ARCH_ HR chat...")
                await chat_link.first.click()
                await page.wait_for_timeout(5000) # Ждем загрузки чата
                
                # Теперь читаем содержимое чата
                print("Reading chat content...")
                # Попробуем взять весь текст из main после клика
                content = await page.inner_text("main")
                
                os.makedirs("obsidian_brain/Context", exist_ok=True)
                with open("obsidian_brain/Context/ARCH_HR_CPTI.md", "w", encoding="utf-8") as f:
                    f.write("# 📦 ARCH_ HR и договорённости (ЦПТИ)\n\n")
                    f.write(content)
                print(f"Archived chat saved! Length: {len(content)}")
            else:
                print("Could not find ARCH_ HR link on the page.")
                
            await browser.close()
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(read_arch_chat())
