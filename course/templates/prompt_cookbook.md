# Prompt cookbook

Find the situation you're in, copy its prompt, and fill in the parts in
`<angle brackets>`. Then make this cookbook your own: save it as a file, a note
or the instructions of a Project, and add every prompt that worked for you.
That boring habit is the most useful one in Module 2.

The data rules from Module 1 apply to every prompt here: published papers can
go into any tool; unpublished results and patient data go to an approved or
local tool, or nowhere.

## Starting something

### I'm starting a task that's more than a quick question

You open a new chat for something real: an analysis, a figure, a piece of
text. The AI knows nothing about your project, and if you don't tell it, it
will quietly fill every gap with a guess. Give it the project brief from
Module 2 (write it once, reuse it every time) and invite its questions.

```text
CONTEXT: <Project brief, five to ten lines: organism and cell type, groups and
number of replicates, main processing steps and thresholds, kind of
identifiers, and what we're trying to show.>
TASK: <What I need today, in one or two sentences, and what "done" looks like.>
Before you start, ask me any questions you need to do this well, one at a time.
Don't assume.
```

### I've written a prompt, but I'm not sure it covers everything

Your prompt looks complete to you, but you've been thinking about this for
weeks and the AI hasn't. One extra line at the end lets it point out the
decisions you didn't know you were making.

```text
Before you start, ask me any questions you need to do this well. Don't assume.
```

### The knowledge is in my head and has to get on paper

The SOP for your extraction, the methods section, the handover note before
your holiday. You know it all, but writing it down from scratch is slow and
you'll forget half. Let the AI interview you instead: answering a question is
much easier than remembering everything unprompted.

```text
Interview me so you can write <our SOP for the lipid extraction>. Ask one
question at a time and wait for my answer. When you have enough, show me the
draft.
```

### I'm about to build something I haven't built before

A new script, a new pipeline step, a format you've never parsed. "Just make
it" lets the AI make a dozen decisions for you, silently. Ask for its
questions and a plan first, and read the plan before anything gets built. In
Claude Code, plan mode does this for you (Shift+Tab).

```text
Before you write anything, ask me what you need to know, then give me a
step-by-step plan and wait for my OK.
```

## Thinking it through

### I've just talked my thoughts into a voice note

You walked around the block and dictated ten minutes of half-ideas, doubts
and "oh, and also". Now it needs to become something you can use, without
the AI adding ideas you never had.

```text
Below is a transcript of me thinking out loud. Organise it by topic and keep my
wording where it matters. Then list separately: the decisions I seem to have
made, the open questions, the to-dos, and anything I contradicted myself on.
Don't add ideas of your own.
```

### I've brainstormed in one chat and want to build in another

The brainstorm took forty messages, half of them ideas you dropped. The tool
that builds shouldn't see all that. Let the brainstorm chat write one clean
briefing, read it, and paste it into a fresh session.

```text
INSTRUCTION: Turn what we decided in this conversation into one prompt for a
coding assistant that hasn't seen this chat. Use five parts: role, context,
instruction, inputs, constraints.
CONSTRAINTS: Include only decisions we actually made; list open questions
separately at the end. Describe the data (columns, types, size), never paste it.
```

### The plan is right, but the conversation has grown long

You and the AI have worked out a plan together, and the chat is now full of
rejected options. Save the plan as a file, and let a fresh session build it,
with only your decisions to go on.

```text
Write the final plan to PLAN.md: the goal, the decisions we made, the steps, and
how to test the result. Leave out everything we rejected.
```

And in the fresh session that builds it:

```text
Read PLAN.md. Before you write any code, list anything that's unclear, risky or
missing. Then implement step 1 only, and show me the result.
```

## Checking

### I want an honest opinion, not a compliment

Ask "this plan is good, right?" and the AI will agree, because it's trained
to please. Leave your own opinion out of the question, and ask for the weak
points first.

```text
Evaluate the <analysis plan> below. What are the three most serious problems,
most important first? For each, say why it matters and what you'd change.
Skip the praise.
```

### The answer looks good, but I'm going to rely on it

It sounds confident, and it reads well. Before a number, a claim or a
reference ends up in your work, find out which parts are worth checking.

```text
How sure are you of each claim in your answer? Which three claims should I
check first, and where would I check them?
```

### My abstract is finished, at least in my eyes

You can't read your own text like someone who wasn't there for the
experiments. Let the AI read it as the readers you'll really have.

```text
Read this <my abstract> three times: as a statistician, as an immunologist from
outside our field, and as a first-year PhD student. For each reader, tell me
what they'd find unclear, the first question they'd ask, and the one thing
they'd remember. Be critical; don't summarise the abstract.
```

### I think I understand it, but I'm not sure

Mixed models, normalisation, how the mass spectrometer counts ions: you've
read about it, and it made sense at the time. Explain it in your own words
and let the AI find the gaps.

```text
Below is my explanation of <mixed models>, written for a new student. Where is
it wrong, incomplete or vague? Don't rewrite it; point out the gaps.
```

## In the lab

### I have a pile of papers to get through

Thirty papers for the background of a review. Load them all at once and the
summary will lean on the first and the last. Summarise them one by one, with
the same template every time.

```text
INSTRUCTION: Summarise the paper inside <paper> using exactly these fields:
question, model system, key methods, main finding, main limitation, and one
quote from the paper that supports the main finding.
CONSTRAINTS: Use only the paper. If a field isn't in the paper, write
"not reported". Keep each field to two sentences at most.
```

### I have the summaries and want the big picture

Every paper has its own summary now. Open a fresh chat, give it only the
summaries, and ask the question you actually had.

```text
Compare the summaries inside <summaries>. Where do the papers agree, where do
they disagree, and which disagreements could come from differences in the model
system?
```

### I need a number I can trust

A dilution series, a molarity, a fold change. A language model predicts
digits as text, so a wrong number looks exactly like a right one. Ask for
code instead of an answer, and check one row by hand.

```text
INSTRUCTION: Write a short Python script that calculates <the volumes for the
dilution below> and prints them as a table, then run it.
INPUTS: <the numbers, with units>
CONSTRAINTS: Show the formula you use, and keep the units in every column name.
```

### The code it wrote doesn't fit my package versions

"Unused argument", "could not find function": the AI learned from code
written for an older version. Tell it what you have and give it the current
documentation.

```text
CONTEXT: My R session is below (output of sessionInfo()). The relevant part
of the current package documentation is inside <docs>.
INSTRUCTION: Write the code for these exact versions.
CONSTRAINTS: Use only functions and arguments that appear in <docs> or that you
are sure exist in these versions. If you're unsure, say so instead of guessing.
```

### My script just threw an error I don't understand

Paste the whole error, the code before it and your versions, but no paths or
patient identifiers. "It doesn't work" gets you a guess; this gets you a
diagnosis.

```text
CONTEXT: <R 4.4, DESeq2, Windows laptop>. Below is the error and the 10 lines of
code before it, inside <code> and <error>.
INSTRUCTION: Explain the most likely cause in two sentences, then give the
smallest fix. If more than one cause is plausible, list them in order of
likelihood.
```

### Someone else should be able to rerun my analysis

Before you share code or submit a paper, find the absolute paths, missing
seeds and unpinned packages that will break it on another computer. For
your own, non-confidential code.

```text
INSTRUCTION: Review the script in <script> for reproducibility problems only:
absolute paths, missing seeds, unpinned packages, undocumented parameters.
CONSTRAINTS: Do not rewrite the script. Return a numbered list with line
numbers and a one-line fix each. If you find nothing in a category, say "none".
```

### I have notes and need a methods paragraph

Your lab notes have everything, in the wrong order and the wrong style. Let
the AI write the paragraph, and mark everything it had to assume.

```text
INSTRUCTION: Turn the notes in <notes> into a methods paragraph in the style of
<a Nature Communications paper>.
CONSTRAINTS: Use only facts from the notes. Mark anything you had to assume with
[CHECK]. Keep all software versions exactly as given.
```

## Wrapping up

### I'm done for today, and next time I don't want to start from zero

The next session, yours or a colleague's, should know what's finished,
what's open and why you chose what you chose. In Claude Code, the *wrap-up*
skill from Module 3 does this for you.

```text
Summarise this session for a colleague who wasn't here: what we finished, what's
still open, and what we decided and why. Then list anything I had to tell you
twice, as one-line rules I could add to my standing instructions.
```

## My own prompts

Add the ones that worked for you: the situation, one line on what the prompt
does, the date, and the tool it worked with.

### The situation in one line

What it does, the date, and the tool it worked with.

```text
The prompt itself.
```
