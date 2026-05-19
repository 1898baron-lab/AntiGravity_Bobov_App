import sys
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')
HTML_FILE = r"C:\ANTIGRAVITY\1\scratch\claude_chat_dom.html"

def parse():
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        html = f.read()
        
    soup = BeautifulSoup(html, "html.parser")
    
    # В Claude сообщения лежат в последовательных блоках.
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
        for prev in chat_history[-3:]: # Проверяем последние 3
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
        
    print(f"📊 Собрано сообщений: {len(chat_history)}")
    for idx, msg in enumerate(chat_history, 1):
        print(f"\n[{idx}] {msg['role']}:")
        print(msg['text'][:300] + "..." if len(msg['text']) > 300 else msg['text'])

if __name__ == "__main__":
    parse()
