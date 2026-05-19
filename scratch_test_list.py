import os
import sys

# Force utf-8 stdout
sys.stdout.reconfigure(encoding='utf-8')

from notebooklm_mcp.auth import load_cached_tokens
from notebooklm_mcp.api_client import NotebookLMClient

tokens = load_cached_tokens()
os.environ['NOTEBOOKLM_AUTHUSER'] = '0'
client = NotebookLMClient(cookies=tokens.cookies, csrf_token="", session_id="")

nbs = client.list_notebooks()
print('Authuser 0 count:', len(nbs))
for nb in nbs:
    print(f'- {nb.title} ({nb.id})')
