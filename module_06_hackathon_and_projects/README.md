# Module 6 · Hackathon & Projects

Picture the end of day two. Four teams, four laptops on the big screen.
One team shows an agent that reads a DEG list and a lipid change matrix and
links `Sptlc2` going up to ceramides going up, with Reactome identifiers
for every claim. Another team shows a fully local question-answering tool
over twenty immunology papers that never sends a byte off the laptop. A
third team shows something that didn't work, and explains exactly why: the
model invented pathway members in 4 out of 20 test cases, and their
validation caught every one. That third demo might be the most useful of the
day.

That's what this module is for. Modules 1 to 5 were like learning each
instrument in the lab on its own: the privacy rules, the art of a good
briefing, shared standards, safe connections to data, and delegating to
agents. The hackathon is the first real experiment where you use them
together, in a small team, under a bit of time pressure, on a question our
lab cares about. Expect some things to work beautifully and others to fall
apart in instructive ways. Both are good results, as long as you can show
which is which.

> **In this chapter**
> - The biological story all tracks share: dendritic cells sensing, maturing and migrating
> - How each module comes back in the hackathon
> - The five tracks (one needs no coding at all), the two-day schedule, the rules and the judging
> - What to hand in, where to get help, and what happens afterwards
> - **Time:** about 25 minutes of reading; the event itself is two days (or one long day)
> - **You need:** Modules 1–5 done (at least the Module 1 and 2 scripts running), a team of 2–4, and an evaluation plan (the next step in this module)

> **Tip:** pick your track with your team before the day, get your data
> loading the week before, and agree on what "success" means before you
> build. And bring snacks. This is not optional.

---

## 1. The biology: one story, many layers

All tracks orbit one biological story that our lab cares about: **how
dendritic cells (DCs) sense a stimulus, remodel their transcriptome and
lipid membranes, mature, and migrate to the lymph node to prime T cells.**
It's a story with a lot of moving parts, which is exactly why it suits a
hackathon. A dendritic cell that meets a bacterial signal like LPS switches
on hundreds of genes within hours, reshapes its membranes (ceramides and
cholesterol shift, prostaglandins are made), puts the receptor CCR7 on its
surface, and travels to the nearest lymph node to show what it found to T
cells. Each of those steps leaves traces in a different kind of data:
RNA-seq for the genes, lipidomics for the membranes, imaging and models for
the migration. No single dataset tells the whole story, and that is where AI
tools can help: connecting layers, digging through literature, and taking
the tedious parts off our hands, as long as we check what they tell us.

| Domain | Typical data | AI opportunity |
|--------|--------------|----------------|
| **Transcriptomics (RNA-seq)** | DESeq2/edgeR DEG tables, normalised counts, time courses after TLR stimulation | Functional annotation of DEG clusters; linking DEGs to DC maturation (CD40, CD80/86, CCR7, IL-12) and migration programmes |
| **Lipidomics & metabolomics** | LC-MS feature tables, lipid species/class change matrices, metabolite concentrations | Mapping lipid IDs to classes and pathways (LIPID MAPS, HMDB, Reactome); linking sphingolipid/ceramide, cholesterol and eicosanoid shifts to gene expression |
| **Multi-omics integration** | DEG list + lipid change matrix from the same perturbation | Cross-layer reasoning: enzymes (e.g. `Sptlc2`, `Cers6`, `Ptgs2`, `Hmgcr`) ↔ products (ceramides, prostaglandins, sterols) |
| **Lymph node / spatial dynamics** | Literature, imaging-derived migration parameters, kinetic/agent-based models | Grounded literature synthesis; parameterising and debugging migration/interaction models |

<!-- speak: A table of four biological domains. Transcriptomics: annotate gene clusters and link them to maturation and migration. Lipidomics and metabolomics: map lipids to classes and pathways and link lipid shifts to gene expression. Multi-omics integration: reason across layers, from enzymes to their products. Lymph node dynamics: grounded literature synthesis and help with migration models. -->

**Data rule for the hackathon:** use **public or synthetic data only**
(GEO, ArrayExpress, MetaboLights, Metabolomics Workbench, simulated
matrices). Confidential lab data may only be used in Track B with a fully
local setup, and with PI approval.

Useful public starting points (check accessions before use):

- GEO: search "bone marrow derived dendritic cells LPS RNA-seq" (mouse BMDC
  time courses).
- MetaboLights / Metabolomics Workbench: search "dendritic cell
  lipidomics" or "macrophage LPS lipidomics" (closely related biology).
- Reactome, KEGG, LIPID MAPS, HMDB and Ensembl APIs for annotation.

<details class="think"><summary>Pause and think: why public or synthetic data only, even though the hackathon is internal?</summary>

Because in two days, under time pressure, people take shortcuts: a quick
paste into a cloud chat to debug something, a file in the wrong folder of a
shared repo, an API key in a commit. With public or synthetic data, none of
those shortcuts can leak anything that matters. It also means every team's
project can be shown, shared and continued afterwards without a data
agreement in the way.

</details>

> **In short**
> - Every track works on the same story: DCs sensing, remodelling, maturing and migrating.
> - Each layer of that story lives in different data; AI can help connect them.
> - Public or synthetic data only (Track B: local and with PI approval).

---

## 2. How the hackathon brings the course together

The word itself is younger than many of us: ["hackathon"](https://en.wikipedia.org/wiki/Hackathon), a blend of
*hack* and *marathon*, was first used in 1999, when developers of the
OpenBSD operating system and, a few days later, the company Sun
Microsystems both organised events where programmers built something
together in one intense stretch. Science picked up the format later, with
bioinformatics and open-data hackathons from the 2010s on. The idea has
stayed the same: a small team, a short time, a concrete question, and a
demo at the end. That's what we'll do here.
Every track uses all five modules; only the emphasis differs. Before the
event, skim your own notes from Modules 1–5 under *Wrap-up* in each module
(or all at once under *My notes*): they're your starting material.

| Module | What you apply in the hackathon | Where it matters most |
|--------|----------------------------------|-----------------------|
| 1 · Foundations | Choose cloud or local per data class; local inference with Ollama; scrub identifiers from logs | B (fully local), C (logs) |
| 2 · Prompting & Context | Five-part prompts, prompt engineering with a small test set, delimited inputs, Pydantic schemas, semantic checks, retries | A, D (structured reports and hypotheses) |
| 3 · Skills & Standards | The lab `CLAUDE.md` in your team repo; reusable prompt templates under version control | All tracks |
| 4 · MCP & Data | Read-only tools for Reactome, LIPID MAPS, local files; least privilege | A (pathway lookups), D (grounding) |
| 5 · Agents & Subagents | Agent loops with human approval, read-only reviewer subagents, Themis audit before code freeze | C (debugger agent), all (review) |
| Self-check experiments | Hypothesis first, ground truth, baseline, n and uncertainty | Your evaluation plan |

<!-- speak: A table showing how each module returns in the hackathon. Module 1: choosing cloud or local and scrubbing logs. Module 2: structured prompts, test sets and validation. Module 3: the lab instruction file and versioned templates. Module 4: read-only tool connections. Module 5: agents with approval and a Themis audit. And the self-check experiments shape your evaluation plan. -->

> **In short**
> - Every module comes back; your module notes are your starting material.
> - The self-check experiments are the model for your evaluation plan.

---

## 3. The tracks

There are five tracks to choose from. They differ in focus and in how much
they lean on cloud or local tools, but each one touches every module. Pick
the one that matches your curiosity, or the problem you'd actually like to
see solved.

| Track | Title | Core skills | Privacy profile |
|-------|-------|-------------|-----------------|
| [A](track_a_multiomics_synthesis/README.md) | Multi-omics synthesis agent | MCP, structured output, HTML reporting | Public/synthetic data; cloud or local |
| [B](track_b_local_immunology_rag/README.md) | Local immunology RAG | Ollama, embeddings, vector database, Streamlit | **Fully local** |
| [C](track_c_pipeline_debugger/README.md) | Pipeline debugger | Log parsing, agents, human approval, tests | Synthetic failing pipelines; cloud or local |
| [D](track_d_dendritic_cell_hypothesis/README.md) | DC hypothesis engine | RAG, Pydantic schemas, prediction + evaluation | Public literature; cloud or local |
| [E](track_e_lab_ai_playbook/README.md) | Lab AI playbook (**no coding**) | Prompt engineering, testing, standing instructions, lab guidelines | Public material; cloud or local |

Each track description (in the *Tracks* step) contains: objective,
background, inputs, required features, suggested architecture, stack,
milestones, success criteria and stretch goals.

<details class="think"><summary>Pause and think: your team has two wet-lab people and one bioinformatician. Which track would you pick?</summary>

Any of them can work, but A and D lean most on biological judgment
(interpreting pathways, judging hypotheses), which plays to wet-lab
strengths, while the bioinformatician wires up tools and validation. B needs
someone comfortable installing local software; C needs someone who has
debugged a lot of pipelines. Mixed teams are deliberate: the biology check
is the part AI can't do for you.

</details>

> **In short**
> - Five tracks: multi-omics synthesis, local RAG, pipeline debugger, hypothesis engine, and a no-code lab AI playbook.
> - Each uses every module; pick by curiosity and by your team's mix of skills.

---

## 4. Format and timing

The rhythm is deliberately simple. Day one is about getting *something*
working from start to finish, however rough: data in, a model doing its job,
a result out. Day two is about making it good and, just as important,
finding out whether it is actually right. The mentor check-in on the first
morning is there to save you from the most common hackathon mistake:
building for a day and a half before deciding how you'll know if it works.
The event takes two consecutive days; it can be compressed into one long
day by dropping the stretch goals.

### Before the event (week before)

A little preparation makes the two days a lot more fun, mostly because
nobody wants to spend the first morning waiting for downloads.

- Track E needs no installs beyond a chat app (and Ollama for local
  work). For the other tracks: install Python 3.10 or newer, Git, Ollama (pull `llama3.1:8b` and an
  embedding model such as `nomic-embed-text`), and Claude Code if your track
  uses it.
- Complete the Modules 1–5 exercises (at minimum: the Module 1 and 2
  scripts run).
- Form teams of **2–4**, mixing wet-lab and computational people. Choose a
  track and register it with the organisers.
- One person per team prepares the input data (public/synthetic) and checks
  it loads.
- Fill in the **evaluation plan** (the next step in this module) together.

### Day 1

| Time | Block |
|------|-------|
| 09:00 | Kick-off: rules, tracks, biology refresher (DC maturation & migration, lipid remodelling) |
| 09:30 | Team planning: write `plan.md` (scope, architecture, roles, minimum viable product) |
| 10:00 | **Plan review** with a mentor (10 min per team) |
| 10:30 | Build sprint 1: data in, first LLM call working end-to-end |
| 12:30 | Lunch |
| 13:15 | Build sprint 2: core feature |
| 15:30 | Stand-up: each team 2 minutes (what works, what is blocked) |
| 15:45 | Build sprint 3: validation and tests |
| 17:30 | End of day 1: commit and push; the core should run end-to-end |

### Day 2

| Time | Block |
|------|-------|
| 09:00 | Stand-up |
| 09:15 | Build sprint 4: quality, evaluation against success criteria |
| 12:00 | Lunch |
| 12:45 | Build sprint 5: stretch goals, documentation, demo prep |
| 14:30 | **Code freeze** |
| 14:45 | Demos: 7 min presentation + 3 min questions per team |
| 16:15 | Jury deliberation; retrospective with all participants |
| 16:45 | Results, wrap-up, decide which projects to continue |

> **It's okay:** if your core isn't running at the end of day one. Cut
> scope, not corners. A smaller thing that works and is honestly evaluated
> beats a big thing that might work.

> **In short**
> - Day one: something working end-to-end. Day two: make it good and find out if it's right.
> - Prepare the week before: installs, data loading, teams, evaluation plan.

---

## 5. Rules

The rules are few, and mostly about keeping data safe and results honest.

1. **Data:** public or synthetic only, except Track B with a fully local
   stack and PI approval. No patient or donor data, no collaborator data, no
   unpublished manuscripts in any cloud tool.
2. **Secrets:** API keys only in environment variables or a git-ignored
   `.env`. A committed key means immediate rotation and a point deduction.
3. **Repository:** each team works in its own repo (or branch) following the
   ENCORE layout, or at least: `README.md`, `plan.md`, `src/`, `tests/`,
   `data/README.md` (describing the data source, not containing private
   data), and `environment.yml` or `requirements.txt`.
4. **Reproducibility:** the demo must run from a fresh clone following the
   README. Record model names and versions.
5. **AI use is encouraged, and disclosed.** That's the point. Say in your
   README which tools you used for what. Text from Claude, Gemini and (in
   the EU) ChatGPT may carry an invisible watermark anyway (Module 1), but
   the watermark is not the disclosure. Keep the lab `CLAUDE.md` (Module 3)
   in your repo and use read-only subagents for review.
6. **Human in the loop:** any agent that edits files, runs commands or
   writes to databases must ask for confirmation (Track C especially).
7. **Honesty:** demo what actually works. Mocked parts must be labelled as
   such.
8. **Run Themis** (Module 5) on your repo before code freeze and include the
   summary line in your README.

> **In short**
> - Safe data, no secrets, a reproducible repo, disclosed AI use.
> - Human approval for agents with side effects; honest demos; a Themis audit before freeze.

---

## 6. Judging, deliverables and support

There's nothing to win but feedback and a bit of glory. The judging is
mainly a way to give each team useful comments and to decide which ideas
the lab wants to keep.

| Criterion | Weight | What the jury looks for |
|-----------|--------|-------------------------|
| Scientific value | 25% | Biologically meaningful output; would this help a real analysis? |
| Technical quality | 20% | Works end-to-end, sensible architecture, tests |
| Correctness & validation | 20% | Outputs checked against ground truth/databases; hallucinations measured and controlled |
| Privacy & safety | 15% | Data handling, secrets, least privilege, human approval |
| Reproducibility | 10% | Fresh-clone run, pinned environment, documented models |
| Demo & documentation | 10% | Clear, honest, understandable to a wet-lab scientist |

<!-- speak: A table of judging criteria. Scientific value counts for a quarter. Technical quality and correctness with validation count for a fifth each. Privacy and safety fifteen percent. Reproducibility and the demo with documentation ten percent each. -->

Notice that correctness and validation weigh as much as technical quality.
A team that measures how often its tool is wrong scores better than a team
with a slicker tool that never checked.

### What to hand in at code freeze

- Repository link with README (how to run, data sources, models used,
  limitations).
- `plan.md` (the original plan plus what changed).
- A short evaluation section: the success criteria from the track
  description and your evaluation plan, and whether each was met, with
  evidence.
- The Themis audit summary line.
- Demo slides or a live demo script (7 minutes at most).

### Support

Nobody is expected to know everything. If you're stuck for more than
twenty minutes, ask.

- **Mentors** rotate between teams; book 10-minute slots on the board.
- **Help channel:** post blockers early; include the error message, scrubbed
  of paths and identifiers (Module 1).
- **Fallbacks:** if the cloud API fails, switch to Ollama; if your local
  model is too weak, reduce scope rather than switching to real data.

<details class="think"><summary>Pause and think: your tool works, but you have no ground truth to compare against. What can you still show the jury?</summary>

Quite a lot. Run-to-run consistency (as in the Module 2 experiment). A
small hand-checked sample: ten outputs that you verified in Reactome or the
literature, with the error count. A baseline: what does a classical method
(enrichment analysis, a keyword search) give for the same input? And an
honest limitations paragraph. "We checked 10, 8 were right, here are the 2
that weren't" is a strong result.

</details>

> **In short**
> - Correctness and validation weigh as much as technical polish.
> - Hand in a reproducible repo, the plan, an evidence-based evaluation and the Themis line.
> - Stuck for twenty minutes? Ask a mentor.

---

## 7. Summary and what's next

### Chapter summary

The hackathon is where the course stops being a set of separate skills and
becomes a way of working. All the research tracks follow the same biological story
of dendritic cells sensing a stimulus, remodelling their genes and
membranes, maturing and migrating, and each touches every module: privacy
choices, structured prompts with a test set, shared standards, read-only
tool connections and agents with a human in the loop.
The format is simple on purpose. Day one gets something working end to end;
day two makes it good and finds out whether it's right. The rules keep data
safe and results honest, and the judging rewards validation as much as
polish. The most valuable output of the two days might not be a tool at all,
but a clear, evidence-based answer to the question "how well does this
actually work?"

**Key points**

- Public or synthetic data only (Track B: fully local, with PI approval).
- Agree on your evaluation plan before you build.
- Day one end-to-end, day two quality and evaluation.
- Disclose AI use, keep humans in the loop, demo honestly.
- "It didn't work, and here's the evidence why" is a good result.

### After the hackathon

The hackathon isn't the end of the course; it's where the useful bits get
picked up and carried into our daily work.

- Winning and promising projects get a follow-up slot in a lab meeting.
- Useful skills, agents and prompt templates are contributed back to this
  repository via pull request.
- Retrospective notes go into `module_06_hackathon_and_projects/` as
  `retrospective_<YYYY-MM>.md` to improve the next edition.

Next in this module: the **Tracks** (pick one), the **Evaluation plan**
(fill it in as a team before the day), and the **kick-off slides** for the
first morning.

---

**Previous:** [Module 5](../module_05_agents_and_subagents/README.md)
