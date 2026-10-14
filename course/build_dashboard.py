#!/usr/bin/env python3
"""Build course/dashboard.html from the course Markdown files.

Browsers do not let a double-clicked HTML file read other files from disk,
so this script packs the content of every slide deck, guide, exercise,
self-check and resource into the dashboard. Participants only need to open
course/dashboard.html; no server or installation is required.

Run after changing any course file:

    python course/build_dashboard.py

Uses only the Python standard library. Markdown is rendered in the browser
by marked (MIT licence), which is bundled from course/vendor/marked.min.js,
so the dashboard works offline and contacts no other websites.
"""

from __future__ import annotations

import base64
import json
import posixpath
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "course" / "dashboard_template.html"
OUTPUT = ROOT / "course" / "dashboard.html"
PLACEHOLDER = "__COURSE_DATA__"
VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip()

# --------------------------------------------------------------------------- #
# Introductions shown at the top of each module's Extra reading step.
M2_INTRO = """This page holds the prompt template from part 2, *What goes into a good prompt?*, as a JSON file that a script can fill in: the five-part briefing with placeholders in `{curly braces}`, example values for our LPS experiment, and the schema the answer has to follow. The Module 2 exercise uses it. Read it once from top to bottom and find the five parts; then copy it and fill in the example values for an experiment of your own. If you don't write code, it works just as well as a checklist to copy into a chat.

While you read, think about why some lines are there. Why is there an `untrusted_content_warning` (part 3, *Prompt injection: it's not a bug, it's a feature*)? Why is there a place for `unassigned_genes` (the honest exit)? And what would you write in the changelog if you changed it and made it version 1.1.0?"""

M3_INTRO = r"""These are five skills to copy and adapt. A skill is a recipe the assistant only pulls out when a task calls for it, so you can keep several without cluttering every conversation. Omics analysis makes the assistant work like an experienced computational bioinformatician: design first, quality control second, statistics that fit the experiment. Research review does the opposite of agreeing with you: it questions your plan before you build it. Clean commits keeps your git history readable, which matters even more once an agent edits your code. The prompt builder turns a rambling brief or voice note into a clean prompt for another AI. And wrap-up ends a work session by updating the project's roadmap, decisions and changelog, so the next session doesn't start from zero.

Each part below explains what the skill makes the assistant do, and ends with the complete skill file. Starting one takes a minute. Make a folder with the skill's name, save the file in it as `SKILL.md` (for example `omics-analysis/SKILL.md`), and put that folder in `~/.claude/skills/` (on Windows `C:\Users\<you>\.claude\skills\`) for all your projects, or in `.claude/skills/` inside a project. Claude Code then uses it by itself when a task matches; type `/omics-analysis` to be sure. No Claude Code? Paste the text below the `---` header into a Project in Claude, ChatGPT or Copilot.

How skills work, and how they differ from `CLAUDE.md` and subagents, is in the chapter (part 2). The lab's `CLAUDE.md` template is in the Exercise step, where you turn it into your project's own."""

M4_INTRO = """This is an example configuration file for connecting AI tools to data through MCP, with the four servers described in part 2, *How do I configure a server?*: a read-only filesystem server in a sealed container, the small Reactome lookup server, a lab-internal service reached with a read-only token, and a fetch server for public web pages. It's meant for reading and adapting, not for installing as it is; the paths and names are examples.

Read the comments, and for each server work out three things: what it can read, whether it could change anything, and where what it reads ends up. Then hold it against the security checklist in part 3. Which server would you leave out for your own project, and why? Notice that `Data/` appears nowhere, and that keys come from environment variables (`${VAR}`), never from the file itself."""

M5_INTRO = r"""These are two subagents to copy, read and pass along. Both are built exactly the way the chapter describes: one clear job, a fresh context, fixed instructions in a single file, and only the tools that job needs. Themis checks whether a project follows the ENCORE structure and is properly documented, the boring audit nobody has time for before submission. Argus reads research code the way a careful colleague would, looking for bugs that change results, duplicated code and anything that makes an analysis hard to reproduce. Both only read and report: neither has a tool that could change a file.

Each part below explains what the agent checks, what it reports and what it leaves alone, and ends with the complete agent file. Starting one takes a minute. Copy that file and save it as `<name>.md` (for example `argus.md`) in `~/.claude/agents/` (on Windows `C:\Users\<you>\.claude\agents\`) for all your projects, or in `.claude/agents/` inside a project to share it with that project. Then ask Claude Code for it by name, for example *"Use argus to review scripts/02_deseq2.R"*, after restarting Claude Code once if it was already open. No Claude Code? Paste the text below the `---` header into a Project in Claude, ChatGPT or Copilot.

The last part shows the same idea without any cloud service, in about fifty lines of Python. How agents work in general, and why they are built this way, is in the chapter (*What is a subagent?* and *Anatomy of an agent file*)."""

M6_INTRO = """Five tracks to choose from, each with its own briefing: objective, background, inputs, required features, a suggested architecture, milestones, success criteria and stretch goals. Track E needs no coding at all. Read all five quickly with your team before you choose; pick the one that matches your curiosity and your team's mix of skills, then read that one properly.

While you read your track, look hard at the success criteria. Which of them can you actually measure in two days, what will you compare against (your ground truth or baseline), and what would count as an honest "it didn't work"? Those answers go straight into your evaluation plan."""

# Course structure. Objectives, "done when" items, the experiment question and
# the first critical question are read from each module's self_check.md, so
# edit them there. Everything else about the structure is configured here.
# --------------------------------------------------------------------------- #
MODULES = [
    {
        "id": "m0", "num": "00", "title": "Orientation", "time": "30 min",
        "summary": "What the course is for, how it works, the one ground rule, and what you need to get started.",
        "objectives": [],
        "done": [
            "Welcome page read (or the orientation session attended)",
            "Privacy settings of my AI accounts checked",
            "I know which chat assistant I may use for work",
            "Optional: Ollama installed and llama3.1:8b downloaded",
        ],
        "steps": [
            {"key": "guide", "label": "Welcome", "kind": "doc", "phase": "learn", "path": "course/orientation.md"},
            {"key": "slides", "label": "Slides", "kind": "slides", "phase": "extra", "path": "course/slides_00_orientation.md"},
            {"key": "progress", "label": "Wrap-up", "kind": "progress", "phase": "reflect"},
        ],
    },
    {
        "id": "m1", "num": "01", "title": "Foundations", "time": "~3 h",
        "summary": "How AI works, which tools there are, what data may go where, what to use it for, and the big debates and limitations.",
        "dir": "module_01_foundations_and_privacy",
        "exercise_files": ["exercises/test_ollama_local.py"],
    },
    {
        "id": "m2", "num": "02", "title": "Prompting & Context", "time": "~2 h",
        "summary": "Prompt engineering: how to ask so you get reliable, checkable answers, and how to test your prompts.",
        "dir": "module_02_prompting_and_context",
        "exercise_files": ["exercises/extract_deg_pathways.py"],
        "materials": [
            ("Prompt template (JSON)", "templates/structured_bio_prompt.json"),
        ],
        "materials_intro": M2_INTRO,
    },
    {
        "id": "m3", "num": "03", "title": "Skills & Standards", "time": "~2 h",
        "summary": "Write your instructions once, so every AI session (and every colleague) starts from the same rules.",
        "dir": "module_03_skills_and_standards",
        "exercise_files": ["templates/CLAUDE.md"],
        "materials": [
            ("Omics analysis", "docs/skill-omics-analysis.md", {"append": "skills/omics-analysis/SKILL.md", "as": "The skill file"}),
            ("Research review", "docs/skill-research-review.md", {"append": "skills/research-review/SKILL.md", "as": "The skill file"}),
            ("Clean commits", "docs/skill-clean-commits.md", {"append": "skills/clean-commits/SKILL.md", "as": "The skill file"}),
            ("Prompt builder", "docs/skill-prompt-builder.md", {"append": "skills/prompt-builder/SKILL.md", "as": "The skill file"}),
            ("Wrap-up", "docs/skill-wrap-up.md", {"append": "skills/wrap-up/SKILL.md", "as": "The skill file"}),
        ],
        "materials_label": "Examples",
        "materials_toggles": True,
        "materials_intro": M3_INTRO,
    },
    {
        "id": "m4", "num": "04", "title": "MCP & Data", "time": "~2 h",
        "summary": "How AI tools look things up in your files and databases, and how to keep that safe: read-only, least privilege.",
        "dir": "module_04_mcp_and_data",
        "exercise_files": [],
        "materials": [
            ("Sample MCP configuration", "mcp_servers/sample_mcp_config.json"),
        ],
        "materials_intro": M4_INTRO,
    },
    {
        "id": "m5", "num": "05", "title": "Agents & Subagents", "time": "~2.5 h",
        "summary": "AI that does small jobs for you: research modes, agents and subagents, how to choose, and how to check their work.",
        "dir": "module_05_agents_and_subagents",
        "exercise_files": ["exercises/build_custom_subagent.md"],
        "materials": [
                        ("Themis: the ENCORE auditor", "docs/themis-in-detail.md", {"append": "agents/themis.md", "as": "The agent file"}),
            ("Argus: the code reviewer", "docs/argus.md", {"append": "agents/argus.md", "as": "The agent file"}),
            ("Running an agent with a local model", "docs/agents-local-model.md"),
        ],
        "materials_label": "Examples",
        "materials_toggles": True,
        "materials_intro": M5_INTRO,
    },
    {
        "id": "m6", "num": "06", "title": "Hackathon", "time": "2 days · teams of 2–4",
        "summary": "Apply everything to RNA-seq, lipidomics and dendritic cell biology, and evaluate it honestly.",
        "dir": "module_06_hackathon_and_projects",
        "exercise_files": [],
        "materials": [
            ("Track A · Multi-omics synthesis", "track_a_multiomics_synthesis/README.md"),
            ("Track B · Local immunology RAG", "track_b_local_immunology_rag/README.md"),
            ("Track C · Pipeline debugger", "track_c_pipeline_debugger/README.md"),
            ("Track D · DC hypothesis engine", "track_d_dendritic_cell_hypothesis/README.md"),
            ("Track E · Lab AI playbook (no coding)", "track_e_lab_ai_playbook/README.md"),
        ],
        "materials_label": "Tracks",
        "materials_intro": M6_INTRO,
        "experiment": "Your project is the experiment: what are your primary outcome, ground truth, baseline and success threshold?",
        "selfcheck_label": "Evaluation plan",
        "no_exercise": True,
    },
]

RESOURCES = [
    ("about", "About this course", "course/about.md", "What the course is and who made it, how to use it, and where its limits are."),
    ("references", "References", "course/references.md", "All papers, policies and sources behind the course, searchable."),
    ("cookbook", "Prompt cookbook", "course/templates/prompt_cookbook.md", "The prompts from the course you'll use again and again, ready to copy into your own file."),
    ("timeline", "Timeline", "course/timeline.md", "The history behind the course in one line, from 1948 to today, with a source for every event."),
]

# The "Limits & workarounds" page is the table from Module 2, part 4, so it's maintained in one place.
LIMITS_SOURCE = "module_02_prompting_and_context/README.md"
LIMITS_INTRO = """# Limits & workarounds

Every AI tool has the same handful of weak spots, and almost every one has a simple way around it. This is the cheat sheet; the story behind it is in Module 2, part 4 (*Working around the limits*), where the three that need a full prompt are worked out: thirty papers without losing the middle, calculating in code, and code for an older package version.

"""


def limits_page() -> dict:
    """The limitations table from Module 2, as its own page."""
    lines = read(LIMITS_SOURCE).splitlines()
    start = lines.index("#### Working around the limits")
    table = [l for l in lines[start + 1:next(i for i in range(start + 1, len(lines)) if lines[i].startswith("#### "))]
             if l.startswith("|")]
    return {"id": "limits", "title": "Limits & workarounds",
            "summary": "The weak spots every AI tool shares, how you notice them, and what to do instead.",
            "doc": doc("course/limits.md", "Limits & workarounds", text=LIMITS_INTRO + "\n".join(table) + "\n")}


# Where exported problem reports should go. Leave empty to only offer copy/download.
CONTACT_EMAIL = ""

LANG = {".py": "python", ".json": "json", ".R": "r", ".sh": "bash", ".md": "markdown"}


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def as_code(rel: str, text: str) -> str:
    """Wrap a file in a fenced block (longer fence if it contains ```)."""
    fence = "````" if "```" in text else "```"
    lang = LANG.get(Path(rel).suffix, "")
    return f"{fence}{lang}\n{text.rstrip()}\n{fence}\n"


def section(text: str, pattern: str) -> str:
    """Return a '## ' section whose heading matches pattern, without trailing rule."""
    lines = text.splitlines()
    start = next((i for i, l in enumerate(lines)
                  if l.startswith("## ") and re.search(pattern, l, re.I)), None)
    if start is None:
        return ""
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    body = "\n".join(lines[start:end]).rstrip()
    return re.sub(r"\n-{3,}\s*$", "", body).rstrip() + "\n"


def strip_md(s: str) -> str:
    return re.sub(r"\*+|`", "", s).strip()


def parse_self_check(text: str) -> dict:
    objectives = []
    obj = section(text, r"^## Learning objectives")
    for block in re.split(r"\n(?=\d+\. )", obj):
        m = re.match(r"\d+\. (.*)", block, re.S)
        if m:
            objectives.append(strip_md(" ".join(m.group(1).split())))

    done = [strip_md(m.group(1)) for m in re.finditer(r"^- \[ \] (.+(?:\n {6}.+)*)", section(text, r"^## Done when"), re.M)]
    done = [" ".join(d.split()) for d in done]

    experiment = ""
    exp = section(text, r"^## Mini-experiment")
    m = re.search(r"\*\*Question\.\*\*\s*(.+?)(?:\n\n|$)", exp, re.S)
    if m:
        experiment = strip_md(" ".join(m.group(1).split()))

    question = ""
    crit = section(text, r"^## Critical questions")
    m = re.search(r"^1\. (.+?)(?=\n\d+\. |\n\n|$)", crit, re.M | re.S)
    if m:
        question = strip_md(" ".join(m.group(1).split()))
    return {"objectives": objectives, "done": done, "experiment": experiment, "question": question}


def parse_glossary(rel: str = "course/glossary.md") -> list[dict]:
    """Turn the glossary tables into dictionary entries: term, definition, category, modules."""
    entries, category = [], ""
    for line in read(rel).splitlines():
        if line.startswith("## "):
            category = line[3:].strip()
            continue
        m = re.match(r"^\| \*\*(.+?)\*\* \| (.+?) \|(?: (.+?) \|)?\s*$", line)
        if m:
            entries.append({"term": m.group(1), "def": m.group(2).strip(), "cat": category,
                            "where": (m.group(3) or "1").strip()})
    entries = sorted(entries, key=lambda e: re.sub(r"[^a-z0-9]", "", e["term"].lower()))
    add_glossary_details(entries)
    return entries


def add_glossary_details(entries: list[dict], rel: str = "course/glossary_details.md") -> None:
    """Merge the examples and 'see also' links from glossary_details.md into the entries."""
    if not (ROOT / rel).exists():
        return
    norm = lambda t: re.sub(r"[`*]", "", t).strip().lower()
    by_term = {norm(e["term"]): e for e in entries}
    current = None
    for line in read(rel).splitlines():
        if line.startswith("### "):
            current = by_term.get(norm(line[4:]))
            if current is None:
                print(f"  warning: glossary_details.md term not in glossary: {line[4:].strip()}")
        elif current is not None and line.startswith("More:"):
            current["more"] = line[len("More:"):].strip()
        elif current is not None and line.startswith("Figure:"):
            path, _, cap = line[len("Figure:"):].partition("|")
            if not (ROOT / path.strip()).exists():
                print(f"  warning: dictionary figure not found: {path.strip()} (under {current['term']})")
            else:
                current["fig"], current["figcap"] = path.strip(), cap.strip()
        elif current is not None and line.startswith("Example:"):
            current["ex"] = line[len("Example:"):].strip()
        elif current is not None and line.startswith("See also:"):
            names = [x.strip() for x in line[len("See also:"):].split(";") if x.strip()]
            for name in names:
                if norm(name) not in by_term:
                    print(f"  warning: unknown 'see also' term {name!r} (under {current['term']})")
            current["see"] = [by_term[norm(n)]["term"] for n in names if norm(n) in by_term]
    missing = [e["term"] for e in entries if "ex" not in e]
    if missing:
        print(f"  note: {len(missing)} dictionary terms have no example yet: {', '.join(missing[:8])}" + (" ..." if len(missing) > 8 else ""))


def embed_figures(md: str, rel: str) -> str:
    """Inline SVG figures as data URIs so the dashboard works without other files."""
    def repl(m: re.Match) -> str:
        alt, src = m.group(1), m.group(2)
        path = ((ROOT / rel).parent / src).resolve()
        if not path.exists():
            print(f"  warning: figure not found: {src} (in {rel})")
            return m.group(0)
        alt = re.sub(r"\s*\b(?:w|h|width|height):\S+", "", alt).strip()
        data = base64.b64encode(path.read_bytes()).decode("ascii")
        title = m.group(3) or ""
        return f"![{alt}](data:image/svg+xml;base64,{data}{title})"
    return re.sub(r"!\[([^\]]*)\]\(([^)\s]+\.svg)(\s+\"[^\"]*\")?\)", repl, md)


def doc(rel: str, title: str, raw: bool = False, text: str | None = None) -> dict:
    rel = posixpath.normpath(rel)
    content = text if text is not None else read(rel)
    if raw or not rel.endswith(".md"):
        content = as_code(rel, content)
    else:
        content = embed_figures(content, rel)
    return {"title": title, "path": rel, "md": content}


def material(d: str, m: tuple) -> dict:
    """An extra-reading document. A third element "raw" shows the file as code;
    a dict {"append": file, "as": title} adds that file as the page's last numbered part."""
    opt = m[2] if len(m) > 2 else None
    if opt == "raw" or (isinstance(opt, dict) and opt.get("raw")):
        out = doc(f"{d}/{m[1]}", m[0], raw=True)
        if isinstance(opt, dict) and opt.get("blurb"):
            out["blurb"] = opt["blurb"]
        return out
    out = doc(f"{d}/{m[1]}", m[0])
    if isinstance(opt, dict) and opt.get("blurb"):
        out["blurb"] = opt["blurb"]
    if isinstance(opt, dict) and opt.get("general"):
        out["general"] = True
    if isinstance(opt, dict) and opt.get("append"):
        rel = f"{d}/{opt['append']}"
        n = len(re.findall(r"(?m)^## ", out["md"])) + 1
        out["md"] = out["md"].rstrip() + f"\n\n---\n\n## {n}. {opt.get('as', 'The file')}\n\nThis is the complete file (`{opt['append']}`), ready to copy.\n\n" + as_code(rel, read(rel))
    return out


def examples_page(d: str, cfg: dict) -> dict:
    """One chapter-like page: the introduction, then every example as a numbered, foldable part."""
    parts = [f"# {cfg.get('materials_label', 'Examples')}\n\n" + cfg.get("materials_intro", "").strip()]
    for n, m in enumerate(cfg["materials"], 1):
        opt = m[2] if len(m) > 2 and isinstance(m[2], dict) else {}
        body = embed_figures(read(f"{d}/{m[1]}"), f"{d}/{m[1]}")
        body = re.sub(r"(?s)^# [^\n]*\n+", "", body)                               # its own title
        body = re.sub(r"(?s)^.*?(?=^## |\Z)", "", body, count=1, flags=re.M) if re.search(r"(?m)^## ", body) else body
        body = re.sub(r"(?m)^## \d+\. What does[^\n]*\n+", "", body)                 # "1. What does X do?"
        body = re.sub(r"(?m)^## (?!#)", "### ", body)                                   # other parts become subsections
        body = re.sub(r"(?m)^---\s*$\n?", "", body).strip()
        if opt.get("append"):
            rel = f"{d}/{opt['append']}"
            body += f"\n\n### {opt.get('as', 'The file')}\n\nThe complete file (`{opt['append']}`), ready to copy.\n\n" + as_code(rel, read(rel))
        parts.append(f"## {n}. {m[0]}\n\n{body}")
    md = "\n\n---\n\n".join(parts) + "\n"
    return {"title": cfg.get("materials_label", "Examples"), "path": f"{d}/README.md", "md": md, "parts": True}


def build_module(cfg: dict) -> dict:
    if "steps" in cfg:  # orientation: fully configured
        steps = []
        for s in cfg["steps"]:
            if s["kind"] == "slides":
                steps.append({**s, "md": embed_figures(read(s["path"]), s["path"])})
            elif s["kind"] == "doc":
                text = read(s["path"])
                if "section" in s:
                    text = section(text, s["section"])
                steps.append({**s, "doc": doc(s["path"], s["label"], text=text)})
            else:
                steps.append(s)
        return {k: v for k, v in cfg.items() if k != "steps"} | {"steps": steps}

    d = cfg["dir"]
    readme = read(f"{d}/README.md")
    sc = parse_self_check(read(f"{d}/self_check.md"))
    hackathon = cfg.get("materials_label") == "Tracks"
    # Learn first (information), then practise (optional exercises/trials), then reflect.
    steps = []
    if cfg.get("intro"):
        steps.append({"key": "basics", "label": cfg["intro"][0], "kind": "doc", "phase": "learn",
                      "doc": doc(f"{d}/{cfg['intro'][1]}", cfg["intro"][0])})
    ex = section(readme, r"Exercise")
    chapter_md = readme.replace(ex.rstrip(), "").rstrip() + chr(10) if ex else readme
    steps.append({"key": "guide", "label": "Hackathon guide" if hackathon else cfg.get("guide_label", "Chapter"), "kind": "doc", "phase": "learn",
                  "doc": doc(f"{d}/README.md", "Chapter", text=chapter_md)})
    if cfg.get("materials"):
        steps.append({"key": "materials", "label": cfg.get("materials_label", "Extra reading"), "kind": "docs",
                      "phase": "learn",
                      **({"intro": "", "docs": [examples_page(d, cfg)]} if cfg.get("materials_toggles") else
                         {"intro": cfg.get("materials_intro", ""), "docs": [material(d, m) for m in cfg["materials"]]})})
    if not cfg.get("no_exercise"):
        parts = []
        if ex:
            parts.append(doc(f"{d}/README.md", "Exercise instructions", text=ex))
        for f in cfg["exercise_files"]:
            parts.append(doc(f"{d}/{f}", Path(f).name))
        steps.append({"key": "exercise", "label": "Exercise", "kind": "docs", "phase": "practice", "docs": parts})
    steps.append({"key": "selfcheck", "label": cfg.get("selfcheck_label", "Self-check"), "kind": "doc",
                  "phase": "apply" if hackathon else "practice",
                  "doc": doc(f"{d}/self_check.md", cfg.get("selfcheck_label", "Self-check"))})
    # Slides come last, as an optional recap of the chapter.
    steps.append({"key": "slides", "label": "Kick-off slides" if hackathon else "Slides", "kind": "slides",
                  "phase": "extra", "path": f"{d}/slides.md", "md": embed_figures(read(f"{d}/slides.md"), f"{d}/slides.md")})
    steps.append({"key": "progress", "label": "Wrap-up", "kind": "progress", "phase": "reflect"})

    out = {k: v for k, v in cfg.items() if k not in ("materials", "exercise_files", "materials_label", "materials_intro", "materials_toggles", "intro",
                                                     "selfcheck_label", "no_exercise", "guide_label")}
    merged = out | sc | {"steps": steps}
    if not merged["experiment"] and cfg.get("experiment"):
        merged["experiment"] = cfg["experiment"]
    return merged


def h2_sections(md: str) -> list[tuple[str, str]]:
    """(heading, text) for every '## ' section, ignoring headings inside code fences."""
    out, cur_h, cur, fence = [], None, [], False
    for line in md.splitlines():
        if line.lstrip().startswith(("```", "~~~")):
            fence = not fence
        if not fence and line.startswith("## "):
            if cur_h is not None:
                out.append((cur_h, "\n".join(cur)))
            cur_h, cur = line[3:].strip(), []
        elif cur_h is not None:
            cur.append(line)
    if cur_h is not None:
        out.append((cur_h, "\n".join(cur)))
    return out


def term_keys(term: str) -> list[str]:
    """Search keys for a term: the full name, the part before brackets, the abbreviation, each '/' alternative."""
    t = re.sub(r"[`*]", "", term)
    keys = [t]
    m = re.match(r"^(.*?)\s*\((.+)\)\s*$", t)
    if m:
        keys += [m.group(1), m.group(2)]
    for k in list(keys):
        keys += [x.strip() for x in k.split("/")]
    keys = [k.strip() for k in keys if len(k.strip()) >= 3 and k.strip().lower() not in ("the", "and", "data")]
    return list(dict.fromkeys(keys))


def add_course_links(modules: list[dict], dictionary: list[dict]) -> None:
    """For each dictionary term, find the chapter sections that explain it.

    A section scores high when the term is in its heading or a sub-heading, or
    has a 'So what is ...?' concept box; lower for a bold mention or several
    mentions. The best three become 'read more in the course' links.
    """
    docs = []
    for m in modules:
        if m["id"] == "m0":
            continue
        for st in m["steps"]:
            if st["kind"] == "doc" and st["key"] in ("guide", "basics"):
                label = st["label"]
                for i, (h, body) in enumerate(h2_sections(st["doc"]["md"])):
                    if re.match(r"^(Chapter summary|Summary|Looking ahead|After the hackathon|Key takeaways|\d+\. Quick check)", h):
                        continue
                    docs.append((m, st, label, i, h, body))
    for e in dictionary:
        keys = term_keys(e["term"])
        scored = []
        for (m, st, label, i, h, body) in docs:
            score = 0
            heads3 = "\n".join(l for l in body.splitlines() if l.startswith(("### ", "#### ")))
            for k in keys:
                pat = r"(?<![\w-])" + re.escape(k) + r"(?:s|es)?(?![\w-])"
                flags = 0 if (k.isupper() or len(k) <= 4) else re.I
                if re.search(pat, h, flags):
                    score = max(score, 6)
                if re.search(pat, heads3, flags):
                    score = max(score, 5)
                if re.search(r"So what (?:is|are) (?:a |an |the )?" + pat, body, flags):
                    score = max(score, 5)
                if re.search(r"\*\*" + pat + r"[^*]{0,40}\*\*", body, flags):
                    score = max(score, 3)
                hits = len(re.findall(pat, body, flags))
                if hits >= 3:
                    score = max(score, 2)
                elif hits:
                    score = max(score, 1)
            if score >= 1:
                scored.append((score, m["num"], i, m, st, label, h))
        scored.sort(key=lambda x: (-x[0], x[1], x[2]))
        if scored and scored[0][0] >= 2:
            scored = [x for x in scored if x[0] >= 2]   # mentions in passing only when nothing better exists
        else:
            scored = scored[:2]
        e["links"] = [{"label": f"Module {int(m['num'])} · {label} · {h}", "href": f"#{m['id']}.{st['key']}.{i}"}
                      for sc, _, i, m, st, label, h in scored[:3]]


def main() -> None:
    modules = [build_module(m) for m in MODULES]
    resources = [{"id": r[0], "title": r[1], "summary": r[3], "doc": doc(r[2], r[1])} for r in RESOURCES]
    resources.append(limits_page())
    dictionary = parse_glossary()
    add_course_links(modules, dictionary)
    # dictionary figures: embedded once, shared by every word that uses them
    dict_figs = {e["fig"]: "data:image/svg+xml;base64," + base64.b64encode((ROOT / e["fig"]).read_bytes()).decode("ascii")
                 for e in dictionary if e.get("fig")}
    data = {"version": VERSION, "built": date.today().isoformat(), "modules": modules, "resources": resources,
            "dictionary": dictionary, "dictionary_path": "course/glossary.md", "dict_figs": dict_figs,
            "contact": CONTACT_EMAIL}

    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    template = TEMPLATE.read_text(encoding="utf-8")
    if PLACEHOLDER not in template:
        raise SystemExit(f"Placeholder {PLACEHOLDER} not found in {TEMPLATE}")
    marked = (ROOT / "course" / "vendor" / "marked.min.js").read_text(encoding="utf-8").replace("</script", r"<\/script")
    html = template.replace(PLACEHOLDER, payload).replace("__MARKED__", marked).replace("__VERSION__", VERSION)
    OUTPUT.write_text(html, encoding="utf-8")

    n_docs = sum(len(s.get("docs", [])) + ("doc" in s) + (s["kind"] == "slides") for m in modules for s in m["steps"])
    print(f"Wrote {OUTPUT.relative_to(ROOT)} (v{VERSION}): {len(modules)} modules, {n_docs} module documents, "
          f"{len(resources)} resources, {len(dictionary)} dictionary terms, {OUTPUT.stat().st_size / 1024:.0f} KB")
    for m in modules:
        if m["id"] != "m0" and (not m["objectives"] or not m["done"]):
            print(f"  warning: {m['id']} has no objectives or done-when items parsed from self_check.md")


if __name__ == "__main__":
    main()
