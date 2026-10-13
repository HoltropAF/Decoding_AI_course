# AI Use Log

Copy this file into `ProjectDocumentation/ai_use_log.md` of any project in
which AI tools contribute to code, analysis, figures or text. One row per
meaningful use; trivial autocomplete does not need a row.

Why: it makes AI-assisted work reproducible and reviewable, lets you write
an accurate methods/disclosure statement later, and documents that data
classification rules were followed.

## Project

- Project: <name>
- Data classification: <public | internal | confidential | restricted>
- Approved AI tools/accounts for this project: <e.g. local Ollama only; Claude Team account>

## Log

| Date | Task | Tool & exact model version | Where it ran | Data sent (class) | Prompt / skill / agent (git ref) | Verification done | Outcome used in |
|------|------|----------------------------|--------------|-------------------|----------------------------------|-------------------|-----------------|
| 2026-01-15 | Draft TIC-normalisation function | Claude Code, <model id> | Cloud (Team, training off) | Column names + synthetic rows (public) | `CLAUDE.md` v1.0.0 | Unit tests pass; compared to manual calc on 3 samples | `Processing/lipids_norm/normalise.py` |
| 2026-01-20 | Pathway annotation of DEG list | Ollama `llama3.1:8b` (digest `<sha>`) | Local | Gene symbols + log2FC (confidential) | `structured_bio_prompt.json` v1.0.0 | 10/10 spot-checked in Reactome; 2 corrected | Supplementary Table S4 (annotation column) |
| | | | | | | | |

Column notes:

- **Exact model version**: the model ID or local tag *and digest*
  (`ollama show <model> --modelfile` or `ollama list`).
- **Data sent**: describe what left your machine, not the whole dataset.
- **Verification done**: tests, recomputation, database checks, manual
  review. "Looked fine" is not verification.

## Disclosure statement (draft for the manuscript)

Note: since August 2026, text from Claude, Gemini and (in the EU) ChatGPT
may carry an invisible watermark that survives copy-paste and light
editing (see Module 1, part 4). A
watermark is not a disclosure: state your AI use yourself, whichever tool
you used.

Adapt to the journal's policy (see the References page, policy section):

> Large language model tools were used to assist with code development
> (<tool, model version>) and with the initial functional annotation of
> differentially expressed genes (<tool, model version, run locally>). All
> AI-generated code was reviewed and tested by the authors, and all
> annotations were verified against Reactome (release <n>). Prompts and
> templates are available in the code repository (<DOI/URL>). The authors
> take full responsibility for the content of this publication.
