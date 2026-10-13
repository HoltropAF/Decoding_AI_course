# Skill: clean commits

What the skill makes the assistant do. How to start it is at the top
of this step; the skill file itself is the last part of this page.

## 1. What does the skill do?

### What it is

Git keeps the history of a project, but only if that history is readable.
This skill teaches the assistant (and, along the way, you) to make commits
that each hold one logical change, with a message that explains why. That
matters even more once AI writes part of your code: small, well-described
commits are what let you see, and undo, exactly what an agent changed
(Module 5's "git commit and pray" tip).

### What it covers

The core rule is simple: group what belongs together, keep apart what
doesn't. A bug fix and the test that proves it go in one commit; a bug fix
and an unrelated clean-up go in two. Formatting changes never hide inside a
logic change, and two dependency upgrades only share a commit when they
can't work without each other. Before every commit, the skill has the
assistant ask: can this be described in one sentence, and if I had to undo
it, would I want to undo all of it?

Commit messages follow a fixed shape: a type (`feat`, `fix`, `refactor`,
`docs`, `test` and a few more), a short subject in the imperative ("fix
null handling in sample sheet parser", not "fixed stuff"), and a body that
says what changed and why, because the code already shows how. The skill
also covers when to squash work-in-progress commits, how to split a large
refactor into readable steps, and the red flags of a commit that should be
split, such as a subject with "and" in it.

### What you get back

When the assistant commits for you, smaller commits with clear messages.
When you ask it to review, a judgment per commit (keep, split or squash)
with a better message where needed.

### Its limits

The skill can only judge what it sees: a diff and a message. Whether a
change is *correct* is a different question, for tests and for a reviewer
such as Argus (Module 5). And it describes one common style; if your lab
or a project you contribute to uses another, follow theirs.
