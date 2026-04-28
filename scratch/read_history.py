import asyncio
from playwright.async_api import async_playwright
import os

async def read_history():
    async with async_playwright() as p:
        try:
            browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
            context = browser.contexts[0]
            
            target_url = "tekhnologiia-mashinostroeniia"
            target_page = None
            
            for pg in context.pages:
                if target_url in pg.url:
                    target_page = pg
                    break
            
            if target_page:
                print(f"Reading history from: {target_page.url}")
                # Скроллим вверх, чтобы подгрузить историю (если нужно)
                await target_page.evaluate("window.scrollTo(0, 0)")
                await asyncio.sleep(2)
                
                # Собираем все сообщения
                messages = await target_page.query_selector_all('[data-message-author-role]')
                history_content = "# 📜 История чата: Технология машиностроения\n\n"
                
                for msg in messages:
                    role = await msg.get_attribute("data-message-author-role")
                    text = await msg.inner_text()
                    history_content += f"### {role.upper()}\n{text}\n\n---\n\n"
                
                os.makedirs("obsidian_brain/Context", exist_ok=True)
                with open("obsidian_brain/Context/Engineering_GPT_History.md", "w", encoding="utf-8") as f:
                    f.write(history_content)
                print(f"History saved to obsidian_brain/Context/Engineering_GPT_History.md. Messages found: {len(messages)}")
            else:
                print("Target engineering chat tab not found.")
                
            await browser.close()
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(read_history())
