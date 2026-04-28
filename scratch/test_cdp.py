import asyncio
from playwright.async_api import async_playwright

async def test_cdp():
    try:
        async with async_playwright() as p:
            print("Connecting to 127.0.0.1:9222...")
            browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
            print(f"Connected! Contexts: {len(browser.contexts)}")
            for i, context in enumerate(browser.contexts):
                print(f"Context {i} pages: {len(context.pages)}")
                for page in context.pages:
                    print(f" - Page: {page.url} ({await page.title()})")
            await browser.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_cdp())
