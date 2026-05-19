import os
import json
import subprocess
import time

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
CHUNK_SIZE = 400_000  # 400k символов на один кусок, чтобы не превысить лимиты NotebookLM

def send_rpc(proc, req_dict):
    req_str = json.dumps(req_dict) + "\n"
    proc.stdin.write(req_str.encode('utf-8'))
    proc.stdin.flush()
    
    # Ждем ответа
    while True:
        line = proc.stdout.readline()
        if not line:
            return None
        line_str = line.decode('utf-8').strip()
        if not line_str:
            continue
        try:
            resp = json.loads(line_str)
            if "id" in resp and resp["id"] == req_dict.get("id"):
                return resp
        except:
            pass

def main():
    print("Запускаем локальный MCP-сервер NotebookLM...")
    proc = subprocess.Popen(
        [r"C:\ANTIGRAVITY\1\.venv\Scripts\python.exe", "-m", "notebooklm_mcp"], 
        stdin=subprocess.PIPE, 
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # 1. Initialize
    print("Инициализация MCP...")
    init_req = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "upload_script", "version": "1.0.0"}
        }
    }
    send_rpc(proc, init_req)
    
    proc.stdin.write((json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized"}) + "\n").encode('utf-8'))
    try:
        proc.stdin.flush()
    except Exception as e:
        print("Ошибка при записи в stdin:", e)
        print("STDERR:")
        print(proc.stderr.read().decode('utf-8', errors='ignore'))
        return
        
    time.sleep(2)
    
    # 2. Загрузка файлов
    req_id = 2
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
        
        # Разбиваем на куски
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
            
            resp = send_rpc(proc, req)
            if resp and "error" not in resp:
                print(f"  -> {title} загружено успешно!")
            else:
                print(f"  -> ОШИБКА загрузки {title}: {resp}")
            req_id += 1
            time.sleep(2) # Пауза чтобы не спамить API Google
            
    proc.terminate()
    print("Вся загрузка завершена!")

if __name__ == "__main__":
    main()
