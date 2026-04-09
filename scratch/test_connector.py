import json
import urllib.request

url = "http://127.0.0.1:8765/v1/messages"
data = {
    "messages": [
        {"role": "user", "content": "Это тестовый запрос от AntiGravity. Ответь только одним словом: 'РАБОТАЕТ'"}
    ]
}

req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})

print("Отправка запроса в коннектор...")
try:
    with urllib.request.urlopen(req, timeout=120) as response:
        result = json.loads(response.read().decode('utf-8'))
        print("Ответ получен:")
        print(json.dumps(result, ensure_ascii=False, indent=2))
except Exception as e:
    print(f"Ошибка при тестировании: {e}")
