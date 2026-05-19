import asyncio
import sys
import os
import json
sys.stdout.reconfigure(encoding='utf-8')
from playwright.async_api import async_playwright

SESSION_FILE = r"C:\ANTIGRAVITY\1\claude_session.json"
YANDEX_PATH = r"C:\Users\Sasha  Baron\AppData\Local\Yandex\YandexBrowser\Application\browser.exe"

async def extract_chat(page, chat_url, output_path):
    print(f"\n📥 Извлечение чата: {chat_url}...")
    await page.goto(chat_url, wait_until="load", timeout=60000)
    await asyncio.sleep(7)
    
    # Пытаемся получить заголовок чата
    title_element = await page.query_selector("h1, [data-testid='chat-title'], title")
    chat_title = await title_element.inner_text() if title_element else "Без названия"
    chat_title = chat_title.replace(" - Claude", "").strip()
    
    # Собираем блоки сообщений
    # Claude использует структуру, где сообщения идут последовательно в DOM
    # Мы можем найти все элементы с data-testid="user-message" и data-testid="ai-message" в порядке их появления
    message_elements = await page.query_selector_all('[data-testid="user-message"], [data-testid="ai-message"]')
    
    chat_history = []
    
    for element in message_elements:
        testid = await element.get_attribute("data-testid")
        role = "User" if "user-message" in testid else "Claude"
        
        # Для извлечения форматированного текста, включая код, списки и параграфы
        text = await element.inner_text()
        chat_history.append({
            "role": role,
            "text": text.strip()
        })
        
    print(f"✅ Успешно собрано сообщений: {len(chat_history)}")
    
    # Формируем Markdown файл
    md_content = f"# 💬 Чат: {chat_title}\n"
    md_content += f"* **Ссылка на оригинал**: [{chat_url}]({chat_url})\n"
    md_content += f"* **Количество сообщений**: {len(chat_history)}\n\n"
    md_content += "---\n\n"
    
    for msg in chat_history:
        role_emoji = "👤 **Вы**" if msg["role"] == "User" else "🤖 **Claude**"
        md_content += f"### {role_emoji}:\n\n"
        # Форматируем текст сообщения (добавляем отступы для блоков кода и т.д.)
        md_content += f"{msg['text']}\n\n"
        md_content += "---\n\n"
        
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(md_content)
        
    print(f"💾 Чат сохранен в файл: {output_path}")
    return chat_title, len(chat_history), chat_history

async def main():
    print("🚀 Запуск экстрактора чатов...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            executable_path=YANDEX_PATH,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-setuid-sandbox"
            ]
        )
        
        context = await browser.new_context(storage_state=SESSION_FILE)
        page = await context.new_page()
        
        # 1. Чат по Бобову
        bobov_url = "https://claude.ai/chat/76e34b49-38c7-4c2b-9792-881b93785839"
        bobov_path = r"C:\ANTIGRAVITY\1\obsidian_brain\1_PROJECTS\BOBOV\Claude_Chat_History_Bobov.md"
        bobov_title, bobov_count, bobov_history = await extract_chat(page, bobov_url, bobov_path)
        
        # 2. Чат по кастомным скиллам
        custom_skill_url = "https://claude.ai/chat/cac6f2cc-2dcb-4ad2-882d-a40a34169545"
        custom_skill_path = r"C:\ANTIGRAVITY\1\obsidian_brain\4_ARCHIVE\ChatGPT_Projects\Claude_Chat_Custom_Skill.md"
        skill_title, skill_count, skill_history = await extract_chat(page, custom_skill_url, custom_skill_path)
        
        # Создадим краткие саммари для пользователя
        print("\n\n=== РЕЗУЛЬТАТЫ ЭКСТРАКЦИИ ===")
        print(f"1. Чат по Бобову: '{bobov_title}' ({bobov_count} сообщений) -> Сохранен в Obsidian.")
        print(f"2. Чат по Скиллам: '{skill_title}' ({skill_count} сообщений) -> Сохранен в Obsidian.")
        
        await context.close()

if __name__ == "__main__":
    asyncio.run(main())
