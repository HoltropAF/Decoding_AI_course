# Track B – Local Privacy-Preserving Immunology RAG

**One-liner:** a fully offline question-answering system over a collection of
PDF papers on lymph node microenvironments and DC dynamics, with precise,
verifiable citations — and **zero bytes leaving the machine**.

**Modules used:** 1 (local models, privacy), 2 (grounding, prompt
injection), 3 (standards)
**Team size:** 2–4 · **Difficulty:** ★★☆☆ (MVP) to ★★★★ (stretch)

---

## 1. Background

Literature on DC migration (CCR7/CCL19/CCL21, lymphatic entry, conduit
networks, T-cell zone positioning) and lipid signalling in immunity is vast.
A local retrieval-augmented generation (RAG) system lets the lab query its
own curated PDF collection — including **internal reports and unpublished
drafts** that must never go to a cloud model — and get answers with page
level citations.

RAG = **retrieve** relevant passages from your documents, then **generate**
an answer that may use only those passages.

> **So what is a vector database?** It's a database built to store
> embeddings (see Module 1, part 2) and to find, very quickly, the ones closest
> to a question. You turn every chunk of your PDFs into an embedding once
> and store them; when a question comes in, you turn it into an embedding
> too and ask the database for the nearest few chunks. ChromaDB and FAISS
> are two popular options that run entirely on your own computer, which is
> exactly what this track needs.

## 2. Hard requirement: fully local

- LLM, embedding model, vector store and UI all run on the team's machine.
- Ollama bound to `127.0.0.1`; no cloud API keys present in the
  environment.
- **Prove it:** demo with networking disabled (or show a network monitor
  with no outbound traffic during queries).
- No telemetry: disable Streamlit usage stats
  (`[browser] gatherUsageStats = false` in `.streamlit/config.toml`) and
  ChromaDB anonymised telemetry (`anonymized_telemetry=False`).

## 3. Inputs

- 20–100 PDFs (open-access papers for the demo; e.g. from PubMed Central).
  Keep a `data/README.md` with the list of DOIs.
- Optional: an "internal" folder to demonstrate that confidential documents
  can be included safely (use a fake internal report for the demo).

## 4. Required features (MVP)

1. **Ingestion:** extract text per page (`pymupdf`/`pypdf`), keep metadata
   (file, title, DOI if found, page number).
2. **Chunking:** ~500–1000 tokens with overlap; never split across
   documents; store page ranges per chunk.
3. **Embedding:** local model via Ollama (`nomic-embed-text`,
   `mxbai-embed-large`) or `sentence-transformers`.
4. **Vector store:** ChromaDB (persistent, local) **or** FAISS with a
   metadata sidecar.
5. **Retrieval:** top-k similarity search (k≈5–8) with a minimum score
   threshold.
6. **Grounded generation:** prompt instructs the model to answer **only**
   from the provided passages, cite each claim as `[n]` mapped to
   file + page, and say "not found in the provided documents" when
   appropriate. Retrieved text is delimited and labelled untrusted.
7. **Streamlit UI:** question box, answer with clickable citations, an
   expandable panel showing the retrieved passages, and a model/settings
   sidebar.

## 5. Suggested architecture

```
 PDFs ──► extract (page-level) ──► chunk ──► embed (Ollama) ──► ChromaDB / FAISS
                                                                      │
 question ──► embed ──► top-k retrieve ──► (optional rerank) ─────────┘
                              │
                              ▼
        prompt: system rules + <passages>[1..k]</passages> + question
                              │
                              ▼
             Ollama LLM (llama3.1:8b / qwen2.5:14b)  ──►  answer + [n] citations
                              │
                              ▼
                     Streamlit UI (answer · sources · passages)
```

**Watch the context window.** Ollama's default context is small (often
4,096 tokens) and longer prompts are truncated silently. Eight passages of
~800 tokens plus instructions won't fit: set `num_ctx` (e.g. 16384) in
every request and check with `ollama ps`, or retrieve fewer, shorter
passages.

## 6. Stack

Python 3.11, Ollama, `pymupdf` or `pypdf`, ChromaDB or `faiss-cpu`,
Streamlit, optionally LangChain/LlamaIndex (allowed, but a hand-rolled
pipeline is often clearer and easier to debug).

## 7. Milestones

| By | Milestone |
|----|-----------|
| Day 1, 12:30 | PDFs ingested and chunked with page metadata; embeddings stored |
| Day 1, 17:30 | CLI query returns an answer with citations |
| Day 2, 12:00 | Streamlit UI; evaluation set run; offline demo verified |
| Day 2, 14:30 | Evaluation results documented |

## 8. Evaluation

Build a small **gold set** of 15–20 questions with known answers and source
pages from your PDFs (mix: factual, multi-document, and 3–4 questions whose
answer is *not* in the collection). Measure:

| Metric | Definition |
|--------|------------|
| Retrieval hit rate@k | Gold source page among retrieved chunks |
| Answer correctness | Judged by a team member (correct / partial / wrong) |
| Citation precision | Cited passage actually supports the claim |
| Abstention | Correctly says "not found" for out-of-collection questions |
| Latency | Seconds per query on your hardware |

## 9. Success criteria

- [ ] Works with networking disabled; no cloud keys in the environment.
- [ ] Every answer sentence that states a fact has a citation to file +
      page.
- [ ] Citation precision ≥ 80% on the gold set.
- [ ] Correct abstention on ≥ 3 of the out-of-collection questions.
- [ ] Re-indexing a new PDF folder is one command.
- [ ] README documents models (with tags), chunking parameters and
      evaluation results.

## 10. Stretch goals

- Hybrid retrieval (BM25 + embeddings) and a local cross-encoder reranker.
- Table and figure-caption extraction (immune cell counts, migration speeds).
- Per-document access control (public vs internal collections).
- Compare two local models and two chunk sizes on the gold set.
- Highlight the cited sentence in a PDF viewer.

## 11. Pitfalls

- Two-column PDFs and headers/footers garble text: check extraction on a
  few pages before chunking everything.
- Small local models ignore citation instructions under long contexts: keep
  k small, passages short, and give one formatted example.
- Prompt injection inside PDFs is real: keep retrieved text delimited and
  never give this pipeline tools with side effects.
