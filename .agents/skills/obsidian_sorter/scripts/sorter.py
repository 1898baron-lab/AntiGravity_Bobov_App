import os
import sys
import shutil
import httpx
import json
from pathlib import Path
from datetime import datetime
import pypdf

# Устанавливаем UTF-8 для вывода в консоль Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Настройки путей
BRAIN_PATH = Path(r"C:\ANTIGRAVITY\1\obsidian_brain")
INPUT_DIR = BRAIN_PATH / "1_PROJECTS" / "Clippings"
OUTPUT_DIR = BRAIN_PATH / "2_KNOWLEDGE" / "WIKI"

# Конфигурация LLM
LLM_URL = "http://127.0.0.1:1234/v1/chat/completions"
LLM_MODEL = "google/gemma-4-e4b"

def setup_dirs():
    """Создает необходимые директории, если их нет."""
    INPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def extract_pdf_text(filepath: Path) -> str:
    """Извлекает текст из PDF-файла."""
    try:
        reader = pypdf.PdfReader(filepath)
        text = ""
        for page in reader.pages:
            t = page.extract_text()
            if t:
                text += t + "\n"
        return text.strip()
    except Exception as e:
        print(f"Ошибка извлечения текста из PDF {filepath.name}: {e}")
        return ""

def process_with_llm(content: str) -> dict:
    """Обрабатывает текст через локальную нейросеть."""
    prompt = f"""
Проанализируй следующую заметку/статью.
Ответь СТРОГО в формате JSON со следующими ключами:
- "summary": краткая выжимка (3-4 предложения, суть).
- "tags": список из 3-5 релевантных тегов (без решетки).
- "category": одно слово-категория для папки (например, "Programming", "News", "AI", "Engineering", "Business", "Other").

Текст:
{content[:5000]}
"""

    payload = {
        "model": LLM_MODEL,
        "messages": [
            {"role": "system", "content": "Ты - система анализа текстов. Твоя задача возвращать исключительно валидный JSON без маркдаун-оболочек (без ```json)."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.1,
        "max_tokens": 1024
    }

    try:
        with httpx.Client(timeout=120.0) as client:
            response = client.post(LLM_URL, json=payload)
            response.raise_for_status()
            result_text = response.json()["choices"][0]["message"]["content"]
            # Пытаемся распарсить JSON, если модель отдала с маркдауном
            result_text = result_text.replace("```json", "").replace("```", "").strip()
            return json.loads(result_text)
    except Exception as e:
        print(f"Ошибка LLM или парсинга JSON: {e}")
        return None

def process_file(filepath: Path):
    """Считывает файл, прогоняет через ИИ и перемещает."""
    print(f"\nОбработка: {filepath.name}")
    suffix = filepath.suffix.lower()
    
    # 1. Читаем контент в зависимости от расширения
    if suffix == ".pdf":
        content = extract_pdf_text(filepath)
        if not content:
            print(f"Не удалось извлечь текст из PDF {filepath.name}. Пропускаем.")
            return
    elif suffix in [".md", ".txt", ".skill", ".prompt"]:
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
        except UnicodeDecodeError:
            try:
                print(f"Предупреждение: не удалось декодировать {filepath.name} в UTF-8. Пробуем CP1251...")
                with open(filepath, "r", encoding="cp1251") as f:
                    content = f.read()
            except Exception as e:
                print(f"Предупреждение: не удалось декодировать {filepath.name} в CP1251. Читаем с игнорированием ошибок...")
                with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
        except Exception as e:
            print(f"Ошибка чтения {filepath.name}: {e}")
            return
    else:
        print(f"Неподдерживаемый тип файла {filepath.name}. Пропускаем.")
        return

    if not content.strip():
        print(f"Файл {filepath.name} пуст. Пропускаем.")
        return

    # 2. Запрашиваем ИИ
    ai_data = process_with_llm(content)
    if not ai_data:
        print(f"Пропуск {filepath.name} из-за ошибки ИИ.")
        return

    summary = ai_data.get("summary", "")
    tags = ai_data.get("tags", [])
    category = ai_data.get("category", "Unsorted").replace(" ", "_").replace("/", "")

    # 3. Формируем Markdown-файл
    tags_yaml = "\n".join([f"  - {t}" for t in tags])
    frontmatter = f"---\ntags:\n{tags_yaml}\ndate_processed: {datetime.now().strftime('%Y-%m-%d')}\n---\n\n"
    summary_section = f"> [!abstract] ИИ Выжимка\n> {summary}\n\n"

    # Папка назначения
    target_dir = OUTPUT_DIR / category
    target_dir.mkdir(parents=True, exist_ok=True)

    if suffix == ".md":
        # Перезаписываем исходный .md с выжимкой и перемещаем
        new_content = frontmatter + summary_section + content
        target_path = target_dir / filepath.name
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
            shutil.move(str(filepath), str(target_path))
            print(f"Успешно обработан и перенесен MD: {target_path.name}")
        except Exception as e:
            print(f"Ошибка при сохранении MD {filepath.name}: {e}")
    else:
        # Для PDF, TXT, SKILL генерируем отдельную Markdown-заметку
        md_filename = filepath.stem + ".md"
        md_target_path = target_dir / md_filename
        
        # Контент для заметки
        note_content = frontmatter + summary_section
        if suffix in [".txt", ".skill", ".prompt"]:
            note_content += f"## Содержимое файла\n```text\n{content}\n```\n"
        else:
            note_content += f"## Вынутый текст из PDF\n{content}\n"
            
        try:
            # Записываем Markdown
            with open(md_target_path, "w", encoding="utf-8") as f:
                f.write(note_content)
            # Переносим оригинальный файл рядом с Markdown
            orig_target_path = target_dir / filepath.name
            shutil.move(str(filepath), str(orig_target_path))
            print(f"Успешно обработан и перенесен файл: {filepath.name} (Markdown-выжимка: {md_filename})")
        except Exception as e:
            print(f"Ошибка при обработке стороннего файла {filepath.name}: {e}")

def main():
    setup_dirs()
    print("Запуск авто-сортировщика заметок...")
    
    # Ищем все файлы в Clippings
    all_files = []
    for ext in ["*.md", "*.pdf", "*.txt", "*.skill", "*.prompt"]:
        all_files.extend(list(INPUT_DIR.glob(ext)))
        
    if not all_files:
        print("В папке Clippings нет новых файлов для сортировки.")
        return
        
    print(f"Найдено файлов для обработки: {len(all_files)}")
    for file in all_files:
        process_file(file)
        
    print("\nСортировка и уборка завершены!")

if __name__ == "__main__":
    main()
