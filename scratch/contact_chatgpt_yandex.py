import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

url = "http://localhost:8001/v1/messages"

payload = {
    "messages": [
        {"role": "user", "content": "Привет! Я Antigravity. Кирилл просил меня связаться с тобой именно через Яндекс Браузер. Подтверди, что ты меня видишь и готов к работе в составе нашей ИИ-фабрики Mastodont."}
    ]
}

try:
    print(f"Connecting to ChatGPT Yandex Connector at {url}...")
    response = requests.post(url, json=payload, timeout=300)
    if response.status_code == 200:
        data = response.json()
        text = data["content"][0]["text"]
        print("--- RESPONSE FROM CHATGPT (YANDEX) ---")
        print(text)
        print("---------------------------------------")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"Critical Error: {e}")
