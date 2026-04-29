import requests
import json

url = "http://127.0.0.1:8001/v1/messages"
payload = {
    "messages": [{"content": "Привет, Улучшатель Райт! Мы проектируем модульный мангал. Помоги составить финальное техническое задание для деталировки узла стыковки двух модулей (основной 800мм и печной 300мм). Учти ГОСТ и требования Росатома к качеству швов и соединений."}],
    "chat_url": "https://chatgpt.com/g/g-68a38fb191b081918f4984b1a9261f02-uluchshatel-rait"
}

response = requests.post(url, json=payload)
data = response.json()

with open("C:/ANTIGRAVITY/1/scratch/wright_final_mangal_tz.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
