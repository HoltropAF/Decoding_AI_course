# Roadmap

Where the course stands and where it's going. *Now* is the to-do list.
Finished items move to `CHANGELOG.md`; the reasons behind choices go in
`DECISIONS.md`.

## Now

- [x] Add the "In practice" box type and the first use case (plan before
      you build, Module 2).
- [x] Add the running-start use case (Module 3), the `wrap-up` example
      skill, and this repository as a worked example (Module 5).
- [ ] Set up the project hook that blocks commits on `main`
      (`.claude/settings.json` and `.claude/hooks/protect_main.py`) and
      the project copy of the `wrap-up` skill (`.claude/skills/wrap-up/`).
- [ ] Release v1.1.0: merge `development` into `main` and tag it.

## Next

- [ ] More "In practice" use cases across the modules, one at a time.
- [ ] Collect all "In practice" boxes on one dashboard page.

## Later

- [ ] A chapter-reviewer subagent that checks a new chapter against
      `course/chapter_recipe.md`, once chapters are written more often.
      If it's added, it also goes into Module 5's Examples.
