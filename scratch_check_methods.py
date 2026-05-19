import sys
import os
sys.stdout.reconfigure(encoding='utf-8')
from notebooklm_mcp.auth import load_cached_tokens
from notebooklm_mcp.api_client import NotebookLMClient

tokens = load_cached_tokens()
os.environ['NOTEBOOKLM_AUTHUSER'] = '0'
client = NotebookLMClient(cookies=tokens.cookies, csrf_token="", session_id="")

notebook_id = "fa23a402-6e1b-4f36-8820-5128a4f18f90"

# Check available methods
methods = [m for m in dir(client) if not m.startswith('_')]
print("Available methods:", methods)
