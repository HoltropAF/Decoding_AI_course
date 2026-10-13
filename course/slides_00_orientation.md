---
marp: true
theme: default
paginate: true
size: 16:9
header: 'Decoding AI'
footer: 'Orientation'
style: |
  section { font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif; font-size: 26px; color: #1d2b36; background: #fbfcfc; }
  h1, h2 { color: #0f4c5c; }
  section.lead { background: #0f4c5c; color: #f4f8f8; }
  section.lead h1, section.lead h2 { color: #ffffff; }
  section.lead header, section.lead footer { color: #b9d3d6; }
  table { font-size: 20px; }
  code { font-size: 0.85em; }
  blockquote { border-left: 6px solid #e07a2f; color: #3a4a55; }
  .small { font-size: 19px; }
---

<!-- _class: lead -->
<!-- _paginate: false -->

# Decoding AI
## From LLM mechanics to read-only agents and a multi-omics hackathon

Orientation session

<!--
Welcome. This session takes about 30 minutes. Goal: everyone knows the route
through the course, what is expected, and the privacy ground rules, before
touching any tool.
-->

---

## Why this course exists

- AI tools are already used in the lab, mostly ad hoc and individually
- Results vary: impressive one day, confidently wrong the next
- Unpublished data ends up in chat windows without anyone deciding that
- Good prompts and workflows live in one person's chat history

**Aim:** use these tools as a *method*: understood, measured, documented
and shared.

<!--
Ask the room: who has used ChatGPT, Claude or Copilot for work in the past
month? Who has pasted real data? Keep it non-judgmental. The point is that
we have no shared practice yet.
-->

---

## What you'll be able to do

This course is about **using** AI well, not building it. By the end you can:

1. **Explain** roughly how AI works, and why it fails the way it does
2. **Join the debates**: privacy, bias, copyright, energy, authorship
3. **Spot the limits**: invented facts, flattery, outdated knowledge
4. **Use it** in your daily work: which tool, which data, which task
5. **Prompt** so you get reliable, checkable answers

No programming needed: every exercise has a no-code version.

<!--
This is the promise of the course. Modules 1 and 2 are the heart; Modules 3
to 5 show how to get more out of the tools, with technical parts people can
skim. Ask the room which of the five they care about most.
-->

---

## The route

| # | Module | You leave with |
|---|--------|----------------|
| 1 | Foundations | A local model running; a data-classification habit |
| 2 | Prompting & Context | Schema-validated JSON from a DEG list |
| 3 | Skills & Standards | A lab `CLAUDE.md` in your own project |
| 4 | MCP & Data | A read-only tool connection |
| 5 | Agents & Subagents | Themis + your own read-only subagent |
| 6 | Hackathon | A team project with an honest evaluation |

Modules 1–5: self-paced or in group sessions (~2 h each). Module 6: teams of 2–4.

<!--
Emphasise that every module builds on the previous one. Modules can be done
alone, but the discussion questions work much better in a group. Suggest a
rhythm: one module every one to two weeks, hackathon after module 5.
-->

---

## How each module works

1. **Chapter**: read it like a textbook chapter, ~30–45 min
2. **Extra reading**: deep dives, if you want more
3. **Exercise**: hands-on, with a "done when" list
4. **Self-check**: questions, a mini-experiment, critical questions
5. **Slides** (like these): an optional recap
6. **Wrap-up**: your checklist and notes, in the dashboard

Nothing is graded. The self-checks are for *you*.

<!--
Show the folder structure briefly and open course/dashboard.html in a
browser. Point out the little "Pause and think" questions in each chapter,
and that progress is stored only in their own browser.
-->

---

## The scientific stance

We treat an LLM like a new instrument:

- What does it measure (generate), and how?
- What are its **error modes** and **error rates**?
- What is the **ground truth** and the **baseline**?
- Is it **reproducible**: same input, same output, next month?
- Is it **documented** well enough for a methods section?

Every module has a small experiment that measures one of these.

<!--
This is the core message of the course. Compare with introducing a new mass
spectrometer: nobody would publish data from it without calibration,
QC samples and documented settings. Same here.
-->

---

## Privacy ground rules (from day one)

> Cloud model = your data leaves the machine. Settings only decide what
> happens after.

| Data class | Example | Cloud LLM? |
|------------|---------|-----------|
| Public | GEO dataset, published paper | Yes |
| Internal | Analysis code, protocols | With training opt-out |
| Confidential | Unpublished DEGs, lipid matrices, drafts | Only approved contracts, else **local** |
| Restricted | Patient/donor data, DUA data | **Never** |

All course exercises use **public or synthetic data**.

<!--
Non-negotiable. Ask everyone to check their AI account privacy settings
this week (Module 1's *Where does my data go?* has the checklist).
-->

---

## What you need

- Laptop with Python ≥ 3.10 and Git
- [Ollama](https://ollama.com) + `ollama pull llama3.1:8b` (~5 GB)
- ≥ 16 GB RAM recommended for local models
- Optional: Claude Code (Modules 3–5), Node.js 18+ (Module 4)
- A GitHub account with access to the course repository

Setup instructions: root `README.md` → *Getting started*.

<!--
Hardware check: people with 8 GB RAM can use smaller models (llama3.2:3b,
qwen2.5:3b). Make sure someone can help with installs before Module 1.
-->

---

## Course-wide resources

- `course/dashboard.html` – route, chapters, checklists and notes
- `course/glossary.md` – terms used throughout
- **References** – all papers and sources behind the course, searchable
- `course/templates/ai_use_log.md` – record AI use in your projects
- `course/templates/ai_output_verification_checklist.md` – check AI output
  before you trust it

<!--
The two templates are useful immediately, before finishing the course.
Encourage people to start an AI use log in their current project today.
-->

---

## House rules (the friendly kind)

- **There are no stupid questions.** Half of us are learning this as we go
- **Break things.** Use copies and fake data, then go wild
- **Information first, practice second.** Exercises and experiments are
  optional, but they're where it clicks
- **Bring a real problem** from your own work to each session
- **Share what failed** as well as what worked; negative results count here too
- **Snacks are encouraged**

<!--
Set the tone: this is learning together among colleagues and friends, not a
course with an exam. Nobody is graded. The point is that everyone ends up
comfortable and careful with these tools.
-->

---

## New to all of this? Start with the basics

Module 1 opens with **the foundations, in plain language**:

- What AI, machine learning, generative AI and LLMs are (and aren't)
- How an LLM is made, and why it sometimes makes things up
- Cloud vs local, and which data may go where
- Five myths, quickly busted

No background needed. If you can explain a western blot to your family, you're fine.

<!--
Reassure the people who feel they are behind. The basics page is the first
step of Module 1 in the dashboard.
-->

---

<!-- _class: lead -->

# Next: Module 1
## Foundations

Before the session: install Ollama and run
`python module_01_foundations_and_privacy/exercises/test_ollama_local.py`

<!--
Close with logistics: date of Module 1, who to contact for install
problems, where to ask questions.
-->
