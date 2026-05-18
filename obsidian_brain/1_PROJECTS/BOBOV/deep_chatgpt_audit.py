import json
import os

def deep_analyze_chatgpt():
    input_file = r'C:/ANTIGRAVITY/1/chatgpt_session.json'
    output_report = r'C:/ANTIGRAVITY/1/obsidian_brain/1_PROJECTS/BOBOV/CHATGPT_HISTORY_AUDIT.md'
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            # Читаем файл как текст, так как это может быть дамп сессии с куками в начале
            raw_content = f.read()
            
        # Попытка найти JSON объект внутри дампа (если там куки в начале)
        json_start = raw_content.find('{')
        if json_start == -1:
            print("JSON не найден")
            return
            
        data = json.loads(raw_content[json_start:])
        
        report = ["# АУДИТ ИСТОРИИ CHATGPT (2025-2026)\n"]
        report.append("Этот документ содержит структурированные инсайты, извлеченные из твоих прошлых диалогов.\n")

        # 1. Сбор контекста из localStorage (там часто лежат инструкции и кастомные настройки)
        if "origins" in data:
            for origin in data["origins"]:
                if "chatgpt.com" in origin.get("origin", ""):
                    for item in origin.get("localStorage", []):
                        if "instructions" in item.get("name", ""):
                            report.append("## ПЕРСОНАЛЬНЫЕ ИНСТРУКЦИИ (Identity)\n")
                            report.append(f"```text\n{item.get('value')}\n```\n")

        # 2. Поиск диалогов (в экспорте они обычно в 'conversations' или 'mapping')
        # Если это дамп сессии, диалоги могут быть в IndexedDB или вложенных структурах.
        # В данном дампе мы видим метаданные файлов.
        
        report.append("## ВАЖНЫЕ ФАЙЛЫ ИЗ ИСТОРИИ\n")
        # Ищем все вхождения "name": "..." в сыром тексте для полноты
        import re
        file_matches = re.findall(r'\"name\":\"(.*?)\"', raw_content)
        for fm in set(file_matches):
            if fm.endswith(('.pdf', '.txt', '.xlsx', '.docx')):
                report.append(f"- [ ] {fm}")
        
        report.append("\n## СТРАТЕГИЧЕСКИЕ ИНСАЙТЫ (Анализ по ключевым словам)\n")
        
        sections = {
            "ЮРИДИЧЕСКАЯ АТАКА": ["125 УПК", "Мовланов", "кража", "Бобов", "12 млн"],
            "ПРОЕКТ ЗЕВС (Росатом)": ["Ду170", "Клапан", "АМг6", "ЦПТИ", "весовая сводка"],
            "MASTODONT (Бот и Гриль)": ["Мангал", "dxf", "telegram", "webhook"]
        }
        
        for section, keywords in sections.items():
            report.append(f"### {section}")
            found_anything = False
            for kw in keywords:
                # Ищем контекст (250 символов вокруг)
                matches = re.finditer(re.escape(kw), raw_content, re.IGNORECASE)
                for match in matches:
                    snippet = raw_content[match.start()-100 : match.end()+250]
                    # Очистка от JSON мусора
                    clean_snippet = re.sub(r'[\"{}\[\]]', '', snippet).replace('\\n', ' ')
                    report.append(f"> ...{clean_snippet}...")
                    found_anything = True
                    break # Только одно вхождение на слово для краткости
            if not found_anything:
                report.append("*Информации не найдено.*")
            report.append("\n")

        with open(output_report, 'w', encoding='utf-8') as f_out:
            f_out.write("\n".join(report))
            
        print(f"Глубокий анализ завершен: {output_report}")

    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    deep_analyze_chatgpt()
