import asyncio
import os
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

SESSION_FILE = r"C:\ANTIGRAVITY\1\scripts\claude_connector\claude_session.json"

async def test_extraction():
    print("Testing extraction logic...")
    async with async_playwright() as p:
        browser_path = r"C:\Users\Sasha  Baron\AppData\Local\Yandex\YandexBrowser\Application\browser.exe"
        browser = await p.chromium.launch(executable_path=browser_path, headless=False)
        context = await browser.new_context(storage_state=SESSION_FILE)
        page = await context.new_page()
        await Stealth().apply_stealth_async(page)
        
        await page.goto("https://claude.ai/new")
        await asyncio.sleep(5)
        
        # Test input
        try:
            input_box = await page.wait_for_selector('[contenteditable="true"]', timeout=10000)
            await input_box.fill("Tell me a short joke.")
            await page.keyboard.press("Enter")
        except Exception as e:
            print(f"Failed to find input box: {e}")
            await page.screenshot(path=r"C:\ANTIGRAVITY\1\logs\failed_to_find_input.png")

        print("Waiting for response...")
        await asyncio.sleep(15) # More time for full generation
        
        # Dump possible response containers
        selectors = ['[data-testid="ai-message"]', '.font-claude-response', '.ProseMirror']
        for sel in selectors:
            elements = await page.query_selector_all(sel)
            print(f"Found {len(elements)} elements for selector {sel}")
            for i, el in enumerate(elements):
                text = await el.inner_text()
                print(f"[{i}] Text length: {len(text)}")
                if text:
                    print(f"[{i}] Start of text: {text[:50]}...")
        
        await page.screenshot(path="C:\\ANTIGRAVITY\\1\\logs\\extraction_test.png")
        print("Screenshot saved to logs/extraction_test.png")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(test_extraction())
