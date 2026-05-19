import os
import json
import time
import requests

NOTEBOOKS = {
    "НТД": "abebf3ce-8e1b-4826-83eb-1d59cee4b922",
    "ЕСКД": "af428a9c-b714-45bc-bf47-87a7defb6e8c",
    "Учебные": "85cc6feb-be41-4d40-a063-5103fc7643a6",
    "Личные": "1d66e347-7703-47c4-86df-105481676d19"
}

MAPPING = {
    "НТД_Сводка.txt": "НТД",
    "ЕСКД_Сводка.txt": "ЕСКД",
    "ТК_Сводка.txt": "ЕСКД",
    "Рабочие программы дисциплин_Сводка.txt": "Учебные",
    "Рабочие программы практик_Сводка.txt": "Учебные",
    "Корневые_документы_Сводка.txt": "Учебные"
}

SOURCE_DIR = r"C:\ANTIGRAVITY\1\obsidian_brain\1_PROJECTS\Downloads_GDrive_Parsed"
CHUNK_SIZE = 400_000

def main():
    print("Подключаемся к локальному SSE серверу...")
    # 1. Получаем SSE сессию
    try:
        # Мы просто сделаем stream запрос чтобы получить endpoint
        resp = requests.get("http://127.0.0.1:8766/sse", stream=True)
        post_endpoint = None
        for line in resp.iter_lines():
            if line:
                decoded = line.decode('utf-8')
                if decoded.startswith("event: endpoint"):
                    # Следующая строка будет data
                    continue
                if decoded.startswith("data: "):
                    post_endpoint = decoded[6:]
                    break
    except Exception as e:
        print("Ошибка подключения к SSE:", e)
        return

    if not post_endpoint:
        print("Не удалось получить post_endpoint")
        return
        
    print(f"Получен endpoint: {post_endpoint}")
    
    # 2. Теперь можем постить JSON-RPC
    if post_endpoint.startswith("/"):
        post_url = f"http://127.0.0.1:8766{post_endpoint}"
    else:
        post_url = post_endpoint
        
    req_id = 1
    for file in os.listdir(SOURCE_DIR):
        if not file.endswith(".txt"):
            continue
            
        target_notebook_key = MAPPING.get(file, "Личные")
        notebook_id = NOTEBOOKS[target_notebook_key]
        filepath = os.path.join(SOURCE_DIR, file)
        
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
        except:
            continue
            
        if not content.strip():
            continue
            
        print(f"[{target_notebook_key}] Загрузка {file} (размер {len(content)} симв.)...")
        chunks = [content[i:i+CHUNK_SIZE] for i in range(0, len(content), CHUNK_SIZE)]
        
        for idx, chunk in enumerate(chunks):
            title = file.replace(".txt", "")
            if len(chunks) > 1:
                title += f" (Часть {idx+1})"
                
            req = {
                "jsonrpc": "2.0",
                "id": req_id,
                "method": "tools/call",
                "params": {
                    "name": "notebooklm_notebook_add_text",
                    "arguments": {
                        "notebook_id": notebook_id,
                        "title": title,
                        "text": chunk
                    }
                }
            }
            
            try:
                # Отправляем в фоне
                post_resp = requests.post(post_url, json=req)
                print(f"  -> {title} отправлен. Статус: {post_resp.status_code}")
            except Exception as e:
                print(f"  -> ОШИБКА загрузки {title}: {e}")
                
            req_id += 1
            time.sleep(3) # Пауза чтобы NotebookLM не забанил за Rate Limit
            
    print("Вся загрузка завершена!")

if __name__ == "__main__":
    main()
