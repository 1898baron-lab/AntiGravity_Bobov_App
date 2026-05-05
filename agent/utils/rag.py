import os
import re
import math
from collections import Counter
from agent.config import (
    DEFAULT_SEARCH_PATHS, IGNORE_DIRS, MAX_CONTEXT_WORDS, 
    CHUNK_SIZE_WORDS, CHUNK_OVERLAP_WORDS, MAX_CHUNKS_PER_FILE,
    MIN_KEYWORD_LENGTH
)

def normalize_words(text):
    return re.findall(r"\w+", text.lower())

def split_paragraphs(text):
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n+", text) if p.strip()]
    return paragraphs if paragraphs else [text.strip()]

def chunk_text(text):
    chunks = []
    for paragraph in split_paragraphs(text):
        words = paragraph.split()
        if not words:
            continue
        if len(words) <= CHUNK_SIZE_WORDS:
            chunks.append(paragraph)
            continue
        step = max(CHUNK_SIZE_WORDS - CHUNK_OVERLAP_WORDS, 1)
        for start in range(0, len(words), step):
            window = words[start:start + CHUNK_SIZE_WORDS]
            if not window:
                break
            chunks.append(" ".join(window).strip())
            if len(window) < CHUNK_SIZE_WORDS:
                break
    return chunks

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
                if filename.endswith(".md") or filename.endswith(".txt"):
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

def find_relevant_context(query):
    query_terms = build_query_terms(query)
    all_files = get_all_md_files(DEFAULT_SEARCH_PATHS)
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
        context += f"--- ФАЙЛ: {os.path.basename(chunk['filepath'])} ---\n{chunk['text']}\n\n"
        word_count += chunk_words
        used_files.append(os.path.basename(chunk['filepath']))
        if word_count >= MAX_CONTEXT_WORDS:
            break
    return context, list(dict.fromkeys(used_files))
