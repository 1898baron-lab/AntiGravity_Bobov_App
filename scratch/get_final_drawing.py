import requests
import json

url = "http://127.0.0.1:8001/v1/messages"
improved_prompt = "Сгенерируй финальный инженерный чертеж согласно твоему улучшенному ТЗ: Узел стыковки модулей 800 и 300 мм, фланцевое соединение, болты М8, ГОСТ, ЕСКД. Покажи детальный вид соединения в разрезе."
payload = {
    "messages": [{"content": improved_prompt}],
    "chat_url": "https://chatgpt.com/c/69eb9a94-782c-83eb-bfd2-c3dc8db5c4c8"
}

print("Requesting final drawing from ChatGPT via BOM...")
response = requests.post(url, json=payload)
data = response.json()

with open("C:/ANTIGRAVITY/1/scratch/chatgpt_final_drawing.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("Final response saved to scratch/chatgpt_final_drawing.json")
