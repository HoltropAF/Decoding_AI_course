# Facilitator Guide

For whoever runs a group session. Anyone who has completed the module can
facilitate it; you do not need to be an AI expert, only to have done the
exercise yourself the week before.

---

## Standard 2-hour session

| Time | Block | Notes |
|------|-------|-------|
| 0:00 | Recap & check-in (10 min) | What did people try since last time? Any surprises or failures? |
| 0:10 | Slides (30–35 min) | `module_XX/slides.md`; speaker notes contain the talking points |
| 0:45 | Live demo (10–15 min) | Run the exercise yourself, on screen, including at least one failure |
| 1:00 | Hands-on (35–40 min) | Exercise first, then the mini-experiment in pairs |
| 1:40 | Results & critical questions (20 min) | Collect experiment numbers on a shared table; discuss 2 critical questions |
| 2:00 | Close | Confidence re-rating in the dashboard; next session date |

Self-paced learners read the chapter (README) first, then do the exercise
and self-check; the slides are an optional recap. In a group session the
slides work well as the shared summary, because everyone has read the
chapter beforehand.

## Preparation checklist (one week before)

- [ ] Do the exercise and mini-experiment yourself on a clean machine
- [ ] Check that links, model tags and package versions still work
      (models and APIs change quickly; update the module if needed)
- [ ] Prepare a shared results table (whiteboard or spreadsheet) for the
      mini-experiment
- [ ] Send install instructions to participants (see per-module notes)
- [ ] Choose which two critical questions to discuss
- [ ] Export the slides: `npx @marp-team/marp-cli@latest module_XX/slides.md --pptx`
      (or `--pdf`)

## Per-module notes

### Orientation (`course/slides_00_orientation.md`, 30 min)

Can be combined with Module 1 in a single 2.5-hour session. Ask everyone to
check their AI account privacy settings before Module 1.

### Module 1 – Foundations

- **Pre-install:** Ollama and `llama3.1:8b` (~5 GB). People with 8 GB RAM:
  `llama3.2:3b`. Large downloads on conference Wi-Fi fail; install
  beforehand.
- **Demo that lands:** disconnect Wi-Fi and run the local model.
- **Pitfall:** the discussion drifts into "which model is best". Steer back
  to "how would we measure that?"
- **Experiment pooling:** combine everyone's citation counts into one
  table; the pooled n makes the confidence-interval point concrete.

### Module 2 – Prompting & Context

- **Pre-install:** `pip install requests pydantic`.
- **Demo:** `--dry-run` first so people see the assembled five-part prompt.
- **Pitfall:** slow local models make 15 runs take long. Let pairs split
  conditions and pool results.
- **Discussion starter:** run the same gene list with the context changed to
  "hepatocytes, fasting" and compare pathways.

### Module 3 – Skills & Standards

- **Needs:** Claude Code (or another agent that reads instruction files).
- **Demo:** fresh session, ask "what rules will you follow?", with and
  without the file.
- **Pitfall:** people paste huge style guides. Enforce the < 200 line rule.
- **Output to collect:** rules people added; candidates for the lab master
  template.

### Module 4 – MCP & Data

- **Needs:** Node.js 18+ or Docker for the filesystem server; `pip install
  "mcp[cli]"` for the custom server.
- **Demo:** `/mcp` listing tools, then a failed write attempt.
- **Pitfall:** Docker not available on managed laptops. Fall back to the
  `npx` filesystem server with client deny rules, and explain that this is
  weaker.
- **Security emphasis:** "read-only" ≠ "private" with a cloud model.

### Module 5 – Agents & Subagents

- **Needs:** Claude Code; a scratch ENCORE project with git initialised.
- **Prepare:** a seeded project with the 10 planted problems from the
  self-check, so the experiment starts immediately.
- **Demo:** ask Themis to fix something and show `git status` afterwards.
- **Pitfall:** over-enthusiasm for autonomy. Keep returning to "how would
  you know it is right?"

### Module 6 – Hackathon

- See `module_06_hackathon_and_projects/README.md` for timing, rules and
  judging.
- **Mentors:** at least one per 3 teams. Mentors approve `plan.md` only if
  it contains an evaluation plan (outcome, ground truth, baseline,
  threshold).
- **Prepare:** public datasets per track, tested to load; a failure zoo
  starter for Track C; a small PDF set for Track B.

## Handling common questions

| Question | Suggested answer |
|----------|------------------|
| "Can I use my real data?" | Only if its classification allows the tool you use. In this course: public or synthetic only. |
| "Which model should I use?" | The one that passes your evaluation for your task at acceptable cost and privacy. Measure it. |
| "Isn't this replacing analysts?" | It shifts work from writing to specifying and verifying. The verification skills in this course are the point. |
| "The model gave a different answer than yesterday." | Expected. Record versions; measure consistency (Module 2). |
| "Is this allowed by the journal?" | Check the journal's policy; disclose use; humans remain responsible. See the References page. |

## Keeping the course current

AI tools change monthly. After each run of a module:

- Update model tags, commands and screenshots that broke
- Record what confused people in a short note at the bottom of the
  module README
- Bump the version line in `CLAUDE.md`/templates if they changed
- Submit changes via pull request
