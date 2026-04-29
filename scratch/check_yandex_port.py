import asyncio
from playwright.async_api import async_playwright

async def check_port(port):
    pw = await async_playwright().start()
    try:
        browser = await pw.chromium.connect_over_cdp(f"http://localhost:{port}")
        print(f"CONNECTED TO PORT {port}")
        for page in browser.contexts[0].pages:
            print(f"Page: {page.title()} - {page.url}")
        await browser.close()
        return True
    except Exception as e:
        print(f"Failed to connect to {port}: {e}")
        return False

async def main():
    for port in range(9222, 9225):
        if await check_port(port):
            break

asyncio.run(main())
