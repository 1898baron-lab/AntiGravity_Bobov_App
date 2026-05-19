import sys
import re
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

HTML_FILE = r"C:\ANTIGRAVITY\1\scratch\claude_chat_dom.html"

def analyze():
    print("📖 Чтение сохраненного HTML...")
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        html = f.read()
        
    soup = BeautifulSoup(html, "html.parser")
    
    print("\n🔍 Анализ структуры страницы:")
    
    # 1. Посмотрим на title страницы
    print(f"Title: {soup.title.string if soup.title else 'No Title'}")
    
    # 2. Найдем все теги, содержащие текст сообщений
    # Попробуем найти уникальные слова, которые точно есть в чате (например, "делай", "скилл")
    print("\n🕵️ Поиск элементов с ключевыми словами:")
    keywords = ["делай", "скилл", "custom", "skill"]
    for kw in keywords:
        elements = soup.find_all(string=re.compile(kw, re.IGNORECASE))
        print(f"Найдено элементов с '{kw}': {len(elements)}")
        for idx, el in enumerate(elements[:3]):
            parent = el.parent
            # Выведем цепочку родителей и их классы
            path = []
            curr = parent
            while curr and curr.name != "body":
                class_str = f".{'.'.join(curr.get('class', []))}" if curr.get('class') else ""
                path.append(f"{curr.name}{class_str}")
                curr = curr.parent
            path.reverse()
            print(f"  Match {idx+1}: '{el.strip()[:100]}'")
            print(f"    Path: {' > '.join(path[-4:])}")
            
    # 3. Выведем все уникальные классы div-ов, которые содержат сообщения
    # Обычно сообщения лежат в div с классом, содержащим 'message' или 'bubble'
    print("\n📋 Поиск div-ов с классами, похожими на сообщения:")
    divs = soup.find_all("div")
    message_classes = set()
    for div in divs:
        classes = div.get("class", [])
        for c in classes:
            if "message" in c.lower() or "chat" in c.lower() or "bubble" in c.lower() or "user" in c.lower() or "assistant" in c.lower() or "ai" in c.lower():
                message_classes.add(c)
    print(f"Найденные классы: {list(message_classes)[:20]}")

if __name__ == "__main__":
    analyze()
