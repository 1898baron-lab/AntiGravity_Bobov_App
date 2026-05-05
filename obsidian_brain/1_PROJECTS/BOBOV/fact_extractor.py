import re

def extract_legal_facts(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Удаляем скрипты и стили
    clean_text = re.sub(r'var GLOBALS.*?;', '', content, flags=re.DOTALL)
    clean_text = re.sub(r'<script.*?>.*?</script>', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'<style.*?>.*?</style>', '', clean_text, flags=re.DOTALL)
    
    # Ищем потенциальные суммы (цифры + валюта/сокращения)
    money_pattern = r'(\d[\d\s,.]+\s?(руб|р\.|USD|\$|евро|EUR))'
    money_matches = re.findall(money_pattern, clean_text, re.IGNORECASE)
    
    # Ищем даты
    date_pattern = r'(\d{2}\.\d{2}\.\d{4})'
    date_matches = re.findall(date_pattern, clean_text)
    
    # Ищем упоминания "кражи", "самоуправства", "полиции"
    keywords = ['кража', 'хищение', 'Бобов', '330', '158', 'УПК', 'следователь', 'изъятие', 'имущество']
    found_keywords = [word for word in keywords if word.lower() in clean_text.lower()]

    return {
        "money": list(set([m[0] for m in money_matches])),
        "dates": list(set(date_matches)),
        "keywords": found_keywords,
        "sample": clean_text[:2000] # Первые 2к символов чистого текста
    }

filepath = r'C:\ANTIGRAVITY\1\obsidian_brain\1_PROJECTS\BOBOV\mht_extracted_text.txt'
results = extract_legal_facts(filepath)

print("--- MONEY ---")
print("\n".join(results["money"][:20]))
print("\n--- DATES ---")
print("\n".join(results["dates"][:10]))
print("\n--- KEYWORDS ---")
print(", ".join(results["keywords"]))
print("\n--- TEXT SAMPLE ---")
print(results["sample"])
