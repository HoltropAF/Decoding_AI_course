---
name: clean-commits
description: Make and review clean git commits - one logical change per commit, grouped sensibly, with a clear message that explains why. Use when committing changes, planning how to split work into commits, or reviewing recent commits.
---

# Clean commits

Help make commits that each hold one logical change and together tell a
readable story of how the code evolved. The history should be
understandable without reading the code.

## When to use

- Before committing: deciding what goes into which commit.
- Writing or improving a commit message.
- Reviewing recent commits, or cleaning up a branch before merging.

## How to work

1. **Look at what changed** (`git status`, `git diff`) and group the
   changes by purpose.
2. **Ask of each group:** is this one logical change? Can it be described
   in one sentence? If it had to be undone, would all of it go?
3. **Split** anything that fails those questions into separate commits.
4. **Write the message** in the format below.
5. **Check the result** against the red flags before committing.

## Standards

### Group together

- One feature or fix, with its tests and the documentation that explains
  it.
- One refactor of one component.
- Dependencies that only work together.
- Configuration changes for one purpose.

### Keep separate

- A bug fix and an unrelated refactor.
- Two features, unless one depends on the other.
- Formatting and logic changes.
- Several unrelated bugs (one commit each).
- Upgrades of unrelated packages (one commit each:
  `chore: upgrade <package> to <version>`).

### Message format

```
<type>: <subject>

<body>
```

- Types: `feat`, `fix`, `refactor`, `test`, `docs`, `style`, `perf`,
  `chore`, `ci`.
- Subject: at most 50 characters, imperative mood ("fix", not "fixed"), no
  full stop, specific ("add PQN normalisation for lipidomics", not
  "update code").
- Body (recommended): a blank line after the subject, wrapped at 72
  characters, explaining what changed and why; reference issues
  ("Fixes #123").

### Squash or keep

Keep commits that are separate logical steps and each pass the tests.
Squash work-in-progress commits, typo fixes and repeated attempts at the
same thing. Split a large refactor into steps (rename → restructure →
optimise) that each make sense on their own.

## Output

When committing: the proposed commits, each with its files and message.
When reviewing: per commit, keep, split or squash, with a better message
where needed.

## Never

- Mix unrelated changes, or formatting with logic, in one commit.
- Write a subject with "and" joining two topics, or a message like "fixed
  stuff".
- Commit secrets, raw data or large binaries.
- Rewrite history on a shared branch without agreement.
