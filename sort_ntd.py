import os
import shutil

BASE_DIR = r"C:\Users\Sasha  Baron\Documents\1. Рабочка_КО\15.03.05 Конструкторско-технологическое обеспечение машиностроительных производств\НТД"

CATEGORIES = {
    "ЕСКД": ["ГОСТ 2.", "ГОСТ Р 2.", "Перечень ГОСТов группы ЕСКД", "gost_2"],
    "Крепеж": ["Винт", "Шайб", "Болт", "Гайк", "Штифт", "DIN", "ISO", "крепежн"],
    "Материалы и Сортамент": ["Прокат", "Стекло", "Плит", "Лист", "Алюминий", "Сталь", "Профил", "Швеллер", "Угол", "Труб", "Пластин", "Сплав"],
    "Сварка": ["Сварн", "сварка", "ИСО 13920"],
    "Покрытия и Защита": ["ГОСТ 9.", "ЕСЗКС", "Единая система защиты", "Покрыти", "Окрашивани"],
    "Допуски, Посадки и Резьбы": ["взаимозаменяемости", "допуск", "посадк", "Резьб", "шпоночн", "ГОСТ 30893", "ГОСТ 25346", "ГОСТ 25347", "ГОСТ 8724", "ГОСТ 10549"],
    "Отраслевые стандарты (ОСТ, НП)": ["ОСТ", "НП-"],
    "Судостроение": ["судов", "иллюминатор", "Трапы", "люков"],
    "Организация и Нормы": ["СРПП", "ГОСТ 15.", "ГОСТ Р 15.", "Типовые нормы времени", "Р 50-", "ЕК 001"],
}

def get_category(filename):
    filename_lower = filename.lower()
    for cat, keywords in CATEGORIES.items():
        for kw in keywords:
            if kw.lower() in filename_lower:
                return cat
    return "Разное"

def main():
    if not os.path.exists(BASE_DIR):
        print(f"Директория не найдена: {BASE_DIR}")
        return

    moved_count = 0
    for file in os.listdir(BASE_DIR):
        file_path = os.path.join(BASE_DIR, file)
        
        # Пропускаем директории
        if os.path.isdir(file_path):
            continue
            
        category = get_category(file)
        cat_dir = os.path.join(BASE_DIR, category)
        
        if not os.path.exists(cat_dir):
            os.makedirs(cat_dir)
            
        dest_path = os.path.join(cat_dir, file)
        shutil.move(file_path, dest_path)
        print(f"[{category}] Перемещен: {file}")
        moved_count += 1
        
    print(f"Готово! Перемещено {moved_count} файлов.")

if __name__ == "__main__":
    main()
