from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Список исключений для индексации
IGNORE_DIRS = {".git", ".docs", "venv", ".venv", "__pycache__", "node_modules", ".agents", ".github", ".vscode"}
SEARCH_EXTENSIONS = {".md", ".txt"}

# Основные пути
KNOWLEDGE_BASE = ROOT / "knowledge_base"
DOCS_DIR = ROOT / ".docs"

# Директории для поиска (только база знаний по умолчанию)
DEFAULT_SEARCH_PATHS = [
    KNOWLEDGE_BASE,
]

CHAT_HISTORY_FILE = KNOWLEDGE_BASE / "archive" / "chat_history.md"

# Настройки Ollama
OLLAMA_URL = "http://localhost:11434"
DEFAULT_MODEL = "gemma4:26b-lite"
MAX_CONTEXT_WORDS = 800
MAX_HISTORY_MESSAGES = 10

# Настройки чанкинга
CHUNK_SIZE_WORDS = 160
CHUNK_OVERLAP_WORDS = 40
MAX_CHUNKS_PER_FILE = 20
MIN_KEYWORD_LENGTH = 4
