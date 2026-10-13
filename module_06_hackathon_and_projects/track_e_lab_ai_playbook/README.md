# Track E – The Lab AI Playbook (no coding needed)

**One-liner:** build, test and hand over the lab's own playbook for using AI
well: a tested prompt cookbook for our most common tasks, a one-page set of
lab guidelines, and the evidence that the prompts actually work.

**Modules used:** 1 (tools, data rules, limitations, debates), 2 (prompt
engineering, test sets), 3 (standing instructions), 5 (checking research
reports)
**Team size:** 2–4 · **Difficulty:** ★☆☆☆ (MVP) to ★★★☆ (stretch) ·
**Coding:** none required

---

## 1. Background

Most of what the lab will do with AI isn't building pipelines; it's
everyday use: explaining an error, tidying a paragraph, summarising a
paper, drafting a plotting script, getting into a new topic. Right now
every one of us does that with our own prompts, our own habits and our own
idea of what's allowed. This track turns that into something shared and
tested, so that a new PhD student can be useful and safe with AI in their
first week.

It's also the most direct way to practise the heart of the course: prompt
engineering as a method (Module 2), and honest evaluation of what AI gets
right and wrong.

## 2. What you build

1. **A prompt cookbook** for at least **five** common lab tasks. For
   example:
   - explaining an R or Python error message;
   - writing a ggplot script for a volcano plot from a described table;
   - summarising a published paper for journal club;
   - turning rough notes into a methods paragraph;
   - getting oriented in a new topic with a research mode;
   - checking a draft for unclear sentences (in English and Dutch).

   Each recipe has: when to use it, the prompt (five-part structure), which
   tool and data class it's suitable for, and what to check afterwards.
2. **Lab standing instructions**: a short text for ChatGPT custom
   instructions, a Claude Project or a Gemini Gem that the whole lab can
   copy (Module 3, "In the chat apps you already use").
3. **One-page lab AI guidelines**: what may go into which tool, how to
   disclose AI use, what never to do. Written for a new colleague, in plain
   language.
4. **The evidence**: for each recipe, a small test (section 4) showing that
   the final prompt beats a naive one.

## 3. Inputs

- Public material only: published papers, public datasets (GEO,
  MetaboLights), made-up example notes and error messages.
- The chat apps the lab has access to, plus Ollama for anything that must
  stay local.
- Your own experience: ask colleagues which tasks they use AI for most.

## 4. How to test a recipe

Treat every prompt like a small experiment (Module 2, section 6):

1. Make a **test set** of three to five inputs per task (three error
   messages, three papers, three sets of notes), with a short description
   of what a good answer contains.
2. Write a **naive prompt** ("explain this error") and your **recipe
   prompt**.
3. Run both on every input, ideally twice, in fresh chats.
4. Score each answer on a simple scale (for example: correct / partly /
   wrong; invented anything yes / no) and note the time it saved.
5. Keep the recipe only if it clearly beats the naive prompt.

## 5. Milestones

| When | Milestone |
|------|-----------|
| Day 1, morning | Tasks chosen (ask at least three colleagues), test sets written |
| Day 1, afternoon | First versions of all recipes; naive vs recipe runs for two tasks |
| Day 2, morning | All tests done; recipes improved; standing instructions drafted |
| Day 2, early afternoon | Guidelines page written; cookbook formatted for the course repository |

## 6. Success criteria

- At least five recipes, each tested on at least three inputs.
- For each recipe, the evidence shows it does better than the naive prompt
  (fewer errors or invented facts, or less work afterwards).
- The guidelines fit on one page and a colleague who hasn't done the course
  understands them.
- Everything respects the data rules: no unpublished or patient data was
  used.

## 7. Stretch goals

- Test the same recipes in two different tools (for example ChatGPT and a
  local model) and report where the difference matters.
- Add a "red team" recipe: prompts that try to make the model invent
  references, and how the recipe prevents it.
- Turn the cookbook into a page of this course, so it's in the dashboard for
  everyone.

## 8. Demo

Show one recipe live: the naive prompt, the recipe prompt, and the test
results side by side. Then hand the lab its playbook.
