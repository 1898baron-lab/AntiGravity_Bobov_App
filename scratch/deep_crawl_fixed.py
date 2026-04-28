import asyncio
from playwright.async_api import async_playwright
import os

async def deep_crawl_fixed():
    async with async_playwright() as p:
        try:
            browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
            context = browser.contexts[0]
            page = await context.new_page()
            
            # Прямой переход в группу
            url = "https://chatgpt.com/g/g-p-68ef8d5df22481918bbd5d83c91aa554-tekhnologiia-mashinostroeniia/project"
            print(f"Navigating to: {url}")
            await page.goto(url)
            await page.wait_for_timeout(5000)
            
            print("Loading more discussions...")
            for _ in range(5): # Жмем 5 раз для верности
                load_more = page.get_by_text("Загрузить больше", exact=False)
                if await load_more.count() > 0:
                    await load_more.first.click()
                    await page.wait_for_timeout(2000)
                else:
                    break
            
            missing_targets = [
                "05_План освоения", 
                "Разработка технологических", 
                "Цифровая модель"
            ]

            os.makedirs("obsidian_brain/Context", exist_ok=True)

            for target in missing_targets:
                print(f"Opening: {target}")
                chat_link = page.get_by_text(target, exact=False)
                if await chat_link.count() > 0:
                    await chat_link.first.click()
                    await page.wait_for_timeout(5000)
                    content = await page.inner_text("main")
                    safe_name = target.replace(" ", "_").replace("/", "-")[:50]
                    file_path = f"obsidian_brain/Context/{safe_name}.md"
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(f"# {target}\n\n")
                        f.write(content)
                    print(f"Saved: {file_path}")
                    # Возвращаемся в группу
                    await page.goto(url)
                    await page.wait_for_timeout(3000)
                else:
                    print(f"Still not found: {target}")
                    
            await page.close()
            await browser.close()
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(deep_crawl_fixed())
