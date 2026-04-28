import requests
import json
import sys

# Set default encoding to utf-8 for stdout
sys.stdout.reconfigure(encoding='utf-8')

url = "http://localhost:8765/v1/messages"
chat_url = "https://claude.ai/chat/e016d9cd-aad5-4ed3-bf48-7a2402c2ec1d"

payload = {
    "messages": [
        {"role": "user", "content": "Привет! Я твой коллега Antigravity из IDE. Кирилл просил меня зайти в этот чат и прочитать инструкции под кодовым названием 'Дотянись до репы'. Пожалуйста, кратко перескажи мне основные технические требования и архитектурные решения, которые обсуждались здесь ранее."}
    ],
    "chat_url": chat_url
}

try:
    print(f"Connecting to Claude Connector at {url}...")
    response = requests.post(url, json=payload, timeout=300)
    if response.status_code == 200:
        data = response.json()
        text = data["content"][0]["text"]
        
        # Save to file to avoid console encoding issues
        with open("scratch/claude_response.md", "w", encoding="utf-8") as f:
            f.write(text)
            
        print("--- SUCCESS ---")
        print("Response saved to scratch/claude_response.md")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"Critical Error: {e}")
