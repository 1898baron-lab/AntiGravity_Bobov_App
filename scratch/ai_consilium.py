import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Конфиги
CLAUDE_URL = "http://localhost:8765/v1/messages"
CHATGPT_URL = "http://localhost:8001/v1/messages"
CHAT_CLAUDE_URL = "https://claude.ai/chat/e016d9cd-aad5-4ed3-bf48-7a2402c2ec1d"

# Читаем код ядра для анализа
with open("scripts/agent_core.py", "r", encoding="utf-8") as f:
    core_code = f.read()

# 1. Запрос к Клоду (Архитектор)
prompt_claude = f"""
Привет! Я Antigravity. Мы с Кириллом строим 'Mastodont AI Factory'. 
Твоя роль: Главный Архитектор и эксперт по НТД.
Посмотри на этот код 'agent_core.py':
{core_code}

Задача: Предложи архитектуру для модуля 'verifier.py'. 
Как нам встроить туда проверку по ГОСТам (например, ГОСТ 30893.1), чтобы агент не выдавал непроверенную информацию? 
Опиши структуру классов или функций для верификации.
"""

# 2. Запрос к ChatGPT (Аудитор)
prompt_chatgpt = f"""
Привет! Я Antigravity. 
Твоя роль: Инженер по надежности (SRE) и системный программист.
Посмотри на этот код 'agent_core.py':
{core_code}

Задача: Проведи аудит этого кода. 
Где он может упасть? Как нам лучше организовать асинхронный цикл (loop), чтобы он работал стабильно в фоне? 
Есть ли риск блокировок при работе с файлами Obsidian?
"""

def call_ai(url, prompt, name, chat_url=None):
    payload = {"messages": [{"role": "user", "content": prompt}]}
    if chat_url: payload["chat_url"] = chat_url
    
    try:
        print(f"--- Sending to {name} ---")
        response = requests.post(url, json=payload, timeout=300)
        if response.status_code == 200:
            return response.json()["content"][0]["text"]
        else:
            return f"Error from {name}: {response.status_code}"
    except Exception as e:
        return f"Critical error calling {name}: {e}"

# Выполняем звонки
claude_resp = call_ai(CLAUDE_URL, prompt_claude, "Claude (Architect)", CHAT_CLAUDE_URL)
chatgpt_resp = call_ai(CHATGPT_URL, prompt_chatgpt, "ChatGPT (Auditor)")

# Сохраняем результат
result_md = f"""# 🏛 Консилиум ИИ: Проектирование Verifier Layer

## 🧙‍♂️ Вердикт Claude (Архитектор)
{claude_resp}

---

## 🤖 Вердикт ChatGPT (Аудитор)
{chatgpt_resp}
"""

with open("obsidian_brain/_AI_EXCHANGE/AI_CONSULTATION_RESULT.md", "w", encoding="utf-8") as f:
    f.write(result_md)

print("--- ALL SYSTEMS GO ---")
print("Result saved to obsidian_brain/_AI_EXCHANGE/AI_CONSULTATION_RESULT.md")
