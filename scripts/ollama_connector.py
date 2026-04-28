#!/usr/bin/env python3
"""Ollama Connector for local Gemma integration.

Простой локальный HTTP-прокси, который принимает запросы и перенаправляет их в
локальный Ollama сервер на http://localhost:11434.

Запуск:
    python scripts/ollama_connector.py

Использование:
    POST /api/generate
    POST /v1/chat/completions
    GET  /health
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

BASE_OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
API_KEY = os.getenv("OLLAMA_API_KEY", "")

DEFAULT_PORT = 11435


def forward_request(path: str, method: str = "POST", body: bytes | None = None, headers=None):
    url = urllib.parse.urljoin(BASE_OLLAMA_URL.rstrip("/"), path)
    req_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    if headers:
        req_headers.update(headers)
    if API_KEY:
        req_headers["Authorization"] = f"Bearer {API_KEY}"

    req = urllib.request.Request(url, data=body, headers=req_headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            response_body = resp.read()
            status = resp.getcode()
            response_headers = dict(resp.getheaders())
            return status, response_headers, response_body
    except urllib.error.HTTPError as exc:
        body = exc.read()
        return exc.code, dict(exc.headers), body
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Failed to connect to Ollama at {BASE_OLLAMA_URL}: {exc.reason}")


class OllamaProxyHandler(BaseHTTPRequestHandler):
    server_version = "OllamaConnector/1.0"

    def _send_json(self, status_code: int, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _proxy(self, path: str):
        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length) if length else None
        try:
            status, response_headers, response_body = forward_request(path, method=self.command, body=body)
        except Exception as exc:
            self._send_json(502, {"error": str(exc)})
            return

        # Пробросить тело и заголовки обратно клиенту
        self.send_response(status)
        content_type = response_headers.get("Content-Type", "application/json")
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(response_body)))
        self.end_headers()
        self.wfile.write(response_body)

    def do_GET(self):
        if self.path == "/health":
            try:
                status, headers, body = forward_request("/v1/models", method="GET")
                if status == 200:
                    self._send_json(200, {
                        "status": "ok",
                        "ollama_url": BASE_OLLAMA_URL,
                        "port": self.server.server_port,
                    })
                else:
                    self._send_json(502, {
                        "status": "error",
                        "ollama_status": status,
                        "ollama_body": body.decode("utf-8", errors="replace"),
                    })
            except Exception as exc:
                self._send_json(502, {"error": str(exc)})
            return

        self._send_json(404, {"error": "Not found"})

    def do_POST(self):
        if self.path in ["/api/generate", "/v1/chat/completions"]:
            self._proxy(self.path)
            return

        self._send_json(404, {"error": "Not found"})

    def log_message(self, format, *args):
        sys.stdout.write("[OllamaConnector] %s - - [%s] %s\n" % (self.client_address[0], self.log_date_time_string(), format % args))


def parse_args():
    parser = argparse.ArgumentParser(description="Run a local Ollama proxy for Gemma/Ollama integration.")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="Local port for the connector")
    parser.add_argument("--ollama-url", default=BASE_OLLAMA_URL, help="Base URL of the Ollama server")
    return parser.parse_args()


def run_server(port: int, ollama_url: str):
    global BASE_OLLAMA_URL
    BASE_OLLAMA_URL = ollama_url
    address = ("", port)
    server = ThreadingHTTPServer(address, OllamaProxyHandler)
    print(f"Ollama Connector started on http://localhost:{port}")
    print(f"Forwarding requests to {BASE_OLLAMA_URL}")
    print("Endpoints: GET /health, POST /api/generate, POST /v1/chat/completions")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
        print("Ollama Connector stopped")


if __name__ == "__main__":
    args = parse_args()
    run_server(args.port, args.ollama_url)
