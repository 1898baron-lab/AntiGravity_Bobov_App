import os
import json
import urllib.request
import sys
import re

# Настройки RAG
SEARCH_DIRS = [
    r"C:\ANTIGRAVITY\1\obsidian_brain",
    r"C:\ANTIGRAVITY\1\legal",
    r"C:\ANTIGRAVITY\1\Internship_NTD",
]
IGNORE_DIRS = {".git", ".docs", "venv", ".venv", "__pycache__", "node_modules"}
MAX_CONTEXT_WORDS = 800 # Ограничение для gemma4:26b-lite (num_ctx=2048)
MODEL_NAME = "gemma4:26b-lite"
HISTORY_FILE = r"C:\ANTIGRAVITY\1\obsidian_brain\chat_history.md"

def get_chat_history():
    if not os.path.exists(HISTORY_FILE):
        return ""
    try:
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            # Берем последние 20 строк истории (чтобы не переполнить контекст)
            return "".join(lines[-20:])
    except Exception:
        return ""

def save_chat_history(query, response):
    try:
        os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
        with open(HISTORY_FILE, 'a', encoding='utf-8') as f:
            f.write(f"USER: {query}\nAI: {response}\n\n")
    except Exception as e:
        print(f"[Ошибка] Не удалось сохранить историю: {e}")

def get_all_md_files(directories):
    files = []
    for d in directories:
        if not os.path.exists(d):
            continue
        for root, dirs, filenames in os.walk(d):
            dirs[:] = [sub for sub in dirs if sub not in IGNORE_DIRS]
            if any(part in IGNORE_DIRS for part in root.split(os.sep)):
                continue
            for filename in filenames:
                if filename.endswith(".md"):
                    files.append(os.path.join(root, filename))
    return files

def score_file(filepath, query_words):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        return 0, ""
    
    content_lower = content.lower()
    score = 0
    for word in query_words:
        if len(word) > 3 and word in content_lower:
            score += content_lower.count(word)
            
    return score, content

def find_relevant_context(query):
    print("[RAG] Сканирование базы знаний...")
    query_words = re.findall(r'\w+', query.lower())
    
    all_files = get_all_md_files(SEARCH_DIRS)
    scored_files = []
    
    for filepath in all_files:
        score, content = score_file(filepath, query_words)
        if score > 0:
            scored_files.append((score, filepath, content))
            
    # Сортируем по релевантности
    scored_files.sort(key=lambda x: x[0], reverse=True)
    
    context = ""
    word_count = 0
    used_files = []
    
    for score, filepath, content in scored_files:
        words_in_file = len(content.split())
        if word_count + words_in_file <= MAX_CONTEXT_WORDS:
            filename = os.path.basename(filepath)
            context += f"--- ФАЙЛ: {filename} ---\n{content}\n\n"
            word_count += words_in_file
            used_files.append(filename)
        else:
            # Если файл слишком большой, берем кусок (первые 300 слов)
            if word_count < MAX_CONTEXT_WORDS:
                filename = os.path.basename(filepath)
                snippet = " ".join(content.split()[:300])
                context += f"--- ФАЙЛ: {filename} (фрагмент) ---\n{snippet}...\n\n"
                used_files.append(filename)
                break
                
    return context, used_files

def ask_ollama_with_context(query, context):
    url = "http://localhost:11434/api/generate"
    
    history = get_chat_history()
    history_block = f"ИСТОРИЯ ПРЕДЫДУЩИХ СООБЩЕНИЙ:\n{history}\n\n" if history else ""

    system_prompt = (
        "Ты - интеллектуальный агент системы AntiGravity. "
        "Твоя задача - отвечать на вопросы пользователя, строго опираясь на предоставленные ниже документы из базы знаний (RAG) и историю диалога.\n"
        "Если ответа нет в документах, так и скажи. Не придумывай факты.\n\n"
        f"{history_block}"
        f"ДОКУМЕНТЫ:\n{context}\n\n"
        f"ВОПРОС ПОЛЬЗОВАТЕЛЯ:\n{query}"
    )
    
    data = {
        "model": MODEL_NAME,
        "prompt": system_prompt,
        "stream": True,
        "options": {
            "num_ctx": 2048
        }
    }
    
    req = urllib.request.Request(
        url, 
        data=json.dumps(data).encode('utf-8'),
        headers={'Content-Type': 'application/json; charset=utf-8'}
    )
    
    full_response = ""
    print(f"\n[Ollama] Отправка запроса к {MODEL_NAME}...\n")
    try:
        with urllib.request.urlopen(req) as response:
            for line in response:
                if line:
                    decoded_line = line.decode('utf-8')
                    try:
                        json_resp = json.loads(decoded_line)
                        chunk = json_resp.get("response", "")
                        print(chunk, end="", flush=True)
                        full_response += chunk
                    except json.JSONDecodeError:
                        pass
            print("\n")
        
        # Сохраняем историю
        save_chat_history(query, full_response)
        
    except Exception as e:
        print(f"\n[Ошибка] Не удалось связаться с Ollama: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        user_query = " ".join(sys.argv[1:])
    else:
        user_query = input("Введите ваш вопрос для RAG-поиска: ")
        
    if not user_query.strip():
        print("Вопрос не задан.")
        sys.exit(0)
        
    context, files_used = find_relevant_context(user_query)
    
    if not context:
        print("[RAG] В базе знаний не найдено подходящих документов. Модель ответит на основе своих общих знаний.")
    else:
        print(f"[RAG] Найдены релевантные файлы: {', '.join(files_used)}")
        
    ask_ollama_with_context(user_query, context)
