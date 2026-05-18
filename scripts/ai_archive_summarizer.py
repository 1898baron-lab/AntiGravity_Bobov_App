import os
import re
import json
import urllib.request
import sys

# Настройка кодировки для Windows
if sys.stdout.encoding != 'utf-8':
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

# Папки
INPUT_DIR = r"C:\ANTIGRAVITY\1\obsidian_brain\4_ARCHIVE\ChatGPT_Total_Dump"
OUTPUT_DIR = r"C:\ANTIGRAVITY\1\obsidian_brain\1_PROJECTS\Summaries"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Модель в Ollama
MODEL_NAME = "gemma4:latest"
OLLAMA_URL = "http://127.0.0.1:11434/api/chat"

PROMPT = """Ты - старший инженер и системный аналитик (ПНАЭ Г, ГОСТ). 
Твоя задача проанализировать этот архивный лог чата и извлечь самую важную фактуру для Базы Знаний Obsidian.
Тебе нужно составить структурированную выжимку в формате Markdown:

# Краткая суть
(2-3 предложения о чем была речь)

# 📌 Ключевые факты и параметры
- (Список: выбранные материалы, например АМг6, ГОСТы, ТТХ, цифры, номера телефонов, ФИО, договоренности)

# 🚀 Action Items (Что осталось сделать)
- [ ] (Список незакрытых задач из разговора)

ВАЖНО: Пиши на русском языке, кратко и строго по делу. Без "Я проанализировал" и прочего мусора. Сразу выдавай структуру."""

def query_ollama(text):
    data = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": PROMPT},
            {"role": "user", "content": f"Вот текст чата:\n\n{text}"}
        ],
        "stream": False,
        "options": {
            "num_ctx": 8192
        }
    }
    
    req = urllib.request.Request(
        OLLAMA_URL, 
        data=json.dumps(data).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result['message']['content']
    except Exception as e:
        print(f"[ERR] Ошибка Ollama: {e}")
        return None

def process_single_file(filename):
    file_path = os.path.join(INPUT_DIR, filename)
    out_path = os.path.join(OUTPUT_DIR, f"{os.path.splitext(filename)[0]}_Summary.md")
    
    # Если уже есть summary - пропускаем
    if os.path.exists(out_path):
        print(f"[SKIP] {filename} уже обработан.")
        return
        
    print(f"\n[AI] Обработка файла: {filename}...")
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Обрезаем текст до 8000 символов, чтобы гарантированно влезть в контекст
    truncated_content = content[:8000]
    
    print("  -> Отправка в Ollama (может занять 30-60 сек)...")
    summary = query_ollama(truncated_content)
    
    if summary:
        final_md = f"# Summary: {os.path.splitext(filename)[0]}\n"
        final_md += f"**Оригинал:** [[{os.path.splitext(filename)[0]}]]\n\n"
        final_md += summary
        
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(final_md)
        print(f"  [OK] Выжимка сохранена!")
    else:
        print("  [ERR] Не удалось получить ответ.")

def main():
    if not os.path.exists(INPUT_DIR):
        print(f"Папка {INPUT_DIR} не найдена.")
        return
        
    files = [f for f in os.listdir(INPUT_DIR) if f.endswith(".md") and not f.startswith("00_")]
    print(f"Найдено {len(files)} файлов для суммаризации.")
    
    # Пакетный запуск: обрабатываем все файлы
    for i, file in enumerate(files):
        print(f"\n[{i+1}/{len(files)}]")
        process_single_file(file)

if __name__ == "__main__":
    main()
