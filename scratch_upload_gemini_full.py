import sys
import os
sys.stdout.reconfigure(encoding='utf-8')
from notebooklm_mcp.auth import load_cached_tokens
from notebooklm_mcp.api_client import NotebookLMClient

tokens = load_cached_tokens()
os.environ['NOTEBOOKLM_AUTHUSER'] = '0'
client = NotebookLMClient(cookies=tokens.cookies, csrf_token="", session_id="")

notebook_id = "fa23a402-6e1b-4f36-8820-5128a4f18f90"

# Get sources and delete old partial version
sources = client.get_notebook_sources_with_types(notebook_id)
print(f"Found {len(sources)} sources in notebook")
for s in sources:
    title = getattr(s, 'title', str(s))
    sid = getattr(s, 'id', None)
    print(f"  - {title} ({sid})")
    if sid and ("Gemini_Chat_Bobov" in title or "Gemini_Chat_Extraction" in title):
        print(f"    -> Deleting old source: {title}")
        client.delete_source(sid)

# Upload the full 31-message version
filepath = r"C:\ANTIGRAVITY\1\obsidian_brain\1_PROJECTS\BOBOV\Gemini_Chat_Full.md"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

print(f"\nUploading full chat ({len(content)} chars, {len(content)//1024} KB)...")
source_id = client.add_text_source(notebook_id, text=content, title="Gemini_Chat_Bobov_FULL_31msg.md")
print(f"Done: {source_id}")
