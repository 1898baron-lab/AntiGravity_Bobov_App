import json
import math
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


STOP_WORDS = {
    "для", "или", "как", "это", "что", "этот", "все", "всех", "был", "была", "было", "были", 
    "какая", "какой", "какое", "какие", "под", "над", "при", "про", "без", "около", 
    "перед", "через", "после", "между", "один", "два", "три", "ваш", "ваша", "ваше", "ваши",
    "твой", "твоя", "твое", "твои", "свой", "своя", "свое", "свои"
}


def stem_word(word: str) -> str:
    word = word.lower()
    if not re.match(r"^[а-яё]+$", word):
        return word
    # Усекаем падежные окончания русских существительных и прилагательных
    word = re.sub(r"(ами|ями|ов|ев|ам|ям|ах|ях|ом|ем|ой|ей|ия|ию|ие|ии|ия|ы|и|а|я|о|е|у|ю)$", "", word)
    return word


def normalize_query(query: str) -> List[str]:
    tokens = re.findall(r"\w+", query.lower())
    result = []
    for token in tokens:
        if len(token) <= 2:
            continue
        if token in STOP_WORDS:
            continue
        result.append(stem_word(token))
    return result


def score_document(text: str, query_tokens: List[str]) -> int:
    """
    Продвинутый скоринг с двумя факторами:
    1. log1p(count) — сглаживает влияние огромных файлов с высокой частотой.
    2. unique_matches^3 — сильно поднимает документы, покрывающие БОЛЬШЕ слов запроса.
    """
    if not query_tokens:
        return 0
    lower = text.lower()
    score = 0.0
    unique_matches = 0
    for token in query_tokens:
        count = lower.count(token)
        if count > 0:
            unique_matches += 1
            score += math.log1p(count) * 10.0
    # Кубический буст за покрытие: документ с 3 из 3 слов >> документа с 1 из 3
    return int(score * (unique_matches ** 3))


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
