import asyncio
from playwright.async_api import async_playwright

async def work_with_tabs():
    try:
        async with async_playwright() as p:
            print("Connecting to 127.0.0.1:9222...")
            browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
            context = browser.contexts[0]
            
            claude_text = ""
            chatgpt_page = None
            
            for page in context.pages:
                url = page.url
                if "claude.ai" in url:
                    # Читаем Клода
                    messages = await page.query_selector_all('[data-testid="ai-message"], .font-claude-response')
                    if messages:
                        claude_text = (await messages[-1].inner_text()).strip()
                
                if "chatgpt.com" in url:
                    chatgpt_page = page
            
            print(f"CLAUDE LATEST: {claude_text}")
            
            if chatgpt_page:
                print(f"Found ChatGPT at {chatgpt_page.url}. Sending message...")
                prompt = "Привет! Я Antigravity. Кирилл перенаправил меня в это окно. Мы строим verifier.py. Клод предложил трехуровневую систему (Структура, База НТД, Confidence). Что думаешь об этом с точки зрения стабильности кода?"
                
                input_box = await chatgpt_page.wait_for_selector('#prompt-textarea', timeout=10000)
                await input_box.click()
                await chatgpt_page.keyboard.type(prompt, delay=10)
                await chatgpt_page.keyboard.press("Enter")
                print("Message sent to ChatGPT.")
            else:
                print("ChatGPT tab not found.")
                
            await browser.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(work_with_tabs())
