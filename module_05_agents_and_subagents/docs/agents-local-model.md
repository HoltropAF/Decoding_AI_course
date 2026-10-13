# Running an agent with a local model

The agents here run in Claude Code, but the idea works without any cloud
service: a fixed system prompt, a fresh context, a short list of read-only
tools and a report at the end. Below is a complete version in Python with
Ollama, so nothing leaves your machine. It loads the instructions from any
of the agent files; change `AGENT` to switch between Themis and Argus.

### What you need

A local model that supports tool calling, and the `ollama` Python package.
For Themis a general model works; for Argus, a model trained on code
(such as `qwen2.5-coder`) does better.

```bash
ollama pull qwen2.5:14b
pip install ollama
```

### The whole agent in Python

```python
# subagent.py - minimal read-only subagent with a local model
from pathlib import Path
import ollama

ROOT = Path(".").resolve()
AGENT = "module_05_agents_and_subagents/agents/themis.md"   # or agents/argus.md
SYSTEM = Path(AGENT).read_text(encoding="utf-8")
SYSTEM = SYSTEM.split("---", 2)[2]          # drop the Claude Code front matter

def _safe(path: str) -> Path:
    p = (ROOT / path).resolve()
    if ROOT not in p.parents and p != ROOT:
        raise ValueError("Path outside project root")
    return p

def list_dir(path: str = ".") -> str:
    """List files and folders in a directory (read-only)."""
    p = _safe(path)
    return "\n".join(f"{'D' if c.is_dir() else 'F'} {c.relative_to(ROOT)}" for c in sorted(p.iterdir()))

def read_file(path: str) -> str:
    """Read a text file (read-only, first 20k characters)."""
    return _safe(path).read_text(encoding="utf-8", errors="replace")[:20_000]

TOOLS = {"list_dir": list_dir, "read_file": read_file}   # no write tools exist

def run_subagent(task: str, model: str = "qwen2.5:14b", max_steps: int = 40) -> str:
    messages = [{"role": "system", "content": SYSTEM},   # fixed instructions
                {"role": "user", "content": task}]        # fresh, isolated context
    for _ in range(max_steps):                            # circuit breaker
        reply = ollama.chat(model=model, messages=messages, tools=list(TOOLS.values()))
        messages.append(reply.message)
        if not reply.message.tool_calls:
            return reply.message.content                  # only the report goes back
        for call in reply.message.tool_calls:
            fn = TOOLS.get(call.function.name)
            try:
                result = fn(**call.function.arguments) if fn else "Unknown tool"
            except Exception as exc:                      # report errors to the model
                result = f"Error: {exc}"
            messages.append({"role": "tool", "content": str(result), "tool_name": call.function.name})
    return "Stopped: step limit reached."

if __name__ == "__main__":
    print(run_subagent("Audit the project in the current directory."))
```

Every property of a subagent from the chapter is in there. The fixed
instructions are `SYSTEM`, read from the same version-controlled agent
file. The isolated memory is the new `messages` list that each call starts
with, and only the final text is returned, so the noisy tool results stay
inside `run_subagent`. The restricted tools are just `list_dir` and
`read_file`, confined to the project folder; there is no write or execute
tool to misuse. And `max_steps` is the circuit breaker.

Expect weaker results than from a large cloud model: local models that fit
on a laptop are less reliable at long, multi-step work, and find the
obvious problems sooner than the subtle ones. That's still useful for
projects and code you can't send to the cloud.
