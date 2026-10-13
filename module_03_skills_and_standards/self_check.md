# Module 3 – Self-Check, Experiment & Critical Questions

---

## Learning objectives

After this module you can:

1. **Distinguish** system prompts, `CLAUDE.md`, skills, subagents and hooks,
   and **choose** the right one for a given rule or workflow.
2. **Write** persistent instructions that are specific and checkable.
3. **Describe** a versioned, reviewed workflow for shared team standards.
4. **Test** whether a set of instructions actually changes model behaviour.
5. **Set up** standing instructions in the chat app you use (custom
   instructions, a Project or a Gem), even without any coding.

---

## Knowledge check

No pressure, nobody's watching. Try to answer before you peek.

**1. Where does each belong: (a) "Never modify `Data/raw/`"; (b) the
lab's 12-step DE report procedure; (c) "run `ruff` after every Python
edit"; (d) auditing a project's documentation?**

<details><summary>Answer</summary>

(a) `CLAUDE.md` (applies to every task), ideally also a permission deny
rule; (b) skill (recurring, occasional workflow); (c) hook (must happen
every time, deterministic); (d) subagent (noisy, scoped, read-only).
</details>

**2. Rewrite as a checkable rule: "Write reproducible R code."**

<details><summary>Answer</summary>

For example: "Manage packages with `renv` and commit `renv.lock`; use
`here::here()` for paths, never `setwd()`; call `set.seed()` before any
random step and record the seed in the output."
</details>

**3. Why keep `CLAUDE.md` short?**

<details><summary>Answer</summary>

It is loaded into the context of every session. Long files cost tokens and
dilute attention, so important rules are followed less reliably.
</details>

**4. A skill exists in `.claude/skills/` but Claude never uses it. Name two
causes and two fixes.**

<details><summary>Answer</summary>

Causes: vague `description`, task wording that does not match, too many
competing skills. Fixes: specific "Use when…" description, invoke it
explicitly (`/skill-name`), or enforce activation with a hook.
</details>

**5. Is it acceptable to put the read-only database password in
`CLAUDE.md` because the repo is private?**

<details><summary>Answer</summary>

No. `CLAUDE.md` is sent to the model provider every session and private
repos get shared, forked or made public. Reference the environment variable
name only.
</details>

---

## Mini-experiment: does the CLAUDE.md change behaviour?

*Optional, but this is where it gets fun.* You treat the AI like a new
lab instrument and find out how well it actually performs. Do it in pairs
if you can; comparing results is half the fun.

**Question.** How much does the lab `CLAUDE.md` improve adherence to our
coding standards?

**Hypothesis (write yours first).** Example: "With the `CLAUDE.md`,
adherence on a 6-item rubric rises from ≤ 2 to ≥ 5 items."

**Method**

1. Create two copies of a small scratch project: **A** without and **B**
   with `templates/CLAUDE.md` (filled in).
2. In a *fresh* Claude Code session in each, give the same three tasks:
   - "Write a Python function that normalises a lipid intensity table to
     total ion count and saves the result."
   - "Write an R script that runs DESeq2 on `counts.csv` with sample sheet
     `samples.csv`."
   - "Add a step that clusters samples with k-means and plots them."
3. Score each output with the rubric (1 = followed, 0 = not):

| Rubric item | A1 | A2 | A3 | B1 | B2 | B3 |
|-------------|----|----|----|----|----|----|
| Relative paths only (no absolute paths/`setwd`) | | | | | | |
| Does not write into `Data/raw/` | | | | | | |
| Seed set and recorded for random steps | | | | | | |
| Dependencies declared, not installed in script | | | | | | |
| Tests added or proposed | | | | | | |
| Documentation (docstring/README/parameters) | | | | | | |
| **Total /6** | | | | | | |

**Interpretation**

- With 3 tasks per condition, what can and can't you conclude? What would
  you change to make this a fair comparison (blinding the scorer,
  randomising order, more tasks)?
- Which rules were followed without the file (the model's defaults)? Those
  are candidates to delete from `CLAUDE.md`.
- Which rules were ignored even with the file? Those need a hook,
  permission rule or test instead.

---

## Critical questions

No right answers here. Pick one or two that make you itch and talk them
through with a colleague over coffee.

1. Persistent instructions encode one group's preferences. When does a lab
   standard become a constraint that hides better methods?
2. If a published analysis depended on a `CLAUDE.md` or skill, should that
   file be part of the code deposited with the paper?
3. How do you notice when a rule has become stale (e.g. a renamed folder)?
   Who is responsible for pruning?
4. Skills from third parties are instructions your agent will follow. How
   would you review one before installing it?
5. A rule is followed 90% of the time. Is that good enough for "never
   modify raw data"? What does that imply about instructions vs
   enforcement?

---

## Common misconceptions

| Misconception | Better model |
|---------------|--------------|
| "Put everything in `CLAUDE.md`." | Short, broad rules there; workflows in skills; guarantees in hooks/permissions. |
| "If it's written down, it's followed." | Measure adherence; enforce what must never fail. |
| "Prompts aren't code." | Version, review and test them like code. |

## Done when

- [ ] A filled-in `CLAUDE.md` in one of your projects
- [ ] A fresh session demonstrably follows at least three rules
- [ ] Mini-experiment rubric scored for at least one task per condition
- [ ] One rule deleted or moved because the experiment showed it was not
      needed or not followed
