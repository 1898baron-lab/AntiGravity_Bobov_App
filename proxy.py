from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import httpx, json, asyncio

app = FastAPI()

@app.post("/v1/messages")
async def proxy(request: Request):
    body = await request.json()
    messages = [{"role": m["role"], "content": m["content"]} for m in body.get("messages", [])]
    ollama_payload = {
        "model": "gemma4:26b-lite",
        "messages": messages,
        "stream": False
    }
    async with httpx.AsyncClient(timeout=120) as client:
        r = await client.post("http://localhost:11434/api/chat", json=ollama_payload)
        data = r.json()
        text = data.get("message", {}).get("content", "")
    return {
        "id": "msg_local",
        "type": "message",
        "role": "assistant",
        "content": [{"type": "text", "text": text}],
        "model": "gemma4:26b-lite",
        "stop_reason": "end_turn",
        "usage": {"input_tokens": 0, "output_tokens": 0}
    }