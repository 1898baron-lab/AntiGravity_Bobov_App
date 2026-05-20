#!/usr/bin/env python3
"""
AntiGravity Gemma Local Chat
Интерактивный консольный чат с вашей локальной моделью gemma4 через Ollama API.
Сохраняет всю переписку в Obsidian.
"""

import os
import sys
import json
import requests
from datetime import datetime

OLLAMA_URL = "http://localhost:11434/api/chat"
DEFAULT_MODEL = "gemma4:latest"
OBSIDIAN_INBOX_DIR = r"C:\ANTIGRAVITY\1\obsidian_brain\0_INBOX"

# Настройка кодировки терминала для корректного вывода кириллицы на Windows
if sys.platform.startswith("win"):
    import ctypes
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleCP(65001)
    kernel32.SetConsoleOutputCP(65001)
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    sys.stdin.reconfigure(encoding="utf-8")

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def print_header():
    print("=" * 60)
    print("      🛸 ANTI-GRAVITY LOCAL GEMMA CHAT (v1.0) 🛸")
    print("      Полностью оффлайн. Без затрат облачных токенов.")
    print("=" * 60)
    print(" Доступные команды:")
    print("   /exit, /выход  - завершить чат и сохранить диалог в Obsidian")
    print("   /clear, /очистить - очистить историю текущего диалога")
    print("   /status        - проверить подключение к Ollama")
    print("=" * 60)

def save_to_obsidian(history):
    if not history:
        return
    
    if not os.path.exists(OBSIDIAN_INBOX_DIR):
        os.makedirs(OBSIDIAN_INBOX_DIR, exist_ok=True)
        
    date_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"Локальный_чат_Gemma_{date_str}.md"
    filepath = os.path.join(OBSIDIAN_INBOX_DIR, filename)
    
    markdown_content = []
    markdown_content.append("---")
    markdown_content.append("tags: [локальный_чат, gemma4, диалог]")
    markdown_content.append(f"date: {datetime.now().strftime('%Y-%m-%d')}")
    markdown_content.append("---")
    markdown_content.append(f"\n# 💬 Локальный диалог с Gemma ({datetime.now().strftime('%d.%m.%Y %H:%M')})\n")
    
    for msg in history:
        role = msg["role"]
        content = msg["content"]
        if role == "user":
            markdown_content.append(f"### 👤 Вы:\n{content}\n")
        elif role == "assistant":
            markdown_content.append(f"### 🤖 Gemma:\n{content}\n")
            markdown_content.append("---")
            
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(markdown_content))
        print(f"\n[Успех] Диалог успешно сохранен в Obsidian:")
        print(f"👉 {filepath}")
    except Exception as e:
        print(f"\n[Ошибка] Не удалось сохранить файл в Obsidian: {e}")

def chat_loop():
    messages = []
    model = DEFAULT_MODEL
    
    # Проверка доступности Ollama перед запуском
    try:
        resp = requests.get("http://localhost:11434/api/tags", timeout=5)
        if resp.status_code != 200:
            print("[Ошибка] Ollama сервер отвечает некорректно. Запуск невозможен.")
            return
    except Exception as e:
        print("[Ошибка] Не удалось подключиться к Ollama. Убедитесь, что приложение Ollama запущено.")
        print(f"Детали ошибки: {e}")
        return

    print_header()
    print(f"Подключение установлено. Активная модель: {model}")
    print("Начните диалог (введите сообщение и нажмите Enter):\n")

    while True:
        try:
            user_input = input("👤 Вы > ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nВыход...")
            save_to_obsidian(messages)
            break

        if not user_input:
            continue

        if user_input.lower() in ["/exit", "/выход", "exit", "выход"]:
            print("\nЗавершение сессии...")
            save_to_obsidian(messages)
            break

        if user_input.lower() in ["/clear", "/очистить"]:
            messages = []
            clear_screen()
            print_header()
            print("[Инфо] История чата очищена.")
            continue

        if user_input.lower() == "/status":
            print(f"Ollama URL: http://localhost:11434")
            print(f"Текущая модель: {model}")
            print(f"Сообщений в контексте памяти: {len(messages)}")
            continue

        # Добавляем сообщение пользователя в историю
        messages.append({"role": "user", "content": user_input})
        
        print("\n🤖 Gemma > ", end="", flush=True)
        
        payload = {
            "model": model,
            "messages": messages,
            "stream": True,
            "options": {
                "temperature": 0.3,
                "num_ctx": 4096  # Хороший размер контекста для Gemma 4
            }
        }
        
        assistant_response = ""
        try:
            response = requests.post(OLLAMA_URL, json=payload, stream=True, timeout=120)
            if response.status_code != 200:
                print(f"\n[Ошибка API] Статус-код: {response.status_code}")
                # Удаляем последнее сообщение из истории, так как ответ не был получен
                messages.pop()
                continue
                
            for chunk in response.iter_lines():
                if chunk:
                    chunk_data = json.loads(chunk.decode("utf-8"))
                    content_part = chunk_data.get("message", {}).get("content", "")
                    print(content_part, end="", flush=True)
                    assistant_response += content_part
            
            print("\n")
            # Добавляем ответ ассистента в историю
            messages.append({"role": "assistant", "content": assistant_response})
            
        except Exception as e:
            print(f"\n[Ошибка связи] Не удалось получить ответ: {e}")
            if messages and messages[-1]["role"] == "user":
                messages.pop()

if __name__ == "__main__":
    chat_loop()
