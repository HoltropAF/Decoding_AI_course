# Contributing

How changes to Decoding AI are made, committed and released.

## Branches

| Branch | Purpose |
|---|---|
| `main` | Released course only. Participants clone this. Never commit here directly. |
| `development` | All day-to-day work. Merged into `main` at release time. |

For a large or experimental change (a new module, a dashboard rewrite) you
can branch off `development`, for example `feature/module-07`, and merge it
back when it works. Small changes go straight onto `development`.

## Commit messages

We use [Conventional Commits](https://www.conventionalcommits.org):

```
<type>(<scope>): <summary in the imperative, max 72 characters>

<body: why the change was made and what it affects, wrapped at ~72
characters. The diff already shows what changed.>

<footer: issue references, BREAKING CHANGE: ..., Co-Authored-By: ...>
```

| Type | Use for | Example |
|---|---|---|
| `feat` | new content or functionality | `feat(module_04): add MCP database exercise` |
| `fix` | corrections | `fix(module_02): correct prompt example output` |
| `docs` | README, guides, reference text | `docs: update clone instructions` |
| `style` | layout or formatting only | `style(figures): align module colours` |
| `refactor` | restructuring with the same result | `refactor(course): split build script` |
| `chore` | housekeeping, version bumps | `chore(release): v1.1.0` |

The scope is optional: use a module (`module_03`), `course`, `dashboard`,
`figures` or `reference`.

- Keep one logical change per commit, and leave the course working after
  each one.
- Before pushing, you may squash messy local work-in-progress commits into
  clean ones. Don't rewrite commits that are already pushed.

## Versions

Versions follow `MAJOR.MINOR.PATCH`:

- **MAJOR** (`2.0.0`): course restructure, such as modules added, removed
  or reordered.
- **MINOR** (`1.1.0`): new chapter, exercise or dashboard feature.
- **PATCH** (`1.0.1`): typos, broken links, small fixes.

The `VERSION` file in the repository root is the single source. The build
puts it in the dashboard title, menu, footer and every export.

## Releasing

1. On `development`, set the new number in `VERSION` and in the title line
   of `README.md`.
2. In `CHANGELOG.md`, rename `[Unreleased]` to `[X.Y.Z] - YYYY-MM-DD` and
   start a new empty `[Unreleased]` section above it.
3. Rebuild the dashboard: `python course/build_dashboard.py`.
4. Commit as `chore(release): vX.Y.Z` and push `development`.
5. Open a pull request from `development` to `main` and merge it with a
   **merge commit**, not a squash. Squashing would break the shared history
   between the two branches and cause conflicts at the next release.
6. Tag the merge on `main` and push the tag:

   ```bash
   git switch main && git pull
   git tag -a vX.Y.Z -m "vX.Y.Z"
   git push origin vX.Y.Z
   git switch development
   ```

7. Optionally, create a GitHub Release from the tag, using the changelog
   section as release notes.

To see only the releases on `main`, use `git log --first-parent main`.
