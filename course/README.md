# Course Resources

Everything that spans all modules: the route through the course, slides
for the orientation, shared templates, and background reading.

**The goal of the course:** colleagues know roughly how AI works, the
current debates and the limitations, how to use it in their daily work, and
how to prompt it well. It's about using AI, not building it.

| File | What it is for |
|------|----------------|
| `dashboard.html` | **The course itself:** every slide deck, guide, exercise, self-check and resource in one page, with your own checklists and notes (stored in your browser only). Generated; do not edit by hand |
| `dashboard_template.html`, `build_dashboard.py` | Layout of the dashboard and the script that packs all course files into it |
| `orientation.md` | The Welcome page of the Orientation in the dashboard: what the course is for, how it works, the ground rule, getting ready |
| `slides_00_orientation.md` | 30-minute opening session: why, the route, the scientific stance, privacy ground rules |
| `facilitator_guide.md` | How to run a 2-hour group session; per-module preparation and pitfalls |
| `glossary.md` | Definitions of all terms used in the course |
| `references.md` | All papers, policies and sources behind the course (the References page in the dashboard) |
| `templates/ai_use_log.md` | Record AI use in your own projects; includes a draft disclosure statement |
| `templates/ai_output_verification_checklist.md` | Check AI output before treating it as a result |

## The route

```
Orientation ─► M1 Foundations ─► M2 Prompting & Context ─► M3 Skills & Standards
                                                                              │
          M6 Hackathon (teams) ◄─ M5 Agents & Subagents ◄─ M4 MCP & Data ◄────┘
```

- **Modules 1–5** can be done alone or in group sessions of ~2 hours.
  Group sessions are recommended: the experiments and critical questions
  work better with pooled results and discussion.
- **Module 6** is a team event (2–4 people per team) after everyone has
  finished Modules 1–5.
- Suggested pace: one module every one to two weeks; about 12–15 hours in
  total before the hackathon.

## Each module reads like a chapter

Every module is written as a chapter of a small textbook, by a colleague
rather than a committee: an opening story, parts that each end with a
short **In short** recap, little **Pause and think** questions with hidden
answers, coffee notes and tips along the way, and a chapter summary at the
end. The recipe is in [`chapter_recipe.md`](chapter_recipe.md).

| Part, in this order | File | Time |
|------|------|------|
| Chapter (read this first) | `README.md` | 30–45 min reading |
| Extra reading | `docs/`, `templates/` | optional |
| Exercise | the *Exercise* section at the end of the README, plus `exercises/` | ~45 min |
| Self-check: objectives, knowledge check, mini-experiment, critical questions | `self_check.md` | ~30 min |
| Slides with speaker notes (optional recap, or for a group session) | `slides.md` | ~30 min |

Module 1 opens with the plain-language foundations (parts 1 and 2 of its
chapter) for anyone new to all of it; later modules add the basics they need
where they need them.

Nothing is graded. The mini-experiments are there to build the habit of
measuring AI tools before trusting them.

## Opening the dashboard

Double-click `course/dashboard.html`; it opens in your browser. Everything
is inside: pick a module in the sidebar and follow its steps.

- **Learn:** the chapter, then extra reading
- **Practice (optional):** exercise, self-check with mini-experiment
- **Extra:** the slides, as a recap
- **Wrap up:** tick off the "done when" items, read back your saved notes,
  and add new ones

Progress, notes and ratings are saved in your browser only; they are not
shared. Everything the dashboard needs is inside the file: it works
offline and makes no requests to other websites.

## Updating the dashboard (for maintainers)

The dashboard contains a copy of all course files. After changing any
slide deck, README, self-check or resource, rebuild it: on Windows,
double-click `course/update_dashboard.bat`, or run:

```bash
python course/build_dashboard.py
```

The script uses only the Python standard library. Objectives, "done when"
items, the experiment question and the first critical question are read
from each module's `self_check.md`. Keep the order of "done when" items
stable, or participants' ticks will shift to different items.

The Dictionary is built from `glossary.md` (term, definition, module) and
`glossary_details.md` (an example and "see also" links per term). The build
warns when a "see also" name doesn't match a term.

## Viewing and exporting slides

The slides are Markdown files in [Marp](https://marp.app) format, so they
live in git next to the content they summarise.

- **Preview:** install the "Marp for VS Code" extension and open a
  `slides.md` file; click the preview button.
- **Export to PowerPoint or PDF:**

  ```bash
  npx @marp-team/marp-cli@latest module_01_foundations_and_privacy/slides.md --pptx
  npx @marp-team/marp-cli@latest module_01_foundations_and_privacy/slides.md --pdf
  ```

  By default the PowerPoint export renders slides as images (not editable
  text). Edit the Markdown and re-export instead of editing the `.pptx`.
- Speaker notes are the HTML comments (`<!-- ... -->`) under each slide and
  appear as presenter notes in the export.

## Background notes

The `reference/` folder at the repository root holds the original course
planning notes and a summary of practitioner sources on context engineering.
They are optional reading; nothing in the modules depends on them.
