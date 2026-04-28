import asyncio
from playwright.async_api import async_playwright

async def scan_tabs():
    try:
        async with async_playwright() as p:
            print("Connecting to 127.0.0.1:9222...")
            browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
            context = browser.contexts[0]
            
            print(f"Total tabs found: {len(context.pages)}")
            
            for i, page in enumerate(context.pages):
                url = page.url
                title = await page.title()
                print(f"--- Tab {i}: {title} ({url}) ---")
                
                if "claude.ai" in url:
                    # Извлекаем последнее сообщение Клода
                    try:
                        messages = await page.query_selector_all('[data-testid="ai-message"], .font-claude-response')
                        if messages:
                            last_msg = (await messages[-1].inner_text()).strip()
                            print(f"CLAUDE SAYS: {last_msg[:500]}...")
                    except:
                        print("Could not read Claude message.")
                        
                if "chatgpt.com" in url:
                    # Извлекаем последнее сообщение ChatGPT
                    try:
                        messages = await page.query_selector_all('[data-message-author-role="assistant"]')
                        if messages:
                            last_msg = (await messages[-1].inner_text()).strip()
                            print(f"CHATGPT SAYS: {last_msg[:500]}...")
                    except:
                        print("Could not read ChatGPT message.")
            
            await browser.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(scan_tabs())
