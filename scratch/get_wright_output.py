import requests
import json

url = "http://127.0.0.1:8001/v1/messages"
payload = {
    "messages": [{"content": "Рома Райт, используя свою методику, улучши этот промпт для генерации инженерного чертежа узла стыковки модулей мангала (800+300мм). Нам нужен чертеж фланцевого соединения на болтах М8 с учетом ТТ по ГОСТ. Выдай готовый текст промпта."}],
    "chat_url": "https://chatgpt.com/c/69eb9a94-782c-83eb-bfd2-c3dc8db5c4c8"
}

print("Sending request to ChatGPT via BOM...")
response = requests.post(url, json=payload)
data = response.json()

with open("C:/ANTIGRAVITY/1/scratch/chatgpt_wright_output.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("Output saved to scratch/chatgpt_wright_output.json")
