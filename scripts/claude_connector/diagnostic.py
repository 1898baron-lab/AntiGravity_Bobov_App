import asyncio
import os
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

SESSION_FILE = "C:\\ANTIGRAVITY\\1\\scripts\\claude_connector\\claude_session.json"
OUTPUT_IMAGE = "C:\\ANTIGRAVITY\\1\\logs\\claude_debug.png"

async def diagnostic():
    print("Starting Claude Diagnostic...")
    async with async_playwright() as p:
        # Use Yandex Browser if available, else Chromium
        browser_path = r"C:\Users\Sasha  Baron\AppData\Local\Yandex\YandexBrowser\Application\browser.exe"
        
        args = [
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox"
        ]
        
        browser = await p.chromium.launch(
            executable_path=browser_path if os.path.exists(browser_path) else None,
            headless=True,
            args=args
        )
        
        # Load session if exists
        context_args = {}
        if os.path.exists(SESSION_FILE):
            context_args["storage_state"] = SESSION_FILE
            print(f"Loading session from {SESSION_FILE}")
        
        context = await browser.new_context(**context_args)
        page = await context.new_page()
        
        # Stealth
        stealth = Stealth()
        await stealth.apply_stealth_async(page)
        
        print("Navigating to Claude.ai...")
        try:
            await page.goto("https://claude.ai/new", wait_until="networkidle", timeout=60000)
        except Exception as e:
            print(f"Navigation error: {e}")
            
        await asyncio.sleep(5) # Wait for any dynamic content
        
        # Take screenshot
        os.makedirs(os.path.dirname(OUTPUT_IMAGE), exist_ok=True)
        await page.screenshot(path=OUTPUT_IMAGE, full_page=True)
        print(f"Screenshot saved to {OUTPUT_IMAGE}")
        
        # Check for selectors
        input_selectors = [
            '[contenteditable="true"][data-testid="composer-input"]',
            '[contenteditable="true"].ProseMirror',
            'div[contenteditable="true"]'
        ]
        
        for sel in input_selectors:
            found = await page.query_selector(sel)
            print(f"Selector '{sel}': {'FOUND' if found else 'NOT FOUND'}")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(diagnostic())
