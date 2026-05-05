import re

def deep_scan(filepath):
    results = []
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            # Ищем любые числа больше 100 000 (потенциальный ущерб)
            matches = re.findall(r'(\d{3,}\s?\d{3,})', line)
            if matches:
                # Берем контекст вокруг числа
                results.append(line.strip())
    return results

filepath = r'C:\ANTIGRAVITY\1\obsidian_brain\1_PROJECTS\BOBOV\extracted_correspondence.txt'
findings = deep_scan(filepath)

print(f"Found {len(findings)} potential matches.")
for f in findings[:30]:
    print(f"MATCH: {f[:200]}...")
