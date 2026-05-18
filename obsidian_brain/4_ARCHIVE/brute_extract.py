import json
import re

def extract_all_russian_text():
    input_file = r'C:/ANTIGRAVITY/1/chatgpt_session.json'
    output_file = r'C:/ANTIGRAVITY/1/obsidian_brain/Archives/TOTAL_EXTRACT_RU.txt'
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Находим все последовательности русских букв и знаков препинания (минимум 10 символов)
        # Также учитываем юникод-последовательности \u04xx
        
        # Декодируем юникод-эскейпы
        decoded_content = content.encode().decode('unicode_escape')
        
        # Ищем длинные русские фразы
        russian_matches = re.findall(r'[А-Яа-яЁё\s\d.,!?;:()"-]{10,}', decoded_content)
        
        with open(output_file, 'w', encoding='utf-8') as f_out:
            for match in russian_matches:
                clean_match = match.strip()
                if clean_match:
                    f_out.write(clean_match + "\n\n")
                    
        print(f"Экстракция завершена. Файл: {output_file}")
        
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    extract_all_russian_text()
