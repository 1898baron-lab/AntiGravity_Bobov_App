import os
import fitz  # PyMuPDF
from docx import Document

SOURCE_DIR = r"C:\Users\Sasha  Baron\Documents\1. Рабочка_КО\15.03.05 Конструкторско-технологическое обеспечение машиностроительных производств"
OUTPUT_DIR = r"C:\ANTIGRAVITY\1\obsidian_brain\1_PROJECTS\Downloads_GDrive_Parsed"

def extract_pdf_text(filepath):
    try:
        text = ""
        with fitz.open(filepath) as doc:
            for page in doc:
                text += page.get_text() + "\n"
        return text
    except Exception as e:
        return f"Ошибка парсинга PDF: {str(e)}"

def extract_docx_text(filepath):
    try:
        doc = Document(filepath)
        return "\n".join([p.text for p in doc.paragraphs])
    except Exception as e:
        return f"Ошибка парсинга DOCX: {str(e)}"

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    stats_parsed = 0
    stats_errors = 0
    
    # Мы будем группировать файлы по имени их родительской папки относительно SOURCE_DIR
    for root, dirs, files in os.walk(SOURCE_DIR):
        if not files:
            continue
            
        # Имя папки
        rel_path = os.path.relpath(root, SOURCE_DIR)
        if rel_path == ".":
            category_name = "Корневые_документы"
        else:
            category_name = rel_path.replace("\\", "_").replace("/", "_")
            
        output_file_path = os.path.join(OUTPUT_DIR, f"{category_name}_Сводка.txt")
        
        with open(output_file_path, "w", encoding="utf-8") as out_file:
            out_file.write(f"# Сводная база знаний: {category_name}\n\n")
            
            for file in files:
                ext = file.lower().split('.')[-1]
                if ext not in ['pdf', 'docx', 'txt']:
                    continue
                    
                filepath = os.path.join(root, file)
                out_file.write(f"\n{'='*40}\n")
                out_file.write(f"=== ДОКУМЕНТ: {file} ===\n")
                out_file.write(f"{'='*40}\n\n")
                
                extracted_text = ""
                if ext == 'pdf':
                    extracted_text = extract_pdf_text(filepath)
                elif ext == 'docx':
                    extracted_text = extract_docx_text(filepath)
                elif ext == 'txt':
                    try:
                        with open(filepath, "r", encoding="utf-8") as f:
                            extracted_text = f.read()
                    except Exception as e:
                        try:
                            with open(filepath, "r", encoding="cp1251") as f:
                                extracted_text = f.read()
                        except:
                            extracted_text = f"Ошибка чтения TXT: {str(e)}"
                
                if "Ошибка парсинга" in extracted_text:
                    stats_errors += 1
                else:
                    stats_parsed += 1
                    
                out_file.write(extracted_text)
                out_file.write("\n\n")
                
        print(f"[{category_name}] Создан мега-файл. Сохранено в {output_file_path}")
        
    print(f"\n--- ГОТОВО ---")
    print(f"Успешно распарсено файлов: {stats_parsed}")
    print(f"Ошибок при парсинге: {stats_errors}")

if __name__ == "__main__":
    main()
