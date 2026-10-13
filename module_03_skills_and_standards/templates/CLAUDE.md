# CLAUDE.md – Lab Bioinformatics Standards

<!--
Template version: 1.0.0
Source: Decoding_AI_course/module_03_skills_and_standards/templates/CLAUDE.md
Copy into the project root. Fill in the "Project-specific" section, delete
rules that do not apply, keep the file under ~200 lines.
Never put credentials, internal hostnames or real data values in this file.
-->

## Project-specific (fill in)

- **Project:** <short name> – <one-sentence aim>
- **Organism / system:** <e.g. Mus musculus, BMDCs; human lymph node biopsies>
- **Data types:** <e.g. bulk RNA-seq (DESeq2), untargeted lipidomics (LC-MS), targeted metabolomics>
- **Main languages:** <Python 3.11 / R 4.4>
- **Environment:** <conda env `environment.yml` | `renv.lock` | `pyproject.toml` + uv>
- **Run tests:** `<pytest -q>` / `<Rscript -e 'testthat::test_dir("tests")'>`
- **Lint/format:** `<ruff check . && ruff format .>` / `<Rscript -e 'styler::style_dir()'>`
- **Pipeline entry point:** `<snakemake -n | nextflow run main.nf -profile test>`
- **Data classification:** <public | internal | confidential | restricted> – see "Data & privacy"

## Project structure (ENCORE)

This project follows the ENCORE layout (van Kampen et al., Nat Commun 2024):

- `Data/` – input data. **`Data/raw/` is read-only: never modify, move or overwrite.**
- `Processing/` – code and analyses; each analysis in its own subfolder with a README.
- `Manuscript/` – manuscript drafts and figures.
- `ProjectDocumentation/` – protocols, meeting notes, decisions.
- `Sharing/` – material prepared for collaborators or repositories.
- `.navigate/` – navigation files.
- `0_PROJECT.md` – project log; append an entry for every significant change.

When adding a folder, add a README explaining what it contains. When renaming
or moving anything, update every document that references it.

## Golden rules

1. **Never modify raw data.** Read from `Data/raw/`, write derived files to `Processing/<analysis>/output/` (or `Data/processed/`).
2. **Relative paths only.** No absolute paths (`C:\Users\...`, `/home/...`). Use `pathlib.Path(__file__).parent` / project-root helpers in Python and `here::here()` in R.
3. **Reproducible by default.** Set and record random seeds; pin package versions; record tool versions in outputs.
4. **Do not compute statistics in prose.** Every number in a report must come from code that is in the repository.
5. **Ask before destructive actions.** Deleting files, rewriting git history, or overwriting outputs requires explicit confirmation.
6. **Plan before large changes.** For multi-file changes, propose a plan (files, approach, tests) and wait for approval.

## Python conventions

- Python ≥ 3.10, type hints on all public functions, docstrings (NumPy style) stating inputs, outputs and units.
- Formatting and linting: `ruff format` and `ruff check`; line length 100.
- Use `pathlib`, not `os.path` string manipulation.
- Data frames: `pandas` (or `polars` if already used in the project). Never rely on implicit index alignment between omics tables; join explicitly on identifiers and assert expected row counts.
- No `import *`, no mutable default arguments, no bare `except:`.
- CLI scripts use `argparse` (or `typer`) with `--help`; no hardcoded input files.
- Logging via `logging`, not `print`, in library code.
- Configuration (thresholds, paths, sample sheets) lives in `config/*.yaml`, not in code.

## R conventions

- R ≥ 4.3, tidyverse style guide; format with `styler`, lint with `lintr`.
- Dependencies managed with `renv`; commit `renv.lock`; never call `install.packages()` inside analysis scripts.
- Paths via `here::here()`; never `setwd()`.
- Use `<-` for assignment; explicit namespaces for less common packages (`ComplexHeatmap::Heatmap`).
- Bioconductor objects (`SummarizedExperiment`, `DESeqDataSet`) are preferred over loose matrices for count data; keep `colData` sample annotation in sync.
- Quarto/R Markdown reports render from a clean session and end with `sessionInfo()`.

## Omics-specific conventions

- **Identifiers:** keep stable IDs (Ensembl gene IDs, LIPID MAPS / HMDB IDs, InChIKey) as primary keys; map to symbols/common names only for display. Record the annotation version (e.g. Ensembl release, LIPID MAPS date).
- **Lipid nomenclature:** use LIPID MAPS shorthand (`PC 34:1`, `Cer d18:1/16:0`); state whether species level or molecular species level.
- **RNA-seq:** default DE thresholds padj < 0.05 and |log2FC| > 1 unless the analysis README states otherwise; always report the full results table, not only significant genes.
- **Lipidomics/metabolomics:** document normalisation (internal standards, TIC, PQN), missing-value handling and batch correction explicitly in the analysis README.
- **Multiple testing:** Benjamini–Hochberg unless justified otherwise; never report uncorrected p-values as findings.
- **Units:** state units for every quantitative column (counts, log2 intensity, nmol/mg protein).

## Testing

- Every function that transforms data has at least one unit test with a small synthetic fixture in `tests/fixtures/` (never real data).
- Test edge cases relevant to omics data: all-NaN rows, zero counts, duplicated identifiers, mismatched sample order.
- Python: `pytest`; R: `testthat`. Pipelines: a dry run (`snakemake -n`, `nextflow -profile test`) must pass.
- After changing code, run the tests and report the result; do not claim success without running them.
- Bug fixes include a regression test that fails before the fix.

## Reproducibility

- Environment files (`environment.yml`, `renv.lock`, `pyproject.toml`/lock file) are updated in the same commit as new dependencies.
- Random seeds are set explicitly and written to output metadata.
- Each analysis folder README states: purpose, inputs, outputs, how to run, software versions, date.
- Output files include provenance (script name, git commit, parameters) in a sidecar `*.json` or header.
- Prefer containers (Docker/Apptainer) or workflow managers for multi-step pipelines.

## Git

- Small, focused commits with imperative messages (`Add PQN normalisation for lipidomics`).
- Never commit raw data, large binaries, `.env` files, credentials or patient identifiers; check `.gitignore` before adding files.
- Never force-push to shared branches. Do not commit or push unless asked.

## Data & privacy

- Data classification for this project: **<fill in>**.
- Do not paste or upload contents of `Data/` into prompts or external services unless the classification is "public".
- When help is needed with data handling, use column names, schemas and synthetic examples instead of real values.
- Scrub absolute paths, sample/donor IDs and hostnames from logs before sharing them.
- Secrets come from environment variables (`os.environ["NCBI_API_KEY"]`, `Sys.getenv("NCBI_API_KEY")`); never hardcode them.

## Communication

- When uncertain about biology, statistics or project conventions, ask instead of guessing.
- Clearly separate verified facts (from code output or cited sources) from suggestions.
- When referencing pathways, genes or lipids, use database identifiers where possible so they can be checked.
