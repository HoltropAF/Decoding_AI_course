# Module 2 – Self-Check, Experiment & Critical Questions

---

## Learning objectives

After this module you can:

1. **Write** a five-part prompt (Role, Context, Instruction, Inputs,
   Constraints) for a biological analysis request.
2. **Choose** a prompting technique (few-shot, chain-of-thought,
   self-consistency, prompt chaining) for a given problem and **test**
   whether it helped, using a small test set.
3. **Explain** the three layers of JSON enforcement and **implement**
   schema validation with Pydantic.
4. **Design** semantic checks that a schema cannot express (e.g. no invented
   genes).
5. **Measure** the validity and run-to-run consistency of an LLM step in a
   pipeline.

---

## Knowledge check

No pressure, nobody's watching. Try to answer before you peek.

**1. Why wrap your gene list in `<genes>…</genes>` tags?**

<details><summary>Answer</summary>

Delimiting separates data from instructions, so the model does not confuse
the two, and it is a first defence against instructions hidden in inputs
(prompt injection).
</details>

**2. The API's structured-output mode guarantees valid JSON. Why still
validate in code?**

<details><summary>Answer</summary>

Constrained decoding guarantees *syntax and schema*, not *truth*. The JSON
can be valid and still contain invented genes, wrong directions, or
pathways that do not contain the listed genes. Semantic checks and spot
checks against databases catch those.
</details>

**3. What is the difference between few-shot prompting and
chain-of-thought?**

<details><summary>Answer</summary>

Few-shot gives worked input→output examples to copy format and level of
detail. Chain-of-thought asks for step-by-step reasoning before the answer,
which helps on multi-step logic. They can be combined.
</details>

**4. Your schema has `"confidence": "high" | "medium" | "low"`. Is the model's
confidence calibrated?**

<details><summary>Answer</summary>

Not necessarily. Self-reported confidence is another generated token and is
often poorly calibrated. Treat it as a weak signal and measure calibration
(does "high" correspond to higher accuracy?) before relying on it.
</details>

**5. Which value of `temperature` do you use for extracting pathways, and
why?**

<details><summary>Answer</summary>

Low (0–0.2): you want the most probable, consistent output, not creative
variation.
</details>

**6. You put "never invent genes" in the prompt. Why is that not enough?**

<details><summary>Answer</summary>

Instructions reduce but do not eliminate violations. Enforce it in code
(`semantic_check` in `extract_deg_pathways.py`) and retry on failure.
</details>

**7. A colleague adds "You are a Nobel-prize-winning immunologist" to every
prompt. Does that make the answers more accurate?**

<details><summary>Answer</summary>

Probably not. A large study (Zheng et al., 162 personas, 2,410 questions)
found personas don't improve factual accuracy. A role sets tone and
vocabulary; correctness comes from context, constraints and checking.
</details>

**8. Your pathway prompt works on today's gene list. What do you need before
you can say it "works" in general?**

<details><summary>Answer</summary>

A small test set of inputs with known answers (including awkward cases), a
written definition of "better", and results from more than one run. Then
change one thing at a time and log the effect.
</details>

**9. Why can the *format* of a prompt matter when the meaning stays the same?**

<details><summary>Answer</summary>

The model predicts continuations from everything it sees, including
punctuation, labels and the order of examples. Sclar et al. (2023) found
accuracy differences of up to 76 points from formatting alone in some
models. Modern models are less sensitive, but not immune.
</details>

**10. Why are output tokens slower (and pricier) than input tokens?**

<details><summary>Answer</summary>

The input is processed in parallel in one pass. The output has to be
generated one token at a time, each step depending on the previous one.
</details>

**11. You correct the model in a chat and it says "you're right!". Has the
model learned something for next time?**

<details><summary>Answer</summary>

No. The model's parameters don't change during use. The correction only
exists in this conversation's context; a new chat starts without it
(unless the app's memory feature saves a note).
</details>

---

## Mini-experiment: validity and consistency of an LLM pipeline step

*Optional, but this is where it gets fun.* You treat the AI like a new
lab instrument and find out how well it actually performs. Do it in pairs
if you can; comparing results is half the fun.

**Question.** How often does the pathway extraction produce valid output on
the first attempt, and how similar are the pathway sets between repeated
runs?

**Hypotheses (write yours first).** Example: "Schema-constrained decoding
raises first-attempt validity; higher temperature lowers between-run
consistency."

**Method** (built-in synthetic DEG list, local model)

```bash
cd module_02_prompting_and_context/exercises
for i in 1 2 3 4 5; do python extract_deg_pathways.py --output run_schema_$i.json; done
for i in 1 2 3 4 5; do python extract_deg_pathways.py --no-schema --output run_noschema_$i.json; done
for i in 1 2 3 4 5; do python extract_deg_pathways.py --temperature 0.9 --output run_hot_$i.json; done
```

Each output file records `attempts` in its `provenance` block. Then compute
consistency:

```python
import json, glob, itertools, statistics

def pathway_set(path):
    report = json.load(open(path))["report"]
    return {p["name"].lower() for p in report["pathways"]}

for label in ["schema", "noschema", "hot"]:
    files = sorted(glob.glob(f"run_{label}_*.json"))
    sets = [pathway_set(f) for f in files]
    attempts = [json.load(open(f))["provenance"]["attempts"] for f in files]
    jacc = [len(a & b) / len(a | b) for a, b in itertools.combinations(sets, 2) if a | b]
    print(f"{label:9s} first-attempt valid: {sum(a == 1 for a in attempts)}/{len(files)} "
          f"| mean Jaccard: {statistics.mean(jacc):.2f}")
```

**Results table**

| Condition | First-attempt valid | Mean retries | Mean Jaccard (pathway sets) |
|-----------|--------------------|--------------|-----------------------------|
| Schema, T=0.1 | /5 | | |
| No schema, T=0.1 | /5 | | |
| Schema, T=0.9 | /5 | | |

Runs that fail after all retries stop the script and produce no file. Count
them as invalid.

**Interpretation**

- Exact string matching of pathway names underestimates agreement
  ("Toll-like receptor signaling pathway" vs "TLR signaling"). How would you
  match on database identifiers instead?
- If two runs disagree, which one is right? What is your ground truth?
- What level of consistency would you require before an LLM step goes into
  a pipeline whose output appears in a paper?

---

## Critical questions

No right answers here. Pick one or two that make you itch and talk them
through with a colleague over coffee.

1. A schema-valid, consistent answer can still be biologically wrong. What
   is the cheapest independent check you could add (e.g. overrepresentation
   analysis with `clusterProfiler`/`gseapy`) and how would you compare the
   two?
2. Is LLM pathway annotation better than classical enrichment analysis, or
   a different thing? When would you use each?
3. Your prompt says the cells are "BMDCs stimulated with LPS". How much
   does that context steer the output toward what you expect to see? How
   would you test for that bias (hint: shuffle or mislabel the context)?
4. Who owns a prompt template that produced a published result, and where
   should it be archived?
5. If a reviewer asks "how do you know the model didn't just tell you what
   you wanted to hear?", what evidence would you show?

---

## Common misconceptions

| Misconception | Better model |
|---------------|--------------|
| "Valid JSON = correct answer." | Valid structure, unverified content. |
| "More instructions = better output." | Clear, specific, delimited instructions beat long ones. |
| "Confidence field = probability." | Uncalibrated until measured. |
| "Same prompt = same answer." | Measure consistency; do not assume it. |

## Done when

- [ ] `pathways.json` produced and validated
- [ ] Mini-experiment table filled for at least two conditions
- [ ] Three pathway assignments checked by hand in Reactome or KEGG
- [ ] You can name the three enforcement layers and what each does *not*
      guarantee
