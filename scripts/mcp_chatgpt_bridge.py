import os
import json
import logging
from typing import List, Optional
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import JSONResponse
from mcp.server import Server
from mcp.server.sse import SseServerTransport
from mcp.types import Tool, TextContent

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mcp_chatgpt_bridge")

# Загрузка переменных окружения
load_dotenv(".env.mcp")
TOKEN = os.getenv("CHATGPT_MCP_TOKEN", "mastodont_secret_2026")
KNOWLEDGE_PATH = Path(os.getenv("KNOWLEDGE_PATH", "c:/ANTIGRAVITY/1/knowledge/")).resolve()

# Инициализация MCP сервера
mcp_server = Server("mastodont-knowledge")
sse = SseServerTransport("/messages")

@mcp_server.list_tools()
async def list_tools() -> List[Tool]:
    """Список инструментов для ChatGPT."""
    return [
        Tool(
            name="search_knowledge",
            description="Поиск по инженерной базе знаний и регламентам ЦПТИ/Росатом. Используйте для поиска ГОСТов, ТТ и правил проектирования.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Поисковый запрос (ключевые слова)"}
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="fetch_document",
            description="Получение полного содержания документа из базы знаний. Путь (id) должен быть получен из результатов поиска.",
            inputSchema={
                "type": "object",
                "properties": {
                    "id": {"type": "string", "description": "Путь к файлу или ID документа"}
                },
                "required": ["id"]
            }
        )
    ]

@mcp_server.call_tool()
async def call_tool(name: str, arguments: dict) -> List[TextContent]:
    """Вызов инструментов."""
    if name == "search_knowledge":
        query = arguments.get("query", "").lower()
        results = []
        for file in KNOWLEDGE_PATH.rglob("*.md"):
            try:
                content = file.read_text(encoding="utf-8")
                if query in content.lower() or query in file.name.lower():
                    summary = content[:200].replace("\n", " ") + "..."
                    results.append({
                        "id": str(file.relative_to(KNOWLEDGE_PATH)),
                        "title": file.name,
                        "url": f"https://local-resource/{file.name}",
                        "snippet": summary
                    })
            except Exception as e:
                logger.error(f"Error reading {file}: {e}")
        
        response_data = {"results": results[:10]}
        return [TextContent(type="text", text=json.dumps(response_data, ensure_ascii=False))]

    elif name == "fetch_document":
        doc_id = arguments.get("id", "")
        file_path = (KNOWLEDGE_PATH / doc_id).resolve()
        
        if not str(file_path).startswith(str(KNOWLEDGE_PATH)):
            raise ValueError("Access Denied")
            
        if not file_path.exists():
            return [TextContent(type="text", text="Ошибка: Документ не найден.")]
            
        try:
            content = file_path.read_text(encoding="utf-8")
            fetch_data = {
                "id": doc_id,
                "title": file_path.name,
                "text": content,
                "url": f"https://local-resource/{doc_id}"
            }
            return [TextContent(type="text", text=json.dumps(fetch_data, ensure_ascii=False))]
        except Exception as e:
            return [TextContent(type="text", text=f"Ошибка чтения: {str(e)}")]

    else:
        raise ValueError(f"Unknown tool: {name}")

# Создание FastAPI приложения
app = FastAPI(title="Mastodont ChatGPT Bridge")

@app.get("/health")
async def health():
    """Проверка состояния сервера."""
    return {"status": "ok", "server": "Mastodont MCP Bridge", "version": "1.0.0"}

@app.get("/sse")
async def handle_sse(request: Request):
    """Подключение по SSE."""
    logger.info("New SSE connection established")
    async with sse.connect_sse(request.scope, request.receive, request._send) as (read_stream, write_stream):
        await mcp_server.run(read_stream, write_stream, mcp_server.create_initialization_options())

@app.post("/messages")
async def handle_messages(request: Request):
    """Обработка входящих сообщений."""
    logger.info("Processing post message from client")
    return await sse.handle_post_message(request.scope, request.receive, request._send)

# Middleware для проверки токена
@app.middleware("http")
async def check_auth(request: Request, call_next):
    # ChatGPT может присылать токен в Authorization заголовке
    auth_header = request.headers.get("Authorization")
    if auth_header != f"Bearer {TOKEN}" and request.url.path not in ["/docs", "/openapi.json", "/sse", "/messages", "/health"]:
        logger.warning(f"Unauthorized access attempt to {request.url.path}")
        return JSONResponse(status_code=401, content={"detail": "Unauthorized"})
    response = await call_next(request)
    return response

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("MCP_SERVER_PORT", 8000))
    logger.info(f"🚀 Starting Mastodont MCP Bridge on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
