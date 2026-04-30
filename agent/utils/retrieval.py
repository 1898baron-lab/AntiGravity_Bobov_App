import json
import re
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

from agent.config import IGNORE_DIRS, SEARCH_EXTENSIONS, DEFAULT_SEARCH_PATHS


def list_document_paths(paths: Iterable[Path]) -> List[Path]:
    files = []
    for root in paths:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if path.is_dir():
                if path.name in IGNORE_DIRS:
                    continue
                continue
            if path.suffix.lower() not in SEARCH_EXTENSIONS:
                continue
            if any(part in IGNORE_DIRS for part in path.parts):
                continue
            files.append(path)
    return sorted(files)


def normalize_query(query: str) -> List[str]:
    tokens = re.findall(r"\w+", query.lower())
    return [token for token in tokens if len(token) > 2]


def score_document(text: str, query_tokens: List[str]) -> int:
    lower = text.lower()
    return sum(lower.count(token) for token in query_tokens)


def build_context(query: str, max_words: int = 800) -> Tuple[str, List[str]]:
    query_tokens = normalize_query(query)
    documents = list_document_paths(DEFAULT_SEARCH_PATHS)
    scored = []

    for path in documents:
        try:
            content = path.read_text(encoding="utf-8")
        except Exception:
            continue
        score = score_document(content, query_tokens)
        if score > 0:
            scored.append((score, path, content))

    scored.sort(key=lambda item: item[0], reverse=True)

    context_blocks = []
    included_files = []
    word_count = 0

    for _, path, content in scored:
        words = content.split()
        if word_count + len(words) <= max_words:
            context_blocks.append(f"--- ФАЙЛ: {path.name} ---\n{content}\n")
            word_count += len(words)
            included_files.append(str(path.relative_to(Path.cwd())))
        else:
            snippet = " ".join(words[:300])
            context_blocks.append(f"--- ФАЙЛ: {path.name} (фрагмент) ---\n{snippet}...\n")
            included_files.append(str(path.relative_to(Path.cwd())))
            break

    return "\n".join(context_blocks), included_files


def get_recent_history(path: Path, max_messages: int = 10) -> str:
    if not path.exists():
        return ""
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except Exception:
        return ""

    messages = []
    for line in lines:
        if line.startswith("USER:") or line.startswith("AI:"):
            messages.append(line)
    return "\n".join(messages[-max_messages:])


def save_history(path: Path, query: str, response: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(f"USER: {query}\nAI: {response}\n\n")


def format_prompt(query: str, context: str, history: str) -> str:
    prompt = [
        "Ты интеллектуальный агент локальной системы. Отвечай на вопрос пользователя на основе доступной базы знаний.",
    ]
    if history:
        prompt.append("ИСТОРИЯ ДИАЛОГА:\n" + history)
    if context:
        prompt.append("ДОКУМЕНТЫ:\n" + context)
    prompt.append("ВОПРОС ПОЛЬЗОВАТЕЛЯ:\n" + query)
    prompt.append("Если ответа нет в документах, скажи честно, что не знаешь.")
    return "\n\n".join(prompt)


def save_to_file(path: Path, data: Dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
