#!/usr/bin/env python3
"""
Gemma + Ollama helper for AntiGravity_Bobov_App

Этот скрипт помогает проверить доступность локального Ollama API,
просмотреть установленные модели и отправить тестовый запрос.
"""

import argparse
import json
import os
import ssl
import sys
import urllib.error
import urllib.request

BASE_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
API_KEY = os.getenv("OLLAMA_API_KEY", "")

HEADERS = {
    "Content-Type": "application/json",
}
if API_KEY:
    HEADERS["Authorization"] = f"Bearer {API_KEY}"


def build_url(path: str) -> str:
    return f"{BASE_URL.rstrip('/')}{path}"


def request_json(path: str, method: str = "GET", data=None):
    url = build_url(path)
    body = None
    if data is not None:
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=body, headers=HEADERS, method=method)
    try:
        with urllib.request.urlopen(req, context=ssl.create_default_context()) as resp:
            text = resp.read().decode("utf-8", errors="replace")
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                return text
    except urllib.error.HTTPError as exc:
        message = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code} {exc.reason}: {message}")
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Connection failed: {exc.reason}")


def status() -> dict:
    try:
        result = request_json("/v1/models")
        return {
            "status": "ok",
            "base_url": BASE_URL,
            "models_count": len(result["data"]) if isinstance(result, dict) and "data" in result else None,
            "raw": result,
        }
    except Exception as exc:
        return {"status": "error", "error": str(exc), "base_url": BASE_URL}


def list_models() -> list:
    result = request_json("/v1/models")
    if isinstance(result, dict) and "data" in result:
        return result["data"]
    raise RuntimeError(f"Unexpected /v1/models response: {result}")


def generate(model: str, prompt: str, max_tokens: int = 1024, temperature: float = 0.0):
    payload = {
        "model": model,
        "prompt": prompt,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "stream": False,
    }
    result = request_json("/api/generate", method="POST", data=payload)
    return result


def print_json(value):
    print(json.dumps(value, ensure_ascii=False, indent=2))


def parse_args():
    parser = argparse.ArgumentParser(description="Gemma + Ollama helper for AntiGravity_Bobov_App")
    parser.add_argument("command", choices=["status", "list", "chat", "generate"], help="Action to perform")
    parser.add_argument("--model", default="gemma-4-e2b-it", help="Model name, например gemma-4-e2b-it")
    parser.add_argument("--prompt", help="Текст запроса")
    parser.add_argument("--prompt-file", help="Файл с текстом запроса")
    parser.add_argument("--output", help="Файл для сохранения ответа")
    parser.add_argument("--max-tokens", type=int, default=1024, help="Максимальное количество токенов")
    parser.add_argument("--temperature", type=float, default=0.0, help="Температура генерации")
    return parser.parse_args()


def read_prompt(args):
    if args.prompt_file:
        with open(args.prompt_file, "r", encoding="utf-8") as f:
            return f.read().strip()
    if args.prompt:
        return args.prompt.strip()
    raise RuntimeError("Укажите --prompt или --prompt-file")


def main():
    args = parse_args()

    if args.command == "status":
        result = status()
        print_json(result)
        return

    if args.command == "list":
        models = list_models()
        if not models:
            print("Модели не найдены.")
            return
        for model in models:
            name = model.get("name") if isinstance(model, dict) else str(model)
            print(f"- {name}")
        return

    prompt = read_prompt(args)
    if args.command in ["chat", "generate"]:
        result = generate(args.model, prompt, max_tokens=args.max_tokens, temperature=args.temperature)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                if isinstance(result, dict):
                    f.write(json.dumps(result, ensure_ascii=False, indent=2))
                else:
                    f.write(str(result))
            print(f"Ответ сохранён в {args.output}")
        if isinstance(result, dict):
            if "response" in result:
                print(result["response"])
            else:
                print_json(result)
        else:
            print(result)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"Ошибка: {exc}", file=sys.stderr)
        sys.exit(1)
