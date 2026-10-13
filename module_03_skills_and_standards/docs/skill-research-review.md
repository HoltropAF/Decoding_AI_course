# Skill: research review

What the skill makes the assistant do. How to start it is at the top
of this step; the skill file itself is the last part of this page.

## 1. What does the skill do?

### What it is

Where the omics analysis skill helps you *do* an analysis,
this one argues with you about whether it's the right analysis at all. It
turns the assistant into a critical research advisor for computational
biology and bioinformatics: someone who asks "why this question, why this
method, and what would prove you wrong?" before you spend weeks on it.

### What it covers

Models are trained to be helpful, and that easily turns into agreeing with
you (Module 1 calls it sycophancy). This skill pushes the other way. It
tells the assistant to question the premise before accepting it, to ask
for a justification for every methodological choice, and to point out gaps
between the research question and the proposed method. Vague answers don't
count: "better statistics" isn't enough, it wants to know which test and
why.

The questions come in four groups. About the goal: what exactly is the
question, which gap does it fill, has it been tried before? About the
method: why this one, what are its known limitations, how sensitive is it
to its parameters, and how will you validate it? About the data: where does
it come from, is it suitable, which biases and artefacts might it carry?
And about interpretation: what does a result mean biologically, which
alternative explanations are there, and how would you test it in the lab?
Its scope runs from sequence analysis and NGS pipelines to structural
biology, systems modelling and machine learning.

### What you get back

Not a verdict, but a conversation: pointed questions, the red flags it
sees, the limitations you haven't mentioned, and, where it helps,
references to methods, benchmarks or groups working on something similar.
It keeps asking until the plan is clear, which can feel uncomfortable;
that's the point.

### Its limits

A model playing the critic can be confidently wrong too: it may push for a
method that doesn't suit your data, or name a benchmark or a lab that
doesn't exist. Check the methods and references it brings up, and keep the
final judgment yourself. And unpublished plans and grant drafts fall under
the data rules (Module 1), so use an account that's allowed for them.
