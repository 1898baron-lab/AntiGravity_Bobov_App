import sys
sys.stdout.reconfigure(encoding='utf-8')
from notebooklm_mcp.auth import load_cached_tokens
from notebooklm_mcp.api_client import NotebookLMClient

tokens = load_cached_tokens()
client = NotebookLMClient(cookies=tokens.cookies, csrf_token="", session_id="")

notebooks_to_delete = [
    ("696122f7-8a00-4c54-bb18-7b8a7c2d1ed6", "Сравнение Покраски Автомобиля и Яхты"),
    ("28299e24-dfb8-4e04-866d-332b26188f91", "Технология окраски судов"),
    ("00a054c0-2d9b-4dee-b42c-9b155bc0a779", "Проект EAGLE"),
    ("0c562cb9-6bee-488d-b6a4-9579fa002f80", "Nobilis"),
    ("2bd61c97-204f-4b36-8b8e-8d51671c5dba", "Современная стоматология"),
    ("53bb3da1-d7a9-4d0c-a477-f4619764a38d", "Травяной Микс"),
    ("682efbe5-e66b-4891-9e5c-c0a93546f183", "Телемское Древо"),
    ("a4ffa4f0-280b-42d1-94ef-d1ab04edf8e4", "Еврейская мудрость"),
    ("3bc11a9d-c8c7-4176-8338-f7b2734290f3", "KOMPAS-3D & ESCD Mastery"),
    ("527370ea-666a-4ad2-a345-bfe4b5c1da70", "Махинации с Лицевыми Счетами"),
    ("2a8851db-cac3-4c8f-b227-263d31e91a19", "Arena AI")
]

for nb_id, title in notebooks_to_delete:
    try:
        print(f"Deleting {title} ({nb_id})...")
        success = client.delete_notebook(nb_id)
        print(f"  Success: {success}")
    except Exception as e:
        print(f"  Error: {e}")
