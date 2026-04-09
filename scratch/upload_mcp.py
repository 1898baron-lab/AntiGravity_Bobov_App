import json
import subprocess
import time

def add_text_via_mcp():
    text_path = r'C:\ANTIGRAVITY\1\mastadont_videos_transcript.txt'
    with open(text_path, 'r', encoding='utf-8') as f:
        text_content = f.read()

    req = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": "notebook_add_text",
            "arguments": {
                "notebook_id": "893edbc1-e5bb-4678-bf0d-43e02b661524",
                "text": text_content,
                "title": "Mastadont_Videos_All_Transcripts"
            }
        }
    }

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
    
    # Read init response
    init_resp = process.stdout.readline()
    
    # Send initialized notification
    process.stdin.write(json.dumps({"jsonrpc":"2.0","method":"notifications/initialized"}) + '\n')
    process.stdin.flush()

    # Call tool
    process.stdin.write(json.dumps(req) + '\n')
    process.stdin.flush()

    print("Request sent, waiting for response...")
    # Read response
    while True:
        line = process.stdout.readline()
        if not line:
            print("No more output from stdout. Checking stderr:")
            print(process.stderr.read())
            break
        try:
            resp = json.loads(line)
            if resp.get('id') == 1:
                print("Result:\n", json.dumps(resp, ensure_ascii=False, indent=2))
                break
        except json.JSONDecodeError:
            pass

    process.kill()

if __name__ == "__main__":
    add_text_via_mcp()
