# Skill: wrap-up

What the skill makes the assistant do. How to start it is at the top
of this step; the skill file itself is the last part of this page.

## 1. What does the skill do?

### What it is

Every new AI chat starts from zero, and after a week away, so do we.
This skill closes a work session by bringing the project's status files up
to date: what's finished, what's still open, and what was decided and why.
Together with a `CLAUDE.md` that reads those files in at the start of every
session (the *In practice* box in part 2 of the chapter), it gives the next
session, yours or a colleague's, a running start instead of a blank page.

### Why a skill and not a hook

A hook runs every time, without judgment, and that's exactly what this job
doesn't need. Deciding whether something was finished or only started, or
whether a remark was a real decision, takes reading the conversation and
sometimes asking. And it's a routine you start when *you* decide the
session is over. A recipe the assistant follows when asked is a skill.

### What it covers

The skill first looks for the status files the project's `CLAUDE.md`
names: usually a `ROADMAP.md` with *Now*, *Next* and *Later*, a
`DECISIONS.md` and a changelog. In an ENCORE project, `0_PROJECT.md` (the
project log) takes the changelog's place. It then works out what happened
from the conversation and from git, ticks off finished tasks, adds new
ones, records each real decision with its reason, and logs the finished
work. If you had to correct the assistant on the same thing twice, it
proposes a line for `CLAUDE.md`, the habit from the *Tip* in part 2.

Everything is shown before it's saved, and the skill ends by proposing a
commit, so the status files travel with the work they describe.

### What you get back

A short summary of the session (finished, open, decided), the proposed
change to each file, and a commit message. After your OK, the files are
updated and ready for the next session.

### Its limits

The skill can only record what was said or done in the session; a decision
you made over coffee isn't in there unless you mention it. It can't judge
whether finished work is *correct*: that's for tests and reviewers. And it
only helps if you run it. A roadmap that's three weeks out of date
misleads a new chat more than no roadmap at all, so prune it when it
drifts.
