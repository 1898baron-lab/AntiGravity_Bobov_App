import os
import json
import shutil
import re

# Каталоги
SUMMARIES_DIR = r"C:\ANTIGRAVITY\1\obsidian_brain\1_PROJECTS\Summaries"
KNOWLEDGE_BASE_DIR = r"C:\Users\Sasha  Baron\.gemini\antigravity\knowledge"

def sync_all():
    if not os.path.isdir(SUMMARIES_DIR):
        print(f"[SYNC] Папка {SUMMARIES_DIR} не найдена.")
        return

    summaries = [f for f in os.listdir(SUMMARIES_DIR) if f.lower().endswith('.md')]
    print(f"[SYNC] Найдено {len(summaries)} выжимок для импорта.")

    for summary_file in summaries:
        src_path = os.path.join(SUMMARIES_DIR, summary_file)
        base_name = summary_file.replace('_Summary.md', '')
        safe_dir_name = re.sub(r'[^\w\s-]', '', base_name).strip().replace(' ', '_').lower()
        ki_dir = os.path.join(KNOWLEDGE_BASE_DIR, safe_dir_name)
        ki_artifacts_dir = os.path.join(ki_dir, 'artifacts')
        os.makedirs(ki_artifacts_dir, exist_ok=True)
        
        dest_path = os.path.join(ki_artifacts_dir, summary_file)
        shutil.copy2(src_path, dest_path)

        metadata = {
            "summary": f"Суммаризированная фактура (ТТХ, задачи, решения) из старого чата: {base_name}",
            "created_at": "2026-05-05T00:00:00Z",
            "references": [
                f"file:///{src_path.replace(chr(92), '/')}"
            ]
        }
        
        meta_path = os.path.join(ki_dir, "metadata.json")
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, ensure_ascii=False, indent=4)
            
        print(f"  [+] Интегрировано в базу знаний: {safe_dir_name}")

if __name__ == "__main__":
    sync_all()
