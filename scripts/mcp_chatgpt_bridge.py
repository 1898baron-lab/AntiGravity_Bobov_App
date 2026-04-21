import os
import json
import logging
from typing import List, Optional
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import JSONResponse
from mcp.server.fastapi import FastApiServer
from mcp.server import Server
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mcp_chatgpt_bridge")

# Загрузка переменных окружения
load_dotenv(".env.mcp")
TOKEN = os.getenv("CHATGPT_MCP_TOKEN", "mastodont_secret_2026")
KNOWLEDGE_PATH = Path(os.getenv("KNOWLEDGE_PATH", "c:/ANTIGRAVITY/1/knowledge/")).resolve()

# Инициализация MCP сервера
mcp_server = Server("mastodont-knowledge")

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
        
        # Простой поиск по файлам в knowledge/
        for file in KNOWLEDGE_PATH.rglob("*.md"):
            try:
                content = file.read_text(encoding="utf-8")
                if query in content.lower() or query in file.name.lower():
                    # Формируем краткое описание для ChatGPT
                    summary = content[:200].replace("\n", " ") + "..."
                    results.append({
                        "id": str(file.relative_to(KNOWLEDGE_PATH)),
                        "title": file.name,
                        "url": f"local://{file.name}", # Заглушка URL
                        "snippet": summary
                    })
            except Exception as e:
                logger.error(f"Error reading {file}: {e}")
        
        # OpenAI требует обертку "results" внутри JSON-строки для Company Knowledge
        # Но для обычных инструментов возвращаем просто текст
        response_data = {"results": results[:10]}
        return [TextContent(type="text", text=json.dumps(response_data, ensure_ascii=False))]

    elif name == "fetch_document":
        doc_id = arguments.get("id", "")
        file_path = (KNOWLEDGE_PATH / doc_id).resolve()
        
        # Проверка безопасности: нельзя выходить за пределы KNOWLEDGE_PATH
        if not str(file_path).startswith(str(KNOWLEDGE_PATH)):
            raise ValueError("Access Denied: Path outside of knowledge base")
            
        if not file_path.exists():
            return [TextContent(type="text", text="Ошибка: Документ не найден.")]
            
        try:
            content = file_path.read_text(encoding="utf-8")
            # OpenAI Fetch формат: id, title, text
            fetch_data = {
                "id": doc_id,
                "title": file_path.name,
                "text": content,
                "url": f"local://{doc_id}"
            }
            return [TextContent(type="text", text=json.dumps(fetch_data, ensure_ascii=False))]
        except Exception as e:
            return [TextContent(type="text", text=f"Ошибка чтения: {str(e)}")]

    else:
        raise ValueError(f"Unknown tool: {name}")

# Создание FastAPI приложения с MCP адаптером
app = FastAPI(title="Mastodont ChatGPT Bridge")
mcp_app = FastApiServer(mcp_server)

# Middleware для проверки токена
@app.middleware("http")
async def check_auth(request: Request, call_next):
    # ChatGPT может присылать токен в Authorization заголовке
    auth_header = request.headers.get("Authorization")
    if auth_header != f"Bearer {TOKEN}" and request.url.path not in ["/docs", "/openapi.json"]:
        return JSONResponse(status_code=401, content={"detail": "Unauthorized"})
    response = await call_next(request)
    return response

# Монтирование MCP путей
app.mount("/", mcp_app)

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("MCP_SERVER_PORT", 8000))
    logger.info(f"Starting Mastodont MCP Bridge on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
