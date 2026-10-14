# How a chapter is built

Every module is written as a chapter of a small textbook, but one written by a
colleague, not by a committee. This page is the recipe. Use it when you edit a
chapter or write a new one, and give it to an AI assistant if you ask one to
help ("follow `course/chapter_recipe.md`").

---

## The order of a module

Each module in the dashboard follows the same route:

| Step | What it is | Where it lives |
|------|-----------|----------------|
| 1. **Chapter** | The story: background, ideas, examples. Read this first. | `module_XX/README.md` |
| 2. **Extra reading** *(only if needed)* | Templates and reference files. Information everyone needs belongs in the chapter itself, not here | `module_XX/docs/`, `templates/`, … |
| 3. **Exercise** | Hands-on work, always on public or synthetic data | The `## Exercise` section of the README, plus `exercises/` |
| 4. **Self-check** | Questions with hidden answers, a mini-experiment, critical questions | `module_XX/self_check.md` |
| *(Slides, optional)* | The same ideas in slide form. Not a step in the bar: linked from "Looking ahead" | `module_XX/slides.md` |
| 5. **Wrap-up** | The done-when checklist, your saved notes, and new notes | Saved in your browser |

Module 1's chapter opens with the plain-language foundations (what AI is, how
an LLM is made, why it makes things up) for anyone who's new to all of it.
The basics each later module needs are explained right where it needs them.

The dashboard takes the `## Exercise…` section out of the chapter and shows it
in the Exercise step, so reading and doing stay separate. On GitHub you still
see the whole README.

---

## The shape of a chapter

1. **Title**: `# Module N · Title`.
2. **Opening**: one to three paragraphs of story. A situation from lab life
   that this chapter is about. No bullet points yet.
3. **"In this chapter" box**: a blockquote starting with `**In this chapter**`:
   what you'll learn (3–5 points), how long it takes, and what you need.
4. **Parts and subsections.** A few main parts (`## 1. What is AI?`,
   `## 2. How does it work?`, …) are the toggles in the dashboard and the
   entries in the sidebar. Inside each part, subsections (`### …`) carry
   question-style titles that read as a flowing list. Each part:
   - starts with a sentence or two explaining *why* it matters, and picks up
     the question the previous part left open, so the chapter reads as one
     story with a running example;
   - is written as running prose: no paragraphs that open with a bold label,
     and as few bullet lists as possible;
   - contains at least one example from our own work (RNA-seq, lipidomics,
     dendritic cells, ENCORE projects), and introduces any example (such as
     AlphaFold) before relying on it;
   - includes a short piece of history where it helps: where an idea or
     word came from, and how we got here;
   - has one or two **Pause and think** questions with a hidden answer;
   - ends with one **In short** box of three or four bullets, for the whole
     part rather than for every subsection.
5. **Summary and what's next**: the last numbered part
   (`## N. Summary and what's next`), with two subsections. `### Chapter
   summary` retells the chapter in story form in a few paragraphs, then gives
   the key points as a list. `### Looking ahead` is one paragraph on how the
   next module builds on this one, and a link to the slides: "Prefer a quick
   recap first? There are [slides for this module](slides.md)."
6. **Exercise**: `## Exercise: …`, at the very end, like the exercises at the
   end of a textbook chapter.

Aim for 3,000–6,000 words per chapter. That's 20–40 minutes of reading.
Long is fine, as long as it reads like a story and not like a list of facts.

---

## The boxes, and how to write them

The dashboard gives each kind of box its own colour. Start the blockquote with
the bold label shown here and it is styled automatically.

| Box | How to write it | Use it for |
|-----|-----------------|-----------|
| In this chapter | `> **In this chapter**` | The opening overview |
| Concept | `> **So what is a …?**` | Explaining a term that the text needs |
| Tip | `> **Tip:** …` | A practical trick |
| Coffee note | `> **Coffee note:** …` | A light aside, an anecdote, a bit of honesty |
| It's okay | `> **It's okay:** …` | Reassurance: "it's okay if this feels like a lot" |
| Watch out | `> **Watch out:** …` | A common mistake or a risk |
| In practice | `> **In practice: <title>.** …` | A use case: a real situation, what to do, and what to check before you accept the result |
| In short | `> **In short**` followed by bullets | The end of each section |
| AI-researched | `> **AI-researched · current information (checked <date>)**` | Facts that change quickly and were found by an AI search |

### Pause and think

A question for the reader, with the answer hidden until they click. Write it
in HTML so it can be folded. Keep the blank lines: they let you use Markdown
inside.

```html
<details class="think"><summary>Pause and think: why would a model invent a gene that isn't in your list?</summary>

Because it predicts what a plausible answer looks like, and plausible pathway
lists usually contain more genes than yours...

</details>
```

The read-aloud button reads the question and then says the answer is on screen;
it reads the answer only if you've opened it.

---

## Figures and their colours

Every figure uses the same colours for the same roles, so readers learn
them once. The dashboard turns each colour into its dark-mode partner
automatically, so only use these:

| Role | Fill | Outline |
|------|------|---------|
| The model | `#0f5b6b` (white text) | none |
| The app, the system, neutral steps | `#d5e7ea` or `#e2ecea` | `#8fb2b9` / `#9fb3b8` |
| You, and the thing to notice | `#f6e4d2` | `#d9a576` or `#b8641d` |
| Files, rules and instructions | `#cfe3d6` | `#8bb89a` |
| Data and tool output | `#efe9f4` | `#b9a7cc` |
| Warning or the full-window box | `#fff6ea` | `#d9a576` |
| Plain items | `#ffffff` | `#9fb3b8` |

Text is `#1d2b36`, secondary text `#55676d`, headings and arrows `#0f5b6b`.
Escape `<` and `&` in labels (`&lt;`, `&amp;`), or the figure won't load.

## Tone

- Write as a colleague explaining something over coffee: "we", "you", "our lab".
- Explain first, then list. A table without a paragraph in front of it reads
  like a spec sheet.
- One idea per paragraph. Short sentences are fine; so is the odd joke.
- Be honest about uncertainty: "the evidence is mixed", "we don't know yet".
- Cite papers with a link when a claim matters ([Author et al. year](link)),
  and add them to `course/references.md`.
- Check facts that change quickly (prices, model names, policies) and mark
  them with the AI-researched box and a date.
- No real data, secrets or internal hostnames in examples.

---

## After editing

Run `course/update_dashboard.bat` (or `python course/build_dashboard.py`) and
reload the dashboard.
