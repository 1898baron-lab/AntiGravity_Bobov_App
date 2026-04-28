import asyncio
from playwright.async_api import async_playwright
import os

async def take_screenshots():
    try:
        async with async_playwright() as p:
            print("Connecting to 127.0.0.1:9222...")
            browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
            context = browser.contexts[0]
            
            os.makedirs("artifacts/screenshots", exist_ok=True)
            
            for i, page in enumerate(context.pages):
                try:
                    title = await page.title()
                    path = f"artifacts/screenshots/tab_{i}.png"
                    await page.screenshot(path=path)
                    print(f"Screenshot saved for {title}: {path}")
                except Exception as e:
                    print(f"Could not screenshot tab {i}: {e}")
            
            await browser.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(take_screenshots())
