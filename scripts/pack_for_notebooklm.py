import os

def pack_directory(source_dir, output_file, name):
    if not os.path.exists(source_dir):
        print(f"[!] Директория {source_dir} не найдена. Пропуск.")
        return
        
    print(f"[*] Сборка тома: {name} из {source_dir}...")
    count = 0
    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write(f"=== ТОМ: {name} ===\n\n")
        
        for root, _, filenames in os.walk(source_dir):
            for filename in filenames:
                if filename.endswith('.md'):
                    filepath = os.path.join(root, filename)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as infile:
                            content = infile.read()
                            
                        outfile.write(f"\n\n--- НАЧАЛО ДОКУМЕНТА: {filename} ---\n")
                        outfile.write(content)
                        outfile.write(f"\n--- КОНЕЦ ДОКУМЕНТА: {filename} ---\n")
                        count += 1
                    except Exception as e:
                        print(f"  [Ошибка] Не удалось прочитать {filepath}: {e}")
                        
    print(f"[+] Успешно упаковано {count} файлов в {output_file}")

if __name__ == "__main__":
    out_dir = r"C:\ANTIGRAVITY\1\notebooklm_exports"
    os.makedirs(out_dir, exist_ok=True)
    
    pack_directory(
        r"C:\ANTIGRAVITY\1\legal", 
        os.path.join(out_dir, "Legal_Corpus.txt"), 
        "Юридическое Досье Бобова"
    )
    
    pack_directory(
        r"C:\ANTIGRAVITY\1\Internship_NTD", 
        os.path.join(out_dir, "Engineering_Corpus.txt"), 
        "Инженерные чертежи и нормативы Росатома"
    )
    
    pack_directory(
        r"C:\ANTIGRAVITY\1\obsidian_brain", 
        os.path.join(out_dir, "Obsidian_Core.txt"), 
        "База Знаний и Дневники"
    )
    
    print(f"\nСборка завершена! Все 3 тома лежат в папке {out_dir}")
    print("Теперь вы можете просто загрузить эти 3 файла в NotebookLM!")
