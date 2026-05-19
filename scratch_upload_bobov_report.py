import sys
import os
sys.stdout.reconfigure(encoding='utf-8')
from notebooklm_mcp.auth import load_cached_tokens
from notebooklm_mcp.api_client import NotebookLMClient

tokens = load_cached_tokens()
os.environ['NOTEBOOKLM_AUTHUSER'] = '0'
client = NotebookLMClient(cookies=tokens.cookies, csrf_token="", session_id="")

try:
    notebook_id = None
    nbs = client.list_notebooks()
    for nb in nbs:
        if "Дело Бобова" in nb.title:
            notebook_id = nb.id
            break

    if notebook_id:
        filepath = r"C:\ANTIGRAVITY\1\obsidian_brain\1_PROJECTS\BOBOV\Property_Damage_Report.md"
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        filename = os.path.basename(filepath)
        source_id = client.add_text_source(notebook_id, text=content, title=filename)
        print(f"Uploaded {filename}: {source_id}")
    else:
        print("Bobov notebook not found.")
except Exception as e:
    print(f"Error: {e}")
