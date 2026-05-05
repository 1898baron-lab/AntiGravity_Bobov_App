import os
import json
import logging
import urllib.request
from typing import List, Optional, Dict
from pathlib import Path
from dotenv import load_dotenv
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', filename='mcp_obsidian_ollama.log')
logger = logging.getLogger("mcp_obsidian_ollama")

# Загрузка переменных окружения
load_dotenv(".env.mcp")

KNOWLEDGE_PATH = Path(os.getenv("KNOWLEDGE_PATH", "c:/ANTIGRAVITY/1/obsidian_brain/Engineering/")).resolve()
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
MAX_CHARS = 10000

class KnowledgeStore:
    """Класс для управления поиском по базе знаний Obsidian."""
    def __init__(self, path: Path):
        self.path = path
        self.cache: Dict[str, str] = {}
        self.load_cache()

    def load_cache(self):
        """Предзагрузка всех документов в память."""
        if not self.path.exists():
            logger.warning(f"Path {self.path} does not exist!")
            return

        for file in self.path.rglob("*.md"):
            try:
                rel_path = str(file.relative_to(self.path))
                content = file.read_text(encoding="utf-8")
                self.cache[rel_path] = content
            except Exception as e:
                logger.error(f"Error indexing {file}: {e}")
        logger.info(f"Indexing complete. {len(self.cache)} documents loaded.")

    def search(self, query: str) -> List[Dict]:
        if not query.strip(): return []
        query = query.lower()
        results = []
        for doc_id, content in self.cache.items():
            content_lower = content.lower()
            if query in content_lower or query in doc_id.lower():
                score = content_lower.count(query)
                if query in doc_id.lower(): score += 10
                summary = content[:300].replace("\n", " ") + "..."
                results.append({"id": doc_id, "title": Path(doc_id).name, "score": score, "snippet": summary})
        return sorted(results, key=lambda x: x["score"], reverse=True)

    def get_content(self, doc_id: str) -> Optional[str]:
        content = self.cache.get(doc_id)
        if content and len(content) > MAX_CHARS:
            return content[:MAX_CHARS] + "\n\n... [ДОКУМЕНТ УСЕЧЕН ДЛЯ ЭКОНОМИИ ТОКЕНОВ] ..."
        return content

# Инициализация хранилища
store = KnowledgeStore(KNOWLEDGE_PATH)

# Инициализация MCP сервера
mcp_server = Server("obsidian-ollama-hub")

@mcp_server.list_tools()
async def list_tools() -> List[Tool]:
    return [
        Tool(
            name="search_obsidian",
            description="Поиск по инженерной базе знаний в Obsidian (ГОСТы, ТТ, регламенты).",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Поисковый запрос"}
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="fetch_obsidian_doc",
            description="Чтение полного текста заметки из Obsidian.",
            inputSchema={
                "type": "object",
                "properties": {
                    "id": {"type": "string", "description": "ID документа из результатов поиска"}
                },
                "required": ["id"]
            }
        ),
        Tool(
            name="ask_ollama",
            description="Вызов локальной нейросети Ollama для сложных инженерных рассуждений или генерации идей.",
            inputSchema={
                "type": "object",
                "properties": {
                    "prompt": {"type": "string", "description": "Запрос к нейросети"},
                    "model": {"type": "string", "description": "Модель (например, deepseek-r1:8b)", "default": "deepseek-r1:8b"}
                },
                "required": ["prompt"]
            }
        )
    ]

@mcp_server.call_tool()
async def call_tool(name: str, arguments: dict) -> List[TextContent]:
    if name == "search_obsidian":
        query = arguments.get("query", "")
        found = store.search(query)
        return [TextContent(type="text", text=json.dumps({"results": found[:10]}, ensure_ascii=False))]

    elif name == "fetch_obsidian_doc":
        doc_id = arguments.get("id", "")
        content = store.get_content(doc_id)
        if not content: return [TextContent(type="text", text="Ошибка: Документ не найден.")]
        return [TextContent(type="text", text=json.dumps({"id": doc_id, "text": content}, ensure_ascii=False))]

    elif name == "ask_ollama":
        prompt = arguments.get("prompt", "")
        model = arguments.get("model", "deepseek-r1:8b")
        data = {"model": model, "prompt": prompt, "stream": False}
        try:
            req = urllib.request.Request(OLLAMA_URL, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))
                return [TextContent(type="text", text=result.get("response", "Нет ответа от Ollama"))]
        except Exception as e:
            return [TextContent(type="text", text=f"Ошибка подключения к Ollama: {e}")]

    raise ValueError(f"Unknown tool: {name}")

async def run():
    async with stdio_server() as (read_stream, write_stream):
        await mcp_server.run(read_stream, write_stream, mcp_server.create_initialization_options())

if __name__ == "__main__":
    import asyncio
    asyncio.run(run())
