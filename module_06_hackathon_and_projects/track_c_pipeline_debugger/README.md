# Track C – Automated Pipeline Debugger & Log Analyzer

*Nextflow and chill, until the cluster crashes: every bioinformatician's
weekend plans. Or: dependency hell, and how to escape it with AI.*

**One-liner:** an agent that reads failed bioinformatics pipeline runs
(Nextflow, Snakemake, plain Python/R scripts), pinpoints the failing step and
root cause, proposes a verified code patch, and re-runs the task — with a
human approving every change.

**Modules used:** 2 (structured output), 3 (CLAUDE.md), 4 (tools,
sandboxing), 5 (agents, HITL)
**Team size:** 2–4 · **Difficulty:** ★★★☆

---

## 1. Background

Pipeline failures cost the lab hours: a Snakemake rule that dies on a
missing column, a Nextflow process that runs out of memory, a Python script
whose sample sheet order no longer matches the count matrix. The
information to diagnose them is in the logs, but scattered across
`.nextflow.log`, `work/<hash>/.command.err`, `.snakemake/log/*.log` and
tracebacks. An agent can do the tedious triage; a human decides on the fix.

## 2. Inputs

A **failure zoo**: a set of small, deliberately broken pipelines with
synthetic data, created by the team (and swapped between teams for
evaluation). Include at least these failure classes:

| # | Class | Example |
|---|-------|---------|
| 1 | Syntax/runtime error | Typo in a Python function name; R `object not found` |
| 2 | Data alignment | Sample sheet order ≠ count matrix column order; duplicated gene IDs |
| 3 | Schema/format | Lipid table with renamed column (`log2FC` → `logFC`); wrong delimiter |
| 4 | Missing file / path | Hardcoded absolute path; missing input in Snakemake rule |
| 5 | Resources | Nextflow process exceeding memory (exit 137) |
| 6 | Environment | Missing package/version conflict in conda env |
| 7 | Silent error | Pipeline "succeeds" but output has all-NaN column (detected by a check) |

Each zoo case has a `EXPECTED.md` with the true root cause and fix (hidden
from the agent).

## 3. Required features (MVP)

1. **Log collection:** given a run directory, locate relevant logs per
   engine:
   - Nextflow: `.nextflow.log`, failing task `work/*/.command.{err,out,sh}`,
     exit status.
   - Snakemake: `.snakemake/log/*.snakemake.log`, rule-specific logs.
   - Scripts: captured stderr/stdout and exit code.
2. **Parsing:** extract failing step, exit code, traceback/last error lines,
   and the relevant source files into a structured `FailureReport`
   (Pydantic).
3. **Diagnosis:** LLM produces a structured diagnosis: failure class (from
   the table), root cause, evidence (quoted log lines with file:line), and
   confidence.
4. **Patch proposal:** a unified diff restricted to code/config files (never
   data, never `Data/raw/`).
5. **Human-in-the-loop:** show diagnosis + diff; apply **only** after
   explicit approval (`[y/N]`).
6. **Verification:** after applying, re-run the failing step (or a dry run /
   test) in a sandbox and report pass/fail. On failure, at most N further
   attempts, then stop (circuit breaker).
7. **Audit log:** JSON lines file of every tool call, diagnosis, diff,
   approval decision and re-run result.

## 4. Suggested architecture

```
 run dir ──► collector (engine-specific) ──► parser ──► FailureReport (JSON)
                                                          │
                                                          ▼
                                  diagnosis agent (read-only tools: read_file, grep, list)
                                                          │  Diagnosis + Patch (JSON + diff)
                                                          ▼
                                  HUMAN APPROVAL  ──no──► stop, save report
                                                          │ yes
                                                          ▼
                       apply patch on a git branch ──► sandboxed re-run (Docker/conda, no network)
                                                          │
                                         pass ──► summary + audit log
                                         fail ──► retry (max N) ──► stop
```

Separation of duties: the **diagnosis agent is read-only**. Applying the
patch and re-running are done by deterministic code after human approval,
not by the model.

## 5. Stack

Python 3.11, `subprocess`, pydantic, `unidiff`/`git apply`, Docker or a
dedicated conda env for re-runs; Claude API / Claude Agent SDK or Ollama
(`qwen2.5-coder:14b`); Snakemake and Nextflow installed for the zoo.
Optional: Claude Code with a project-level read-only diagnosis subagent
(Module 5 pattern) plus hooks.

## 6. Milestones

| By | Milestone |
|----|-----------|
| Day 1, 12:30 | Failure zoo with ≥ 5 cases; collector + parser for one engine |
| Day 1, 17:30 | Diagnosis JSON for all cases; patch proposal for class 1–3 |
| Day 2, 12:00 | Approval flow, sandboxed re-run, audit log; second engine |
| Day 2, 14:30 | Evaluation on another team's zoo documented |

## 7. Success criteria

- [ ] Correct failure class and root cause for ≥ 70% of zoo cases
      (scored against `EXPECTED.md`).
- [ ] Automatically diagnoses a broken matrix processing script (data
      alignment or schema case), proposes a fix, and — after approval —
      re-runs it successfully.
- [ ] No file is modified without explicit approval; patches never touch
      data files (enforced in code and tested).
- [ ] Every diagnosis quotes concrete log evidence with file:line.
- [ ] Retry limit enforced; audit log complete.
- [ ] Re-runs execute in a sandbox without network access.

## 8. Stretch goals

- Watch mode: monitor a running pipeline and trigger on failure.
- Support both Nextflow and Snakemake plus R scripts.
- Regression test generation: for each fix, generate a test that fails
  before and passes after.
- Knowledge base of past failures (local RAG over previous audit logs).
- Post the diagnosis as a draft (not sent) issue/PR description.

## 9. Pitfalls

- Logs contain absolute paths, usernames and sometimes data rows: scrub
  before sending to a cloud model (Module 1 helpers).
- Long logs blow up context: send the tail, the error block and the
  relevant source excerpt, not entire logs.
- "Fixes" that silence errors (e.g. `try/except: pass`, dropping NaN rows
  without reason) are failures — reject them in the evaluation.
- Never let the model run arbitrary shell commands; whitelist the re-run
  command.
