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

try:
    nbs = client.list_notebooks()
    for nb in nbs:
        print(f"- {nb.title} ({nb.id})")
except Exception as e:
    print(f"Error: {e}")
