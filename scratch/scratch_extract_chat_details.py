import asyncio
import sys
import os
from bs4 import BeautifulSoup
sys.stdout.reconfigure(encoding='utf-8')
from playwright.async_api import async_playwright

SESSION_FILE = r"C:\ANTIGRAVITY\1\claude_session.json"
YANDEX_PATH = r"C:\Users\Sasha  Baron\AppData\Local\Yandex\YandexBrowser\Application\browser.exe"

async def extract_chat(page, chat_url, output_path):
    print(f"\n📥 Извлечение чата: {chat_url}...")
    await page.goto(chat_url, wait_until="load", timeout=60000)
    await asyncio.sleep(7)
    
    # Делаем прокрутку вверх несколько раз, чтобы загрузить всю историю сообщений (если чат длинный)
    for _ in range(5):
        await page.evaluate("window.scrollTo(0, 0)")
        await asyncio.sleep(0.5)
        
    html = await page.content()
    soup = BeautifulSoup(html, "html.parser")
    
    # Название чата
    title_element = soup.find("h1") or soup.find(class_=lambda x: x and 'chat-title' in x) or soup.title
    chat_title = title_element.get_text().strip() if title_element else "Без названия"
    chat_title = chat_title.replace(" - Claude", "").strip()
    
    # Парсим сообщения по порядку DOM
    # Пользовательские реплики: класс '!font-user-message'
    # Ответы Claude: класс 'standard-markdown'
    elements = soup.find_all(class_=lambda x: x and ('!font-user-message' in x or 'standard-markdown' in x))
    
    chat_history = []
    for idx, el in enumerate(elements):
        classes = el.get("class", [])
        classes_str = " ".join(classes)
        
        if "!font-user-message" in classes_str:
            role = "User"
            text = el.get_text(separator="\n").strip()
        elif "standard-markdown" in classes_str:
            role = "Claude"
            text = el.get_text(separator="\n").strip()
        else:
            continue
            
        if not text:
            continue
            
        # Защита от дубликатов из-за вложенности
        if chat_history and chat_history[-1]["text"] == text:
            continue
            
        # Если новый элемент вложен в предыдущий или наоборот
        is_sub = False
        for prev in chat_history[-3:]:
            if prev["role"] == role and (text in prev["text"] or prev["text"] in text):
                is_sub = True
                if len(text) > len(prev["text"]):
                    prev["text"] = text
                break
        if is_sub:
            continue
            
        chat_history.append({
            "role": role,
            "text": text
        })
        
    print(f"✅ Успешно собрано сообщений: {len(chat_history)}")
    
    # Формируем Markdown
    md_content = f"# 💬 Чат: {chat_title}\n"
    md_content += f"* **Ссылка на оригинал**: [{chat_url}]({chat_url})\n"
    md_content += f"* **Количество сообщений**: {len(chat_history)}\n\n"
    md_content += "---\n\n"
    
    for msg in chat_history:
        role_emoji = "👤 **Вы**" if msg["role"] == "User" else "🤖 **Claude**"
        md_content += f"### {role_emoji}:\n\n"
        md_content += f"{msg['text']}\n\n"
        md_content += "---\n\n"
        
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(md_content)
        
    print(f"💾 Чат сохранен в файл: {output_path}")
    return chat_title, len(chat_history)

async def main():
    print("🚀 Запуск экстрактора чатов с улучшенными селекторами...")
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
        bobov_title, bobov_count = await extract_chat(page, bobov_url, bobov_path)
        
        # 2. Чат по кастомным скиллам
        custom_skill_url = "https://claude.ai/chat/cac6f2cc-2dcb-4ad2-882d-a40a34169545"
        custom_skill_path = r"C:\ANTIGRAVITY\1\obsidian_brain\4_ARCHIVE\ChatGPT_Projects\Claude_Chat_Custom_Skill.md"
        skill_title, skill_count = await extract_chat(page, custom_skill_url, custom_skill_path)
        
        # 3. Чат по стоимости ЗЕВС (давай его тоже сохраним, это очень важно!)
        zeus_chat_url = "https://claude.ai/chat/015e6317-5cd2-4d0c-8af5-df4451f8e092"
        zeus_chat_path = r"C:\ANTIGRAVITY\1\obsidian_brain\1_PROJECTS\ZEUS\Design_History\Claude_Chat_Zeus_Cost.md"
        zeus_title, zeus_count = await extract_chat(page, zeus_chat_url, zeus_chat_path)
        
        print("\n\n=== РЕЗУЛЬТАТЫ ЭКСТРАКЦИИ ===")
        print(f"1. Чат по Бобову: '{bobov_title}' ({bobov_count} сообщений) -> Сохранен в Obsidian.")
        print(f"2. Чат по Скиллам: '{skill_title}' ({skill_count} сообщений) -> Сохранен в Obsidian.")
        print(f"3. Чат по Зевсу: '{zeus_title}' ({zeus_count} сообщений) -> Сохранен в Obsidian.")
        
        await context.close()

if __name__ == "__main__":
    asyncio.run(main())
