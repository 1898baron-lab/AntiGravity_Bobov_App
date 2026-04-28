import asyncio
from playwright.async_api import async_playwright

async def scan():
    async with async_playwright() as p:
        try:
            browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
            print(f"Contexts: {len(browser.contexts)}")
            for i, ctx in enumerate(browser.contexts):
                print(f"Context {i} pages:")
                for pg in ctx.pages:
                    print(f"  - {pg.url}")
            await browser.close()
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(scan())
