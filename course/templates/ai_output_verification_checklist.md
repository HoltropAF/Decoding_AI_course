# AI Output Verification Checklist

Use before AI output goes into code you rely on, an analysis, a figure, a
manuscript or a decision. Scale the effort to the stakes: a brainstorm
needs little; a methods section needs all of it.

## 1. Claims and facts

- [ ] Every factual claim is either common knowledge in the field or traced
      to a source I have opened myself
- [ ] Every citation resolves (DOI/PubMed) **and** says what it is cited for
- [ ] Gene, protein, lipid and metabolite identifiers exist and match the
      organism (Ensembl/MGI/HGNC, LIPID MAPS, HMDB)
- [ ] Pathway memberships checked in the database (with release noted)

## 2. Numbers

- [ ] No number comes from the model's text; all are produced by code I can
      run
- [ ] Results recomputed or sanity-checked on a small example (manual
      calculation, known positive control)
- [ ] Units, scales (log2 vs linear) and thresholds are stated and correct
- [ ] Multiple-testing correction applied where needed

## 3. Code

- [ ] I understand what every non-trivial line does
- [ ] Tests exist and pass, including edge cases (NaN, zeros, duplicated
      IDs, sample order)
- [ ] No hardcoded absolute paths, secrets or writes to raw data
- [ ] Dependencies declared and versions pinned
- [ ] Output compared with an independent method on at least one dataset

## 4. Reasoning and interpretation

- [ ] The conclusion follows from the evidence shown, not from the
      framing of my prompt
- [ ] I tried at least one counter-prompt ("what argues against this?") or
      a context swap to test for confirmation bias
- [ ] Uncertainty and limitations are stated, not smoothed over
- [ ] Alternative explanations considered

## 5. Reproducibility

- [ ] Model name and exact version recorded
- [ ] Prompt/template/skill/agent version recorded (git reference)
- [ ] Temperature and other parameters recorded
- [ ] Re-run gives the same or an equivalent result (or variation is
      measured and reported)
- [ ] Entry added to the project's AI use log

## 6. Data and ethics

- [ ] Data sent to the tool was allowed for its classification
- [ ] No identifiers, collaborator data or material under review was shared
- [ ] AI use will be disclosed according to the journal/funder policy
      (AI-generated text may carry an invisible watermark; that does not
      replace your own disclosure)
- [ ] No "AI checker" result is used as evidence about someone else's work
- [ ] Text is my own wording or clearly adapted; no copied passages from
      sources without attribution

**If any box in sections 1–3 stays unchecked, the output is a draft, not a
result.**
