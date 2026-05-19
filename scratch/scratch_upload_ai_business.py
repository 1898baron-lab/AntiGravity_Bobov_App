import sys, os
sys.stdout.reconfigure(encoding='utf-8')
from notebooklm_mcp.auth import load_cached_tokens
from notebooklm_mcp.api_client import NotebookLMClient

tokens = load_cached_tokens()
os.environ['NOTEBOOKLM_AUTHUSER'] = '0'
client = NotebookLMClient(cookies=tokens.cookies, csrf_token="", session_id="")

notebook_id = "a614a4d2-a3d5-489b-974c-5c285dcf55f9"

# 1. Загружаем структурированный разбор
filepath_struct = r"C:\ANTIGRAVITY\1\obsidian_brain\2_KNOWLEDGE\AI_Business\AI_Business_Strategy_2026.md"
with open(filepath_struct, 'r', encoding='utf-8') as f:
    struct_content = f.read()
res1 = client.add_text_source(notebook_id, text=struct_content, title="AI_Business_Strategy_2026.md")
print(f"✅ Загружен структурированный разбор: {res1}")

# 2. Загружаем оригинальную статью Teletype
filepath_orig = r"C:\Users\Sasha  Baron\.gemini\antigravity\brain\6227f2d7-5238-4357-8df0-f38c9d71d49f\.system_generated\steps\3581\content.md"
with open(filepath_orig, 'r', encoding='utf-8') as f:
    orig_content = f.read()
res2 = client.add_text_source(notebook_id, text=orig_content, title="Teletype_Original_Article_100k.md")
print(f"✅ Загружен первоисточник статьи: {res2}")
