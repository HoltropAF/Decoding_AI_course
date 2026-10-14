# Changelog

All notable changes to the course are listed here, newest first.
Versions follow `MAJOR.MINOR.PATCH` as described in
[CONTRIBUTING.md](CONTRIBUTING.md).

## [Unreleased]

### Added
- `CHANGELOG.md` and `CONTRIBUTING.md` with the commit convention and
  release steps.
- "In practice" box type for use cases: a real situation, what to do and
  what to check.
- Module 2: let the AI ask clarifying questions before it starts, and an
  "In practice: plan before you build" box on plan mode. The plan-mode
  tips in Modules 4 and 5 now point back to it.
- Module 2: "Think out loud, then let the AI sort it": dictate your
  thinking, then let the AI organise it into topics, decisions, questions
  and to-dos, with a dated note comparing dictation tools (including
  Wispr Flow).
- Module 2: being interviewed by the AI (the flipped interaction), "The
  yes-man reflex" on sycophancy in part 3, "Ask a panel of readers"
  (let the AI read your draft as three different readers), and a coffee note on whether politeness
  matters.
- Module 2: "In practice: plan in one session, build in another", with
  the plan as a `PLAN.md` handover file.
- Module 3: "In practice: give every new chat a running start" (roadmap,
  decisions and changelog read in by `CLAUDE.md`), a fifth example skill
  `wrap-up`, and a stretch step in the exercise.
- Module 5: "In practice: one AI to plan, another to code", with the
  coding agent reviewing the plan before it builds.
- Module 5: this repository as a worked example of choosing building
  blocks.
- `CLAUDE.md`, `ROADMAP.md` and `DECISIONS.md` for working on the course
  itself.
- Finish page: a confetti celebration (with a button to fire it again) and
  "One last piece of advice": help or automation, once or always,
  generative or predictive, and the ladder from rule to generative AI.
- Module 1: myths 6 and 7 ("It reads everything you give it", "The longer
  the chat, the better it knows me"); the myths are now seven.
- Module 2: "Working around the limits", a table of thirteen limitations
  with how you notice them and what to do, plus three worked sections:
  thirty papers without losing the middle, calculating in code, and code
  for an older package version.
- A "Limits & workarounds" cheat-sheet page in the menu, built from the
  same table.
- A "Prompt cookbook" (`course/templates/prompt_cookbook.md`), also in the
  menu: about twenty reusable prompts from the course, from a session
  starter to a wrap-up, to copy into your own file. Module 2's coffee note
  points to it.
  It starts from situations ("I have a pile of papers to get through"):
  in the dashboard you pick a situation on the left and get a short sketch
  and the suggested prompt on the right, with a copy button, the parts to
  fill in highlighted, and a button to save it as your own file.
- A "Copy" button on every code block in the dashboard.
- Arrow up and down move through the situations in the Prompt cookbook
  and through the words in the Dictionary's look-up view, also while the
  cursor is in the search box.
- "Extra reading" under "General" in the menu, laid out like a module:
  numbered steps for the Prompt cookbook, Limits & workarounds and the
  Timeline, with Next buttons. The pages no longer have their own menu items.
- Four new Extra reading pages on more advanced topics: "Inside the
  model" (interpretability and whether a reasoning model's thinking is
  faithful), "AI built for biology" (protein and single-cell language
  models, AI for spectra and antigens, how to read the next foundation
  model paper), "Local models, one step further" (quantisation levels,
  context length and the KV cache, licences, testing on your own task)
  and "AI in papers, grants and review" (journal and funder rules).
  Modules 1, 2, 5 and 6 and hackathon track B link to them where the
  topic comes up. Their sources are in the References.
- "Inside the model" and "AI built for biology" end with an optional
  deep-dive part that reads the key papers closely: methods, data, the
  numbers and the limitations (sparse autoencoders, circuit tracing,
  faithfulness tests; ESM-2, ESM3, and the two single-cell benchmarks).
- A second menu item next to Extra reading, "Deep dives", for optional,
  more technical pages: "Inside the model" and "Local models, one step
  further" moved there. Extra reading keeps the nice-to-haves: Prompt
  cookbook, Limits & workarounds, AI built for biology, AI in papers,
  grants and review, and the Timeline.
- Step bars that are wider than the screen get arrow buttons at both
  ends, scroll with the mouse wheel, and fade on the side with more steps.

### Changed
- Version numbers now use three parts: `1.0` became `1.0.0`.
- The dashboard shows at 75% on computer screens by default; Preferences
  has a "Page size" setting (75%, 90%, 100%). Phones stay at full size.
- The network picture in the menu is now a background layer behind the
  menu instead of a block at the bottom.
- Less space between the chapter parts of an open module in the menu, so
  the menu fits on the screen.

### Removed
- The certificate on the finish page.

## [1.0.0] - 2026-10-13

First release of Decoding AI: six modules, the course dashboard,
glossary, facilitator guide and reference material. Released as `v1.0`.
