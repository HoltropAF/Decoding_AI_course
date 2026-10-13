# Module 5 – Self-Check, Experiment & Critical Questions

---

## Learning objectives

After this module you can:

1. **Describe** the agent loop (plan → act → observe → refine) and
   **decide** between an agent and a deterministic workflow.
2. **Explain** the four defining properties of a subagent: scoped task,
   isolated memory, fixed instructions, restricted tools.
3. **Install, run and verify** a read-only subagent (Themis).
4. **Evaluate** an agent quantitatively against a manual ground truth.
5. **Check** a research-mode report: read its sources, verify the key
   claims, and ask what's missing.

---

## Knowledge check

No pressure, nobody's watching. Try to answer before you peek.

**1. Your DESeq2 analysis always runs the same 6 steps. Agent or script?**

<details><summary>Answer</summary>

Script/workflow. Fixed steps, exact reproducibility and unattended runs are
the strengths of deterministic code. Agents are for paths that depend on
what is found.
</details>

**2. You tell a subagent "check the issue we discussed earlier". Why does
it fail?**

<details><summary>Answer</summary>

It has isolated memory: it never saw your main conversation. Delegations
must be self-contained (what, where, what to return).
</details>

**3. Themis's instructions say "never edit files". What actually guarantees
that?**

<details><summary>Answer</summary>

Its tool list: `tools: Read, Grep, Glob`. It has no tool that can write. The
instruction expresses intent; the tool restriction enforces it.
</details>

**4. What happens if you omit the `tools:` line in an agent file?**

<details><summary>Answer</summary>

The agent inherits all tools available to the main session, including edit
and shell access.
</details>

**5. Name two safety patterns for agents that run longer loops.**

<details><summary>Answer</summary>

Human approval before side effects; step/cost limits (circuit breakers);
separation of duties (implementer vs read-only reviewer); audit logs.
</details>

**6. What's the difference between a chatbot and an agent?**

<details><summary>Answer</summary>

A chatbot answers in text. An agent can also act through tools: read and
edit files, run code, search. More power, so more care needed.
</details>

---

## Mini-experiment: how good is Themis?

*Optional, but this is where it gets fun.* You treat the AI like a new
lab instrument and find out how well it actually performs. Do it in pairs
if you can; comparing results is half the fun.

**Question.** What are Themis's recall and precision on known ENCORE
problems, and is it consistent between runs?

**Hypothesis (write yours first).** Example: "Themis finds ≥ 80% of planted
problems with ≤ 2 false positives, and two runs agree on ≥ 90% of
findings."

**Method**

1. Copy the ENCORE template project (or a finished project whose content is
   already public) to a scratch folder and initialise git so you can confirm
   nothing changes. Not an unpublished project: Themis runs on a cloud model.
2. Plant 10 problems and write them in an answer key **before** running:
   - delete `2_CITATION.md`
   - leave `0_PROJECT.md` with template text only
   - add `Processing/new_analysis/` without README
   - add `Data/processed/lipids/` without README
   - in a README, link to `Processing/old_name/` that does not exist
   - in a README, reference script `run_all.R` that does not exist
   - add `setwd("C:/Users/someone/project")` to an R script
   - add `/home/someone/data/counts.csv` to a Python script
   - remove the environment file (`renv.lock`/`environment.yml`)
   - add a code file newer than the last `0_PROJECT.md` log entry
3. Run Themis twice in two fresh sessions.
4. Score:

| Metric | Run 1 | Run 2 |
|--------|-------|-------|
| Planted problems found (recall) | /10 | /10 |
| False positives | | |
| Findings shared by both runs | | |
| Files changed (`git status`) | must be 0 | must be 0 |

**Interpretation**

- Which planted problem types were missed? Is that a limitation of the
  instructions, the tools, or the model?
- Is a false positive costly here (wasted 2 minutes) or harmless? How does
  that change for an agent that edits code?
- What would you change in `themis.md`, and how would you show that the
  change helped (re-run the same benchmark)?

---

## Critical questions

No right answers here. Pick one or two that make you itch and talk them
through with a colleague over coffee.

1. An agent produces a long, confident, well-formatted report. What makes
   you trust it, and what *should* make you trust it?
2. Automation shifts work from doing to reviewing. Is reviewing an agent's
   output actually faster than doing the task, for this task?
3. If Themis and a human disagree on whether a folder is documented, who is
   right? What does that say about the standard itself?
4. When an agent-generated change causes an error in a published analysis,
   who is responsible?
5. Which tasks in your own work are noisy and repetitive enough to justify
   a subagent, and which should stay manual on purpose?

---

## Common misconceptions

| Misconception | Better model |
|---------------|--------------|
| "Subagents are smarter." | They are organised: fresh context, focused instructions, fewer tools. |
| "An instruction is a permission boundary." | Only the tool list and permission rules are boundaries. |
| "More autonomy is the goal." | The goal is reliable results; autonomy is a cost to justify. |

## Done when

- [ ] Themis installed and visible in `/agents`
- [ ] Themis run on a project; three findings verified by hand
- [ ] Mini-experiment scored for at least one run
- [ ] Your own read-only subagent committed (see `exercises/build_custom_subagent.md`)
