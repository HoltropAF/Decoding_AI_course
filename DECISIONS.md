# Decisions

Why the course is the way it is. Newest first; one entry per choice, with
the reason.

## 2026-10-13 · Status files instead of a prompt log

A roadmap (with the to-do list as its *Now* part), a decisions log and the
changelog, read in by `CLAUDE.md` and updated with the `wrap-up` skill.
**Why:** a log of every prompt grows long and is rarely reread; a new
session needs to know where things stand and why, not every message that
led there. To-do and roadmap are one file so they can't drift apart.

## 2026-10-13 · One hard rule as a hook, the rest as instructions

"Never commit on `main`" is enforced by a hook; everything else lives in
`CLAUDE.md`, `CONTRIBUTING.md` and `course/chapter_recipe.md`.
**Why:** instructions are requests, and this rule must never fail. The
writing style needs judgment, and the recipe already holds it, so there's
no separate writing skill.

## 2026-10-13 · Plan mode is taught in Module 2

The "plan before you build" use case sits right after chain-of-thought;
Modules 4 and 5 point back to it.
**Why:** it's chain-of-thought for a whole task, and the chat version
("ask me questions, then give me a plan") works for everyone from week 2,
without coding tools.

## 2026-10-13 · Use cases get their own box type

`> **In practice: <title>.**`: the situation, what to do, what to check.
**Why:** tips say *what*; a use case shows *when* and *how to check it*,
and one recognisable box makes them easy to find and collect later.

## 2026-10-13 · Work on `development`, release to `main`

Day-to-day work on `development`; `main` gets merge commits (no squash) at
release time, tagged `vX.Y.Z`.
**Why:** participants clone `main`, so it must only hold released
versions. Squash merges would break the shared history and cause conflicts
at the next release.
