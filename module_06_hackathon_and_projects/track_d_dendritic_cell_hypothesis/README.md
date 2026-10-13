# Track D – Hypothesis Engine for Dendritic Cell Modulation

**One-liner:** an interactive tool where a researcher enters an
experimental perturbation (e.g. a TLR agonist on DCs at a given dose and
time) and receives structured, literature-grounded predictions of
downstream gene expression and lipid membrane changes — plus the
experiments that would test them.

**Modules used:** 2 (schemas, CoT), 4 (tools/MCP), 5 (agents), Track B
ideas (RAG)
**Team size:** 2–4 · **Difficulty:** ★★★★

---

## 1. Background

Designing a lipidomics + RNA-seq experiment on stimulated DCs means
predicting what should change, when, and why: e.g. LPS (TLR4) → NF-κB/IRF
programmes, `Il12b`/`Cd40`/`Ccr7` induction, `Ptgs2`-driven prostaglandin
production, ceramide accumulation, suppressed SREBP2-dependent cholesterol
synthesis, itaconate (`Acod1`) induction; versus R848 (TLR7/8), poly(I:C)
(TLR3), CpG (TLR9), or cholesterol/ceramide pathway inhibitors (e.g.
myriocin, statins). A hypothesis engine makes these expectations explicit,
structured and checkable — **predictions to test, not results**.

## 2. Inputs

**User query** (form or JSON):

```json
{
  "cell_type": "murine bone-marrow-derived dendritic cells",
  "perturbation": "LPS",
  "receptor_target": "TLR4",
  "dose": "100 ng/mL",
  "timepoints_h": [2, 6, 24],
  "co_treatment": null,
  "readouts": ["RNA-seq", "lipidomics"],
  "context": "migration to draining lymph node"
}
```

**Knowledge sources** (grounding):

- A local corpus of open-access papers on DC activation, lipid metabolism
  and lymph node migration (reuse a Track B-style index, or a simple
  embedding store).
- Pathway databases via tools/MCP: Reactome (TLR cascades, sphingolipid and
  cholesterol metabolism), LIPID MAPS (class hierarchy), optionally KEGG.

## 3. Output schema (Pydantic)

```python
class GenePrediction(BaseModel):
    gene: str                                  # official symbol, species-specific
    direction: Literal["up", "down", "unchanged"]
    timepoint_h: float
    magnitude: Literal["strong", "moderate", "weak"]
    pathway: str
    evidence: list[str]                        # citation keys / pathway IDs (required, ≥1)
    confidence: Literal["high", "medium", "low"]

class LipidPrediction(BaseModel):
    lipid_class: str                           # LIPID MAPS class, e.g. "Ceramides [SP02]"
    example_species: list[str]                 # e.g. ["Cer d18:1/16:0"]
    direction: Literal["up", "down", "unchanged"]
    timepoint_h: float
    linked_enzymes: list[str]                  # genes in the GenePrediction list where possible
    evidence: list[str]
    confidence: Literal["high", "medium", "low"]

class KineticTrend(BaseModel):
    feature: str                               # gene or lipid class
    shape: Literal["transient", "sustained", "delayed", "biphasic"]
    peak_h: float | None

class ValidationExperiment(BaseModel):
    aim: str
    method: str                                # e.g. "qPCR", "targeted LC-MS/MS", "flow cytometry", "transwell migration"
    readout: str
    expected_result_if_true: str
    controls: list[str]

class Hypothesis(BaseModel):
    statement: str
    mechanism: str
    gene_predictions: list[GenePrediction]
    lipid_predictions: list[LipidPrediction]
    kinetic_trends: list[KineticTrend]
    validation_experiments: list[ValidationExperiment]
    caveats: list[str]

class HypothesisReport(BaseModel):
    query: dict
    hypotheses: list[Hypothesis]               # 1–3 alternatives, ranked
    sources: dict[str, str]                    # citation key -> DOI / pathway URL
    model: str
    generated_at: str
```

## 4. Required features (MVP)

1. **Query form** (Streamlit or CLI) producing the input JSON.
2. **Retrieval:** pull relevant passages and pathway memberships for the
   receptor, downstream signalling, and lipid pathways.
3. **Reasoning step:** the LLM reasons step by step (receptor → signalling →
   transcriptional programme → metabolic enzymes → lipid classes →
   functional consequence for migration/priming), then outputs a
   `HypothesisReport`.
4. **Validation layer:**
   - Pydantic schema validation with retry.
   - Every `evidence` key must resolve to a retrieved source (no invented
     citations).
   - Gene symbols checked against the species' gene list (Ensembl/MGI file);
     lipid classes checked against the LIPID MAPS hierarchy.
   - Consistency check: `linked_enzymes` must appear in `gene_predictions`.
5. **Output:** JSON file + readable HTML/Markdown view, with predictions
   tables, a timeline of kinetic trends, and the validation experiments.

## 5. Evaluation (the important part)

Predictions are only interesting if they can be scored.

1. **Retrospective benchmark:** choose 1–2 public datasets with the same
   perturbation (e.g. LPS-stimulated BMDC RNA-seq from GEO; a public
   macrophage/DC lipidomics dataset). Hide them from the corpus.
2. Generate predictions, then compute:
   - **Direction accuracy** for predicted genes found in the dataset.
   - **Precision@k** of "up" predictions among the dataset's top
     up-regulated genes.
   - Lipid class direction agreement (where lipid data exist).
3. **Baseline:** the same model *without* retrieval/tools. Does grounding
   help?
4. **Expert review:** a lab immunologist rates 10 predictions as
   plausible / implausible / novel-and-testable.

## 6. Suggested architecture

```
 query form ─► query JSON ─► retriever (corpus + Reactome/LIPID MAPS tools)
                                      │ passages + pathway members
                                      ▼
                 LLM reasoning (CoT in a 'reasoning' field or reasoning mode)
                                      │
                                      ▼
                  HypothesisReport (Pydantic) ─► validators ─► retry on failure
                                      │
                                      ▼
                     JSON + HTML view  ─►  benchmark scorer (offline)
```

## 7. Stack

Python 3.11, pydantic, a RAG layer (ChromaDB/FAISS + local embeddings, or
reuse Track B code), `mcp`/requests for Reactome and LIPID MAPS, Streamlit,
pandas for benchmarking; Claude API or Ollama (`qwen2.5:14b` or larger).

## 8. Milestones

| By | Milestone |
|----|-----------|
| Day 1, 12:30 | Schema finalised; corpus indexed; one tool working |
| Day 1, 17:30 | End-to-end valid `HypothesisReport` for LPS query |
| Day 2, 12:00 | Validators complete; benchmark scored vs baseline |
| Day 2, 14:30 | UI, second perturbation, documented evaluation |

## 9. Success criteria

- [ ] Produces schema-valid JSON for at least three perturbations (e.g.
      LPS, R848, poly(I:C)) with target pathways, kinetic trends and
      validation experiments.
- [ ] 0 unresolvable citations; 0 invalid gene symbols or lipid classes
      after validation.
- [ ] Direction accuracy on the retrospective benchmark reported and
      compared with the no-retrieval baseline.
- [ ] Each hypothesis includes at least one concrete, feasible validation
      experiment with controls.
- [ ] The UI clearly labels outputs as *predictions* with confidence levels.

## 10. Stretch goals

- Dose/time interpolation: compare 2 h vs 24 h predictions to the kinetic
  trends.
- Combination perturbations (e.g. LPS + myriocin) and predicted
  interaction effects.
- Link to migration: predict effects on CCR7 surface expression and
  chemotaxis assays.
- Export predictions as a pre-registration-style experiment plan.
- Active learning: ingest a new result table and update confidence.

## 11. Pitfalls

- Overconfident, generic predictions ("inflammation goes up"): require
  specific genes/classes and timepoints in the schema.
- Citation hallucination: only allow citation keys that came from retrieval.
- Species mix-ups (human vs mouse symbols and biology).
- Benchmark leakage: keep evaluation datasets and their papers out of the
  retrieval corpus.
