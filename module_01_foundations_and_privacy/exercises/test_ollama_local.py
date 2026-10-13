#!/usr/bin/env python3
"""Test local LLM inference with Ollama.

Module 1 exercise: confirm that a model runs entirely on this machine, and
measure how fast it is.

Requirements:
    1. Ollama installed and running (https://ollama.com/download)
    2. A pulled model, e.g.  `ollama pull llama3.1:8b`
    3. `pip install requests`  (and optionally `pip install ollama`)

Usage examples:
    python test_ollama_local.py
    python test_ollama_local.py --model qwen2.5:7b
    python test_ollama_local.py --prompt "What does CCR7 do in dendritic cells?"
    python test_ollama_local.py --backend sdk --stream
    python test_ollama_local.py --list
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from urllib.parse import urlparse

import requests

DEFAULT_HOST = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434")
DEFAULT_MODEL = "llama3.1:8b"
DEFAULT_PROMPT = (
    "In three concise bullet points, explain how mature dendritic cells "
    "migrate from peripheral tissue to the draining lymph node. "
    "Name the key chemokine receptor involved."
)
SYSTEM_PROMPT = (
    "You are a concise immunology tutor. Answer accurately; if you are not "
    "sure about a fact, say so instead of guessing."
)
LOCAL_HOSTNAMES = {"localhost", "127.0.0.1", "::1"}


def normalise_host(host: str) -> str:
    """Accept 'localhost:11434' or '0.0.0.0' style OLLAMA_HOST values."""
    if not host.startswith(("http://", "https://")):
        host = "http://" + host
    parsed = urlparse(host)
    hostname = parsed.hostname or "127.0.0.1"
    if hostname == "0.0.0.0":
        hostname = "127.0.0.1"
    port = parsed.port or 11434
    return f"{parsed.scheme}://{hostname}:{port}"


def is_local(host: str) -> bool:
    return (urlparse(host).hostname or "") in LOCAL_HOSTNAMES


def check_server(host: str) -> str:
    """Return the Ollama version, or exit with a helpful message."""
    try:
        response = requests.get(f"{host}/api/version", timeout=5)
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        sys.exit(
            f"[error] Cannot reach Ollama at {host}.\n"
            "        Start it with `ollama serve` (or open the Ollama app) and retry."
        )
    except requests.exceptions.RequestException as exc:
        sys.exit(f"[error] Ollama responded unexpectedly: {exc}")
    return response.json().get("version", "unknown")


def list_models(host: str) -> list[str]:
    response = requests.get(f"{host}/api/tags", timeout=10)
    response.raise_for_status()
    return [m["name"] for m in response.json().get("models", [])]


def ensure_model(host: str, model: str) -> None:
    models = list_models(host)
    wanted = model if ":" in model else f"{model}:latest"
    if model in models or wanted in models:
        return
    available = ", ".join(models) if models else "(none)"
    sys.exit(
        f"[error] Model '{model}' is not available locally.\n"
        f"        Pull it with:  ollama pull {model}\n"
        f"        Installed models: {available}"
    )


def chat_requests(host: str, model: str, prompt: str, stream: bool,
                  temperature: float) -> dict:
    """Call /api/chat with plain HTTP. Returns the final response dict."""
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        "stream": stream,
        "options": {"temperature": temperature},
    }
    url = f"{host}/api/chat"
    if not stream:
        response = requests.post(url, json=payload, timeout=600)
        response.raise_for_status()
        data = response.json()
        print(data["message"]["content"])
        return data

    final: dict = {}
    with requests.post(url, json=payload, stream=True, timeout=600) as response:
        response.raise_for_status()
        for line in response.iter_lines():
            if not line:
                continue
            chunk = json.loads(line)
            print(chunk.get("message", {}).get("content", ""), end="", flush=True)
            if chunk.get("done"):
                final = chunk
    print()
    return final


def chat_sdk(host: str, model: str, prompt: str, stream: bool,
             temperature: float) -> dict:
    """Call the same endpoint through the official `ollama` Python SDK."""
    try:
        import ollama
    except ImportError:
        sys.exit("[error] The SDK backend needs `pip install ollama`.")

    client = ollama.Client(host=host)
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt},
    ]
    options = {"temperature": temperature}
    if not stream:
        result = client.chat(model=model, messages=messages, options=options)
        data = result.model_dump() if hasattr(result, "model_dump") else dict(result)
        print(data["message"]["content"])
        return data

    final: dict = {}
    for chunk in client.chat(model=model, messages=messages, options=options, stream=True):
        data = chunk.model_dump() if hasattr(chunk, "model_dump") else dict(chunk)
        print(data.get("message", {}).get("content", ""), end="", flush=True)
        if data.get("done"):
            final = data
    print()
    return final


def report_stats(result: dict, wall_seconds: float) -> None:
    """Print token counts and throughput from Ollama's timing fields (ns)."""
    prompt_tokens = result.get("prompt_eval_count") or 0
    output_tokens = result.get("eval_count") or 0
    eval_ns = result.get("eval_duration") or 0
    load_ns = result.get("load_duration") or 0
    tokens_per_s = output_tokens / (eval_ns / 1e9) if eval_ns else float("nan")

    print("\n--- run summary ---")
    print(f"prompt tokens     : {prompt_tokens}")
    print(f"output tokens     : {output_tokens}")
    print(f"model load time   : {load_ns / 1e9:.2f} s")
    print(f"generation speed  : {tokens_per_s:.1f} tokens/s")
    print(f"wall-clock time   : {wall_seconds:.2f} s")


def main() -> None:
    parser = argparse.ArgumentParser(description="Test local inference with Ollama.")
    parser.add_argument("--host", default=DEFAULT_HOST, help="Ollama URL (default: %(default)s)")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Model tag (default: %(default)s)")
    parser.add_argument("--prompt", default=DEFAULT_PROMPT, help="Prompt to send")
    parser.add_argument("--backend", choices=["requests", "sdk"], default="requests",
                        help="Use raw HTTP (requests) or the ollama SDK")
    parser.add_argument("--stream", action="store_true", help="Stream tokens as they are generated")
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--list", action="store_true", help="List installed models and exit")
    args = parser.parse_args()

    host = normalise_host(args.host)
    version = check_server(host)
    print(f"Ollama {version} reachable at {host}")

    if args.list:
        for name in list_models(host):
            print(f"  - {name}")
        return

    if not is_local(host):
        print(f"[warning] {host} is NOT a localhost address. Data sent to this "
              "server leaves your machine. Do not use confidential data.")

    ensure_model(host, args.model)
    print(f"Model: {args.model} | backend: {args.backend} | stream: {args.stream}\n")
    print(f">>> {args.prompt}\n")

    start = time.perf_counter()
    chat = chat_sdk if args.backend == "sdk" else chat_requests
    result = chat(host, args.model, args.prompt, args.stream, args.temperature)
    report_stats(result, time.perf_counter() - start)

    if is_local(host):
        print("\nInference ran on this machine; no prompt data left localhost.")


if __name__ == "__main__":
    main()
