# About this course

Everything about the course itself is on this one page: what it is and who
made it, how to find your way through it, and where its limits are. Read
part 2 before you start; the rest can wait until you're curious.

## 1. What is this course?

### What it's for

**Decoding AI**, *the AI whisperer's guide to intelligence*, is a
free, self-paced course about using AI tools well in a lab that works on
lipidomics, metabolomics, RNA-seq and systems immunology. The goal is not
to build AI, but to use it well. It starts at zero (what is AI, what is a
token?), works through prompting and making the tools work for you, and ends
with a hackathon where we combine it all in real research projects. It is
meant to be done together, as colleagues and friends: no exams, no grades,
no stupid questions.

By the end, you should be able to:

1. **Explain how AI works**, roughly: what a language model does when you
   press Enter, and why that makes it good at some things and bad at others
   (Module 1, parts 1 and 2).
2. **Join the current conversations**: privacy, watermarks and the EU rules,
   bias, copyright, energy use, authorship and what journals expect
   (Module 1).
3. **Know the limitations**: when AI invents things, agrees with you too
   easily, or is simply out of date, and how to check (Modules 1 and 2).
4. **Use it in your daily work**: which tool for which job, and what data
   may go where (Module 1), plus how to make tools follow your rules, look
   things up and do small jobs for you (Modules 3 to 5).
5. **Prompt well**: get what you want out of AI, reliably (Module 2).

You don't need to be able to program. Where a module goes technical, it says
so, and every exercise has a version you can do in a normal chat app.

### Why I made it

AI tools showed up in our lab the way they show up everywhere: one person
at a time, each with their own tricks, and with very different ideas about
what is safe to paste into a chat window. Some of us got real value out of
them; others tried once, got a confidently wrong answer, and gave up.

Working with lipidomics and metabolomics data every day, I see both sides:
these tools can save hours on code, pipelines and documentation, and they
can just as easily invent a pathway, a lipid ID or a reference. I wanted us
to learn this together and properly: understand what these models actually
do, know where our unpublished data may and may not go, share the prompts
and setups that work, and keep the same healthy scepticism we apply to any
new method in the lab. This course is my attempt to make that easy and,
hopefully, a bit fun.

### Who made it

**Anne Floor Holtrop**, bioinformatician at Amsterdam UMC, working in the
Epidemiology & Data Science department
([EDS](https://www.vumc.nl/research/overzicht/epidemiologie-en-data-science-eds.htm))
and the Core Facility Metabolomics
([CFM](https://www.amc.nl/web/core-facility-metabolomics.htm)).
I specialise in analysing lipidomics and metabolomics datasets with
bioinformatic pipelines, and I'm developing a diagnostic pipeline for
screening lysosomal storage diseases. I mostly work in R and Python.

- GitHub: [github.com/HoltropAF](https://github.com/HoltropAF)
- LinkedIn: [linkedin.com/in/afholtrop](https://www.linkedin.com/in/afholtrop/)
- Google Scholar: [publications](https://scholar.google.com/citations?user=GmIyf_wAAAAJ)

Questions, ideas or corrections: reach out via GitHub or in our lab group.

### How it was made

This course was written largely with generative AI: mostly with Claude,
with help from ChatGPT, Gemini and Ollama (local models), and reviewed by
the course organisers. Facts and references were checked against sources,
but the text has not yet been checked by a domain expert; a
bioinformatician and an immunologist reading their parts would catch things
a model doesn't. Like any AI-assisted work, it can still contain mistakes.
Check what matters to you, and tell us when something looks off. Consider
it the first exercise: we are practising what we preach about disclosing AI
use (see the AI log in part 2).

> **In short**
> - A free, self-paced course about using AI well in our lab, done together; no programming needed.
> - Made largely with AI and checked against sources, so check what matters and report what looks off.

---

## 2. How do I use it?

### The route

Start with the Orientation, then do Modules 1 to 5 in order. Modules 1 and
2 are the heart of the course; Modules 3 to 5 show how to get more out of
the tools, with technical parts you can skim. Brand new to AI? Module 1
opens with the foundations, all the words in plain language. Do the
modules alone or in group sessions of about two hours (more fun, and you
can compare results); one module every week or two is a comfortable pace.
Module 6, the hackathon, brings it all together: in teams of two to four,
after Modules 1 to 5, you combine everything in one research project.

### Inside a module

Every module takes you through the same steps, in this order:

| Step | What it is |
|------|-----------|
| **Chapter** | The story of the topic. Read this first. |
| **Extra reading** | Templates and reference files, in the modules that have them. |
| **Exercise** | Hands-on work, always on public or synthetic data. Optional, but that's where it clicks. |
| **Self-check** | Questions with hidden answers, a mini-experiment, and critical questions. |
| **Wrap-up** | Tick off what you did, read back your saved notes, add new ones. |

<!-- speak: A table of the steps in every module. The chapter tells the story; read it first. Extra reading has templates and reference files. The exercise is hands-on, on public or synthetic data. The self-check has questions with hidden answers and a mini-experiment. And the wrap-up is where you tick things off and read back and add to your notes. -->

The *Next* button at the bottom of each step takes you through them in
order, and each chapter's *Looking ahead* links to optional slides with the
same ideas as a quick recap. Each chapter reads like a chapter of a
friendly textbook: an opening story, parts that each end with a short
recap, little questions to think about, and a summary at the end. You'll
meet a few kinds of boxes. Try this one:

<details class="think"><summary>Pause and think: if a model writes a reference with a perfect-looking DOI, is the paper real?</summary>

Not necessarily. Models generate what a reference *looks like*, so always
click the DOI. That's what these boxes are for: think first, then open the
answer.

</details>

> **Coffee note:** little asides like this one are scattered through the
> chapters: an anecdote, a bit of honesty, a reminder that it's fine not to
> know everything.

Stuck on a word? Hover over (or tap) any word with a dotted underline for
a quick definition, or open the Dictionary. Prefer listening? Press
**Read aloud** on any page; the space bar pauses it.

### Two habits worth starting now

The first is a short AI log. When you use AI in a real project, write one
line: the date, the tool and version, what you used it for, and what you
checked. It takes ten seconds and makes the disclosure in your paper easy;
a template is in `course/templates/ai_use_log.md`.

The second is to check before you trust. Before AI output goes into an
analysis, a figure or a manuscript, ask yourself five things:

1. Did I check every fact and reference against a source I opened myself?
2. Did every number come from code I can run, not from the model's text?
3. Do I understand the code, and do the tests pass?
4. Did I record the model, version and prompt?
5. Was I allowed to send this data to this tool?

If the answer to any of the first three is no, it's a draft, not a result.
The full checklist is in `course/templates/ai_output_verification_checklist.md`.

### Running a group session

Anyone who has done a module can run it for others. A two-hour session
works well like this: a short check-in (10 min), the slides as a shared
recap (30 min, everyone has read the chapter beforehand), a live demo
including at least one failure (15 min), hands-on work in pairs (40 min),
and the critical questions together (20 min). More tips per module are in
`course/facilitator_guide.md`.

### Your progress, feedback and problems

Your ticks and notes are saved in this
browser, on this device only. They are never uploaded, shared or graded. A
different browser, computer or phone starts empty, and clearing your
browser data erases them, so use **Copy summary** on the dashboard now and
then if you want to keep them. Keep unpublished results and patient
information out of your notes.

Found a mistake, a typo or something that doesn't work? Use **Report a
problem** at the bottom of the menu; your reports are collected in this
browser, and when you have a few, you export them and send them to the
course organiser. Wrote a prompt, skill or subagent that works well? Share
it in the group or as a pull request on the course repository: that is how
the course gets better. Missing a word in the Dictionary? Ask, and we'll
add it. All course material lives in one Git repository, and this
dashboard is generated from it; it is meant for training within our lab
and among friends.

> **In short**
> - Orientation, Modules 1 to 5 in order, then the hackathon; each module goes chapter, extra reading, exercise, self-check, progress.
> - Start two habits now: a one-line AI log, and five questions before you trust an output.
> - Your progress stays in this browser; report problems from the menu.

---

## 3. What are its limits?

A course that teaches you to look critically at AI output should be honest
about its own limits. Here they are.

### What may be out of date

AI changes monthly. Model names, prices, software commands and especially
the watermarking and EU-rules part describe October 2026; the boxes marked
*AI-researched* are the most time-sensitive. The course also leans towards
one vendor: the technical parts of Modules 3 to 5 are built around Claude
Code. The ideas transfer to other tools, but try those too.

The parts below change fastest. Each has a "last checked" date; whoever
looks after the course rechecks them on the schedule shown, updates the
text and the date, and notes the change on the
[References](references.md) page.

| What | Where | Last checked | Recheck |
|------|-------|--------------|---------|
| The tools: what each is good at, account types, privacy terms | Module 1, *Which tool should I use?* | 8 October 2026 | Every 6 months |
| Account types, retention and zero data retention | Module 1, *Where does my data go?* | 8 October 2026 | Every 6 months |
| Watermarks, provenance labels and the EU AI Act | Module 1, *Can you tell what AI made?* | 8 October 2026 | Every 6 months, and after new EU guidance |
| Model names, sizes and Ollama commands | Module 1 exercise, Module 2 | 8 October 2026 | Every 6 months |
| Claude Code features, settings and commands | Modules 3–5 | 8 October 2026 | Every 6 months |
| MCP setup and the list of adopters | Module 4 | 10 October 2026 | Yearly |
| History facts (dates, names) | All modules | 10 October 2026 | Only when a source changes |
| Links on the References page | References | 8 October 2026 | Yearly (check for dead links) |

<!-- speak: A table of the parts that change fastest, with the date they were last checked and how often to recheck them. The tools and their account types and privacy terms, the watermark and EU rules, model names and commands, and Claude Code features are rechecked every six months. MCP setup and the reference links once a year. History facts only when a source changes. -->

Who looks after it is still to be named (see *Still to be arranged*,
below). Until then, use **Report a problem** to flag anything outdated.

### What the course can't promise

The data rules are advice, not policy: the four data classes are sensible
defaults, not official Amsterdam UMC rules, so check with your data steward
or data protection officer, and use the tools and accounts the institution
has approved. The mini-experiments use 5 to 10 runs so they fit in a
session; they show the *kind* of error a tool makes, not a precise error
rate. Automatic checks have limits too: scripts can catch invented genes,
but not whether a gene truly belongs to a pathway, and that stays a human
job. And the read-aloud voices: the built-in ones run on your computer, but
the "online" voices in Microsoft Edge send the text to Microsoft, which is
fine for this course, not for your own unpublished documents.

### Still to be arranged

- Software installs on work laptops may need IT approval.
- The full exercises in Modules 3 to 5 use Claude Code, which needs a paid
  account; who provides it is still open. Each of those modules also has a
  no-code version that works in a normal chat app.
- Hackathon dates, mentors and schedule are placeholders.
- Someone to look after the course and recheck the time-sensitive parts
  (see *What may be out of date*).

Seen something else? Use **Report a problem** in the menu.

> **In short**
> - Time-sensitive parts carry a "last checked" date and a recheck schedule.
> - The data rules are advice, the experiments are small, and automatic checks don't replace you.
