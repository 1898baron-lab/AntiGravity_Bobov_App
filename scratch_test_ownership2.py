import os
import sys

# Force utf-8 stdout
sys.stdout.reconfigure(encoding='utf-8')

from notebooklm_mcp.auth import load_cached_tokens
from notebooklm_mcp.api_client import NotebookLMClient

tokens = load_cached_tokens()

print("\n--- Testing Authuser 0 (Account A) ---")
os.environ['NOTEBOOKLM_AUTHUSER'] = '0'
client = NotebookLMClient(cookies=tokens.cookies, csrf_token="", session_id="")
nbs = client.list_notebooks()
for nb in nbs:
    if "Копилка" in nb.title or "КОМПАС" in nb.title:
        print(f'- {nb.title} (Owned: {nb.is_owned}, Shared: {nb.is_shared})')

print("\n--- Testing Authuser 1 (Account B) ---")
os.environ['NOTEBOOKLM_AUTHUSER'] = '1'
client2 = NotebookLMClient(cookies=tokens.cookies, csrf_token="", session_id="")
nbs2 = client2.list_notebooks()
for nb in nbs2:
    if "Копилка" in nb.title or "КОМПАС" in nb.title:
        print(f'- {nb.title} (Owned: {nb.is_owned}, Shared: {nb.is_shared})')
