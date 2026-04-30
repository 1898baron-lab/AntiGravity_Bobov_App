#!/usr/bin/env python3
import argparse
import json
import ssl
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent.config import CHAT_HISTORY_FILE, DEFAULT_MODEL, MAX_CONTEXT_WORDS, MAX_HISTORY_MESSAGES, OLLAMA_URL
from agent.utils.retrieval import (build_context, format_prompt, get_recent_history,
                                  save_history)


def request_ollama(prompt: str, model: str, max_tokens: int = 1024, temperature: float = 0.0):
    url = OLLAMA_URL.rstrip("/") + "/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "stream": False,
    }
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    headers = {"Content-Type": "application/json; charset=utf-8"}
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, context=ssl.create_default_context()) as response:
            text = response.read().decode("utf-8", errors="replace")
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                return text
    except urllib.error.HTTPError as exc:
        message = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Ollama HTTP {exc.code}: {message}")
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Ollama connection failed: {exc.reason}")


def print_response(result, output_file: Path | None = None):
    if isinstance(result, dict):
        if output_file:
            output_file.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"Ответ сохранен в {output_file}")
        if "response" in result:
            print(result["response"])
        else:
            print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if output_file:
            output_file.write_text(str(result), encoding="utf-8")
            print(f"Ответ сохранен в {output_file}")
        print(result)


def parse_args():
    parser = argparse.ArgumentParser(description="Запуск локального RAG-агента для Ollama")
    parser.add_argument("--query", required=True, help="Вопрос для агента")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Имя модели Ollama")
    parser.add_argument("--max-tokens", type=int, default=1024, help="Максимальное число токенов")
    parser.add_argument("--temperature", type=float, default=0.0, help="Температура генерации")
    parser.add_argument("--output", help="Файл для сохранения ответа")
    return parser.parse_args()


def main():
    args = parse_args()
    history = get_recent_history(CHAT_HISTORY_FILE, max_messages=MAX_HISTORY_MESSAGES)
    context, used_files = build_context(args.query, max_words=MAX_CONTEXT_WORDS)

    if used_files:
        print("Найден контекст из файлов:")
        for item in used_files[:10]:
            print(f" - {item}")
    else:
        print("Релевантный контекст не найден; модель ответит на основе доступных данных.")

    prompt = format_prompt(args.query, context, history)
    result = request_ollama(prompt, args.model, max_tokens=args.max_tokens, temperature=args.temperature)
    print_response(result, Path(args.output) if args.output else None)

    answer = None
    if isinstance(result, dict) and "response" in result:
        answer = result["response"]
    elif isinstance(result, str):
        answer = result

    if answer:
        save_history(CHAT_HISTORY_FILE, args.query, answer)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"Ошибка: {exc}", file=sys.stderr)
        sys.exit(1)
