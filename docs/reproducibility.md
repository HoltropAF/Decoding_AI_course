# Reproduce the course build

The offline dashboard is built with the Python standard library. The reference
check used Python **3.14.7** and Microsoft Edge **158.0.4370.33** on Windows.
Participants only need the dashboard and a browser.

From the repository root, rebuild the file and check it:

```bash
python course/build_dashboard.py
python course/build_dashboard.py --check
```

The check compares the generated and tracked bytes and exits nonzero if the
dashboard is stale. The SHA-256 shown in the dashboard identifies the builder,
template, bundled Markdown renderer and effective course inputs. Git identifies
the checkout used for a published build. See the [source pin workflow](../CONTRIBUTING.md#under-the-hood).

## Export the slides

Use [Marp CLI 4.5.1](https://github.com/marp-team/marp-cli/releases/tag/v4.5.1).
On Windows, the standalone release can export with Edge. The commands below
assume `marp` is on your path. Run them from the repository root.

```bash
marp --browser edge --allow-local-files --pdf module_01_foundations_and_privacy/slides.md
marp --browser edge --allow-local-files --pptx module_01_foundations_and_privacy/slides.md
```

Allow local files only for slide sources you trust. The exact export layout
can vary with the browser and installed fonts.

## Run the local model example

The Module 1 smoke check used Python **3.14.7**, **requests 2.34.2** and
**Ollama 0.40.16** with its local HTTP API. The tested model was
`llama3.1:8b` (GGUF, Q4_K_M), manifest SHA-256
`46e0c10c039e019119339687c3c1757cc81b9da49709a3b3924863ba87ca666e`.

```bash
python -m pip install requests==2.34.2
ollama pull llama3.1:8b
python module_01_foundations_and_privacy/exercises/test_ollama_local.py --prompt "Reply with the word hello, then stop."
```

The model tag can move. To verify the reference model, open
`http://127.0.0.1:11434/api/tags` locally and compare the full `digest` for
`llama3.1:8b`. For the smoke check, expect a short greeting and a successful
exit. Exact output text and timing can vary. [Ollama model-list API](https://docs.ollama.com/api/tags)
