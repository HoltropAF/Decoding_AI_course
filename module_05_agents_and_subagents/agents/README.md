# Agent register

Every subagent the lab uses, in one place. Add a row when you add an agent
(via a pull request), and bump the version when you change its file.

Names follow the convention from Module 5, section 6: the mythology hints at
the kind of job (Greek for checking and quality, Egyptian for writing and
knowledge, West African for stories and building, Norse for fetching and
reporting). The description in the agent file still says plainly what it does.

| Name | Job | Tools | Read-only? | Version | File |
|------|-----|-------|-----------|---------|------|
| Themis | Audits a project against the ENCORE structure and reports findings | Read, Grep, Glob | Yes | not yet versioned | `themis.md` |
