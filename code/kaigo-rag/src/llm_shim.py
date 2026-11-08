"""OpenAI と同じ形の API を手元に立てる中継サーバー。GraphRAG のライブラリを、API キーなしで動かすため。

- POST /v1/chat/completions -> claude -p(model 名に sonnet / opus を含めばそのモデル、ほかは haiku)
- POST /v1/embeddings       -> ruri-v3-310m(文書の接頭辞)
- GET  /v1/models
localhost だけで待ち受ける。キーは確かめない(手元の検証用)
使い方: uv run python src/llm_shim.py   -> base_url は http://127.0.0.1:8766/v1
"""
import json
import subprocess
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

PORT = 8766
SEM = threading.BoundedSemaphore(16)  # claude -p を同時に走らせる数
EMB_LOCK = threading.Lock()
STATS = {"chat": 0, "chat_sec": 0.0, "embed": 0}


def pick_model(name: str) -> str:
    name = (name or "").lower()
    return "sonnet" if "sonnet" in name else "opus" if "opus" in name else "haiku"


def content_text(c):
    if isinstance(c, list):  # [{"type": "text", "text": ...}]
        return "".join(p.get("text", "") for p in c if isinstance(p, dict))
    return c or ""


def chat(body):
    msgs = body.get("messages", [])
    system = "\n\n".join(content_text(m["content"]) for m in msgs if m["role"] == "system") or "You are a helpful assistant."
    rest = [m for m in msgs if m["role"] != "system"]
    if len(rest) == 1:
        prompt = content_text(rest[0]["content"])
    else:
        prompt = "".join(f"[{m['role']}]\n{content_text(m['content'])}\n\n" for m in rest)
    if body.get("response_format", {}).get("type") in ("json_object", "json_schema"):
        system += "\n\nRespond with a single valid JSON object only."
    cmd = ["claude", "-p", "--model", pick_model(body.get("model")), "--output-format", "text",
           "--tools", "", "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}', "--system-prompt", system]
    t0 = time.time()
    with SEM:
        for attempt in range(3):
            r = subprocess.run(cmd, input=prompt, capture_output=True, text=True, timeout=900, cwd="/tmp")
            if r.returncode == 0 and r.stdout.strip():
                break
            time.sleep(5 * (attempt + 1))
    STATS["chat"] += 1
    STATS["chat_sec"] += time.time() - t0
    text = r.stdout.strip()
    if text.startswith("```"):  # JSON を ``` で囲んで返すことがある
        text = text.strip("`").removeprefix("json").strip()
    return text


def embed(inputs):
    from embed import DOC_PREFIX, model
    with EMB_LOCK:
        v = model().encode([DOC_PREFIX + t for t in inputs], batch_size=8, normalize_embeddings=True)
    STATS["embed"] += len(inputs)
    return v.tolist()


class H(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def send(self, obj, code=200):
        b = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def do_GET(self):
        if self.path.rstrip("/").endswith("/models"):
            return self.send({"object": "list", "data": [{"id": m, "object": "model"} for m in ("haiku", "sonnet", "opus", "ruri-v3-310m")]})
        if self.path.rstrip("/").endswith("/stats"):
            return self.send(STATS)
        self.send({"error": "not found"}, 404)

    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
        now = int(time.time())
        if self.path.endswith("/chat/completions"):
            text = chat(body)
            msg = {"role": "assistant", "content": text}
            if body.get("stream"):
                # 1塊だけの SSE で返す
                self.send_response(200)
                self.send_header("Content-Type", "text/event-stream")
                self.end_headers()
                chunk = {"id": f"c{now}", "object": "chat.completion.chunk", "created": now, "model": body.get("model"),
                         "choices": [{"index": 0, "delta": msg, "finish_reason": "stop"}]}
                self.wfile.write(f"data: {json.dumps(chunk, ensure_ascii=False)}\n\ndata: [DONE]\n\n".encode())
                return
            return self.send({"id": f"c{now}", "object": "chat.completion", "created": now, "model": body.get("model"),
                              "choices": [{"index": 0, "message": msg, "finish_reason": "stop"}],
                              "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}})
        if self.path.endswith("/embeddings"):
            inp = body.get("input", [])
            inp = [inp] if isinstance(inp, str) else inp
            vecs = embed(inp)
            return self.send({"object": "list", "model": body.get("model"),
                              "data": [{"object": "embedding", "index": i, "embedding": v} for i, v in enumerate(vecs)],
                              "usage": {"prompt_tokens": 0, "total_tokens": 0}})
        self.send({"error": "not found"}, 404)


if __name__ == "__main__":
    print("shim on", PORT, flush=True)
    ThreadingHTTPServer(("127.0.0.1", PORT), H).serve_forever()
