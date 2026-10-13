# Skill: prompt builder

What the skill makes the assistant do. How to start it is at the top
of this step; the skill file itself is the last part of this page.

## 1. What does the skill do?

### What it is

This skill takes a rambling voice note, a stream of half-sentences or a
messy brief, and turns it into a clean, structured prompt, without losing what you actually meant. It's
the skill version of a tip from Module 2: let one AI write the prompt for
another.

### Why a skill and not a subagent

This skill started out as an agent file, and it makes a good lesson. It
works *with* you: it shows you a list first, asks about contradictions, and
waits for your answers before it finishes. A subagent can't do that: it
gets one task, works alone in a fresh context and hands back one report,
so it can't stop halfway to ask you something. It also wouldn't see your
ramble, which is already in your conversation. A skill runs inside that
conversation, so the back-and-forth just works. It also needs none
of what a subagent offers: there's no noisy work to keep out of your
context, and no tools to restrict. The rule from Module 5 in one line: a
skill changes how the current assistant works; a subagent is a separate
worker.

### What it covers

The skill reads the raw input carefully, including the asides and the
"oh, and also…" remarks, because that's where easily forgotten
requirements hide. Its first pass looks only for hard constraints: what
must be in, what must stay out, length, format, deadlines. It shows you
that list before it writes anything else, so you can catch a misread rule
while it's still cheap to fix.

Only then does it build the prompt, in plain labelled parts such as
Context, Task, Tone and Constraints, adding or dropping parts as your input
needs. While it works, it watches for ambiguities (a phrase that could mean
two things), contradictions ("casual" at the start, "formal" at the end)
and missing information (no audience, no length). It never resolves those
quietly; it lists them separately so you decide. Before it finishes, it
checks the draft against the constraint list once more, and moves any
constraint that ended up buried at the bottom of a long list to a place
where it will be noticed.

### What you get back

Three blocks: the constraints it found, the structured prompt as a draft,
and the flags (or an explicit "no contradictions or ambiguities found").
After you answer, a final version, clearly marked and ready to copy.

### Its limits

The prompt builder organises your intent; it doesn't add any. If the ramble leaves
out something important that you didn't notice either, the flags may catch
it, but they're no guarantee. And a rambling note often contains more than
you'd put in a prompt on purpose, such as names, unpublished results or a
collaborator's idea, so read the final prompt before you pass it on (the
data rules from Module 1).
