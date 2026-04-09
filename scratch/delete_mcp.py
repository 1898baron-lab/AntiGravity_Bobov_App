import json
import subprocess
import time

def delete_sources_via_mcp():
    with open(r'C:\Users\Sasha  Baron\.gemini\antigravity\brain\d5aff1b7-bbe0-4705-b6f2-28739211f178\scratch\video_ids.json', 'r', encoding='utf-8') as f:
        videos = json.load(f)

    # Start notebooklm-mcp process
    process = subprocess.Popen(
        ['notebooklm-mcp'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding='utf-8',
        bufsize=1
    )

    # Initialize MCP
    init_req = {
        "jsonrpc": "2.0",
        "id": 0,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "test", "version": "1.0"}
        }
    }
    
    process.stdin.write(json.dumps(init_req) + '\n')
    process.stdin.flush()
    init_resp = process.stdout.readline()
    process.stdin.write(json.dumps({"jsonrpc":"2.0","method":"notifications/initialized"}) + '\n')
    process.stdin.flush()

    # Delete loop
    for i, v in enumerate(videos, start=1):
        req = {
            "jsonrpc": "2.0",
            "id": i,
            "method": "tools/call",
            "params": {
                "name": "source_delete",
                "arguments": {
                    "source_id": v['id'],
                    "confirm": True
                }
            }
        }
        process.stdin.write(json.dumps(req) + '\n')
        process.stdin.flush()
        
        while True:
            line = process.stdout.readline()
            if not line: break
            try:
                resp = json.loads(line)
                if resp.get('id') == i:
                    print(f"Deleted {v['title']} ({v['id']}):", "success" if not resp.get("isError") else "FAILED")
                    break
            except:
                pass

    process.kill()

if __name__ == "__main__":
    delete_sources_via_mcp()
