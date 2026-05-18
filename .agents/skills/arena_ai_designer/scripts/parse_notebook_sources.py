import os
import json
import re

steps_dir = r"C:\Users\Sasha  Baron\.gemini\antigravity\brain\c73fe980-485b-433b-bbdd-e57bd93eac81\.system_generated\steps"
step_ids = ["6358", "6359", "6360", "6361", "6367", "6368", "6369", "6370", "6377", "6378", "6379", "6380", "6381"]

output_dir = r"C:\ANTIGRAVITY\1\obsidian_brain\2_KNOWLEDGE\SYNTHESIS\NotebookLM_Superpowers"

def sanitize_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', "", filename).strip()

for step_id in step_ids:
    file_path = os.path.join(steps_dir, step_id, "output.txt")
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            if data.get("status") == "success":
                title = data.get("title", "Untitled")
                content = data.get("content", "")
                
                safe_title = sanitize_filename(title)
                output_path = os.path.join(output_dir, f"{safe_title}.md")
                
                with open(output_path, "w", encoding="utf-8") as out_f:
                    out_f.write(f"---\n")
                    out_f.write(f"tags: [NotebookLM, Superpowers]\n")
                    out_f.write(f"title: {title}\n")
                    out_f.write(f"---\n\n")
                    out_f.write(f"# {title}\n\n")
                    out_f.write(content)
                print(f"Saved: {output_path}")
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
