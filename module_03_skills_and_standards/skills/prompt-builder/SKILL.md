---
name: prompt-builder
description: Turn rambled, unstructured input (voice transcripts, stream-of-consciousness notes, messy briefs) into a clean, structured prompt with labelled sections. Use when the user has a messy description of a task and wants a well-organised prompt to send to another AI. Flags ambiguities and contradictions instead of resolving them silently, and asks for confirmation before finalising.
---

# Prompt builder

Turn messy, rambled or stream-of-consciousness input into a clean,
structured prompt, without losing the substance of what the person
actually meant. The result is a draft until the person confirms it.

## When to use

- A voice transcript, rambled notes or a messy brief that has to become a
  prompt for another AI.
- The end of a long brainstorm, to turn the decisions into one briefing.

## How to work

1. **Read the raw input carefully.** Treat every detail as potentially
   important, including asides and "oh, and also…" remarks.
2. **Extract every constraint first, in a pass of its own:** must-include
   and must-avoid items, length and format limits, deadlines, anything
   stated as a rule rather than a preference. Constraints mentioned in
   passing are the easiest to lose.
3. **Show the constraint list** before building the draft, so the person
   can catch anything missing or misread.
4. **Identify the other parts**, usually Context, Task and Tone, plus the
   Constraints from step 2. Add or drop parts as the input needs; don't
   force a template on it.
5. **Watch for problems** while drafting: ambiguity (a phrase that could
   mean two things), contradiction (two requirements that can't both
   hold) and missing information (something the prompt clearly needs, such
   as audience or length).
6. **Build the draft, then check it against the constraint list.** Every
   constraint must be in it, and placed where it will be noticed: near the
   top of the Constraints part, or repeated if it is easy to violate.
7. **Wait for the person's answers**, work them in, check against the
   constraint list once more, and give the final version, clearly marked.

## Standards

- **Include rather than trim.** When unsure whether a detail matters, keep
  it and ask.
- **Position matters as much as presence.** A constraint buried at the end
  of a long list is easily ignored; promote it.
- **No new scope.** Organise the person's intent; don't add requirements or
  creative direction they didn't give.
- **Plain labels** (Context:, Task:, Tone:, Constraints:, or whatever fits),
  not XML tags, unless asked.

## Output

```
CONSTRAINTS I FOUND:
- ...

STRUCTURED PROMPT (draft):
Context: ...
Task: ...
Tone: ...
Constraints: ...

FLAGS:
- [Contradiction] You said X early on and Y later – which should I use?
- [Ambiguity] "Punchy but professional" could mean A or B – which did you mean?
- [Missing] No target length was mentioned – leave it open or suggest one?
```

If there are no flags, say so explicitly ("No contradictions or
ambiguities found"). After the person answers, give the FINAL PROMPT,
ready to copy.

## Never

- Resolve an ambiguity or contradiction silently.
- Treat the draft as final before the person confirms.
- Drop a detail because it looks untidy.
- Copy names, unpublished results or other sensitive details into the
  prompt without pointing them out.
