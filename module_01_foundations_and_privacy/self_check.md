# Module 1 – Self-Check, Experiment & Critical Questions

Use this page after the slides and the guide. Nothing is graded, there's
no exam, and you can't fail. It's here to help you find out what stuck,
and to practise looking at AI output with healthy scepticism.

---

## Learning objectives

After this module you can:

1. **Explain** next-token prediction, tokens and context windows, and
   **predict** two failure modes that follow from them (fabrication,
   unreliable arithmetic).
2. **Compare** a cloud and a local model on capability, privacy, cost and
   reproducibility for a concrete lab task.
3. **Classify** a dataset as public, internal, confidential or restricted
   and **choose** a tool that is allowed for that class.
4. **Run and benchmark** a local model with Ollama.
5. **Explain** what an AI watermark can and cannot show, and why
   disclosing AI use is still your responsibility.

---

## Knowledge check

No pressure, nobody's watching. Try to answer before you peek.

Try to answer before opening the answer.

**1. A model gives a confident, correctly formatted reference for a claim
about CCR7. Why is that no evidence that the paper exists?**

<details><summary>Answer</summary>

The model generates the most plausible token sequence. A plausible-looking
citation (realistic authors, journal, year) is exactly what next-token
prediction produces, whether or not the paper exists. Only lookup in
PubMed/DOI resolvers is evidence.
</details>

**2. Why should an LLM not compute your fold changes or FDR values?**

<details><summary>Answer</summary>

Numbers are generated as text tokens, not calculated. The model may produce
plausible but wrong digits. Let it write code; run the code; check results.
</details>

**3. Your conversation is 150k tokens long and the model starts ignoring an
instruction you gave at the start. What is going on, and what do you do?**

<details><summary>Answer</summary>

Context degradation ("context rot", "lost in the middle"): information in
long contexts, especially in the middle, is used less reliably. Start a new
session with a short summary of what matters, or move persistent rules into
`CLAUDE.md` (Module 3).
</details>

**4. You switch Claude's "use my data for training" setting off. Does your
data still leave your machine?**

<details><summary>Answer</summary>

Yes. Training and retention settings govern what happens *after*
transmission. Only a local model avoids transmission.
</details>

**5. Classify: (a) a GEO dataset from a 2021 paper; (b) your unpublished
lipidomics matrix from BMDCs; (c) lymph node biopsy RNA-seq with donor
codes.**

<details><summary>Answer</summary>

(a) public; (b) confidential; (c) restricted. (c) never goes to a cloud LLM;
(b) only via an institution-approved contract, otherwise local.
</details>

**6. You set `temperature=0`. Are the outputs now reproducible?**

<details><summary>Answer</summary>

More consistent, not guaranteed identical: hardware, batching, and model
updates can change outputs. Record model name and version, and with local
models pin the exact tag.
</details>

**7. You paste a paragraph written by Claude into your manuscript and change
a few words. Does it still carry a watermark? And does that mean you don't
have to mention AI use?**

<details><summary>Answer</summary>

Most likely yes: the watermark is in the word choices and survives light
editing. But no: a watermark only shows that a model was probably involved.
Journals expect you to disclose AI use yourself, watermark or not.
</details>

**8. A colleague runs a student's essay through an online "AI checker",
which says 85% AI. What should you conclude?**

<details><summary>Answer</summary>

Very little. Style-based detectors are unreliable and flag non-native
English writers far more often (Liang et al. 2023). They are not the same
as a watermark check, which only the company holding the key can do. Talk
to the student instead.
</details>

**9. Is AlphaFold generative AI, an LLM, both, or neither?**

<details><summary>Answer</summary>

It is **deep learning**, and it is **not an LLM**: it is trained on protein
sequences and structures, outputs atom coordinates, and you don't chat with
it. It does share the attention mechanism with LLMs. Whether to call it
"generative" depends on the version: AlphaFold 2 predicts a structure,
AlphaFold 3 builds it with a diffusion model.
</details>

**10. Roughly how many tokens is a 750-word abstract?**

<details><summary>Answer</summary>

About 1,000 tokens (750 ÷ 0.75). Scientific terms and IDs push it a bit
higher.
</details>

**11. Where does the model "look up" the facts it gives you?**

<details><summary>Answer</summary>

Nowhere, unless it has a tool. Without tools, the answer is generated from
statistical patterns stored in its parameters during training. That's
why rare facts are shakier than common ones.
</details>

**12. What turns a base model into a helpful assistant?**

<details><summary>Answer</summary>

Post-training: instruction tuning on example conversations and preference
training (e.g. RLHF), where the model is steered toward answers that people
rate as more helpful, honest and safe.
</details>

**13. Does a 4-bit quantised model contain the same information as the
original?**

<details><summary>Answer</summary>

Not exactly. Quantisation rounds every weight to one of a few allowed
values, so the numbers are approximations of the originals. The model's
structure and behaviour stay almost the same, with a small loss in quality,
but you can't get the original numbers back. It's rounding, not zipping.
</details>

---

## Mini-experiment: how often are citations fabricated?

*Optional, but this is where it gets fun.* You treat the AI like a new
lab instrument and find out how well it actually performs. Do it in pairs
if you can; comparing results is half the fun.

Treat the model as an instrument and measure one of its error rates.

**Question.** What fraction of literature references produced by an LLM
(without search tools) are real and correctly attributed?

**Hypothesis (write yours before running).** Example: "A local 8B model
fabricates more references than a cloud flagship model."

**Method**

1. Prompt (identical for each model, public topic only):
   > List 10 peer-reviewed papers on CCR7-dependent migration of dendritic
   > cells to lymph nodes. For each give authors, year, title, journal and
   > DOI.
2. Run on a local model (`test_ollama_local.py --prompt "..."`) and, if
   allowed, on a cloud model *without* web search.
3. Verify each reference in PubMed or via `https://doi.org/<DOI>`.
4. Score each as **correct** (exists, metadata right), **partially
   correct** (exists, but wrong year/authors/DOI), or **fabricated**.

**Results table**

| Model (exact version) | Correct | Partial | Fabricated | Notes |
|-----------------------|---------|---------|------------|-------|
| | /10 | /10 | /10 | |
| | /10 | /10 | /10 | |

**Interpretation**

- With n = 10, how confident are you in any difference between models?
  (A 95% interval around 3/10 runs from roughly 7% to 65%.) What sample size
  would you need?
- Did the DOIs fail more often than titles? Why might that be?
- What does this mean for using LLMs to write introductions or literature
  reviews?

Background: Walters & Wilder (2023), *Scientific Reports* 13:14045, measured
fabricated citations in ChatGPT output. See the References page.

---

## Critical questions

No right answers here. Pick one or two that make you itch and talk them
through with a colleague over coffee.

1. "The model is right most of the time." Most of the time measured how, on
   which tasks, against which ground truth? What error rate would be
   acceptable for (a) brainstorming, (b) a figure legend, (c) a methods
   section?
2. If the provider updates a cloud model next month, can someone reproduce
   your AI-assisted analysis? What would you need to record today?
3. Is "anonymised" lipidomics data from patients really anonymous? Which
   combinations of metadata could re-identify a donor?
4. Where does the energy and cost of a cloud query end up, and does it
   matter for how we use these tools?
5. When a local model is weaker but private, and a cloud model stronger but
   transmits data, who in the lab should make that trade-off, and on what
   basis?
6. Should watermarks be visible to everyone, or is it right that only the
   AI companies (and selected organisations) can check them? Who should be
   allowed to verify?

---

## Common misconceptions

| Misconception | Better model |
|---------------|--------------|
| "It looked it up." | Without a tool, it generated text from its weights. |
| "Turning off training makes it private." | Data still leaves your machine. |
| "Local means worse at everything." | For extraction and reformatting, local models are often close. |
| "Longer context is always better." | Relevant, structured context beats volume. |
| "AI checkers can tell if text is AI-written." | Style-based detectors are unreliable and biased; only a watermark check by the company is meaningful, and even that shows likely involvement, not authorship. |

## Done when

- [ ] `test_ollama_local.py` runs and reports throughput on your machine
- [ ] Mini-experiment table filled for at least one model
- [ ] You can explain the four data classes without looking
- [ ] Your account privacy settings are checked and the date noted
