#!/usr/bin/env python3
"""
AntiGravity Local Chat Server
Запускает красивый веб-чат на localhost:5050, подключённый к Ollama.
Зависимости: НОЛЬ (только стандартная библиотека Python).
"""
import http.server
import json
import socketserver
import sys
import urllib.error
import urllib.request
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

PORT = 5050
OLLAMA_URL = "http://localhost:11434"

HTML = r"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>🛸 AntiGravity Local Chat</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  :root {
    --bg: #0d0d14;
    --surface: #14141f;
    --surface2: #1c1c2e;
    --border: #2a2a40;
    --accent: #7c5cfc;
    --accent2: #a78bfa;
    --text: #e2e2f0;
    --text-dim: #8888aa;
    --user-bg: #1e1a3a;
    --ai-bg: #111120;
    --radius: 14px;
  }
  body {
    font-family: 'Inter', sans-serif;
    background: var(--bg);
    color: var(--text);
    height: 100vh;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }
  header {
    background: var(--surface);
    border-bottom: 1px solid var(--border);
    padding: 14px 24px;
    display: flex;
    align-items: center;
    gap: 12px;
    flex-shrink: 0;
  }
  .logo { font-size: 22px; }
  .header-info h1 { font-size: 16px; font-weight: 600; color: var(--accent2); }
  .header-info p { font-size: 12px; color: var(--text-dim); }
  .status-dot {
    width: 8px; height: 8px; border-radius: 50%;
    background: #22c55e; margin-left: auto;
    box-shadow: 0 0 8px #22c55e;
    animation: pulse 2s infinite;
  }
  @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:.4} }
  .model-select {
    margin-left: 10px;
    background: var(--surface2);
    border: 1px solid var(--border);
    color: var(--text);
    padding: 5px 10px;
    border-radius: 8px;
    font-size: 13px;
    cursor: pointer;
    outline: none;
  }
  #chat {
    flex: 1;
    overflow-y: auto;
    padding: 24px;
    display: flex;
    flex-direction: column;
    gap: 16px;
    scroll-behavior: smooth;
  }
  #chat::-webkit-scrollbar { width: 6px; }
  #chat::-webkit-scrollbar-track { background: transparent; }
  #chat::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
  .msg {
    display: flex;
    gap: 12px;
    max-width: 800px;
    animation: fadeIn .2s ease;
  }
  @keyframes fadeIn { from{opacity:0;transform:translateY(6px)} to{opacity:1;transform:none} }
  .msg.user { align-self: flex-end; flex-direction: row-reverse; }
  .avatar {
    width: 36px; height: 36px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 16px; flex-shrink: 0;
    background: var(--surface2);
    border: 1px solid var(--border);
  }
  .msg.user .avatar { background: var(--accent); border-color: var(--accent); }
  .bubble {
    padding: 12px 16px;
    border-radius: var(--radius);
    font-size: 14px;
    line-height: 1.65;
    max-width: calc(100% - 50px);
    white-space: pre-wrap;
    word-break: break-word;
  }
  .msg.user .bubble {
    background: var(--user-bg);
    border: 1px solid #3a3060;
    border-top-right-radius: 4px;
  }
  .msg.ai .bubble {
    background: var(--ai-bg);
    border: 1px solid var(--border);
    border-top-left-radius: 4px;
  }
  .thinking {
    display: flex; gap: 5px; align-items: center;
    padding: 14px 18px;
  }
  .dot {
    width: 7px; height: 7px; border-radius: 50%;
    background: var(--accent2);
    animation: bounce .9s infinite;
  }
  .dot:nth-child(2){animation-delay:.15s}
  .dot:nth-child(3){animation-delay:.3s}
  @keyframes bounce {
    0%,80%,100%{transform:translateY(0)}
    40%{transform:translateY(-8px)}
  }
  .input-area {
    background: var(--surface);
    border-top: 1px solid var(--border);
    padding: 16px 24px;
    display: flex;
    gap: 12px;
    align-items: flex-end;
    flex-shrink: 0;
  }
  #prompt {
    flex: 1;
    background: var(--surface2);
    border: 1px solid var(--border);
    color: var(--text);
    border-radius: var(--radius);
    padding: 12px 16px;
    font-size: 14px;
    font-family: inherit;
    resize: none;
    min-height: 46px;
    max-height: 200px;
    outline: none;
    transition: border-color .2s;
    line-height: 1.5;
    overflow-y: auto;
  }
  #prompt:focus { border-color: var(--accent); }
  #prompt::placeholder { color: var(--text-dim); }
  #send-btn {
    width: 46px; height: 46px;
    background: var(--accent);
    border: none; border-radius: 12px;
    color: white; font-size: 18px;
    cursor: pointer;
    display: flex; align-items: center; justify-content: center;
    transition: background .2s, transform .1s;
    flex-shrink: 0;
  }
  #send-btn:hover { background: var(--accent2); }
  #send-btn:active { transform: scale(.95); }
  #send-btn:disabled { background: var(--border); cursor: not-allowed; }
  .hint { font-size: 11px; color: var(--text-dim); text-align: center; padding: 4px 0 0; }
  .welcome {
    text-align: center; color: var(--text-dim);
    margin: auto; padding: 40px 20px;
  }
  .welcome .icon { font-size: 48px; margin-bottom: 16px; }
  .welcome h2 { font-size: 20px; color: var(--accent2); margin-bottom: 8px; }
  .welcome p { font-size: 14px; line-height: 1.6; }
</style>
</head>
<body>
<header>
  <span class="logo">🛸</span>
  <div class="header-info">
    <h1>AntiGravity Local Chat</h1>
    <p>100% offline · Без облачных токенов</p>
  </div>
  <select class="model-select" id="model-select">
    <option value="gemma4:latest">gemma4:latest</option>
    <option value="gemma4:26b-lite">gemma4:26b-lite</option>
  </select>
  <div class="status-dot" title="Ollama подключена"></div>
</header>

<div id="chat">
  <div class="welcome" id="welcome">
    <div class="icon">🤖</div>
    <h2>Gemma готова к работе</h2>
    <p>Локальная модель запущена оффлайн.<br>Задайте любой вопрос — токены не тратятся.</p>
  </div>
</div>

<div class="input-area">
  <textarea id="prompt" placeholder="Напишите сообщение... (Enter — отправить, Shift+Enter — новая строка)" rows="1"></textarea>
  <button id="send-btn" title="Отправить">▲</button>
</div>
<div class="hint">Shift+Enter для новой строки</div>

<script>
const chat = document.getElementById('chat');
const prompt = document.getElementById('prompt');
const sendBtn = document.getElementById('send-btn');
const modelSelect = document.getElementById('model-select');
const welcome = document.getElementById('welcome');
let history = [];
let busy = false;

function addMsg(role, text) {
  if (welcome) welcome.style.display = 'none';
  const div = document.createElement('div');
  div.className = `msg ${role}`;
  const avatar = role === 'user' ? '👤' : '🤖';
  div.innerHTML = `<div class="avatar">${avatar}</div><div class="bubble" id="bubble-${Date.now()}">${escHtml(text)}</div>`;
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
  return div.querySelector('.bubble');
}

function addThinking() {
  if (welcome) welcome.style.display = 'none';
  const div = document.createElement('div');
  div.className = 'msg ai';
  div.id = 'thinking-msg';
  div.innerHTML = `<div class="avatar">🤖</div><div class="bubble thinking"><div class="dot"></div><div class="dot"></div><div class="dot"></div></div>`;
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
  return div;
}

function escHtml(s) {
  return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/\n/g,'<br>');
}

async function send() {
  if (busy) return;
  const text = prompt.value.trim();
  if (!text) return;
  busy = true;
  sendBtn.disabled = true;
  prompt.value = '';
  prompt.style.height = 'auto';

  addMsg('user', text);
  history.push({role:'user', content: text});

  const thinking = addThinking();

  try {
    const resp = await fetch('/api/chat', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({model: modelSelect.value, messages: history})
    });
    const data = await resp.json();
    thinking.remove();
    const answer = data.message?.content || data.error || 'Нет ответа';
    addMsg('ai', answer);
    history.push({role:'assistant', content: answer});
  } catch(e) {
    thinking.remove();
    addMsg('ai', '⚠️ Ошибка: ' + e.message);
  }

  busy = false;
  sendBtn.disabled = false;
  prompt.focus();
  chat.scrollTop = chat.scrollHeight;
}

sendBtn.addEventListener('click', send);
prompt.addEventListener('keydown', e => {
  if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send(); }
});
prompt.addEventListener('input', () => {
  prompt.style.height = 'auto';
  prompt.style.height = Math.min(prompt.scrollHeight, 200) + 'px';
});
</script>
</body>
</html>
"""


class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass  # тишина в консоли

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(HTML.encode("utf-8"))

    def do_POST(self):
        if self.path != "/api/chat":
            self.send_response(404)
            self.end_headers()
            return
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length))
        model = body.get("model", "gemma4:latest")
        messages = body.get("messages", [])

        payload = json.dumps({"model": model, "messages": messages, "stream": False}).encode()
        req = urllib.request.Request(
            OLLAMA_URL + "/api/chat",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=180) as resp:
                data = resp.read()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(data)
        except urllib.error.URLError as e:
            err = json.dumps({"error": str(e)}).encode()
            self.send_response(503)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(err)


if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    srv = None
    for port_attempt in range(PORT, PORT + 10):
        try:
            srv = socketserver.TCPServer(("", port_attempt), Handler)
            PORT = port_attempt
            break
        except OSError:
            continue

    if not srv:
        print("[AntiGravity] Blocker: Ports 5050-5059 are all busy!")
        sys.exit(1)

    print(f"[AntiGravity] Local Chat Server zapushchen!")
    print(f"   Otkroj v brauzere: http://localhost:{PORT}")
    print(f"   Ollama: {OLLAMA_URL}")
    print(f"   Ostanovit: Ctrl+C\n")
    
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\n[AntiGravity] Server stopped.")
        srv.server_close()
