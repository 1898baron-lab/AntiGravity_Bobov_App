import sys
import os
sys.stdout.reconfigure(encoding='utf-8')
from notebooklm_mcp.auth import load_cached_tokens
from notebooklm_mcp.api_client import NotebookLMClient

tokens = load_cached_tokens()
os.environ['NOTEBOOKLM_AUTHUSER'] = '0'
client = NotebookLMClient(cookies=tokens.cookies, csrf_token="", session_id="")

title = "🥇 AntiGravity: ЦПТИ / Росатом – Инженерная база знаний и Стажировка"
try:
    notebook_id = client.create_notebook(title).id
    print(f"Created notebook: {notebook_id}")
    
    files_to_upload = [
        r"C:\ANTIGRAVITY\1\obsidian_brain\2_KNOWLEDGE\Engineering\Specs\Epoxy_Painting_Guide.md",
        r"C:\ANTIGRAVITY\1\obsidian_brain\2_KNOWLEDGE\Engineering\Specs\Valve_DN170_BOM.md",
        r"C:\ANTIGRAVITY\1\obsidian_brain\2_KNOWLEDGE\Engineering\TZ\ZEUS_Main_TZ.md",
        r"C:\ANTIGRAVITY\1\obsidian_brain\2_KNOWLEDGE\ESKD\ESKD_BASIC_GUIDE.md",
        r"C:\ANTIGRAVITY\1\obsidian_brain\2_KNOWLEDGE\GOST_Welding_Comparison.md",
        r"C:\ANTIGRAVITY\1\obsidian_brain\2_KNOWLEDGE\STUDY_GUIDE.md"
    ]
    
    for filepath in files_to_upload:
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            filename = os.path.basename(filepath)
            source_id = client.add_text_source(notebook_id, text=content, title=filename)
            print(f"Uploaded {filename}: {source_id}")
        else:
            print(f"File not found: {filepath}")

except Exception as e:
    print(f"Error: {e}")
