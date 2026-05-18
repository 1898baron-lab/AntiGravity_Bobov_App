import os
import shutil

def migrate_history():
    src_dir = r"C:\ANTIGRAVITY\1\История github"
    obsidian_root = r"C:\ANTIGRAVITY\1\obsidian_brain"
    
    mapping = {
        "Filing Police Theft Report.md": "1_PROJECTS/BOBOV/Case_History/Legal_Attack_2025.md",
        "Reviewing AntiGravity Project Updates.md": "1_PROJECTS/ZEUS/Design_History/Zeus_Core_Evolution.md",
        "Designing A Custom Mangal.md": "1_PROJECTS/MANGAL/Mangal_Design_History.md",
        "Locating AutoCAD Conversation History.md": "Knowledge_Base/AutoCAD_Troubleshooting_Log.md",
        "Integrating ChatGPT With AntiGravity.md": "Knowledge_Base/AI_Infrastructure_History.md"
    }
    
    for old_name, new_rel_path in mapping.items():
        src = os.path.join(src_dir, old_name)
        dst = os.path.join(obsidian_root, new_rel_path)
        
        if os.path.exists(src):
            # Читаем и добавляем Frontmatter для Obsidian
            with open(src, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tag = "legal" if "BOBOV" in dst else "engineering" if "ZEUS" in dst else "infrastructure"
            frontmatter = f"---\ntags: [history, {tag}]\noriginal_file: {old_name}\nmigrated: 2026-05-05\n---\n\n"
            
            with open(dst, 'w', encoding='utf-8') as f:
                f.write(frontmatter + content)
            print(f"Мигрировал: {old_name} -> {new_rel_path}")

if __name__ == "__main__":
    migrate_history()
