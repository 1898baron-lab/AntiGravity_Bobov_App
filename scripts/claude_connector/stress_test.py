import asyncio
import os
import json
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

SESSION_FILE = r"C:\ANTIGRAVITY\1\claude_session.json"

async def stress_test():
    print("Starting Stress Test...")
    async with async_playwright() as p:
        browser_path = r"C:\Users\Sasha  Baron\AppData\Local\Yandex\YandexBrowser\Application\browser.exe"
        browser = await p.chromium.launch(executable_path=browser_path, headless=False)
        context = await browser.new_context(storage_state=SESSION_FILE)
        page = await context.new_page()
        await Stealth().apply_stealth_async(page)
        
        await page.goto("https://claude.ai/new")
        await asyncio.sleep(5)
        
        # Complex prompt
        prompt = "Write a 3-paragraph explanation of quantum entanglement for a 5-year-old."
        await page.fill('[contenteditable="true"]', prompt)
        await page.keyboard.press("Enter")
        
        print("Waiting for response to START...")
        # Wait until stop button appears
        try:
            await page.wait_for_selector('[data-testid="stop-button"]', timeout=10000)
            print("Generation started.")
        except:
            print("Stop button never appeared. Maybe it was too fast or failed.")

        # Poll every 500ms
        for i in range(20):
            await asyncio.sleep(0.5)
            # Find last response
            response_elements = await page.query_selector_all('[data-testid="ai-message"]')
            if response_elements:
                last_el = response_elements[-1]
                text = await last_el.inner_text()
                html = await last_el.inner_html()
                print(f"[{i*0.5}s] Text Length: {len(text.strip())}")
                if i % 4 == 0:
                    # Log more detail occasionally
                    print(f"[{i*0.5}s] HTML Sample: {html[:100]}...")
            else:
                print(f"[{i*0.5}s] NO RESPONSE ELEMENT FOUND")
                
        await page.screenshot(path=r"C:\ANTIGRAVITY\1\logs\stress_test_final.png")
        print("Test complete. Check logs.")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(stress_test())
