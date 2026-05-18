import json
import re

def parse_chatgpt_session():
    input_file = r'C:/ANTIGRAVITY/1/chatgpt_session.json'
    output_file = r'C:/ANTIGRAVITY/1/obsidian_brain/1_PROJECTS/BOBOV/chatgpt_insights.txt'
    
    keywords = ['Бобов', '125 УПК', 'ТЗ', 'ЗЕВС', 'Мангал', 'Ду170', 'АМг6', '12 млн']
    
    insights = []
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # Поиск сообщений в localStorage или других частях JSON
        # Обычно ChatGPT экспорт хранит сообщения в структуре 'mapping' или 'messages'
        content_str = json.dumps(data, ensure_ascii=False)
        
        # Простой поиск по ключевым словам в огромной строке, если структура сложная
        for kw in keywords:
            # Находим контекст вокруг ключевого слова (200 символов)
            matches = re.finditer(re.escape(kw), content_str, re.IGNORECASE)
            for match in matches:
                start = max(0, match.start() - 150)
                end = min(len(content_str), match.end() + 300)
                snippet = content_str[start:end].strip()
                insights.append(f"--- НАЙДЕНО: {kw} ---\n...{snippet}...\n")

        with open(output_file, 'w', encoding='utf-8') as f_out:
            if insights:
                f_out.write("\n".join(set(insights))) # set() для удаления дублей
            else:
                f_out.write("Ключевые слова не найдены в сессии.")
                
        print(f"Анализ завершен. Результаты в: {output_file}")
        
    except Exception as e:
        print(f"Ошибка парсинга: {e}")

if __name__ == "__main__":
    parse_chatgpt_session()
