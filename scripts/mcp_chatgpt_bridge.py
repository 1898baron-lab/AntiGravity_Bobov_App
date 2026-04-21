import os
import json
import logging
from typing import List, Optional, Dict
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from mcp.server import Server
from mcp.server.sse import SseServerTransport
from mcp.types import Tool, TextContent
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware


# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("mcp_chatgpt_bridge")

# Загрузка переменных окружения
load_dotenv(".env.mcp")

TOKEN = os.getenv("CHATGPT_MCP_TOKEN")
if not TOKEN:
    logger.error("CRITICAL: CHATGPT_MCP_TOKEN not set in .env.mcp")
    raise RuntimeError("CHATGPT_MCP_TOKEN is mandatory")

KNOWLEDGE_PATH = Path(os.getenv("KNOWLEDGE_PATH", "c:/ANTIGRAVITY/1/obsidian_brain/Engineering/")).resolve()
MAX_CHARS = 10000

class KnowledgeStore:
    """Класс для управления кешированием и поиском по базе знаний."""
    def __init__(self, path: Path):
        self.path = path
        self.cache: Dict[str, str] = {}
        self.load_cache()

    def load_cache(self):
        """Предзагрузка всех документов в память."""
        logger.info(f"Indexing knowledge base at: {self.path}")
        if not self.path.exists():
            logger.warning(f"Path {self.path} does not exist!")
            return

        for file in self.path.rglob("*.md"):
            try:
                rel_path = str(file.relative_to(self.path))
                content = file.read_text(encoding="utf-8")
                self.cache[rel_path] = content
                logger.debug(f"Indexed: {rel_path}")
            except Exception as e:
                logger.error(f"Error indexing {file}: {e}")
        logger.info(f"Indexing complete. {len(self.cache)} documents loaded.")

    def search(self, query: str) -> List[Dict]:
        """Поиск с ранжированием по количеству вхождений (TF)."""
        if not query.strip():
            return []

        query = query.lower()
        results = []

        for doc_id, content in self.cache.items():
            content_lower = content.lower()
            if query in content_lower or query in doc_id.lower():
                # Простая метрика релевантности: частота запроса + бонус за название
                score = content_lower.count(query)
                if query in doc_id.lower():
                    score += 10
                
                summary = content[:300].replace("\n", " ") + "..."
                results.append({
                    "id": doc_id,
                    "title": Path(doc_id).name,
                    "score": score,
                    "snippet": summary
                })

        # Сортировка по убыванию score
        return sorted(results, key=lambda x: x["score"], reverse=True)

    def get_content(self, doc_id: str) -> Optional[str]:
        """Получение контента с лимитом размера."""
        content = self.cache.get(doc_id)
        if content and len(content) > MAX_CHARS:
            logger.warning(f"Document {doc_id} truncated (Original: {len(content)} chars)")
            return content[:MAX_CHARS] + "\n\n... [ДОКУМЕНТ УСЕЧЕН ДЛЯ ЭКОНОМИИ ТОКЕНОВ] ..."
        return content

# Инициализация хранилища
store = KnowledgeStore(KNOWLEDGE_PATH)

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
        query = arguments.get("query", "")
        if not query.strip():
            return [TextContent(type="text", text="Ошибка: Пустой поисковый запрос.")]
        
        logger.info(f"Tool call search_knowledge: query='{query}'")
        found = store.search(query)
        
        response_data = {"results": found[:10]}
        return [TextContent(type="text", text=json.dumps(response_data, ensure_ascii=False))]

    elif name == "fetch_document":
        doc_id = arguments.get("id", "")
        logger.info(f"Tool call fetch_document: id='{doc_id}'")
        
        content = store.get_content(doc_id)
        if not content:
            return [TextContent(type="text", text="Ошибка: Документ не найден в кеше.")]
            
        fetch_data = {
            "id": doc_id,
            "title": Path(doc_id).name,
            "text": content
        }
        return [TextContent(type="text", text=json.dumps(fetch_data, ensure_ascii=False))]

    else:
        raise ValueError(f"Unknown tool: {name}")

# Инициализация FastAPI приложения
app = FastAPI(
    title="Mastodont Engineering Knowledge Base",
    version="2.1.0",
    description="Access the Obsidian Engineering vault. OpenAI Apps SDK / MCP compliant."
)

# ─────────────────────────────────────────────
# CORS for OpenAI
# ─────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://chatgpt.com", "https://openai.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# (Мы убрали SecurityHeadersMiddleware, так как он мешал SSE-потоку)

# ─────────────────────────────────────────────
# REST Tool endpoints for ChatGPT Custom Action
# ─────────────────────────────────────────────
@app.get("/tools/search")
async def rest_search(query: str = ""):
    """ChatGPT Custom Action: поиск по базе знаний."""
    if not query.strip():
        raise HTTPException(status_code=400, detail="Query parameter is required")
    logger.info(f"[ChatGPT Action] search_knowledge: '{query}'")
    found = store.search(query)
    return {"results": found[:10]}

@app.get("/tools/fetch")
async def rest_fetch(id: str = ""):
    """ChatGPT Custom Action: получение полного документа."""
    if not id.strip():
        raise HTTPException(status_code=400, detail="id parameter is required")
    logger.info(f"[ChatGPT Action] fetch_document: '{id}'")
    content = store.get_content(id)
    if not content:
        raise HTTPException(status_code=404, detail=f"Document '{id}' not found")
    return {"id": id, "title": Path(id).name, "text": content}

# ─────────────────────
# Standard endpoints
# ─────────────────────
@app.get("/health")
async def health():
    """Проверка состояния сервера."""
    return {
        "status": "ok",
        "server": "Mastodont MCP Bridge v2.0",
        "docs_count": len(store.cache),
        "knowledge_root": str(KNOWLEDGE_PATH)
    }

# ─────────────────────────────────────────────
# SSE Handlers (Low-level for stability)
# ─────────────────────────────────────────────

@app.get("/sse")
async def handle_sse(request: Request):
    """Подключение по SSE. Мы используем прямое управление стримом."""
    logger.info("New SSE GET connection attempt")
    
    async def sse_stream():
        async with sse.connect_sse(request.scope, request.receive, request._send) as (read_stream, write_stream):
            logger.info("SSE stream established, running MCP server...")
            await mcp_server.run(read_stream, write_stream, mcp_server.create_initialization_options())
            logger.info("MCP server run finished")

    # В FastAPI/Starlette для SSE обычно используют StreamingResponse, 
    # но библиотека MCP сама управляет отправкой через request._send.
    await sse_stream()
    # Мы НИЧЕГО не возвращаем, чтобы не ломать поток данных

@app.post("/sse")
@app.post("/messages")
async def handle_mcp_messages(request: Request):
    """Сверх-стабильный обработчик сообщений для ChatGPT.
    Мы вручную доставляем сообщение и гарантируем правильный JSON-ответ."""
    try:
        body = await request.json()
        session_id = request.query_params.get("session_id")
        
        # Если session_id нет (OpenAI его часто не шлет), берем последний активный
        if not session_id:
            active_sessions = list(sse._read_stream_writers.keys())
            if active_sessions:
                session_id = active_sessions[-1]
            else:
                logger.error("No active sessions found for incoming message")
                return JSONResponse({"error": "no_session"}, status_code=200)

        # Достаем 'писателя' потока для этой сессии
        writer = sse._read_stream_writers.get(session_id)
        if not writer:
            logger.error(f"Session {session_id} writer not found")
            return JSONResponse({"error": "writer_not_found"}, status_code=200)

        # Напрямую записываем сообщение в поток сервера
        logger.info(f"Manually routing message to session {session_id}")
        await writer.write(json.dumps(body))
        
        # ГАРАНТИРУЕМ ответ, который хочет OpenAI
        return JSONResponse(
            content={"status": "received", "sessionId": session_id},
            headers={"Content-Type": "application/json; charset=utf-8"}
        )
    except Exception as e:
        logger.error(f"Critical error in message router: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=200)

# ─────────────────────────────────────────────
# Auth: ОТКЛЮЧЕНО ДЛЯ НАСТРОЙКИ
# ─────────────────────────────────────────────
# (Мы временно убрали Middleware, так как он мешал SSE-потоку)

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("MCP_SERVER_PORT", 8000))
    logger.info(f"🚀 Starting Mastodont MCP Bridge v2.0 on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
