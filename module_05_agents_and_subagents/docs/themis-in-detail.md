# Themis: the ENCORE auditor

What Themis checks and what it leaves alone, beyond what the chapter
says. How to start it is at the top of this step; the agent file
itself is the last part of this page.

## 1. What does Themis do?

### What it is

Themis is a Claude Code subagent: a specialized, scoped AI helper with
fixed instructions, built specifically to audit a project's structure
and documentation against the ENCORE standard (ENhancing COmputational
REproducibility — see van Kampen et al., Nat Commun 2024). The chapter's
*What is a subagent?* explains the general idea, and its *Anatomy of an
agent file* shows how such a file is built.

### What it checks

Themis starts at the top. It checks that the six ENCORE folders are
there (`Data`, `Manuscript`, `Processing`, `ProjectDocumentation`,
`Sharing` and `.navigate`) and the key files in the root: `README.md`,
`0_PROJECT.md`, `2_CITATION.md` and `3_LICENSE.md`. But a file that exists
isn't the same as a file that says something, so it also skims what's
inside. A README with only a heading, leftover template text such as
`<fill in>`, `TODO` or `[Project name]`, or a `0_PROJECT.md` without a
project goal, an approach or any dated log entries all count as empty.

From there it walks down every subfolder of the five main folders, at
every level, and checks that each one explains what it contains. Along
the way it compares the documentation with reality: when a README says
"see folder X" and folder X was renamed, moved or never made, Themis flags
it. Those findings matter most, because they catch documentation that is
actually wrong, not just thin.

Finally it looks for the problems ENCORE's own creators kept finding when
they evaluated their projects. The most common is a hardcoded absolute
path, such as `C:/Users/...`, `/home/...` or `setwd(...)`, which breaks the
moment a project moves or is shared; Themis searches scripts, notebooks,
pipeline files and documentation for them and reports the file and line,
so you can replace them with relative paths (`pathlib` in Python,
`here::here()` in R). It also notices vague instructions for setting up
the software environment, a project that explains how to run things but
not what the goal or method is, and project logs that stopped being
updated while the code kept changing.

### What it reports back

The report appears in your Claude Code chat, not as a separate file. It
opens with a checklist of the top-level structure (✅, ⚠️ or ❌), then
lists the broken references, the known problems and the subfolder sweep
grouped by folder. Anything it couldn't decide gets a ❓ instead of a
confident verdict. It ends with the two or three things most worth fixing
first and a one-line count of all findings. Every finding names a file,
and a line where that helps, so you can check it yourself.

### What it leaves alone

Themis never creates, edits, moves or deletes a file, never runs a git
command that changes the repository, and never touches GitHub. It doesn't
open or quote your data files either; it only looks at their names and the
documentation around them. It also leaves alone what ENCORE allows by
design, such as several format versions of `0_GETTINGSTARTED`, or a
missing step-by-step guide once a project is under way. And if you ask it
to fix something halfway through, it declines and explains that fixing is
a separate step you take yourself.

That isn't only a promise in its instructions. Themis gets three tools,
`Read`, `Grep` and `Glob`, and none of them can change a file, so it
couldn't edit your work even if it wanted to. Think of it as a second pair
of eyes doing an audit. Keep in mind that read-only is about your files,
not about privacy: when Themis runs on a cloud model, the documentation
and code it reads are sent to the provider (the chapter's *What does an
agent send to the cloud?*).

### Its limits

Themis knows ENCORE's top-level structure and the problems described in
the published paper well, but it has no complete list of every subfolder
a project might be expected to have inside `Processing`,
`ProjectDocumentation`, `Data` or `Sharing`, beyond what your own
documentation says. When something is ambiguous, it's built to say so
rather than guess with confidence. And it was built for the standard
ENCORE layout: if your project uses a variation, you can adjust
`themis.md`. Check the ENCORE documentation for what counts as a standard
variation first, or ask an AI to help you edit the file.
