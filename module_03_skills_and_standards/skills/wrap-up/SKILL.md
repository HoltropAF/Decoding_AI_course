---
name: wrap-up
description: End a work session by updating the project's status files (roadmap, decisions, changelog or project log) so the next session can pick up where this one stopped, and propose a commit. Use when the user says they are done for now, asks to wrap up, or asks to update the roadmap or log.
---

# Wrap-up

Close a work session so that the next one, by you, a colleague or a fresh
AI chat, starts with an accurate picture of where the project stands. The
status files are the project's memory between sessions; this skill keeps
them true.

## When to use

- At the end of a work session, or when the user says "let's stop here".
- Before handing a project over to a colleague.
- When the user asks to update the roadmap, the decisions or the log.

## How to work

1. **Find the status files.** Use the ones the project's `CLAUDE.md`
   names. If it names none, look for `ROADMAP.md`, `DECISIONS.md` and
   `CHANGELOG.md` in the root, and in an ENCORE project for `0_PROJECT.md`
   (the project log). If none exist, offer to create `ROADMAP.md` and
   `DECISIONS.md`, and stop until the user agrees.
2. **Work out what happened this session.** Read the conversation and the
   changes (`git status`, `git diff`, and `git log` for commits made in
   this session). List what was finished, what was started but not
   finished, and what was decided.
3. **Update the roadmap.** Tick off finished items under *Now*. Add new
   tasks that came up. Move items between *Now*, *Next* and *Later* only
   if the user said so.
4. **Record decisions.** One entry per real choice, newest first: the
   date, the decision in one line, and why. A decision is a choice someone
   could later question ("we teach plan mode in Module 2 because…"), not
   a task that was done.
5. **Log the changes.** Add finished work to the changelog under
   *Unreleased* (or as a dated entry in `0_PROJECT.md`), grouped as Added,
   Changed and Fixed.
6. **Check `CLAUDE.md`.** If the user had to correct you on the same thing
   twice this session, propose one line for `CLAUDE.md` per correction.
7. **Show, then save.** Show the proposed changes to every file and wait
   for the user's OK before writing them.
8. **Propose a commit** of the status files (and any work not yet
   committed), with a message in the project's style. Don't push.

## Standards

- Write for a reader who wasn't there: full sentences, no "as discussed".
- Keep the files short. The roadmap is a list of tasks, not a diary; the
  details live in the commits.
- Dates as YYYY-MM-DD.
- Only record what actually happened or was actually decided. If you're
  unsure whether something was finished or decided, ask.

## Output

A short summary of the session (finished, open, decided), followed by the
proposed changes per file and the proposed commit message.

## Never

- Tick off a task that wasn't finished or checked.
- Invent decisions or reasons the user didn't give.
- Remove roadmap items without asking; mark them as dropped instead.
- Put secrets, patient data or real data values in the status files.
- Push, or commit without the user's OK.
