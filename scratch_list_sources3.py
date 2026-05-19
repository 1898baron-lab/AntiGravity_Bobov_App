import sys
sys.stdout.reconfigure(encoding='utf-8')
from notebooklm_mcp.api_client import NotebookLMClient
from http.cookies import SimpleCookie

cookie_path = r"C:\Users\Sasha  Baron\.gemini\antigravity\brain\6227f2d7-5238-4357-8df0-f38c9d71d49f\scratch\cookies_b.txt"
with open(cookie_path, 'r', encoding='utf-8') as f:
    raw_cookies = f.read().strip()

cookie_obj = SimpleCookie()
cookie_obj.load(raw_cookies)
cookies = {k: v.value for k, v in cookie_obj.items()}

client = NotebookLMClient(cookies=cookies, csrf_token="", session_id="")

nb_id = "9fc75b2e-bebc-42dc-b07f-3520e48156fb"
try:
    sources = client.get_notebook_sources_with_types(nb_id)
    print("Sources:")
    for src in sources:
        print(f"- {src['title']} ({src['type']})")
except Exception as e:
    print(f"Error: {e}")
