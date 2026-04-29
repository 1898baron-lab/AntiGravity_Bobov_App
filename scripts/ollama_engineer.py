import urllib.request
import json
import sys

def ask_ollama(prompt, model="gemma4:26b"):
    url = "http://localhost:11434/api/generate"
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    
    # Ensure UTF-8 encoding for Russian text
    req = urllib.request.Request(
        url, 
        data=json.dumps(data).encode('utf-8'),
        headers={'Content-Type': 'application/json; charset=utf-8'}
    )
    
    print(f"Отправляю запрос локальной модели {model}...")
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            print("\n=== Ответ Ollama ===")
            print(result.get("response", "Нет ответа"))
            print("====================")
    except Exception as e:
        print(f"Ошибка подключения к Ollama: {e}")

if __name__ == "__main__":
    prompt = """
    Ты - опытный инженер-конструктор. Мы проектируем казан-мангал.
    Нам нужно изменить конструкцию: вместо квадратной печи (300х300) мы делаем 
    цилиндрическую печь из вальцованного листа.
    Опиши, как правильно соединить цилиндрическую печь с прямоугольным коробом мангала.
    Какую толщину металла выбрать для цилиндра? Отвечай кратко и по делу.
    """
    ask_ollama(prompt)
