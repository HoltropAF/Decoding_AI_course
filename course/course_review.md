# Course Review: Problems, Risks and Open Questions

> **AI-researched · current information (checked 8 October 2026)**
> This review was carried out with the help of an AI assistant (Claude),
> which also wrote much of the course. That is a limitation in itself: an
> author reviewing its own work misses things. Treat this page as a
> starting point for a human review, not as a replacement for one.

A course that teaches people to look critically at AI output should be able
to stand the same scrutiny itself. This page records what a critical pass
over the whole course found: factual errors, contradictions between
modules, risks in what we ask people to do, and technical problems. Most of
them have been fixed; some need a decision from the people running the
course.

---

## 1. How the review was done

Every module was read with five questions in mind: is it **true**, is it
**consistent** with the other modules, could following it cause **harm**
(especially to unpublished or patient data), does the **technology**
actually work as described, and what is **missing**. Claims that could be
checked were checked: scripts were run against a local model, paper
references were verified against Crossref and arXiv, and current events
against the original sources plus independent coverage.

---

## 2. Fixed during the review

**A factual error about memory.** AI basics said a model needs "a few GB
of memory per billion parameters". That would put an 8B model at 16–24 GB,
which contradicted the 4.9 GB model everyone downloads in Module 1. The
correct rule (about 2 GB per billion parameters at 16-bit precision, about
a third of that when compressed) is now in the text, and a mislabelled
"full precision" was corrected.

**A silent failure in local models.** Ollama gives models only a small
working memory by default (we measured 4,096 tokens on a standard laptop)
and drops whatever doesn't fit *without an error*. The Module 2 exercise
fitted, but longer gene lists, retries or the Track B literature search
could have been cut off unnoticed. The scripts now set a larger context
explicitly, the Module 1 guide explains the catch, and Track B has a
warning.

**A validation gap that our own test run exposed.** When we ran the Module
2 script, the model put up-regulated ceramide genes in a "down-regulated"
pathway and listed one gene twice, and the script accepted it. That
undermined the lesson of the module. The script now also checks whether a
pathway's direction matches its genes' fold changes, and whether a gene is
listed both as assigned and unassigned.

**The dashboard talked to other websites.** It loaded its fonts from Google
and its Markdown library from a content-delivery network. That meant every
time someone opened the course, their IP address went to two companies, the
course didn't work properly offline, and an outside script ran inside the
page that also holds people's notes. For a course about keeping data under
control, that was a contradiction (and Google Fonts specifically has been
the subject of a German court ruling under the GDPR). Everything is now
inside the file: it works offline and contacts no one.

**Exercises that contradicted the data rules.** Module 1 says unpublished
documents go to cloud tools only under an approved contract. Modules 3, 4
and 5 then asked people to run Claude Code, a cloud agent, on "a copy of
your own project". A copy still contains the unpublished README, project
log and analysis descriptions, and an agent sends every file it reads to
the provider. The exercises now use the ENCORE template or a project with
only public data, and explain why.

**Notes stored in the browser.** The dashboard's notes and experiment logs
live in browser storage, which is not a safe place for confidential
material. There is now a clear warning, including inside the notes field.

**A Windows trap in the MCP example.** The sample configuration uses
`${PWD}` for the project folder, which usually doesn't exist on Windows;
the file now says so.

---

## 3. Still open: decisions for the course organisers

These can't be solved by editing text; they need someone with the
authority or knowledge to decide. Roughly in order of importance:

1. **Check the data rules with the institution.** The four data classes and
   what each may be used with are sensible defaults, but they are *our*
   reading, not Amsterdam UMC policy. Before the course is used, a data
   steward or the data protection officer should confirm them, and the
   course should name the AI tools and account types the institution has
   actually approved. Until then, the rules are advice, not policy.
2. **Check what people may install.** The course asks participants to
   install Ollama, VS Code, Python packages, and optionally Docker and
   Claude Code. On managed work laptops that may need IT approval. Better
   to sort that out once, centrally, than to have each participant run
   into it.
3. **Decide who pays for what.** Modules 3 to 5 lean on Claude Code, which
   needs a paid subscription or API credit. Who provides that, and is there
   a fallback for people without it? (Local models can do parts, but not
   all, of these exercises.)
4. **Make "reviewed by the course organisers" true before sharing.** The
   start page and the About page say the course was reviewed by its
   organisers. That should be the case before colleagues read it. Likewise,
   the "Why I made it" text on the About page was drafted by the AI in the
   author's voice; it should be read and owned, or rewritten.
5. **Have the content checked by people who know it.** The technical
   explanations, the biology examples (for instance what LPS does to
   dendritic cells) and the summaries on the References page were written with
   AI help and checked against sources, but not yet by a domain expert. A
   bioinformatician and an immunologist reading their parts would catch
   what a model doesn't.
6. **Fill in the hackathon practicalities.** Dates, mentors, the schedule
   and the judging weights are placeholders.

---

## 4. Known limitations to keep in mind

**Parts of the course will age quickly.** Model names, prices, Ollama's
defaults, Claude Code commands and settings syntax, and especially the
watermarking and EU-regulation section describe the situation in October
2026. Plan a short update round before each new group starts; the
AI-researched boxes show which parts are most time-sensitive.

**The course leans towards one vendor.** Modules 3 to 5 are built around
Claude Code, and the course itself was largely written with Claude. The
concepts transfer to other tools (and the guides say so), but participants
should know this, and the organisers may want to show at least one
alternative.

**The read-aloud voices.** Built-in system voices run on the computer
itself. The more natural "online" voices in Microsoft Edge send the text to
Microsoft to be spoken. That's harmless for the course material, but people
should not use those voices to read their own unpublished documents.

**Small experiments, wide uncertainty.** The mini-experiments use small
samples (5–10 runs) on purpose, so they fit in a session. Their results
show the *kind* of error a tool makes, not a precise error rate; the
self-checks say so, and pooling results across a group helps.

**Automatic checks have limits.** Even with the extra checks, the Module 2
script cannot tell whether a gene really belongs to a pathway. That
remains the human step ("layer 4"), and the course should keep saying so.

**"Nothing is graded", but the hackathon has judging.** The judging is
meant as feedback, and the hackathon guide says so, but it's worth being
explicit about this when introducing the hackathon.

**The background notes are unverified.** The `reference/` folder holds the
original planning notes, including links to social media posts that were
never checked. Nothing in the course depends on them; consider removing
them before sharing.
