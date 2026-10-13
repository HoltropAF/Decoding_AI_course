---
marp: true
theme: default
paginate: true
size: 16:9
header: 'Decoding AI · Module 6'
footer: 'Hackathon kick-off'
style: |
  section { font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif; font-size: 26px; color: #1d2b36; background: #fbfcfc; }
  h1, h2 { color: #0f4c5c; }
  section.lead { background: #0f4c5c; color: #f4f8f8; }
  section.lead h1, section.lead h2 { color: #ffffff; }
  section.lead header, section.lead footer { color: #b9d3d6; }
  table { font-size: 20px; }
  code { font-size: 0.8em; }
  blockquote { border-left: 6px solid #e07a2f; color: #3a4a55; }
  .small { font-size: 19px; }
---

<!-- _class: lead -->
<!-- _paginate: false -->

# Module 6
## Hackathon: AI for Multi-Omics & DC Biology

Kick-off

<!--
30-minute kick-off at 09:00 on Day 1. Goal: everyone knows the rules, the
biology, their track and the evaluation requirement.
-->

---

## The biological story

How dendritic cells **sense** a stimulus, **remodel** transcriptome and lipid
membranes, **mature**, and **migrate** to the lymph node to prime T cells.

| Layer | Examples |
|-------|----------|
| Transcriptome | `Cd40`, `Cd86`, `Il12b`, `Ccr7`; NF-κB / IRF programmes |
| Lipids | Ceramides (`Sptlc2`, `Cers6`), sterols (`Hmgcr`, SREBP2), eicosanoids (`Ptgs2`) |
| Migration | CCR7 / CCL19 / CCL21, lymphatic entry, T-cell zone positioning |

<!--
Five-minute biology refresher by a lab immunologist works well here.
-->

---

## Four tracks

| Track | Build | Privacy profile |
|-------|-------|-----------------|
| **A** Multi-omics synthesis | DEGs + lipid matrix → MCP lookups → HTML report | Public/synthetic |
| **B** Local immunology RAG | Offline Q&A over PDFs with page citations | **Fully local** |
| **C** Pipeline debugger | Nextflow/Snakemake logs → diagnosis → approved patch | Synthetic failures |
| **D** DC hypothesis engine | Perturbation → structured, grounded predictions | Public literature |

Specs: `track_*/README.md`

---

## Rules

1. Public or synthetic data only (Track B local + PI approval excepted)
2. Secrets only in environment variables or git-ignored `.env`
3. Repo with `README.md`, `plan.md`, `src/`, `tests/`, environment file
4. Demo runs from a fresh clone
5. Human approval before any side effect
6. Demo what works; label mocks
7. Run Themis before code freeze

---

## Evaluate like a scientist

Before building (by 10:00), write in `plan.md`:

- **Primary outcome**: the one number that decides success
- **Ground truth**: made *before* you see outputs
- **Baseline**: what the simplest alternative achieves
- **Threshold**: decided now
- **Threats to validity**: leakage, small n, scorer bias, cherry-picking

Template: `self_check.md`.

<!--
This is the most important slide. Mentors will not approve a plan without
an evaluation section.
-->

---

## Timeline

| Day 1 | Day 2 |
|-------|-------|
| 09:00 Kick-off | 09:00 Stand-up |
| 09:30 `plan.md` + evaluation plan | 09:15 Quality + evaluation |
| 10:00 Plan review with mentor | 12:45 Stretch, docs, demo prep |
| 10:30–17:30 Build sprints (MVP end-to-end) | 14:30 **Code freeze** |
| 15:30 Stand-up | 14:45 Demos (7 + 3 min) |

---

## Judging

| Criterion | Weight |
|-----------|--------|
| Scientific value | 25% |
| Technical quality | 20% |
| Correctness & validation | 20% |
| Privacy & safety | 15% |
| Reproducibility | 10% |
| Demo & documentation | 10% |

Not about prizes: about which tools the lab should keep.

---

## Working with AI during the hackathon

- Research → plan → implement → verify (and keep `plan.md` updated)
- Lab `CLAUDE.md` in your repo
- Read-only reviewer subagent before merging
- New task → new session; keep contexts clean
- Post blockers early, with scrubbed logs

---

## Demo checklist

- The problem, in one sentence a wet-lab colleague understands
- Live run (or recorded, if labelled)
- **Evaluation result vs baseline, with n**
- Limitations and failure modes
- What should the lab keep?

---

<!-- _class: lead -->

# Go build

Plans to mentors by 10:00

<!--
Hand out the mentor slot board and the help-channel details.
-->
