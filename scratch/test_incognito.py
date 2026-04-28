import asyncio
from playwright.async_api import async_playwright

async def send_to_incognito():
    async with async_playwright() as p:
        try:
            browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
            context = browser.contexts[0]
            
            target_chat = "69eb9a94-782c-83eb-bfd2-c3dc8db5c4c8"
            chat_page = None
            
            for pg in context.pages:
                if target_chat in pg.url:
                    chat_page = pg
                    break
            
            if chat_page:
                print(f"Found incognito chat: {chat_page.url}. Sending test message...")
                await chat_page.bring_to_front()
                input_box = await chat_page.wait_for_selector('#prompt-textarea', timeout=10000)
                await input_box.click()
                await chat_page.keyboard.type("ТЕСТ ИНКОГНИТО: Я пробился! Видишь этот текст?", delay=50)
                await chat_page.keyboard.press("Enter")
                print("Message sent successfully!")
            else:
                print("Could not find the specific incognito chat tab.")
                
            await browser.close()
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(send_to_incognito())
