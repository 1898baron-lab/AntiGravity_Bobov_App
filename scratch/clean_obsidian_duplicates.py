import sys, os
sys.stdout.reconfigure(encoding='utf-8')
import shutil
import hashlib

def get_file_hash(filepath):
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def merge_folders(src, dest):
    if not os.path.exists(dest):
        os.makedirs(dest)
    
    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dest_path = os.path.join(dest, item)
        
        if os.path.isdir(src_path):
            merge_folders(src_path, dest_path)
        else:
            if os.path.exists(dest_path):
                # Если файл существует, сравниваем
                src_size = os.path.getsize(src_path)
                dest_size = os.path.getsize(dest_path)
                if src_size > dest_size:
                    # Источник больше, перезаписываем
                    shutil.copy2(src_path, dest_path)
                    print(f"  [Merge] Перезаписан {item} (источник больше: {src_size} > {dest_size} байт)")
                else:
                    print(f"  [Skip] Пропущен {item} (целевой файл больше или равен: {dest_size} >= {src_size} байт)")
            else:
                shutil.copy2(src_path, dest_path)
                print(f"  [Move] Скопирован {item} в {dest}")

def clean_duplicates():
    base_dir = r"C:\ANTIGRAVITY\1\obsidian_brain\4_ARCHIVE\ChatGPT_Projects"
    
    # 1. Список пар дубликатов папок (папка с пробелами -> папка с подчеркиваниями)
    duplicates = [
        ("ChatGPT Prompt Creation", "ChatGPT_Prompt_Creation"),
        ("Clarifying User Intent", "Clarifying_User_Intent"),
        ("Design Draft", "Design_Draft"),
        ("EAGLE Project", "EAGLE_Project"),
        ("Gemini Prompt Creation", "Gemini_Prompt_Creation"),
        ("PC _ Software Upgrade", "PC__Software_Upgrade"),
        ("Анализ ПОС", "Анализ_ПОС"),
        ("Анализ РД", "Анализ_РД"),
        ("ВЕЛИК 2025 _ Ronin Elite L", "ВЕЛИК_2025__Ronin_Elite_L"),
        ("Технология машиностроения", "Технология_машиностроения"),
        ("Улучшатель _ Райт", "Улучшатель__Райт")
    ]
    
    print("🧹 Начинаем слияние дублирующихся папок...")
    for space_name, underscore_name in duplicates:
        src = os.path.join(base_dir, space_name)
        dest = os.path.join(base_dir, underscore_name)
        
        if os.path.exists(src):
            print(f"\nMerging '{space_name}' into '{underscore_name}'...")
            merge_folders(src, dest)
            # После слияния удаляем исходную папку с пробелами
            shutil.rmtree(src)
            print(f"🗑️ Удалена папка с пробелами: {space_name}")
        else:
            print(f"ℹ️ Папка {space_name} не найдена или уже удалена.")
            
    # 2. Удаляем старую папку Archives в корне
    archives_root = r"C:\ANTIGRAVITY\1\obsidian_brain\Archives"
    if os.path.exists(archives_root):
        print(f"\n🗑️ Удаляем устаревшую папку Archives: {archives_root}")
        shutil.rmtree(archives_root)
        print("✅ Устаревшая папка Archives успешно удалена.")
        
    # 3. Удаляем сырой файл новостей ИИ в 0_INBOX
    raw_news = r"C:\ANTIGRAVITY\1\obsidian_brain\0_INBOX\📰 Новости ИИ 2026-05-19.md"
    if os.path.exists(raw_news):
        print(f"\n🗑️ Удаляем сырой авто-файл новостей ИИ: {raw_news}")
        os.remove(raw_news)
        print("✅ Сырой файл новостей успешно удален. Оставлен чистый, красивый дайджест.")

if __name__ == "__main__":
    clean_duplicates()
