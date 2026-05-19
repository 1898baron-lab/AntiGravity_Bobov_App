import sys
import os
sys.stdout.reconfigure(encoding='utf-8')
from notebooklm_mcp.auth import load_cached_tokens
from notebooklm_mcp.api_client import NotebookLMClient

tokens = load_cached_tokens()
os.environ['NOTEBOOKLM_AUTHUSER'] = '1'
client = NotebookLMClient(cookies=tokens.cookies, csrf_token="", session_id="")

try:
    nbs = client.list_notebooks()
    for nb in nbs:
        print(f"Deleting notebook on Account B: {nb.title} ({nb.id})")
        client.delete_notebook(nb.id)
except Exception as e:
    print(f"Error: {e}")
