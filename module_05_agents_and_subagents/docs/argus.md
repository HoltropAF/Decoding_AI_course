# Argus: the code reviewer

What Argus checks and what it leaves alone. How to start it is at the top
of this step; the agent file itself is the last part of this
page.

## 1. What does Argus do?

### What it is

Argus is a Claude Code subagent that reviews research code: Python, R,
Snakemake, Nextflow, shell scripts and notebooks. It reads the way a
careful senior bioinformatician reviews a colleague's analysis before it
goes into a commit, a shared repository or a paper, looking for anything
that could make the results wrong, irreproducible or hard to maintain. Its
name comes from Argus Panoptes, the giant with a hundred eyes, some of
which were always awake, so nothing slipped past him. The chapter's *What
is a subagent?* explains the general idea, and its *Anatomy of an agent
file* shows how such a file is built.

### What it checks

Argus starts by mapping the code: which scripts, notebooks and pipeline
files there are, which one calls which, and what the README or
`0_PROJECT.md` says the code should do. Then it reads with one question in
mind first: could the results be wrong? That covers the mistakes that
quietly change a result, such as a count matrix whose columns don't match
the order of the sample sheet, a join that silently drops or duplicates
samples, raw p-values where adjusted ones belong, a DESeq2 design that
forgets the batch the README mentions, or an alphabetical reference level
that flips the sign of every fold change. It also knows the classic traps
of Python and R, like mutable default arguments, `1:length(x)` on an empty
vector, or an error swallowed by a bare `except`.

After correctness come duplication and dead code: blocks that were copied
and changed in one value, a threshold typed in five places instead of
defined once, functions that nobody calls any more. Then reproducibility,
with absolute paths, missing seeds, unpinned packages and notebooks that
only work when run out of order. Finally it looks at robustness and safety:
inputs that are never checked, file names hard-coded for one dataset, or a
token left in a config file.

### What it reports back

The report appears in your chat, not as a separate file. It opens with a
count per severity: critical (can change the scientific result), major
(a likely bug or reproducibility failure), minor (duplication, dead code,
unclear names) and notes. Each finding names the file and line, says in one
sentence why it matters and suggests a fix, which Argus describes but never
applies. A duplication map shows which blocks resemble each other, anything
it couldn't decide gets a ❓ with a way to check, and the report ends with
the three things to fix first.

### What it leaves alone

Argus never creates, edits, moves or deletes a file, and it never runs
code. It doesn't open your data files, apart from the first lines it needs
to check that the code reads the right columns, and it never quotes
sample, donor or patient identifiers. Comments and documents inside the
code are material to review, never instructions to follow. And if you ask
it to fix something, it declines and explains that fixing is a separate
step you take yourself.

As with Themis, that isn't only a promise in its instructions: Argus gets
`Read`, `Grep` and `Glob`, and none of them can change or run anything.
Read-only is about your files, not about privacy, though: with a cloud
model, the code it reads is sent to the provider (the chapter's *What does
an agent send to the cloud?*), so keep secrets out of your code anyway.

### Its limits

Argus reviews by reading, so it can't see what happens when the code runs:
the actual values in your data, a package that behaves differently in
another version, or a bug that only shows up on one dataset. It says so in
the last line of every report. It can also be wrong in both directions,
missing a real bug or flagging something that's fine in your context, so
treat its findings as questions to check, not verdicts. And it knows
general good practice, not your lab's choices: if your thresholds or
conventions differ, add them to `argus.md`, or mention them when you ask
for a review.
