import asyncio
from playwright.async_api import async_playwright
import os

async def deep_crawl():
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
                print("Page not found.")
                return

            print("Scrolling and loading more discussions...")
            # Пытаемся найти кнопку "Загрузить больше"
            for _ in range(3):
                load_more = page.get_by_text("Загрузить больше", exact=False)
                if await load_more.count() > 0:
                    await load_more.first.click()
                    await page.wait_for_timeout(2000)
                else:
                    break
            
            # Теперь ищем конкретные пропущенные чаты
            missing_targets = [
                "05_План освоения", 
                "Разработка технологических", 
                "Цифровая модель"
            ]

            os.makedirs("obsidian_brain/Context", exist_ok=True)

            for target in missing_targets:
                print(f"Searching for: {target}")
                chat_link = page.get_by_text(target, exact=False)
                if await chat_link.count() > 0:
                    await chat_link.first.click()
                    await page.wait_for_timeout(4000)
                    content = await page.inner_text("main")
                    safe_name = target.replace(" ", "_").replace("/", "-")[:50]
                    file_path = f"obsidian_brain/Context/{safe_name}.md"
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(f"# {target}\n\n")
                        f.write(content)
                    print(f"Saved: {file_path}")
                else:
                    print(f"Not found: {target}")
                    
            await browser.close()
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(deep_crawl())
