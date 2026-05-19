import sys
# Force utf-8 stdout
sys.stdout.reconfigure(encoding='utf-8')

from notebooklm_mcp.auth import load_cached_tokens
from notebooklm_mcp.api_client import NotebookLMClient

tokens = load_cached_tokens()
client = NotebookLMClient(cookies=tokens.cookies, csrf_token="", session_id="")

notebook_id = "6bb454a4-08f3-4711-83eb-810a2d4f93d7"
try:
    print(f"Deleting notebook {notebook_id}...")
    success = client.delete_notebook(notebook_id)
    print(f"Success: {success}")
except Exception as e:
    print(f"Error deleting notebook: {e}")
