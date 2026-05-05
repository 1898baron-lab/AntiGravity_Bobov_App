import sys
import argparse
import json
import urllib.request
from agent.config import OLLAMA_URL, DEFAULT_MODEL, CHAT_HISTORY_FILE, MAX_HISTORY_MESSAGES
from agent.utils.rag import find_relevant_context
import os

def get_chat_history():
    if not os.path.exists(CHAT_HISTORY_FILE):
        return ""
    try:
        with open(CHAT_HISTORY_FILE, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]
        interactions = []
        current = []
        for line in lines:
            if line.startswith("USER:") or line.startswith("AI:"):
                current.append(line)
                if line.startswith("AI:"):
                    interactions.append("\n".join(current))
                    current = []
        return "\n\n".join(interactions[-MAX_HISTORY_MESSAGES:])
    except Exception:
        return ""

def save_chat_history(query, response):
    try:
        os.makedirs(os.path.dirname(CHAT_HISTORY_FILE), exist_ok=True)
        with open(CHAT_HISTORY_FILE, 'a', encoding='utf-8') as f:
            f.write(f"USER: {query}\nAI: {response}\n\n")
    except Exception:
        pass

def ask_ollama(query, context):
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
        "model": DEFAULT_MODEL,
        "prompt": system_prompt,
        "stream": True,
        "options": {"num_ctx": 2048}
    }

    req = urllib.request.Request(
        f"{OLLAMA_URL}/api/generate",
        data=json.dumps(data).encode('utf-8'),
        headers={'Content-Type': 'application/json; charset=utf-8'}
    )

    full_response = ""
    print(f"\n[Ollama] Отправка запроса ({DEFAULT_MODEL})...\n")
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
        save_chat_history(query, full_response)
    except Exception as e:
        print(f"\n[Ошибка] Не удалось связаться с Ollama: {e}")

def main():
    parser = argparse.ArgumentParser(description="AntiGravity Local RAG Agent")
    parser.add_argument("--query", type=str, help="Ваш вопрос для RAG-поиска")
    args = parser.parse_args()

    query = args.query
    if not query:
        query = input("Введите ваш вопрос: ")

    if not query.strip():
        print("Вопрос не может быть пустым.")
        return

    context, files_used = find_relevant_context(query)
    
    if not context:
        print("[RAG] В базе знаний не найдено подходящих документов.")
    else:
        print(f"[RAG] Найдены релевантные файлы: {', '.join(files_used)}")

    ask_ollama(query, context)

if __name__ == "__main__":
    main()
