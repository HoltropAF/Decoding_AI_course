# Track A – Multi-Omics Synthesis Agent

**One-liner:** an agent that takes an RNA-seq DEG list and a lipid change
matrix from the same experiment, looks up pathway context through MCP tools,
and produces an interactive HTML report linking gene expression changes to
lipid remodelling.

**Modules used:** 2 (structured output), 3 (CLAUDE.md), 4 (MCP), 5 (agents)
**Team size:** 2–4 · **Difficulty:** ★★★☆

---

## 1. Background

When DCs are activated (e.g. by LPS via TLR4), their transcriptome and lipid
composition shift together: sphingolipid/ceramide synthesis enzymes,
cholesterol biosynthesis (SREBP2 targets), and eicosanoid pathways
(`Ptgs2` → prostaglandins) change alongside maturation markers (`Cd40`,
`Cd86`, `Ccr7`). Analysts usually inspect the two layers separately and link
them by hand. This track automates the first draft of that synthesis —
**grounded in database lookups, not model memory**.

## 2. Inputs

| Input | Format | Example columns |
|-------|--------|-----------------|
| DEG table | CSV/TSV | `gene`, `log2FoldChange`, `padj` (DESeq2-style) |
| Lipid change matrix | CSV/TSV | `lipid` (LIPID MAPS shorthand, e.g. `Cer d18:1/16:0`), `class`, `log2FC`, `padj` (optionally per time point) |
| Metadata | YAML | organism, cell type, stimulus, time point, thresholds |

Use public data (GEO + MetaboLights/Metabolomics Workbench) or the provided
synthetic generator approach (Module 1 docs, section 3.1). Add a
`data/README.md` describing the source.

## 3. Required features (MVP)

1. **Ingest & validate** both tables (column checks, identifier types,
   thresholds from metadata).
2. **MCP tool server** (Python, FastMCP) exposing at least:
   - `pathways_for_gene(symbol, species)` → Reactome (and/or KEGG) pathways
   - `lipid_class_info(lipid_name)` → LIPID MAPS classification
     (category/main class/subclass)
   - `enzymes_for_lipid_class(class)` → genes encoding key synthesis/
     degradation enzymes (Reactome/Rhea, or a curated local table)
   All tools read-only, with caching (e.g. `requests-cache`/SQLite) to stay
   polite to public APIs.
3. **Linking step**: match DEGs encoding lipid-metabolism enzymes to
   changed lipid classes (e.g. ↑`Cers6` + ↑`Cer d18:1/16:0`), producing
   explicit gene–lipid links with direction concordance.
4. **Structured interpretation**: LLM produces a JSON report validated by a
   Pydantic schema (pathway themes, gene–lipid links, confidence, caveats).
   Every gene and lipid in the output must exist in the inputs (semantic
   check as in Module 2).
5. **HTML report** (Jinja2) with: summary, sortable tables of DEGs and lipid
   classes, a gene–lipid link table with database links, at least one
   interactive plot (Plotly: volcano or class-level bar chart), and a
   provenance section (model, version, tool calls, timestamps, input hashes).

## 4. Suggested architecture

```
 degs.csv ─┐                         ┌──────────── MCP server (read-only) ─────────┐
 lipids.csv┼─► loader/validator ──►  │ pathways_for_gene · lipid_class_info ·      │
 meta.yaml ┘          │              │ enzymes_for_lipid_class  (+ local cache)    │
                      ▼              └──────────────────────▲──────────────────────┘
              deterministic linker ──────── tool calls ─────┤
                      │                                     │
                      ▼                                     │
            LLM synthesis (Claude API or Ollama) ───────────┘
                      │  JSON (Pydantic-validated)
                      ▼
            Jinja2 + Plotly HTML report  ──►  report.html + report.json
```

Design principle: **do deterministic work in code** (filtering, matching
enzymes to classes, statistics) and use the LLM for **interpretation and
narrative**, grounded in tool results.

## 5. Stack

Python 3.11, pandas, pydantic, `mcp` (FastMCP), requests + requests-cache,
Jinja2, Plotly; Claude API (Claude Agent SDK or Messages API with MCP) or
Ollama (`qwen2.5:14b`/`llama3.1:8b` with tool calling).

## 6. Milestones

| By | Milestone |
|----|-----------|
| Day 1, 12:30 | Both tables load and validate; one MCP tool returns real Reactome data |
| Day 1, 17:30 | End-to-end: inputs → tool calls → validated JSON → basic HTML |
| Day 2, 12:00 | Gene–lipid linking, interactive plots, provenance, tests |
| Day 2, 14:30 | Evaluation vs success criteria documented |

## 7. Success criteria

- [ ] Runs end-to-end from a fresh clone with one command
      (`python -m synth --degs ... --lipids ... --meta ...`).
- [ ] Correctly links at least one sphingolipid/ceramide shift and one
      sterol or eicosanoid shift to concordant enzyme-gene changes in the
      demo data (verified by a team member against Reactome/LIPID MAPS).
- [ ] Links DC activation markers (e.g. `Cd40`, `Cd86`, `Ccr7`, `Il12b`) to
      the maturation theme in the report.
- [ ] 0 invented genes/lipids in the output (semantic check passes);
      every pathway in the report traceable to a tool call.
- [ ] MCP server is read-only and has no access to anything except public
      APIs and the input folder.
- [ ] Unit tests for loader, linker and schema validation.

## 8. Stretch goals

- Time-course support (multiple time points; trend classes).
- Switch between cloud and local model via a flag and compare report quality.
- Network view (gene–enzyme–lipid graph with `pyvis` or Cytoscape.js).
- Add metabolomics (HMDB lookup tool) as a third layer.
- Export a "methods paragraph" draft describing exactly what was done.

## 9. Pitfalls

- Lipid name parsing is messy: normalise to LIPID MAPS shorthand before
  lookup; log unparsable names instead of dropping them silently.
- Public APIs rate-limit: cache everything; never call in a tight loop.
- Mouse vs human symbols: set species explicitly in every tool call.
- Do not let the LLM compute statistics — pass computed values in.
