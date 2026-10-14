# Decoding AI course

A course that teaches colleagues in a lipidomics and immunology lab to *use*
AI well: how it roughly works, its limits and debates, daily use and good
prompting. Six modules plus an orientation, built into one HTML dashboard.

## Rules

- Work only on the `development` branch. `main` changes only through a pull
  request at release time. Don't push unless asked.
- Commits follow Conventional Commits; releases follow the steps in
  `CONTRIBUTING.md`.
- Course text follows `course/chapter_recipe.md`: running prose like a
  textbook chapter by a colleague, no paragraphs opening with a bold label,
  few bullet lists, one "In short" box per main part. Every exercise has a
  no-code version.
- New use-case tips go in an `> **In practice: <title>.**` box: the
  situation, what to do, what to check.
- After changing course content, rebuild with
  `python course/build_dashboard.py` and commit the rebuilt
  `course/dashboard.html` with it.
- When you add a skill or agent to the course text, also add it to that
  module's Examples (`skills/` or `agents/` plus a page in `docs/`, and
  register it in `course/build_dashboard.py`).
- No real data, secrets or internal hostnames anywhere.

## Status files

Read these first; update them at the end of a session with `/wrap-up`.
`DECISIONS.md` explains why things are the way they are; read it before
changing structure.

@ROADMAP.md
@CHANGELOG.md
