---
marp: true
theme: default
paginate: true
size: 16:9
header: 'Decoding AI · Module 5'
footer: 'Agents & Subagents'
style: |
  section { font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif; font-size: 26px; color: #1d2b36; background: #fbfcfc; }
  h1, h2 { color: #0f4c5c; }
  section.lead { background: #0f4c5c; color: #f4f8f8; }
  section.lead h1, section.lead h2 { color: #ffffff; }
  section.lead header, section.lead footer { color: #b9d3d6; }
  table { font-size: 20px; }
  code { font-size: 0.8em; }
  pre { font-size: 0.9em; }
  blockquote { border-left: 6px solid #e07a2f; color: #3a4a55; }
  .small { font-size: 19px; }
---

<!-- _class: lead -->
<!-- _paginate: false -->

# Module 5
## Agents & Subagents

Scoped, auditable delegation, and when not to use it

<!--
Recap: model (M1) + structured prompts (M2) + persistent rules (M3) + tools
(M4). Today we put them in a loop.
-->

---

## Learning objectives

1. Describe the agent loop; decide agent vs workflow
2. Explain the four properties of a subagent
3. Install, run and verify Themis
4. Evaluate an agent against a manual ground truth

---

## An agent is a model in a loop with tools

```
   goal ─► PLAN ─► SELECT TOOL ─► EXECUTE ─► OBSERVE ─► done? ─► report
             ▲                                           │ no
             └───────────────────────────────────────────┘
```

Coding agents (Claude Code and others) read, search, run and edit inside this loop.
Background: ReAct (Yao et al. 2023).

---

## Agent or workflow?

| Deterministic workflow | Agent |
|------------------------|-------|
| Steps known and fixed (QC → align → count → DESeq2) | Path depends on what is found (debugging, auditing) |
| Exact reproducibility required | Judgment over messy inputs |
| Runs unattended at scale | A human reviews the result |

Often best: a **script that calls an LLM at one step** (Module 2).

<!--
Push back on the hype here. Most lab pipelines should stay deterministic.
-->

---

## Subagents: four properties

1. **Scoped task**: one job ("audit ENCORE structure")
2. **Isolated memory**: fresh context; does not see your chat
3. **Fixed instructions**: a versioned file, same behaviour for everyone
4. **Restricted tools**: only what the job needs

---

## Why: noise reduction

![Subagent keeps the main context clean h:320](../figures/subagent_context.svg)

The 200 reads never enter your context. Your main session stays sharp.

---

## Instructions vs boundaries

> "Never edit files" in the prompt is a **request**.
> `tools: Read, Grep, Glob` is a **guarantee**.

| Tier | Tools | Risk |
|------|-------|------|
| Read-only | read, list, search | Low (still transmitted to cloud) |
| Write | edit, create | Medium (git can undo) |
| Execute / external | shell, network, push, DB writes | High |

Omit `tools:` → the agent inherits **everything**.

---

## Themis: the ENCORE auditor

- Top-level: `Data`, `Manuscript`, `Processing`, `ProjectDocumentation`,
  `Sharing`, `.navigate`; `README.md`, `0_PROJECT.md`, `2_CITATION.md`, `3_LICENSE.md`
- Empty placeholders and template text
- Undocumented subfolders (recursive)
- **Broken references** (highest priority)
- Absolute paths, vague environments, missing goals, stale log
- Reports in chat; declines to fix; marks uncertainty ❓

<!--
Open agents/themis.md and show the front matter, constraints, procedure and
output format. ENCORE: van Kampen et al., Nat Commun 2024.
-->

---

## Setup in 3 steps

```bash
mkdir -p ~/.claude/agents
cp module_05_agents_and_subagents/agents/themis.md ~/.claude/agents/
cd /path/to/encore-project && claude
```

Then `/agents` → check Themis is listed → "Use the themis agent to audit this project."

Details and Windows commands: the *Examples* step.

---

## Safety patterns

- Start **read-only, report-only**
- **Human approval** before side effects
- **Step and cost limits** (circuit breakers)
- **Separation of duties**: implementer ≠ reviewer
- **Untrusted input** never meets side-effect tools in the same step
- **Audit trail**: agent files in git; record which version produced what

---

## Exercises

1. Run Themis on a copy of the ENCORE template; verify three findings by hand
2. Ask it to fix something; confirm refusal and `git status` clean
3. Build your own read-only subagent (`exercises/build_custom_subagent.md`):
   design → write → test on planted problems → share

---

## Mini-experiment: how good is Themis?

- Plant 10 known problems in an ENCORE project copy (answer key first!)
- Run Themis twice, fresh sessions
- Recall, false positives, agreement between runs, files changed (must be 0)

Steps in `self_check.md`.

<!--
This is the same evaluation logic the hackathon will require: ground truth
before results, then measure.
-->

---

## Critical questions

- A long, confident, well-formatted report: what makes you trust it, and what *should*?
- Is reviewing the agent's output faster than doing the task?
- Themis and a human disagree. Who is right?
- An agent-made change breaks a published analysis. Who is responsible?

---

<!-- _class: lead -->

# Done when

Themis run and verified · experiment scored · your own subagent committed

**Next:** Module 6 – Hackathon
