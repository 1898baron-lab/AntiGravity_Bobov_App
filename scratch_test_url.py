import os
import sys

# Force utf-8 stdout
sys.stdout.reconfigure(encoding='utf-8')

from notebooklm_mcp.auth import load_cached_tokens
from notebooklm_mcp.api_client import NotebookLMClient

tokens = load_cached_tokens()

os.environ['NOTEBOOKLM_AUTHUSER'] = '1'
client = NotebookLMClient(cookies=tokens.cookies, csrf_token="", session_id="")

# Print the URL for list notebooks
url = client._build_url(client.RPC_LIST_NOTEBOOKS)
print("URL:", url)

# Let's also check if "authuser" is in the url
print("authuser in url:", "authuser" in url)
