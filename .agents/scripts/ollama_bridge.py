import requests
import json
import os

def ask_ollama(prompt, model="gemma4:latest"):
    url = "http://localhost:11434/api/generate"
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            return response.json().get('response', 'No response')
        else:
            return f"Error: {response.status_code}"
    except Exception as e:
        return f"Connection failed: {str(e)}"

# Запрос: Идеи для монетизации бренда MASTODONT
prompt = """
Ты — старший AI-предприниматель. Бренд MASTODONT занимается производством премиальных мангалов и систем автоматизации.
Предложи 3 инновационные идеи для монетизации, используя ИИ и лазерную резку.
"""

advice = ask_ollama(prompt)

output_path = r'C:\ANTIGRAVITY\1\obsidian_brain\1_PROJECTS\MANGAL\OLLAMA_ADVICE.md'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(f"# AI Консультация (Ollama)\n\n## Запрос:\n{prompt}\n\n## Ответ:\n{advice}")

print(f"Advice saved to {output_path}")
