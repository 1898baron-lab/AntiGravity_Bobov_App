import os
import json
import logging
import asyncio
import urllib.request
import ssl
from typing import List, Optional, Dict
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from mcp.server import Server
from mcp.server.sse import SseServerTransport
from mcp.types import Tool, TextContent

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', filename='mcp_server_sse.log')
logger = logging.getLogger("mcp_server_sse")

load_dotenv(".env.mcp")
OBSIDIAN_API_KEY = os.getenv("OBSIDIAN_API_KEY")
OBSIDIAN_PORT = os.getenv("OBSIDIAN_PORT", "27123")
OBSIDIAN_URL = f"http://localhost:{OBSIDIAN_PORT}"
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")

def obsidian_request(endpoint: str, method: str = "GET", body: dict = None):
    url = f"{OBSIDIAN_URL}{endpoint}"
    headers = {
        "Authorization": f"Bearer {OBSIDIAN_API_KEY}",
        "Content-Type": "application/json"
    }
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        logger.error(f"Obsidian request failed: {e}")
        return None

app = FastAPI()
mcp_server = Server("AntiGravity_Hub")
sse = SseServerTransport("/messages")

@mcp_server.list_tools()
async def list_tools() -> List[Tool]:
    return [
        Tool(name="search_obsidian", description="Search notes via REST API", inputSchema={"type":"object","properties":{"query":{"type":"string"}}}),
        Tool(name="get_note", description="Read note content via API", inputSchema={"type":"object","properties":{"path":{"type":"string"}}}),
        Tool(name="list_vault", description="List all notes in vault", inputSchema={"type":"object","properties":{}}),
        Tool(name="ask_ollama", description="Reasoning via Ollama", inputSchema={"type":"object","properties":{"prompt":{"type":"string"}}})
    ]

@mcp_server.call_tool()
async def call_tool(name: str, arguments: dict) -> List[TextContent]:
    if name == "search_obsidian":
        query = arguments.get("query", "")
        # Используем поиск через API
        res = obsidian_request(f"/search/gui/?query={urllib.parse.quote(query)}")
        return [TextContent(type="text", text=json.dumps(res, indent=2, ensure_ascii=False))]
    
    elif name == "get_note":
        path = arguments.get("path", "")
        if not path.startswith("/"): path = "/" + path
        res = obsidian_request(f"/vault{path}")
        return [TextContent(type="text", text=str(res))]
    
    elif name == "list_vault":
        res = obsidian_request("/vault/")
        return [TextContent(type="text", text=json.dumps(res, indent=2, ensure_ascii=False))]
    
    elif name == "ask_ollama":
        prompt = arguments.get("prompt", "")
        data = {"model": "gemma4:26b-lite", "prompt": prompt, "stream": False}
        req = urllib.request.Request(OLLAMA_URL, data=json.dumps(data).encode(), headers={'Content-Type':'application/json'})
        try:
            with urllib.request.urlopen(req) as resp:
                res = json.loads(resp.read().decode())
                return [TextContent(type="text", text=res.get("response", ""))]
        except Exception as e:
            return [TextContent(type="text", text=f"Ollama error: {e}")]
            
    return []

@app.get("/health")
async def health():
    return {"status": "ok", "engine": "Obsidian REST API", "port": 8766}

@app.get("/sse")
async def sse_endpoint(request: Request):
    async with sse.connect_scope(request.scope, request.receive, request._send):
        await mcp_server.run(sse.read_stream(), sse.write_stream(), mcp_server.create_initialization_options())

@app.post("/messages")
async def messages_endpoint(request: Request):
    await sse.handle_post_request(request.scope, request.receive, request._send)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8766)
