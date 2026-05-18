import os
import sys
import shutil
from pathlib import Path
from datetime import datetime

# ─── НАСТРОЙКИ ───────────────────────────────────────────────────────────────

ROOT = Path(r"C:\ANTIGRAVITY\1")
OBSIDIAN = ROOT / "obsidian_brain"
ARCHIVE_OLD = OBSIDIAN / "Archives"
ARCHIVE_NEW = OBSIDIAN / "4_ARCHIVE"
META_DIR = OBSIDIAN / "3_META"
TODAY = datetime.now().strftime("%Y-%m-%d")

# ─── ЖЕЛАЕМАЯ СТРУКТУРА OBSIDIAN ──────────────────────────────────────────────

DESIRED_STRUCTURE = {
    "1_PROJECTS/ZEUS": {
        "Zeus_Modernization_2026.md": {
            "tags": ["engineering", "rosatom", "zeus"],
            "title": "Зевс — Инженерный дневник модернизации 2026",
            "body": "## Статус\n- Клапан DN170: проектирование\n- Куратор: Афанасьев А.И. (Красноярск)\n\n## Открытые вопросы\n- [ ] Марка материала на чертежах (вероятно 12Х18Н10Т)\n- [ ] КИМ 0.55–0.65, вес готового ~50–70 кг\n\n## Ссылки\n- [[Zeus_Core_Evolution]]\n"
        },
        "DN170_Valve_Notes.md": {
            "tags": ["engineering", "rosatom", "valve", "zeus"],
            "title": "Клапан запорный Ду170 — Технические заметки",
            "body": "## Параметры\n- Ду: 170 мм\n- Установка: ЗЕВС-М\n- Деталей: 8 оригинальных + покупные\n- Масса готового: ~50–70 кг\n- Масса заготовки: ~84–94 кг\n- КИМ: 0.55–0.65\n\n## Замечания\n- Отсутствует марка материала на чертежах\n- Вероятный материал: 12Х18Н10Т (нержавейка)\n\n## Задачи\n- [ ] Уточнить марку материала у куратора\n- [ ] Весовая оптимизация до 25 кг (ТЗ)\n"
        }
    },
    "1_PROJECTS/MARCH_YACHTS": {
        "MARCH_Project_State.md": {
            "tags": ["engineering", "march-yachts", "shipbuilding"],
            "title": "MARCH Yacht's — Состояние проекта",
            "body": "## О проекте\nСемейный судостроительный проект (Кирилл + отец).\nКатамараны и маломерные суда. Технологии: фанера, стеклопластик, СИС. Без ЧПУ.\n\n## Активные задачи\n- [ ] Рулевая система катамарана (3ds Max 2026, Script Controller)\n- [ ] Кинематика трапеции — тригонометрия\n\n## Разделы\n- [[Steering_Kinematics_3dsMax]]\n- [[SIS_Technology_Notes]]\n"
        },
        "Steering_Kinematics_3dsMax.md": {
            "tags": ["engineering", "march-yachts", "3dsmax", "kinematics"],
            "title": "Рулевая система — Кинематика в 3ds Max 2026",
            "body": "## Задача\nРулевая трапеция катамарана. Кинематика через Script Controller.\n\n## Текущий подход\n- Инструмент: 3ds Max 2026\n- Метод: Script Controller + тригонометрия\n- Статус: в работе\n\n## Заметки\n*(заполнять по ходу работы)*\n"
        },
        "SIS_Technology_Notes.md": {
            "tags": ["engineering", "march-yachts", "technology", "composite"],
            "title": "Технология СИС — Заметки",
            "body": "## Описание\nТехнология сэндвич-интегральных структур (СИС) для корпусов маломерных судов.\n\n## Применение в MARCH Yacht's\n- Материалы: фанера, стеклопластик\n- Методы: ручное ламинирование, раскрой без ЧПУ\n\n## Заметки\n*(заполнять по ходу работы)*\n"
        }
    },
    "1_PROJECTS/KUPE": {
        "KUPE_Project_State.md": {
            "tags": ["engineering", "rosatom", "kupe", "pneumatics"],
            "title": "КУПЕ — Пневматическая установка дистанционного сверления",
            "body": "## Описание\nПневматическая установка дистанционного сверления заглушек контейнеров ОГФУ.\n\n## Ключевые узлы\n- Зажимной узел: 4×Ø80мм цилиндры SMC\n- Захват выдвижной: Сталь 20, HRC 40-45\n- Схема: бистабильный распределитель\n\n## Статус\n- [ ] Анализ поломки рычажного зажима\n- [x] Разработка пневматического зажимного узла\n- [x] Пневмосхема\n- [x] Спецификация с ценами\n\n## Файлы\n- [[KUPE_Pneumo_Scheme]]\n- [[KUPE_Clamp_Node]]\n"
        },
        "KUPE_Pneumo_Scheme.md": {
            "tags": ["engineering", "rosatom", "kupe", "pneumatics"],
            "title": "КУПЕ — Пневматическая схема",
            "body": "## Схема\n- Тип распределителя: бистабильный\n- Рабочая среда: сжатый воздух\n- Производитель арматуры: SMC\n\n## Описание работы\n*(добавить описание цикла работы)*\n"
        },
        "KUPE_Clamp_Node.md": {
            "tags": ["engineering", "rosatom", "kupe", "clamp"],
            "title": "КУПЕ — Зажимной узел",
            "body": "## Параметры\n- Цилиндры: 4×Ø80мм (SMC)\n- Материал захвата: Сталь 20\n- Твёрдость: HRC 40-45\n\n## Анализ отказа\nРычажный зажим — причина поломки:\n*(добавить описание)*\n\n## Решение\nПневматический зажимной узел с 4 цилиндрами по окружности.\n"
        }
    },
    "1_PROJECTS/ZAKRJEP": {
        "ZAKRJEP_2026_Pilot.md": {
            "tags": ["engineering", "rosatom", "fixture", "zakrjep"],
            "title": "ЗАКРЕП-2026 / Pilot — Стапель 1200×800",
            "body": "## Параметры\n- Габарит: 1200×800 мм\n- Профиль: труба 40×40×3\n- Материал: Сталь 20 (контекст Росатом)\n- Допуск: ±1 мм → класс «m» по ГОСТ 30893.1\n\n## Сварка\n- Процесс: MAG-135\n- Требование: антидеформационная последовательность\n\n## Замечания по ТЗ\n- S235 ≠ замена Стали 20 для Росатома (требует согласования)\n- ±1 мм соответствует ~12-му квалитету (строже класса «m»)\n\n## НТД\n- ГОСТ 30893.1-2002\n- ГОСТ 5264 (швы MAG)\n"
        }
    },
    "1_PROJECTS/MANGAL": {
        "Mangal_Flange_Calc.md": {
            "tags": ["engineering", "personal", "mangal", "thermal"],
            "title": "Мангал — Расчёт теплового удлинения фланца",
            "body": "## Конструкция\n- Модульный мангал: 2 секции\n- Соединение: болтовое фланцевое\n- Тип: плавающий фланец (компенсация удлинения)\n\n## Тепловое удлинение\n- Материал: сталь\n- α = 12×10⁻⁶ 1/°C\n- ΔL = α × L × ΔT\n\n## Задачи\n- [ ] Уточнить рабочую температуру\n- [ ] Подобрать зазор в плавающем фланце\n"
        }
    },
    "2_KNOWLEDGE": {
        "GOST_Welding_Comparison.md": {
            "tags": ["knowledge", "gost", "welding", "iso"],
            "title": "Сравнение ГОСТ 14771 и ISO 15614",
            "body": "## ГОСТ 14771\n- Стандарт на швы сварных соединений\n- Геометрия, конструктивные элементы, размеры\n- Обязателен для РФ\n- НЕ является стандартом на аттестацию технологии\n\n## ISO 15614\n- Серия из ~13 частей (по каждому процессу)\n- Аттестация технологии сварки (WPS/PQR)\n- Международное признание\n- Часть 1: MAG/MIG/TIG; Часть 2: газовая; и т.д.\n\n## Аналог в РФ\n- ГОСТ Р ИСО 15614 — прямой перевод\n- РД 03-615 — Ростехнадзор (аттестация)\n\n## Вывод\n- Геометрия швов → ГОСТ 14771\n- Аттестация технологии → РД 03-615 / ГОСТ Р ИСО 15614\n"
        }
    },
    "3_META": {}  # PROJECT_STATE.md уже есть
}

# ─── ФУНКЦИИ ──────────────────────────────────────────────────────────────────

def make_frontmatter(tags: list, title: str) -> str:
    tag_str = ", ".join(tags)
    return f"---\ntags: [{tag_str}]\ntitle: \"{title}\"\ncreated: {TODAY}\n---\n\n"


def scan_directory(path: Path, indent=0) -> list:
    """Рекурсивно сканирует директорию, возвращает список строк для отчёта."""
    lines = []
    try:
        items = sorted(path.iterdir(), key=lambda x: (x.is_file(), x.name))
    except PermissionError:
        return [f"{'  ' * indent}[ACCESS DENIED]"]
    
    for item in items:
        prefix = "  " * indent
        if item.is_dir():
            lines.append(f"{prefix}📁 {item.name}/")
            lines.extend(scan_directory(item, indent + 1))
        else:
            size = item.stat().st_size
            size_str = f"{size:,} B" if size < 1024 else f"{size/1024:.1f} KB"
            lines.append(f"{prefix}📄 {item.name}  [{size_str}]")
    return lines


def create_md_file(filepath: Path, tags: list, title: str, body: str):
    """Создаёт .md файл с frontmatter, если его ещё нет."""
    if filepath.exists():
        print(f"  [SKIP] уже существует: {filepath.relative_to(OBSIDIAN)}")
        return False
    
    filepath.parent.mkdir(parents=True, exist_ok=True)
    content = make_frontmatter(tags, title) + f"# {title}\n\n" + body
    filepath.write_text(content, encoding="utf-8")
    print(f"  [CREATE] {filepath.relative_to(OBSIDIAN)}")
    return True


def fix_tag_in_file(filepath: Path, old_tag: str, new_tag: str):
    """Заменяет тег в существующем файле."""
    if not filepath.exists():
        return False
    content = filepath.read_text(encoding="utf-8")
    if old_tag in content:
        new_content = content.replace(old_tag, new_tag, 1)
        filepath.write_text(new_content, encoding="utf-8")
        print(f"  [FIX TAG] {filepath.name}: '{old_tag}' → '{new_tag}'")
        return True
    return False


def archive_duplicate_folder():
    """Перемещает старую папку Archives/ в 4_ARCHIVE/_old_Archives/."""
    if not ARCHIVE_OLD.exists():
        print("  [OK] Папка Archives/ не найдена — дубля нет.")
        return
    
    dest = ARCHIVE_NEW / "_old_Archives_pre_sync"
    if dest.exists():
        print(f"  [SKIP] {dest.name} уже существует.")
        return
    
    shutil.move(str(ARCHIVE_OLD), str(dest))
    print(f"  [MERGE] Archives/ → 4_ARCHIVE/_old_Archives_pre_sync/")


def generate_audit_report(scan_lines: list, created: list, fixed: list) -> str:
    """Генерирует Markdown-отчёт аудита."""
    report = f"""---
tags: [meta, audit]
title: "Аудит структуры ANTIGRAVITY — {TODAY}"
created: {TODAY}
---

# 🗂 Аудит структуры ANTIGRAVITY
*Дата: {TODAY} | Скрипт: antigravity_obsidian_sync.py*

## 1. Созданные файлы ({len(created)})

"""
    for f in created:
        report += f"- `{f}`\n"
    
    report += f"""
## 2. Исправленные теги ({len(fixed)})

"""
    for f in fixed:
        report += f"- {f}\n"
    
    report += f"""
## 3. Полное дерево C:\\ANTIGRAVITY\\1

```text
"""
    report += "\n".join(scan_lines[:200])  # лимит 200 строк
    if len(scan_lines) > 200:
        report += f"\n... (ещё {len(scan_lines) - 200} строк)"
    report += "\n```\n"
    
    return report


# ─── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print(f"ANTIGRAVITY OBSIDIAN SYNC | {TODAY}")
    print("=" * 60)
    
    if not ROOT.exists():
        print(f"\n[ERROR] Папка не найдена: {ROOT}")
        sys.exit(1)
    
    if not OBSIDIAN.exists():
        print(f"\n[ERROR] Obsidian vault не найден: {OBSIDIAN}")
        sys.exit(1)
    
    created_files = []
    fixed_files = []
    
    # 1. Создаём недостающие файлы
    print("\n📝 Создание недостающих файлов...")
    for folder, files in DESIRED_STRUCTURE.items():
        for filename, meta in files.items():
            filepath = OBSIDIAN / folder / filename
            ok = create_md_file(
                filepath,
                meta["tags"],
                meta["title"],
                meta["body"]
            )
            if ok:
                created_files.append(str(filepath.relative_to(OBSIDIAN)))
    
    # 2. Исправляем теги
    print("\n🔧 Исправление тегов...")
    mangal_file = OBSIDIAN / "1_PROJECTS" / "MANGAL" / "Mangal_Design_History.md"
    if fix_tag_in_file(mangal_file, "infrastructure", "engineering"):
        fixed_files.append("MANGAL/Mangal_Design_History.md: infrastructure → engineering")
    
    # 3. Архивируем дубль
    print("\n🗃 Проверка дублирующих папок...")
    archive_duplicate_folder()
    
    # 4. Сканируем всё дерево
    print("\n🔍 Сканирование C:\\ANTIGRAVITY\\1...")
    scan_lines = scan_directory(ROOT)
    
    # 5. Сохраняем отчёт
    print("\n📊 Сохранение отчёта аудита...")
    audit_path = META_DIR / f"AUDIT_{TODAY}.md"
    META_DIR.mkdir(parents=True, exist_ok=True)
    report = generate_audit_report(scan_lines, created_files, fixed_files)
    audit_path.write_text(report, encoding="utf-8")
    print(f"  [SAVED] {audit_path.relative_to(OBSIDIAN)}")
    
    # 6. Итог
    print("\n" + "=" * 60)
    print(f"✅ ГОТОВО")
    print(f"   Создано файлов:    {len(created_files)}")
    print(f"   Исправлено тегов:  {len(fixed_files)}")
    print(f"   Отчёт:             3_META/AUDIT_{TODAY}.md")
    print("=" * 60)
    print("\n⚡ Следующий шаг: запусти /sync_github для пуша в GitHub")


if __name__ == "__main__":
    main()
