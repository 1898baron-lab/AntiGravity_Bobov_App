import requests
import json

url = "http://127.0.0.1:8001/v1/messages"
payload = {
    "messages": [{"content": "Выдай финальную спецификацию и чертеж узла стыковки модулей мангала (800+300мм) в формате, подходящем для КМД."}],
    "chat_url": "https://chatgpt.com/g/g-68a38fb191b081918f4984b1a9261f02-uluchshatel-rait/c/69f19120-e2b4-83eb-926a-12ef90559b6f"
}

response = requests.post(url, json=payload)
data = response.json()

with open("C:/ANTIGRAVITY/1/scratch/wright_final_specification.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
