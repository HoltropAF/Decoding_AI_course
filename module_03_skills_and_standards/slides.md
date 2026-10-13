---
marp: true
theme: default
paginate: true
size: 16:9
header: 'Decoding AI · Module 3'
footer: 'Skills & Standards'
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

# Module 3
## AI Skills & Operational Standards

Turning good prompts into persistent, shared team rules

<!--
Recap Module 2: five-part prompt and schema enforcement. Problem statement for
today: that good prompt disappears when the chat closes.
-->

---

## Learning objectives

1. Distinguish system prompts, `CLAUDE.md`, skills, subagents and hooks
2. Write instructions that are specific and checkable
3. Describe a versioned, reviewed workflow for team standards
4. Test whether instructions change behaviour

---

## The problem: chat knowledge evaporates

- Every session starts with an empty context window
- The model does not know our folder layout, `renv`, our DESeq2 thresholds,
  or that `Data/raw/` is untouchable
- Each person re-explains it, slightly differently, every time

**Fix:** plain-text instruction files, loaded automatically, versioned in git.

<!--
Ask: what do you find yourself telling the AI over and over? Collect three
answers; they become candidate rules for the exercise.
-->

---

## Five layers of persistent instruction

| Layer | Loaded | Use for |
|-------|--------|---------|
| System prompt | Every API call | One application or script |
| `CLAUDE.md` / `AGENTS.md` | Every session in the folder | Broad project rules |
| Skill | When the task matches | A recurring workflow |
| Subagent | When delegated | Scoped, noisy, restricted job |
| Hook | On an event, always | Must-never-fail actions |

<!--
Key distinction: everything above "hook" is a request to the model. Hooks
and permission rules are enforced by the software.
-->

---

## Choosing the layer

- Applies to almost every task → **`CLAUDE.md`**
- Occasional, multi-step workflow → **skill**
- Noisy, scoped, needs fewer permissions → **subagent** (Module 5)
- Must happen every time → **hook** or permission rule

> The model can forget an instruction. It cannot forget a hook.

---

## Good rules are checkable

| Vague | Checkable |
|-------|-----------|
| Write portable code | Use `pathlib` / `here::here()`; never `setwd()` or absolute paths |
| Be careful with data | Never modify `Data/raw/`; write outputs to `Processing/<analysis>/output/` |
| Make it reproducible | Pin dependencies (`renv.lock`); set and record seeds |
| Test your code | Run `pytest -q`; report the result; never claim success unrun |

Short file (< 200 lines) · exact commands · the *why* in one clause · no secrets.

---

## The lab template

`templates/CLAUDE.md` covers:

- ENCORE structure and golden rules
- Python and R conventions
- Omics conventions: identifiers, LIPID MAPS shorthand, DE thresholds,
  normalisation, multiple testing, units
- Testing, reproducibility, git, data & privacy

Fill in the **Project-specific** block; delete what does not apply.

<!--
Open the template on screen and walk through the sections quickly. Point out
the omics section; that is where the lab-specific value is.
-->

---

## Skills

```markdown
---
name: deg-report
description: Generate the lab's standard DE report from a DESeq2 table.
  Use when asked for a DE report, volcano plot or DEG summary.
---
1. Require columns gene, log2FoldChange, padj ...
2. Thresholds padj < 0.05, |log2FC| > 1 unless specified ...
3. Volcano + MA plot + summary table → Processing/<analysis>/output/
```

Activation is not guaranteed: specific description, or invoke `/deg-report`.

---

## Team standards workflow

1. One source of truth (this repo) for `CLAUDE.md`, skills, agents
2. Projects copy the template and add a short project section
3. Changes via pull request with a one-line reason
4. Version line in the file; projects note their starting version
5. Quarterly pruning: delete what nobody needs

Prompts are code: version them, review them, test them.

---

## Security checkpoint

- No credentials, tokens or internal hostnames in instruction files;
  only environment variable *names*
- No real data in examples
- `CLAUDE.md` is sent to the provider every session: same data-class rules
- Review third-party skills before installing: they are instructions your
  agent will follow

---

## Exercise

1. Copy `templates/CLAUDE.md` into a copy of the ENCORE template; fill in the project block
2. Fresh session: "Summarise the rules you will follow in this project"
3. Ask for a small function (e.g. TIC normalisation of a lipid table)
4. Check: paths, tests, documentation rules followed?
5. Stretch: turn one recurring task into a skill

---

## Mini-experiment: does it change behaviour?

- Same 3 coding tasks, fresh sessions, **with** vs **without** `CLAUDE.md`
- Score a 6-item rubric (paths, raw data, seeds, dependencies, tests, docs)
- Rules followed without the file → delete them
- Rules ignored with the file → enforce them (hook, permission, test)

Rubric in `self_check.md`.

---

## Critical questions

- When does a lab standard hide better methods?
- Should the `CLAUDE.md` behind a published analysis be deposited with the code?
- A rule followed 90% of the time: good enough for "never modify raw data"?
- How would you review a third-party skill?

---

<!-- _class: lead -->

# Done when

A filled `CLAUDE.md` · three rules followed in a fresh session · rubric scored

**Next:** Module 4 – MCP & Data
