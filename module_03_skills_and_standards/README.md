# Module 3 · Skills & Standards

Every lab has that one person who knows how everything is done. Where the
raw data goes, which R packages we pin, why we never use `setwd()`, which
DESeq2 thresholds we agreed on two years ago and why. Ask them anything and
you get a patient, complete answer. The problem is that you have to ask
them, every time, and so does everyone else.

Working with AI tools without shared instructions is like that, but worse.
In Module 2 you learned to write a good briefing. Next week you'll start a
new chat, and the model will have forgotten all of it. So you'll type a
shorter, sloppier version from memory. Your colleague will type a different
one. The model will happily write `setwd("C:/Users/...")` into one person's
script and use `here::here()` in another's, and nobody will notice until a
reviewer tries to rerun the analysis.
This chapter is about writing it down once. We'll look at the files that AI
tools load automatically at the start of every session, how to write rules
that a model actually follows, how to package recurring workflows as
"skills", and how to keep all of it versioned and shared, the way we keep
our SOPs.

> **In this chapter**
> - **Why write instructions down?** Why knowledge in chat windows evaporates, and where the idea of the SOP came from
> - **How do I write instructions once?** The layers (system prompt, `CLAUDE.md`, skills, subagents, hooks), and how to write rules a model follows and a colleague can check
> - **How do we share them safely?** Versioned lab standards, and what must never go into an instruction file
> - **Time:** about 30 minutes of reading, plus about 75 minutes for the exercise and self-check
> - **You need:** Modules 1 and 2; Claude Code (or a similar agent) for the exercise, or just a chat app for the no-code version

> **Good to know:** you don't need to program to get a lot out of this
> chapter. The chat apps have the same idea built in: ChatGPT's *custom
> instructions* and *Projects*, Claude's *Projects* with project
> instructions, and Gemini's *Gems* all let you write your standing
> instructions once, so you don't have to repeat them in every chat.
> Most of this chapter applies to all of them; the parts about files and
> folders are mostly for people who use coding tools.

---

## 1. Why write instructions down?

### Why does chat knowledge evaporate?

Let's start with why this is a problem at all, because it isn't obvious
until it bites.
Every new AI session starts with an empty context window (Module 2). The
model knows nothing about our folder layout, our preference for `renv`, our
DESeq2 thresholds, or that `Data/raw/` is read-only. Whatever good habits
you taught it yesterday lived only in yesterday's conversation. That has
three consequences. Your results depend on what you happened to remember to
say that day. Two people in the same lab get differently styled code for the
same task. And every lesson ("it keeps forgetting to set a seed!") has to be
learned again by everyone, individually.

**Persistent instructions** fix this. They are plain text files that the AI
tool loads automatically at the start of every session, stored in git next
to the code, exactly like any other project file.
If that sounds abstract, think of the lab's SOP folder. Nobody re-explains
to every newcomer how to label tubes or where the raw data goes; it's
written down once, kept up to date, and everyone refers to it. Persistent
instructions are the SOP folder for our AI tools. The difference with a
human SOP is that the AI reads it every single time, without skipping the
boring parts, which makes a well-written file remarkably effective and a
badly written one remarkably annoying.

The SOP itself has a history worth knowing, because it was born from the
same problem. In the 1970s, investigators at the US Food and Drug
Administration found that some laboratories testing the safety of drugs and
chemicals could not show how their results had been produced; at one large
contract lab, [Industrial Bio-Test Laboratories](https://en.wikipedia.org/wiki/Industrial_Bio-Test_Laboratories), studies turned out to be
badly run or even invented. The answer, in 1978, was a set of rules called
[Good Laboratory Practice](https://en.wikipedia.org/wiki/Good_laboratory_practice), and at its heart was a simple demand: write down
how the work is done, follow what is written, and keep records so someone
else can check. Persistent instructions for AI are the newest member of
that family. The idea is old; only the reader is new.

<details class="think"><summary>Pause and think: what are three things you've had to tell an AI tool more than once?</summary>

There's no single right answer, but common ones in our kind of work are:
"use relative paths", "write R, not Python" (or the other way round), "don't
touch anything in Data/raw", "set a random seed", "use our DESeq2
thresholds", "explain what the code does in a comment", "don't install
packages without asking". Each of those is a candidate first rule for your
instruction file. Keep your three; you'll use them in the exercise.

</details>

> **In short**
> - Each AI session starts from zero, so instructions given in chat are lost.
> - Persistent instructions are text files the tool loads automatically, kept in git: the lab's SOP folder, read by the AI every single time.

---

## 2. How do I write instructions once?

### Where can instructions live?

There are several places where you can store instructions for an AI tool.
They overlap a little, which can be confusing at first, so here is an
overview of what each one is for. You don't need all of them on day one;
most of us will mainly use the second one.

| Layer | What it is | Loaded when | Scope | Example |
|-------|-----------|-------------|-------|---------|
| **System prompt** | Fixed instructions set by the application/API call | Every request | One app or script | The `role` in Module 2's template |
| **`CLAUDE.md`** (or `AGENTS.md`, `.cursorrules`, `GEMINI.md`, …) | Project memory file read automatically by coding agents | Start of every session in that folder | Whole project / user / organisation | "Use `pathlib`, never hardcode absolute paths" |
| **Skill** | A packaged, named workflow (instructions + optional scripts/templates) loaded on demand | When the task matches the skill's description | One recurring task | `deg-report`: produce the lab's standard DE report |
| **Subagent** | A separate AI instance with fixed instructions and restricted tools | When delegated a task | One scoped job | Themis, the ENCORE auditor (Module 5) |
| **Hook** | A deterministic command the tool runs on an event | Always, on that event | Enforcement | Run `ruff` after every Python edit |

<!-- speak: A table of five layers of instructions. A system prompt is set by an application for every request. A CLAUDE.md file is read at the start of every session in a project folder. A skill is a packaged workflow loaded when the task matches. A subagent is a separate AI with fixed instructions and limited tools. A hook is a command that always runs on a certain event. -->

It helps to see where all of this ends up. Module 2 showed that the model
reads one long text, the context window, every turn. Before you've typed a
word, that window already holds several of these layers; your conversation
fills the rest.

![The context window in Claude Code from top to bottom: system prompt and tools, your personal CLAUDE.md, the project CLAUDE.md, lists of skills, MCP tools and memory notes, then the growing conversation, then free space; when it is full the conversation is summarised and the CLAUDE.md files are read in again. Chat apps have the same layers: system prompt, custom instructions, project instructions, saved memories and the chat](../figures/context_layers.svg)

*What fills the context window. The green layers come from files; for skills, only the description is loaded until the task needs the full text. The conversation grows until it is summarised.*

<!-- speak: The figure shows what fills the context window in Claude Code, from top to bottom. First the app's own system prompt and tool definitions. Then your personal CLAUDE.md file, the project's CLAUDE.md file, and short lists of skills, MCP tools and memory notes; these are loaded every session, before you type anything. For a skill, only its name and description are loaded at first; the full text follows when the task needs it. Below them the conversation grows: your messages, the answers, files the AI read and command output, which is often the biggest part. Then free space. When the window is full, the conversation is summarised and the CLAUDE.md files are read in again, so rules in files survive. In Claude, ChatGPT and Copilot the layers are the same: the app's system prompt, your custom instructions, project instructions, saved memories, and the chat with its uploads. -->

Look at the dashed green layers. For a skill, only its name and one-line
description sit in the window from the start, a few dozen tokens each. When
your request matches a description, the agent reads the full `SKILL.md`
into the conversation, and only then does it take up real space. That is
why the description matters so much (*Skills in Claude Code*, below): it's
all the model sees when it decides. MCP servers work the same way: their
list of tools is always there, and what a tool returns arrives only when
it's called.

Why does putting text in the window work at all? Remember from Module 2
that the model picks every next token based on everything in front of it.
A rule in `CLAUDE.md` isn't a command the model looks up and obeys; it's
context that makes rule-following continuations more likely, exactly like a
good briefing does. That cuts both ways: lines that don't matter for the
task pull the probabilities in directions you didn't ask for, and a crowded
window dilutes the lines that do matter, which is one more reason to keep
these files short. It's also why rules belong in a file rather than in the
chat. When the window fills up, the conversation is summarised and details
get lost, but the files are simply read in again.

The quickest way to choose is to ask how often the instruction applies and
how bad it would be if it were ignored. A rule that applies to almost every
task in the project goes into `CLAUDE.md`. A recurring workflow you need
now and then becomes a skill. A noisy, scoped job that should run in
isolation with limited permissions is a subagent. And anything that must
happen every single time, without exception, is a hook, because the model
can forget instructions and a hook cannot.
Module 5 puts all the building blocks of the course (scripts, `CLAUDE.md`,
skills, hooks, MCP servers, subagents and agents) side by side in one
decision guide, once you've met them all.

An example helps to see the layers working together. Say our rule is "never
write into `Data/raw/`". Writing it in `CLAUDE.md` means the model knows
about it and will usually respect it. Adding a permission rule that blocks
edits in that folder means the tool *cannot* break it, even on a day the
model forgets. A skill for "process a new lipidomics batch" can then
describe the whole workflow, including where the output *does* go. And a
subagent like Themis can check afterwards that the project still follows the
structure. Each layer covers a weakness of the others.

> **Watch out:** an instruction is a request, not a guarantee. Models follow
> well-written instructions most of the time, but "most of the time" isn't
> good enough for things like protecting raw data. For those, use a
> permission rule or a hook, which the software enforces regardless of what
> the model decides.

#### In the chat apps you already use

Most chat apps have a place for standing instructions. Look for *custom
instructions* or *personalisation* in the settings, or create a *Project*
(ChatGPT, Claude) or a *Gem* (Gemini) for one kind of work. Whatever you
write there is added to every conversation in that place, exactly like a
`CLAUDE.md`. A lab version could look like this:

```text
I'm a researcher in a lipidomics and immunology lab. I work in R (tidyverse)
and sometimes Python.
- Explain briefly, then give the code. Use relative paths, never setwd().
- When you mention a paper, give the DOI; if you're not sure it exists, say so.
- If you're unsure about a fact, say so instead of guessing.
- Never assume data I paste is public; remind me if something looks like
  patient or unpublished data.
```

Ten lines like these save you from repeating yourself in every chat, and
they nudge the model towards the habits from Modules 1 and 2.

#### CLAUDE.md in Claude Code

Claude Code reads `CLAUDE.md` files in layers, from general to specific:

- `~/.claude/CLAUDE.md`: your personal preferences, all projects
- `<project>/CLAUDE.md`: shared project rules, committed to git
- `<project>/CLAUDE.local.md`: personal project notes, git-ignored
- `<project>/<subfolder>/CLAUDE.md`: loaded when working in that subfolder

Other agents use equivalent files. `AGENTS.md` is a widely supported
cross-tool convention, and the content principles are identical: you can
copy one file to the other names.

#### Skills in Claude Code

> **It's okay:** if you don't use coding tools, you can skim the rest of
> this section. The idea to take away: a skill is a saved recipe that the
> AI pulls out only when the task calls for it. In chat apps, a Project or
> Gem for one recurring task does much the same.

A skill is a folder `.claude/skills/<skill-name>/` containing a `SKILL.md`
with a name and a description (used to decide when to activate it), the
instructions, and optionally scripts or templates. Think of it as a
protocol card in a drawer: the model only takes it out when the task calls
for it, so it doesn't cost context the rest of the time.

```markdown
---
name: deg-report
description: Generate the lab's standard differential expression report from a DESeq2 results table. Use when the user asks for a DE report, volcano plot or DEG summary.
---

# DEG report

1. Load the results table with `readr::read_csv`; require columns gene, log2FoldChange, padj.
2. Apply thresholds padj < 0.05 and |log2FC| > 1 unless the user specifies others.
3. Produce: volcano plot (ggplot2, labelled top 15), MA plot, summary table.
4. Write outputs to `Processing/<analysis>/output/` and record parameters in the analysis README.
```

Skills don't always activate reliably just because they exist. Name them
clearly, write a specific description that says *when* to use them, and
invoke them explicitly (`/deg-report`) when it matters. The *Examples* step of
this module has four complete skills to copy and adapt: omics analysis,
research review, clean commits and a prompt builder.

<details class="think"><summary>Pause and think: "always use our lab's colour palette for figures". CLAUDE.md, skill or hook?</summary>

Probably a skill, or a short line in CLAUDE.md pointing to one. It applies
only when making figures, not to every task, and it may need a file (the
palette definition) next to it. If it's one line ("use the palette in
R/theme_lab.R"), CLAUDE.md is fine. A hook would be overkill: nothing breaks
badly if one exploratory plot uses default colours.

</details>

### What makes a good rule?

Writing instructions for an AI turns out to be a lot like writing a protocol
for a new lab member: be specific, explain the why, and leave out what
everyone already knows. Everything you learned about prompts in Module 2
applies, with one twist: this text is sent along with *every* request, so
each line has to earn its place.
Keep `CLAUDE.md` short, ideally under 200 lines, because every line costs
context in every session. Write rules that are **specific and checkable**:
"use `here::here()` for paths in R" beats "write portable code". Include the
exact commands for running tests, linting and building the environment,
and state hard prohibitions explicitly: "never modify files in
`Data/raw/`". For any rule that isn't obvious, add the *why* in one clause;
models follow rules better when they understand them. And review the file
now and then, because stale rules are worse than none.

What to leave out is just as important. Don't paste entire style guides or
textbooks; link to them. Don't duplicate what the code or the linter
configuration already enforces. Don't write vague aspirations such as "be
careful" or "high quality". And never include secrets, tokens, internal
hostnames or real data values (more on that in *What must never go into an
instruction file?*).

Specificity matters so much because the model takes your words both very
literally and very generously. "Write clean code" leaves it to decide what
clean means, and it will decide differently every session. "Use `pathlib`
for paths, add a docstring stating units, and add a pytest test with a
synthetic fixture" leaves nothing to interpretation. A good test for any
rule: could a colleague check, in thirty seconds, whether it was followed?
If not, rewrite it until they could.

Here's what that looks like in practice, as a before and after:

| Vague | Specific and checkable |
|-------|------------------------|
| "Write reproducible code." | "Set a seed (`set.seed(42)` / `np.random.default_rng(42)`) at the top of every script that uses randomness." |
| "Be careful with data." | "Never write to `Data/`. Outputs go to `Processing/<analysis>/output/`." |
| "Document your work." | "Every new folder in `Processing/` gets a README with inputs, outputs and the command to run it." |
| "Use good statistics." | "Report padj (BH), not raw p-values. Thresholds: padj < 0.05, \|log2FC\| > 1 unless stated." |

<!-- speak: A table comparing vague rules with specific ones. Instead of "write reproducible code": set a seed at the top of every script that uses randomness. Instead of "be careful with data": never write to the Data folder, outputs go to the Processing output folder. Instead of "document your work": every new folder in Processing gets a README. Instead of "use good statistics": report adjusted p-values with the agreed thresholds. -->

> **Tip:** the template in `templates/CLAUDE.md` (shown in this module's
> Exercise step) is a ready-made starting point for Python and R
> bioinformatics projects. Copy it, delete what doesn't apply, and add your
> own three rules.

<details class="think"><summary>Pause and think: why would "explain the why in one clause" make a model follow a rule better?</summary>

Because the model predicts what a sensible continuation looks like, and a
reason gives it a way to apply the rule to cases you didn't list. "Never
write to Data/raw/" covers that folder. "Never write to Data/raw/, because
raw data must stay exactly as received from the instrument" also nudges it
away from overwriting a raw file you happened to copy elsewhere. It's the
same with people: a rule with a reason gets applied with judgment.

</details>

> **Tip:** treat `CLAUDE.md` as a living document. Whenever you have to
> correct the AI on the same thing twice, add one line. You can let the AI
> keep the books: end a session with "Add to CLAUDE.md anything I had to
> tell you twice in this session, one line each, and show me the change
> before you save it." Prune the file every month or so, and check that a
> new rule actually changes what the AI does. And a rule that must hold
> every single time doesn't belong in the file at all: make it a check that
> runs automatically, such as a hook, a test or a pre-commit check.

> **In short**
> - Five layers: system prompt, `CLAUDE.md`, skills, subagents and hooks. `CLAUDE.md` for project rules, skills for recurring workflows, hooks and permissions for anything that must never fail.
> - Instructions are requests; enforcement needs permissions or hooks.
> - Good rules are short, specific, checkable and explained in one clause: could a colleague check in thirty seconds whether a rule was followed?

---

## 3. How do we share them safely?

### How do we share standards as a lab?

So far we've talked about one person's file in one project. The real gain
comes when a lab shares its standards. A lab-wide standard is just a set of
persistent instructions that everyone agrees on and that lives in one place.
Here's a workflow we propose for our lab. There is one source of truth: a
`lab-standards` repository in **Git** (or this course repository) holds the
master `CLAUDE.md` and the shared skills and subagents. Each ENCORE project
copies `templates/CLAUDE.md` into its root and adds a short project-specific
section. Any change to a shared rule is proposed as a **pull request**, a
proposed change that colleagues can read and approve, with a one-line
reason and at least one other lab member as reviewer, much like checking a
protocol change before it goes into the SOP folder. The master file carries
a version line, so projects can note which version they started from. And
once a quarter, someone prunes the rules nobody needs and promotes the rules
people keep adding by hand.

Prompts and skills deserve the same care. Treat them like code: give them a
version number (`1.2.0`), keep a short changelog, and test them against the
small test set from Module 2. Store prompt templates next to the scripts
that use them, and for results that end up in a paper, record the template
version and the model version in the analysis log.

This may sound like a lot of process for a handful of text files, but the
benefit shows up quickly. When someone discovers that the model keeps
writing `setwd()` into R scripts, they add one line to the shared file, open
a short pull request, and from that moment everyone's sessions improve.
Without a shared file, that lesson stays in one person's head. Versioning
also protects our results: if a figure in a paper was made with help from a
prompt template, we can point to exactly which version of that template it
was.

> **Coffee note:** nobody enjoys process for its own sake. If the
> pull-request step feels heavy for a one-line change, agree that one
> reviewer and a two-word reason ("keeps forgetting seeds") is enough. The
> point is that someone else saw it, not that it was a ceremony.

<details class="think"><summary>Pause and think: two lab members want opposite rules ("always use tidyverse" vs "base R only"). Where should that disagreement be settled?</summary>

In the pull request, before the rule goes into the shared file, the same way
we'd settle a disagreement about an SOP. One option is to keep the shared
file neutral on style and let each project's own section decide. What
shouldn't happen is both rules quietly ending up in different copies, so
that the model gets contradictory instructions depending on whose template
a project started from.

</details>

### What must never go into an instruction file?

Instruction files feel harmless: they're just text. But they're sent along
with every request, and they often end up in shared or public repositories.
A few things should never be in them. No credentials, in `CLAUDE.md`,
skills, system prompts or templates: refer to the *name* of an environment
variable (`$NCBI_API_KEY`), never its value. No private endpoints or
hostnames of internal systems in files that might be shared publicly. And
no real data in examples; use synthetic values. Remember that `CLAUDE.md`
is sent to the model provider in every session, so it falls under the same
data rules as any prompt (Module 1).
Skills from other people need a different kind of care. A skill is
instructions, and possibly scripts, that the agent will follow with your
permissions, so installing one is closer to running someone's script than
to reading their notes. Read it before you install it.

<details class="think"><summary>Pause and think: a colleague shares a skill from a website that "automatically writes your methods section". What would you check before installing it?</summary>

Read the SKILL.md and any scripts in the folder. Does it run commands, and
which? Does it send anything anywhere (web requests, uploads)? Does it ask
the agent to read files outside the project, or to change settings? Does the
description make it activate on tasks it has no business with? If it
contains scripts you can't follow, don't install it, or ask someone who can
read them. Same rule as for any code from the internet.

</details>

> **In short**
> - One shared, versioned source of truth; changes go through a short review, like an SOP change.
> - Record which prompt or template version produced a published result.
> - No secrets, hostnames or real data in instruction files; read other people's skills before you install them.

---

## 4. Summary and what's next

### Chapter summary

We started with the lab's walking encyclopedia and the uncomfortable fact
that AI tools forget everything between sessions. Without shared
instructions, the quality of our AI-assisted work depends on who typed what,
on which day, from memory. Persistent instructions solve that by writing our
conventions down once, in files the tools load automatically.

There are several layers, each for a different job. `CLAUDE.md` (or
`AGENTS.md`) holds the project-wide rules. Skills package recurring
workflows and load only when needed. Subagents run scoped jobs with their
own instructions and tools, which is where Module 5 picks up. And hooks and
permission rules enforce what must never fail, because an instruction is
only ever a request.

Writing good instructions is a lot like writing a good protocol: short,
specific, checkable, with a reason for anything that isn't obvious. When a
lab shares these files, versions them and reviews changes the way it reviews
SOPs, every lesson learned by one person improves everyone's sessions. And
because these files are sent with every request and often shared, they must
never contain secrets or real data, and other people's skills deserve the
same scrutiny as other people's code.

**Key points**

- AI sessions start from zero; persistent instruction files make your conventions stick.
- `CLAUDE.md` for project rules, skills for workflows, subagents for scoped jobs, hooks and permissions for enforcement.
- Good rules are short, specific, checkable and explained in one clause.
- Share one versioned set of standards for the lab and review changes.
- No secrets, internal hostnames or real data in instruction files; read skills before installing them.

### Looking ahead

So far the model has only worked with what we put in front of it: a prompt,
a set of rules. In Module 4 we let it fetch information itself, from files,
databases and websites, through the Model Context Protocol. That raises a
new question that will follow us for the rest of the course: how do you let
an AI *look* at your data without letting it *touch* it? Prefer a quick recap first? There are [slides for this module](slides.md).

---

## Exercise: build your project's CLAUDE.md

Now make one for your own work. Don't aim for perfect: a short file with a
handful of rules you actually care about is the goal.

1. Copy `templates/CLAUDE.md` into a scratch copy of the **ENCORE template
   project**, or a project that contains only public or synthetic data. Not
   into a real project (yet): a copy of a real project still contains its
   unpublished documentation, and a cloud agent sends every file it reads to
   the provider. Once you've set up the deny rules from Module 5 (part 3) and
   checked what your account type allows, you can use it on your own work.
2. Fill in the **Project-specific** section: organism, data types, key
   analyses, environment manager, test command.
3. Delete any rules that do not apply. Add at most three rules from your own
   experience (the three from the first Pause-and-think question).
4. Start a fresh Claude Code session in that project and ask:
   *"Summarise the rules you will follow in this project."* Check that it
   picked up your file.
5. Ask it to write a small function (for example, normalise a lipidomics
   matrix to total ion count) and check whether it followed the path,
   testing and documentation rules.
6. **Stretch:** turn one recurring task into a skill in
   `.claude/skills/<name>/SKILL.md` and invoke it.

### No-code version

1. In your chat app, open the custom instructions (or create a Project or
   Gem) and write five to ten standing instructions for your own work, like
   the example in *Where can instructions live?*.
2. Start a new chat and ask: *"What instructions will you follow?"* Check it
   picked them up.
3. Ask for something your rules should affect (an R plotting script, a
   summary with references) and check whether it followed them.
4. Share your best two rules with a colleague. Did they work for them too?


**Done when** a fresh session demonstrably follows at least three rules
from your file without being reminded.

---

**Previous:** [Module 2](../module_02_prompting_and_context/README.md) ·
**Next:** [Module 4 – MCP & Data](../module_04_mcp_and_data/README.md)
