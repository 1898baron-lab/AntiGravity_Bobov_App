import asyncio
from playwright.async_api import async_playwright
import os

async def gemini_recon():
    async with async_playwright() as p:
        try:
            browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
            context = browser.contexts[0]
            page = await context.new_page()
            
            url = "https://gemini.google.com/u/1/app?pageId=none"
            print(f"Navigating to Gemini /u/1/...")
            await page.goto(url)
            await page.wait_for_timeout(10000) # Даем прогрузиться всему

            # Делаем скриншот для диагностики
            os.makedirs("artifacts", exist_ok=True)
            await page.screenshot(path="artifacts/gemini_debug.png", full_page=True)
            print("Screenshot saved to artifacts/gemini_debug.png")

            # Выводим структуру ссылок для анализа
            links = await page.eval_on_selector_all("a", "links => links.map(a => ({text: a.innerText, href: a.href, class: a.className}))")
            for l in links[:20]:
                print(f"Link: {l['text']} -> {l['href']} (Class: {l['class']})")

            await page.close()
            await browser.close()
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(gemini_recon())
