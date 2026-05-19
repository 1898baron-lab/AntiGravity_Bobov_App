import sys
import os
sys.stdout.reconfigure(encoding='utf-8')
from notebooklm_mcp.auth import load_cached_tokens
from notebooklm_mcp.api_client import NotebookLMClient

tokens = load_cached_tokens()
os.environ['NOTEBOOKLM_AUTHUSER'] = '0'
client = NotebookLMClient(cookies=tokens.cookies, csrf_token="", session_id="")

try:
    nbs = client.list_notebooks()
    for nb in nbs:
        if nb.title in [
            "Копилка слов благодарности и идей для выпускного",
            "Arena AI",
            "NotebookLM Получил НОВУЮ Суперсилу (AntiGravity)",
            "Russian Nuclear Fuel Cycle Safety Standards and Regulations",
            "Махинации с Лицевыми Счетами: Обман Матвиенко, Набиуллиной и Миллера",
            "Промпт Инжиниринг: Курс Алексея Хнова"
        ]:
            print(f"Deleting notebook on Account A: {nb.title} ({nb.id})")
            client.delete_notebook(nb.id)
except Exception as e:
    print(f"Error: {e}")
