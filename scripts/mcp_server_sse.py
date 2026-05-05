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

# Настройка логирования
logging.basicConfig(level=logging.INFO, filename='mcp_server_sse.log')
logger = logging.getLogger("mcp_server_sse")

load_dotenv(".env.mcp")
KNOWLEDGE_PATH = Path(os.getenv("KNOWLEDGE_PATH", "c:/ANTIGRAVITY/1/obsidian_brain/")).resolve()
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")

app = FastAPI()
mcp_server = Server("Obsidian_Ollama_Hub")
sse = SseServerTransport("/messages")

# [Тут будет та же логика поиска и Ollama, что и в прошлом скрипте]
# (Для краткости я сейчас подготовлю полный файл и запущу его)

@app.get("/sse")
async def sse_endpoint(request: Request):
    async with sse.connect_scope(request.scope, request.receive, request._send):
        await mcp_server.run(
            sse.read_stream(),
            sse.write_stream(),
            mcp_server.create_initialization_options()
        )

@app.post("/messages")
async def messages_endpoint(request: Request):
    await sse.handle_post_request(request.scope, request.receive, request._send)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8765)
