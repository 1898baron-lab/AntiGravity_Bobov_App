from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

IGNORE_DIRS = {".git", ".docs", "venv", ".venv", "__pycache__", "node_modules"}
SEARCH_EXTENSIONS = {".md", ".txt"}

KNOWLEDGE_BASE = ROOT / "knowledge_base"
DOCS_DIR = ROOT / ".docs"

DEFAULT_SEARCH_PATHS = [
    KNOWLEDGE_BASE,
    ROOT / "obsidian_brain",
    ROOT / "legal",
    ROOT / "Internship_NTD",
]

CHAT_HISTORY_FILE = KNOWLEDGE_BASE / "chat_history.md"

OLLAMA_URL = "http://localhost:11434"
DEFAULT_MODEL = "gemma4:26b-lite"
MAX_CONTEXT_WORDS = 800
MAX_HISTORY_MESSAGES = 10
