import os
import json
import logging
import asyncio
import urllib.request
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
KNOWLEDGE_PATH = Path(os.getenv("KNOWLEDGE_PATH", "c:/ANTIGRAVITY/1/obsidian_brain/")).resolve()
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")

class KnowledgeStore:
    def __init__(self, path: Path):
        self.path = path
        self.cache: Dict[str, str] = {}
        self.load_cache()

    def load_cache(self):
        if not self.path.exists(): return
        for file in self.path.rglob("*.md"):
            try:
                if any(part.startswith(".") or part.startswith("_") for part in file.parts): continue
                rel_path = str(file.relative_to(self.path))
                self.cache[rel_path] = file.read_text(encoding="utf-8")
            except: pass

    def search(self, query: str) -> List[Dict]:
        query = query.lower()
        results = []
        for path, content in self.cache.items():
            if query in content.lower() or query in path.lower():
                preview = content[:200].replace("\n", " ") + "..."
                results.append({"path": path, "preview": preview})
        return results[:10]

store = KnowledgeStore(KNOWLEDGE_PATH)
app = FastAPI()
mcp_server = Server("Obsidian_Ollama_Hub")
sse = SseServerTransport("/messages")

@mcp_server.list_tools()
async def list_tools() -> List[Tool]:
    return [
        Tool(name="search_obsidian", description="Search Obsidian notes", inputSchema={"type":"object","properties":{"query":{"type":"string"}}}),
        Tool(name="fetch_obsidian_doc", description="Read note content", inputSchema={"type":"object","properties":{"path":{"type":"string"}}}),
        Tool(name="ask_ollama", description="Deep reasoning via Ollama", inputSchema={"type":"object","properties":{"prompt":{"type":"string"}}})
    ]

@mcp_server.call_tool()
async def call_tool(name: str, arguments: dict) -> List[TextContent]:
    if name == "search_obsidian":
        res = store.search(arguments.get("query", ""))
        return [TextContent(type="text", text=json.dumps(res, indent=2, ensure_ascii=False))]
    elif name == "fetch_obsidian_doc":
        path = arguments.get("path", "")
        content = store.cache.get(path, "File not found")
        return [TextContent(type="text", text=content[:10000])]
    elif name == "ask_ollama":
        prompt = arguments.get("prompt", "")
        data = {"model": "deepseek-r1:8b", "prompt": prompt, "stream": False}
        req = urllib.request.Request(OLLAMA_URL, data=json.dumps(data).encode(), headers={'Content-Type':'application/json'})
        with urllib.request.urlopen(req) as resp:
            res = json.loads(resp.read().decode())
            return [TextContent(type="text", text=res.get("response", ""))]
    return []

@app.get("/sse")
async def sse_endpoint(request: Request):
    async with sse.connect_scope(request.scope, request.receive, request._send):
        await mcp_server.run(sse.read_stream(), sse.write_stream(), mcp_server.create_initialization_options())

@app.post("/messages")
async def messages_endpoint(request: Request):
    await sse.handle_post_request(request.scope, request.receive, request._send)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8765)
