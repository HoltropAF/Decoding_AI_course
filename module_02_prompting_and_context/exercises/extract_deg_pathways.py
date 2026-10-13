#!/usr/bin/env python3
"""Force structured, schema-validated JSON from an LLM for an RNA-seq DEG list.

Module 2 exercise. Demonstrates the three enforcement layers:
    1. Ask for JSON (five-part prompt from templates/structured_bio_prompt.json)
    2. Constrain decoding with a JSON schema (Ollama `format` field)
    3. Validate in code (Pydantic + semantic checks), retrying with the error

Requirements:
    pip install requests pydantic
    ollama pull llama3.1:8b

Usage:
    python extract_deg_pathways.py
    python extract_deg_pathways.py --input degs.csv --output pathways.json
    python extract_deg_pathways.py --no-schema          # compare failure rate
    python extract_deg_pathways.py --dry-run            # print prompt only

Input CSV/TSV columns: gene, log2FoldChange, padj  (DESeq2-style names; the
aliases 'symbol', 'logFC', 'adj.P.Val', 'FDR' are also recognised).

Privacy: this sends the gene list to whatever host you configure. The default
is a local Ollama server. Do not point it at a cloud endpoint with
pre-publication data (see Module 1).
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from pathlib import Path
from typing import Literal

import requests
from pydantic import BaseModel, ConfigDict, Field, ValidationError

TEMPLATE_PATH = Path(__file__).resolve().parent.parent / "templates" / "structured_bio_prompt.json"
DEFAULT_HOST = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434")
DEFAULT_MODEL = "llama3.1:8b"

# Synthetic demo: LPS-stimulated murine BMDCs (values are illustrative, not real data).
DEMO_DEGS = [
    ("Ccr7", 4.12, 1.2e-30), ("Il12b", 6.80, 3.4e-45), ("Cd40", 3.05, 2.2e-22),
    ("Cd86", 2.41, 5.6e-18), ("Cd80", 2.10, 1.1e-12), ("Fscn1", 3.60, 7.5e-25),
    ("Il6", 7.25, 1.0e-50), ("Tnf", 3.90, 4.4e-28), ("Il1b", 5.50, 8.1e-40),
    ("Socs3", 3.30, 9.9e-21), ("Nfkbia", 2.75, 3.3e-19), ("Irf7", 2.95, 6.0e-16),
    ("Isg15", 3.80, 2.7e-23), ("Cxcl10", 6.10, 1.5e-38), ("Ptgs2", 4.40, 4.0e-26),
    ("Acod1", 8.10, 1.0e-60), ("Ldlr", -1.35, 2.1e-04), ("Hmgcr", -1.10, 6.3e-03),
    ("Srebf2", -1.05, 8.8e-03), ("Cd36", -2.20, 1.4e-09), ("Ppara", -1.60, 3.0e-05),
    ("Sptlc2", 1.45, 1.9e-04), ("Cers6", 1.70, 4.2e-06), ("Asah1", -1.20, 1.1e-03),
]


# --------------------------------------------------------------------------- #
# Schema (must match output_schema in the JSON template)
# --------------------------------------------------------------------------- #
class Pathway(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str = Field(min_length=3)
    database: Literal["Reactome", "KEGG", "GO", "WikiPathways", "Other"]
    genes: list[str] = Field(min_length=1)
    direction: Literal["up", "down", "mixed"]
    confidence: Literal["high", "medium", "low"]
    rationale: str = Field(max_length=400)


class PathwayReport(BaseModel):
    model_config = ConfigDict(extra="forbid")
    pathways: list[Pathway]
    unassigned_genes: list[str]
    summary: str = Field(max_length=800)


# --------------------------------------------------------------------------- #
# Input handling
# --------------------------------------------------------------------------- #
GENE_COLS = ("gene", "symbol", "gene_name", "gene_symbol")
LFC_COLS = ("log2foldchange", "logfc", "log2fc")
PADJ_COLS = ("padj", "adj.p.val", "fdr", "qvalue")


def _pick(header: list[str], candidates: tuple[str, ...]) -> str:
    lowered = {h.lower(): h for h in header}
    for c in candidates:
        if c in lowered:
            return lowered[c]
    raise SystemExit(f"[error] Missing column; expected one of {candidates}, got {header}")


def load_degs(path: Path | None) -> list[tuple[str, float, float]]:
    if path is None:
        return DEMO_DEGS
    with path.open(newline="", encoding="utf-8") as fh:
        sample = fh.read(2048)
        fh.seek(0)
        dialect = csv.Sniffer().sniff(sample, delimiters=",\t;")
        reader = csv.DictReader(fh, dialect=dialect)
        header = reader.fieldnames or []
        g, l, p = _pick(header, GENE_COLS), _pick(header, LFC_COLS), _pick(header, PADJ_COLS)
        rows = []
        for row in reader:
            try:
                rows.append((row[g].strip(), float(row[l]), float(row[p])))
            except (ValueError, KeyError):
                continue  # skip NA rows
    if not rows:
        raise SystemExit(f"[error] No usable rows in {path}")
    return rows


def format_deg_table(degs: list[tuple[str, float, float]], max_genes: int) -> str:
    degs = sorted(degs, key=lambda r: r[2])[:max_genes]
    lines = ["gene\tlog2FoldChange\tpadj"]
    lines += [f"{g}\t{lfc:.2f}\t{padj:.2e}" for g, lfc, padj in degs]
    return "\n".join(lines)


# --------------------------------------------------------------------------- #
# Prompt assembly from the template
# --------------------------------------------------------------------------- #
def build_prompt(template: dict, deg_table: str, overrides: dict[str, str]) -> tuple[str, str]:
    """Return (system_prompt, user_prompt) assembled from the five-part template."""
    values: dict[str, str] = {}
    values.update(template["role"]["defaults"])
    for section in ("context", "instruction", "inputs", "constraints"):
        values.update(template[section].get("example_values", {}))
    values.update(overrides)
    values["input_data"] = deg_table

    system_prompt = template["role"]["persona"].format_map(values)

    ctx = template["context"]
    context_lines = [
        f"- {key.replace('_', ' ').capitalize()}: {ctx[key].format_map(values)}"
        for key in ctx
        if key != "example_values"
    ]

    instr = template["instruction"]
    steps = [f"{i}. {s.format_map(values)}" for i, s in enumerate(instr["steps"], 1)]

    inputs = template["inputs"]
    cons = template["constraints"]
    rules = [f"- {r.format_map(values)}" for r in cons["rules"]]

    few_shot = "\n\n".join(
        f"Example input:\n{ex['input']}\nExample output:\n{json.dumps(ex['output'])}"
        for ex in template.get("few_shot_examples", [])
    )

    user_prompt = "\n".join([
        "## CONTEXT", *context_lines, "",
        "## INSTRUCTION", instr["task"].format_map(values), *steps, "",
        "## INPUTS", inputs["untrusted_content_warning"],
        inputs["format"].format_map(values), "",
        "## CONSTRAINTS", *rules, cons["output_format"], "",
        "## OUTPUT SCHEMA", json.dumps(template["output_schema"], indent=2), "",
        "## EXAMPLE", few_shot,
    ])
    return system_prompt, user_prompt


# --------------------------------------------------------------------------- #
# LLM call + validation
# --------------------------------------------------------------------------- #
def call_ollama(host: str, model: str, system: str, messages: list[dict],
                schema: dict | None, temperature: float, num_ctx: int) -> str:
    # num_ctx: Ollama's default context window is small (often 4096 tokens) and
    # longer prompts are truncated silently, so we set it explicitly.
    payload = {
        "model": model,
        "messages": [{"role": "system", "content": system}, *messages],
        "stream": False,
        "options": {"temperature": temperature, "num_ctx": num_ctx},
    }
    if schema is not None:
        payload["format"] = schema  # constrained decoding (Ollama >= 0.5)
    try:
        response = requests.post(f"{host.rstrip('/')}/api/chat", json=payload, timeout=900)
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        sys.exit(f"[error] Cannot reach Ollama at {host}. Is `ollama serve` running?")
    return response.json()["message"]["content"]


def strip_fences(text: str) -> str:
    """Remove ```json fences that some models add despite instructions."""
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1] if "\n" in text else ""
        text = text.rsplit("```", 1)[0]
    return text.strip()


def semantic_check(report: PathwayReport, input_genes: dict[str, float]) -> list[str]:
    """Checks a JSON schema cannot express. input_genes maps gene -> log2 fold change."""
    errors = []
    lookup = {g.lower(): lfc for g, lfc in input_genes.items()}
    used: set[str] = set()
    for pw in report.pathways:
        signs = set()
        for gene in pw.genes:
            if gene.lower() not in lookup:
                errors.append(f"Pathway '{pw.name}' contains gene '{gene}' that is not in the input.")
            else:
                signs.add("up" if lookup[gene.lower()] > 0 else "down")
            used.add(gene.lower())
        expected = next(iter(signs)) if len(signs) == 1 else "mixed"
        if signs and pw.direction != expected:
            errors.append(f"Pathway '{pw.name}' is labelled '{pw.direction}', but its genes' "
                          f"log2 fold changes say '{expected}'.")
    for gene in report.unassigned_genes:
        if gene.lower() not in lookup:
            errors.append(f"unassigned_genes contains '{gene}' that is not in the input.")
        elif gene.lower() in used:
            errors.append(f"'{gene}' is listed both in a pathway and in unassigned_genes.")
    accounted = used | {g.lower() for g in report.unassigned_genes}
    missing = {g for g in input_genes if g.lower() not in accounted}
    if missing:
        errors.append(
            "These input genes appear in neither pathways nor unassigned_genes: "
            + ", ".join(sorted(missing))
        )
    return errors


def extract(host: str, model: str, system: str, user: str, input_genes: dict[str, float],
            use_schema: bool, temperature: float, max_retries: int,
            num_ctx: int = 8192) -> tuple[PathwayReport, int]:
    schema = PathwayReport.model_json_schema() if use_schema else None
    messages = [{"role": "user", "content": user}]

    for attempt in range(1, max_retries + 2):
        print(f"[info] attempt {attempt}: calling {model} (schema={'on' if use_schema else 'off'})")
        raw = call_ollama(host, model, system, messages, schema, temperature, num_ctx)
        try:
            report = PathwayReport.model_validate_json(strip_fences(raw))
            problems = semantic_check(report, input_genes)
            if not problems:
                print(f"[ok] valid report with {len(report.pathways)} pathways")
                return report, attempt
            error_text = "Semantic validation failed:\n- " + "\n- ".join(problems)
        except ValidationError as exc:
            error_text = f"JSON schema validation failed:\n{exc}"

        shown = [l for l in error_text.splitlines() if l.strip()][:3]
        print("[warn] " + "\n       ".join(shown))
        messages += [
            {"role": "assistant", "content": raw},
            {"role": "user", "content": (
                f"{error_text}\n\nReturn a corrected JSON object only. "
                "Use only genes from the input."
            )},
        ]

    sys.exit(f"[error] No valid output after {max_retries + 1} attempts.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--input", type=Path, help="CSV/TSV with gene, log2FoldChange, padj")
    parser.add_argument("--output", type=Path, default=Path("pathways.json"))
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--max-genes", type=int, default=60,
                        help="Send at most N most significant genes (default: %(default)s)")
    parser.add_argument("--temperature", type=float, default=None)
    parser.add_argument("--num-ctx", type=int, default=8192,
                        help="Ollama context window in tokens (default: %(default)s; Ollama's own default is often only 4096)")
    parser.add_argument("--no-schema", action="store_true",
                        help="Disable constrained decoding (prompt-only JSON)")
    parser.add_argument("--organism", help="Override template organism")
    parser.add_argument("--comparison", help="Override template comparison")
    parser.add_argument("--dry-run", action="store_true", help="Print the prompt and exit")
    args = parser.parse_args()

    template = json.loads(TEMPLATE_PATH.read_text(encoding="utf-8"))
    degs = load_degs(args.input)
    deg_table = format_deg_table(degs, args.max_genes)
    input_genes = {row.split("\t")[0]: float(row.split("\t")[1]) for row in deg_table.splitlines()[1:]}

    overrides = {k: v for k, v in {"organism": args.organism,
                                   "comparison": args.comparison}.items() if v}
    system, user = build_prompt(template, deg_table, overrides)

    if args.dry_run:
        print("=== SYSTEM ===\n" + system + "\n\n=== USER ===\n" + user)
        return

    temperature = args.temperature if args.temperature is not None \
        else template["constraints"]["temperature"]
    report, attempts = extract(args.host, args.model, system, user, input_genes,
                     use_schema=not args.no_schema, temperature=temperature,
                     max_retries=template["constraints"]["max_retries_on_validation_error"],
                     num_ctx=args.num_ctx)

    result = {
        "provenance": {
            "model": args.model,
            "host": args.host,
            "template": template["template_name"],
            "template_version": template["template_version"],
            "input": str(args.input) if args.input else "built-in synthetic demo",
            "n_genes_sent": len(input_genes),
            "schema_enforced": not args.no_schema,
            "temperature": temperature,
            "attempts": attempts,
        },
        "report": report.model_dump(),
    }
    args.output.write_text(json.dumps(result, indent=2), encoding="utf-8")

    print(f"\nSummary: {report.summary}\n")
    for pw in report.pathways:
        print(f"  [{pw.confidence:<6}] {pw.direction:<5} {pw.name} ({pw.database}): {', '.join(pw.genes)}")
    if report.unassigned_genes:
        print(f"  unassigned: {', '.join(report.unassigned_genes)}")
    print(f"\nWrote {args.output}. Verify pathway assignments against Reactome/KEGG before use.")


if __name__ == "__main__":
    main()
