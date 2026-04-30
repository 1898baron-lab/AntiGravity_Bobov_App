import os
import json
import urllib.request
import sys
import re
import math
from pathlib import Path
from collections import Counter

# Настройки RAG
REPO_ROOT = Path(__file__).resolve().parents[1]
OBSIDIAN_DIR = REPO_ROOT / "obsidian_brain"
LEGAL_DIR = REPO_ROOT / "legal"
INTERNSHIP_DIR = REPO_ROOT / "Internship_NTD"
KNOWLEDGE_BASE_DIR = REPO_ROOT / "knowledge_base"

SEARCH_DIRS = [
    str(OBSIDIAN_DIR),
    str(LEGAL_DIR),
    str(INTERNSHIP_DIR),
    str(KNOWLEDGE_BASE_DIR),
]
IGNORE_DIRS = {".git", ".docs", "venv", ".venv", "__pycache__", "node_modules"}
MAX_CONTEXT_WORDS = 800  # Ограничение для gemma4:26b-lite (num_ctx=2048)
CHUNK_SIZE_WORDS = 160
CHUNK_OVERLAP_WORDS = 40
MAX_HISTORY_MESSAGES = 10
MIN_KEYWORD_LENGTH = 4
MAX_CHUNKS_PER_FILE = 20
MODEL_NAME = "gemma4:26b-lite"
HISTORY_FILE = str(KNOWLEDGE_BASE_DIR / "chat_history.md")


def normalize_words(text):
    return re.findall(r"\w+", text.lower())


def split_paragraphs(text):
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n+", text) if p.strip()]
    return paragraphs if paragraphs else [text.strip()]


def chunk_text(text, chunk_size=CHUNK_SIZE_WORDS, overlap=CHUNK_OVERLAP_WORDS):
    chunks = []
    for paragraph in split_paragraphs(text):
        words = paragraph.split()
        if not words:
            continue

        if len(words) <= chunk_size:
            chunks.append(paragraph)
            continue

        step = max(chunk_size - overlap, 1)
        for start in range(0, len(words), step):
            window = words[start:start + chunk_size]
            if not window:
                break
            chunks.append(" ".join(window).strip())
            if len(window) < chunk_size:
                break

    return chunks


def get_chat_history():
    if not os.path.exists(HISTORY_FILE):
        return ""

    try:
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]

        interactions = []
        current = []
        for line in lines:
            if line.startswith("USER:") or line.startswith("AI:"):
                current.append(line)
                if line.startswith("AI:"):
                    interactions.append("\n".join(current))
                    current = []

        if current:
            interactions.append("\n".join(current))

        return "\n\n".join(interactions[-MAX_HISTORY_MESSAGES:])
    except Exception:
        return ""


def save_chat_history(query, response):
    try:
        os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
        with open(HISTORY_FILE, 'a', encoding='utf-8') as f:
            f.write(f"USER: {query}\nAI: {response}\n\n")
    except Exception as e:
        print(f"[Ошибка] Не удалось сохранить историю: {e}")


def get_all_md_files(directories):
    files = []
    for d in directories:
        if not os.path.exists(d):
            continue
        for root, dirs, filenames in os.walk(d):
            dirs[:] = [sub for sub in dirs if sub not in IGNORE_DIRS]
            if any(part in IGNORE_DIRS for part in root.split(os.sep)):
                continue
            for filename in filenames:
                if filename.endswith(".md"):
                    files.append(os.path.join(root, filename))
    return files


def load_file_content(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception:
        return ""


def build_query_terms(query):
    terms = [word for word in normalize_words(query) if len(word) >= MIN_KEYWORD_LENGTH]
    return terms or normalize_words(query)


def score_chunks(chunks, query_terms):
    total_chunks = len(chunks)
    if total_chunks == 0:
        return []

    doc_freq = Counter()
    for chunk in chunks:
        chunk_terms = set(normalize_words(chunk['text']))
        for term in query_terms:
            if term in chunk_terms:
                doc_freq[term] += 1

    idf = {
        term: math.log((total_chunks + 1) / (1 + doc_freq[term])) + 1
        for term in query_terms
    }

    scored = []
    for chunk in chunks:
        freq = Counter(normalize_words(chunk['text']))
        score = sum(freq[term] * idf.get(term, 1.0) for term in query_terms if term in freq)
        if score > 0:
            scored.append({**chunk, 'score': score})

    return scored


def format_chunk_context(chunk):
    filename = os.path.basename(chunk['filepath'])
    return f"--- ФАЙЛ: {filename} | ЧАНК {chunk['chunk_id']} ---\n{chunk['text']}\n\n"


def find_relevant_context(query):
    print("[RAG] Сканирование базы знаний...")
    query_terms = build_query_terms(query)

    all_files = get_all_md_files(SEARCH_DIRS)
    all_chunks = []
    for filepath in all_files:
        content = load_file_content(filepath)
        if not content:
            continue

        file_chunks = chunk_text(content)
        for idx, chunk in enumerate(file_chunks[:MAX_CHUNKS_PER_FILE], start=1):
            all_chunks.append({
                'filepath': filepath,
                'chunk_id': idx,
                'text': chunk,
            })

    scored_chunks = score_chunks(all_chunks, query_terms)
    if not scored_chunks:
        return "", []

    scored_chunks.sort(key=lambda item: item['score'], reverse=True)

    context = ""
    used_files = []
    word_count = 0

    for chunk in scored_chunks:
        chunk_words = len(chunk['text'].split())
        if word_count + chunk_words > MAX_CONTEXT_WORDS:
            continue

        context += format_chunk_context(chunk)
        word_count += chunk_words
        used_files.append(os.path.basename(chunk['filepath']))

        if word_count >= MAX_CONTEXT_WORDS:
            break

    used_files = list(dict.fromkeys(used_files))
    return context, used_files


def ask_ollama_with_context(query, context):
    url = "http://localhost:11434/api/generate"

    history = get_chat_history()
    history_block = f"ИСТОРИЯ ПРЕДЫДУЩИХ СООБЩЕНИЙ:\n{history}\n\n" if history else ""

    system_prompt = (
        "Ты - интеллектуальный агент системы AntiGravity. "
        "Твоя задача - отвечать на вопросы пользователя, строго опираясь на предоставленные ниже документы из базы знаний (RAG) и историю диалога.\n"
        "Если ответа нет в документах, так и скажи. Не придумывай факты.\n\n"
        f"{history_block}"
        f"ДОКУМЕНТЫ:\n{context}\n\n"
        f"ВОПРОС ПОЛЬЗОВАТЕЛЯ:\n{query}"
    )

    data = {
        "model": MODEL_NAME,
        "prompt": system_prompt,
        "stream": True,
        "options": {
            "num_ctx": 2048
        }
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode('utf-8'),
        headers={'Content-Type': 'application/json; charset=utf-8'}
    )

    full_response = ""
    print(f"\n[Ollama] Отправка запроса к {MODEL_NAME}...\n")
    try:
        with urllib.request.urlopen(req) as response:
            for line in response:
                if line:
                    decoded_line = line.decode('utf-8')
                    try:
                        json_resp = json.loads(decoded_line)
                        chunk = json_resp.get("response", "")
                        print(chunk, end="", flush=True)
                        full_response += chunk
                    except json.JSONDecodeError:
                        pass
            print("\n")

        save_chat_history(query, full_response)

    except Exception as e:
        print(f"\n[Ошибка] Не удалось связаться с Ollama: {e}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        user_query = " ".join(sys.argv[1:])
    else:
        user_query = input("Введите ваш вопрос для RAG-поиска: ")

    if not user_query.strip():
        print("Вопрос не задан.")
        sys.exit(0)

    context, files_used = find_relevant_context(user_query)

    if not context:
        print("[RAG] В базе знаний не найдено подходящих документов. Модель ответит на основе своих общих знаний.")
    else:
        print(f"[RAG] Найдены релевантные файлы: {', '.join(files_used)}")

    ask_ollama_with_context(user_query, context)
