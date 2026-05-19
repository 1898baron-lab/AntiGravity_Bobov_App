import sys, os
sys.stdout.reconfigure(encoding='utf-8')
from notebooklm_mcp.auth import load_cached_tokens
from notebooklm_mcp.api_client import NotebookLMClient

tokens = load_cached_tokens()
os.environ['NOTEBOOKLM_AUTHUSER'] = '0'
client = NotebookLMClient(cookies=tokens.cookies, csrf_token="", session_id="")

notebook_id = "fa23a402-6e1b-4f36-8820-5128a4f18f90"

# Get sources, find and delete old CAREER_PATH_BOBOV
sources = client.get_notebook_sources_with_types(notebook_id)
for s in sources:
    title = s.get('title', '') if isinstance(s, dict) else getattr(s, 'title', '')
    sid = s.get('id', '') if isinstance(s, dict) else getattr(s, 'id', '')
    if 'CAREER_PATH_BOBOV' in title and sid:
        print(f"Удаляю старый: {title}")
        client.delete_source(sid)

# Upload updated v3.0
filepath = r"C:\ANTIGRAVITY\1\obsidian_brain\2_KNOWLEDGE\Legal_Tactics\CAREER_PATH_BOBOV.md"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

result = client.add_text_source(notebook_id, text=content, title="CAREER_PATH_BOBOV_v3.md")
print(f"✅ Загружен v3.0: {result}")
