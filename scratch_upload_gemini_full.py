import sys
import os
sys.stdout.reconfigure(encoding='utf-8')
from notebooklm_mcp.auth import load_cached_tokens
from notebooklm_mcp.api_client import NotebookLMClient

tokens = load_cached_tokens()
os.environ['NOTEBOOKLM_AUTHUSER'] = '0'
client = NotebookLMClient(cookies=tokens.cookies, csrf_token="", session_id="")

# Find the Bobov notebook
notebook_id = None
nbs = client.list_notebooks()
for nb in nbs:
    if "Бобова" in nb.title or "Bobov" in nb.title:
        notebook_id = nb.id
        print(f"Found notebook: {nb.title} -> {nb.id}")
        break

if not notebook_id:
    print("ERROR: Bobov notebook not found.")
    sys.exit(1)

# Delete old partial version first
sources = client.list_sources(notebook_id)
for s in sources:
    if "Gemini_Chat_Bobov" in s.title or "Gemini_Chat_Extraction" in s.title:
        print(f"Deleting old source: {s.title} ({s.id})")
        client.delete_source(s.id)

# Upload the full 31-message version
filepath = r"C:\ANTIGRAVITY\1\obsidian_brain\1_PROJECTS\BOBOV\Gemini_Chat_Full.md"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

source_id = client.add_text_source(notebook_id, text=content, title="Gemini_Chat_Bobov_FULL_31msg.md")
print(f"Uploaded full chat ({len(content)} chars): {source_id}")
