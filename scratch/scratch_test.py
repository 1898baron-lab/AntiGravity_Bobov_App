import os
import sys

# Force utf-8 stdout
sys.stdout.reconfigure(encoding='utf-8')

from notebooklm_mcp.auth import load_cached_tokens
from notebooklm_mcp.api_client import NotebookLMClient

tokens = load_cached_tokens()
print('Tokens loaded:', tokens is not None)

print("\n--- Testing Authuser 0 (Account A) ---")
os.environ['NOTEBOOKLM_AUTHUSER'] = '0'
client2 = NotebookLMClient(cookies=tokens.cookies, csrf_token="", session_id="")
# Hack the HTTP client headers
client2._get_client().headers["X-Goog-AuthUser"] = "0"

try:
    nbs2 = client2.list_notebooks()
    print('Authuser 0 count:', len(nbs2))
    for nb in nbs2[:3]:
        print(f'- {nb.title}')
except Exception as e:
    print('Error:', e)

print("\n--- Testing Authuser 1 (Account B) ---")
os.environ['NOTEBOOKLM_AUTHUSER'] = '1'
client = NotebookLMClient(cookies=tokens.cookies, csrf_token="", session_id="")
# Hack the HTTP client headers
client._get_client().headers["X-Goog-AuthUser"] = "1"

try:
    nbs = client.list_notebooks()
    print('Authuser 1 count:', len(nbs))
    for nb in nbs[:3]:
        print(f'- {nb.title}')
except Exception as e:
    print('Error:', e)
