from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import httpx

app = FastAPI()

@app.post("/v1/messages")
async def proxy(request: Request):
    body = await request.json()
    messages = []
    for m in body.get("messages", []):
        content = m["content"]
        if isinstance(content, list):
            text = " ".join(c.get("text","") for c in content if c.get("type")=="text")
        else:
            text = content
        messages.append({"role": m["role"], "content": text})
    
    ollama_payload = {
        "model": "gemma4:26b-lite",
        "messages": messages,
        "stream": False
    }
    async with httpx.AsyncClient(timeout=120) as client:
        r = await client.post("http://localhost:11434/api/chat", json=ollama_payload)
        data = r.json()
    
    text = data.get("message", {}).get("content", "")
    
    return JSONResponse({
        "id": "msg_local_001",
        "type": "message",
        "role": "assistant",
        "model": "gemma4:26b-lite",
        "content": [{"type": "text", "text": text}],
        "stop_reason": "end_turn",
        "stop_sequence": None,
        "usage": {"input_tokens": 10, "output_tokens": 10}
    })