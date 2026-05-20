from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import httpx, json

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
            text = str(content)
        messages.append({"role": m["role"], "content": text})

    ollama_payload = {"model": "gemma4:26b-lite", "messages": messages, "stream": False}

    async with httpx.AsyncClient(timeout=120) as client:
        r = await client.post("http://localhost:11434/api/chat", json=ollama_payload)
        text = r.json().get("message", {}).get("content", "")

    def stream():
        yield "event: message_start\ndata: " + json.dumps({
            "type":"message_start","message":{"id":"msg_1","type":"message",
            "role":"assistant","content":[],"model":"gemma4:26b-lite",
            "stop_reason":None,"usage":{"input_tokens":10,"output_tokens":0}}}) + "\n\n"
        yield "event: content_block_start\ndata: " + json.dumps({
            "type":"content_block_start","index":0,
            "content_block":{"type":"text","text":""}}) + "\n\n"
        yield "event: content_block_delta\ndata: " + json.dumps({
            "type":"content_block_delta","index":0,
            "delta":{"type":"text_delta","text":text}}) + "\n\n"
        yield "event: content_block_stop\ndata: " + json.dumps({
            "type":"content_block_stop","index":0}) + "\n\n"
        yield "event: message_delta\ndata: " + json.dumps({
            "type":"message_delta","delta":{"stop_reason":"end_turn"},
            "usage":{"output_tokens":10}}) + "\n\n"
        yield "event: message_stop\ndata: " + json.dumps({"type":"message_stop"}) + "\n\n"

    return StreamingResponse(stream(), media_type="text/event-stream")