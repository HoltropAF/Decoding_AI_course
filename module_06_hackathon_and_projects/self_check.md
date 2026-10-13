# Module 6 – Evaluation Plan, Self-Check & Critical Questions

The hackathon is where the AI tools become a method in your research. Treat
your project like any experiment: decide **before building** what you will
measure, against what, and what result would count as failure.

---

## Learning objectives

After the hackathon you can:

1. **Scope** an AI-assisted research tool with measurable success criteria.
2. **Build** an end-to-end pipeline combining prompting, schemas, tools and
   agents with appropriate privacy controls.
3. **Evaluate** it against a ground truth and a simple baseline.
4. **Communicate** results and limitations honestly to wet-lab and
   computational colleagues.

---

## Evaluation plan (fill in on Day 1, before 10:00)

Copy this section into your team's `plan.md`.

```markdown
## Evaluation plan – <team / track>

**Research question:** What should the tool do, for whom?

**Primary outcome:** The one number that decides success.
  e.g. "citation precision on a 20-question gold set" (Track B)
       "fraction of zoo failures correctly diagnosed" (Track C)

**Ground truth:** Where do correct answers come from, and who made them?
  (Must exist before you look at the tool's output.)

**Baseline:** What does the simplest alternative achieve?
  e.g. same model without retrieval; classical enrichment analysis;
       a human with 10 minutes; grep over the logs.

**Success threshold:** Decided now, not after seeing results.
  e.g. "≥ 80% precision and better than baseline by ≥ 15 points"

**Secondary outcomes:** latency, cost, consistency across runs, abstention.

**Known threats to validity:**
  - Leakage (test data in the corpus or prompt examples)
  - Small n (how many test cases? what interval?)
  - Scorer bias (is the scorer blind to the condition?)
  - Cherry-picking demo examples

**Data and privacy:** data sources, data class, where the model runs.
```

---

## Knowledge check

No pressure, nobody's watching. Try to answer before you peek.

**1. Your RAG system answers 18/20 gold questions correctly. What is
missing before you can call it good?**

<details><summary>Answer</summary>

A baseline (how many does the model get *without* retrieval?), the
uncertainty around 18/20 (95% interval roughly 68–99%), whether the gold
questions were written independently of the system's development, and
whether answers were also correctly *cited*.
</details>

**2. You tuned prompts on the same 10 examples you then report results on.
What is the problem?**

<details><summary>Answer</summary>

Overfitting / test-set leakage: the reported score is optimistic. Keep a
held-out set that you only run once at the end.
</details>

**3. Why does each track require human approval before side effects?**

<details><summary>Answer</summary>

Agents can be wrong and confident, inputs can carry injected instructions,
and some actions (overwriting data, pushing code) are hard to undo.
</details>

---

## Critical questions for the demo and retrospective

No right answers here. Pick one or two that make you itch and talk them
through with a colleague over coffee.

1. Would you use this tool on your own next dataset? What would have to be
   true first?
2. What is the failure mode you are most worried about, and did your
   evaluation test it?
3. Which part of the result depends on the specific model version? What
   happens when that model is retired?
4. Did the tool save time once you count verification time?
5. What did the AI make *harder* or *worse* during the hackathon?
6. Which component is reusable (prompt template, MCP tool, subagent,
   schema) and should be contributed back to this repository?

---

## Done when

- [ ] Evaluation plan written before building and committed in `plan.md`
- [ ] Primary outcome measured on a held-out set and compared with a
      baseline
- [ ] Limitations section in the README
- [ ] Themis summary line in the README
- [ ] Retrospective notes written
