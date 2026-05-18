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
PROJECTS_ROOT = r"C:\ANTIGRAVITY\1\obsidian_brain\4_ARCHIVE\ChatGPT_Projects"
OUTPUT_DIR = r"C:\ANTIGRAVITY\1\obsidian_brain\1_PROJECTS\Summaries"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Модель в Ollama
MODEL_NAME = "gemma4:latest"
OLLAMA_URL = "http://127.0.0.1:11434/api/chat"

SYSTEM_PROMPT = """Ты - старший системный аналитик и архитектор знаний. 
Твоя задача: проанализировать подборку чатов из одного проекта и составить комплексный отчет для Obsidian.
Нужно извлечь ценные идеи, технические параметры, важные контакты и незавершенные задачи.

Формат отчета:
# Проект: [Название проекта]

## 📋 Общее описание
(Суть проекта и основных обсуждений в 3-4 предложениях)

## 📌 Ключевая фактура
- (Технические параметры, цифры, ГОСТы, материалы)
- (Важные имена, ссылки, телефоны)
- (Уникальные идеи или инсайты)

## 🚀 Action Items & Статус
- [ ] (Что осталось сделать или какие вопросы остались открытыми)

## 🔗 Связанные чаты
(Перечисли основные темы чатов, которые были в папке)

Пиши строго по делу, на русском языке, без лишних вступлений."""

def query_ollama(text):
    data = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Вот содержимое всех чатов проекта:\n\n{text}"}
        ],
        "stream": False,
        "options": {
            "num_ctx": 16384  # Увеличиваем контекст для суммаризации целой папки
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

def summarize_project_folder(folder_name):
    folder_path = os.path.join(PROJECTS_ROOT, folder_name)
    out_path = os.path.join(OUTPUT_DIR, f"Project_{folder_name}_Summary.md")
    
    if os.path.exists(out_path):
        print(f"[SKIP] {folder_name} уже обработан.")
        return

    print(f"\n[AI] Анализ проекта: {folder_name}...")
    
    # Собираем текст из всех файлов в папке (кроме индекса)
    combined_content = ""
    files = [f for f in os.listdir(folder_path) if f.endswith(".md") and not f.startswith("00_INDEX")]
    
    if not files:
        print(f"  [WARN] В папке {folder_name} нет файлов для анализа.")
        return

    for fname in files:
        fpath = os.path.join(folder_path, fname)
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                # Берем только первые 3000 символов из каждого файла, чтобы не перегрузить модель
                combined_content += f"\n--- Файл: {fname} ---\n"
                combined_content += f.read()[:3000] 
        except Exception as e:
            print(f"  [ERR] Ошибка чтения {fname}: {e}")

    # Ограничиваем общий объем для Ollama
    truncated_total = combined_content[:15000]
    
    print(f"  -> Отправка в Ollama ({len(files)} файлов, ~{len(truncated_total)} симв.)...")
    summary = query_ollama(truncated_total)
    
    if summary:
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(summary)
        print(f"  [OK] Отчет по проекту сохранен!")
    else:
        print("  [ERR] Не удалось получить ответ.")

def main():
    if not os.path.exists(PROJECTS_ROOT):
        print(f"Папка {PROJECTS_ROOT} не найдена.")
        return
        
    folders = [d for d in os.listdir(PROJECTS_ROOT) if os.path.isdir(os.path.join(PROJECTS_ROOT, d))]
    print(f"Найдено {len(folders)} проектов для анализа.")
    
    for i, folder in enumerate(folders):
        print(f"\n[{i+1}/{len(folders)}]")
        summarize_project_folder(folder)

if __name__ == "__main__":
    main()
