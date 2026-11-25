# AI development, Claude Code, context engineering, and agentic workflows

## Main takeaway

The material points to one central idea: AI development is moving from “write a good prompt” toward **building reusable agent infrastructure**. The most useful setups combine clear context, persistent project memory, reusable skills, explicit plans, verification loops, MCP/tool access, subagents, and orchestration. This connects nicely to the epiplexity paper: what matters is not just raw information, but **usable structure** that a computationally bounded system can actually exploit.

Source:
- https://arxiv.org/html/2601.03220v2

---

## 1. Theory: structural information, epiplexity, and why “better context” matters

**What:** The paper **“From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence”** introduces *epiplexity* as a way to describe the structural information that a computationally bounded observer can learn from data. The paper argues that classic Shannon information and Kolmogorov complexity do not fully capture the kind of useful, learnable structure modern AI systems rely on.

**Why:** This is relevant for AI development because it gives a theoretical framing for something practical: not all context is equally valuable. A large dump of random or poorly structured information may be less useful than a smaller, well-organized set of files, examples, workflows, and decisions. The paper links epiplexity to data selection, data transformation, curriculum, and out-of-distribution generalization.

**How:** For projects, this means we should organize context so the agent can reuse structure: project rules, recurring decisions, known file paths, test commands, domain-specific terminology, examples of good outputs, and repeatable workflows. In practical terms, this supports using files like `CLAUDE.md`, `research.md`, `plan.md`, project READMEs, reusable skills, and task-specific checklists.

**Sources:**
- https://arxiv.org/abs/2601.03220
- https://arxiv.org/html/2601.03220v2
- Uploaded image: `image(5).png` — paper announcement / value-of-data figure.

---

## 2. Claude Code workflow: research → plan → annotate → implement → verify

**What:** The strongest recurring workflow is to separate thinking from coding. Claude Code should first inspect the codebase, produce a written understanding, then create a plan, then only implement after the human has reviewed and corrected the plan. Boris Tane’s workflow makes this very explicit: Claude writes `research.md`, then `plan.md`, the human annotates the plan, and only then Claude implements.

**Why:** This prevents the most expensive failure mode of AI coding: code that works in isolation but breaks the existing system. Anthropic’s own Claude Code best practices emphasize that context fills quickly, model performance can degrade as context fills, and Claude should be given specific context, clear constraints, and a way to verify its work.

**How:** For meaningful tasks, use a workflow like this:

1. Ask Claude to inspect the relevant folder/files deeply and write `research.md`.
2. Ask Claude to create `plan.md` with file paths, trade-offs, code snippets, and testing strategy.
3. Review and annotate the plan yourself.
4. Tell Claude to update the plan but explicitly say **do not implement yet**.
5. Once the plan is correct, ask Claude to implement exactly the plan.
6. Require verification through tests, type checks, linting, screenshots, or command output.

**Sources:**
- https://boristane.com/blog/how-i-use-claude-code/
- https://code.claude.com/docs/en/best-practices

---

## 3. Reusable agent infrastructure: skills, commands, subagents, hooks, MCP

**What:** The Claude Code materials strongly suggest that productivity compounds when you build reusable workflows instead of starting from zero each time. Claude Code supports `CLAUDE.md`, skills, hooks, custom subagents, plugins, CLI tools, and MCP servers. Skills can hold domain-specific knowledge or repeatable workflows; subagents can investigate in separate contexts; hooks can enforce deterministic actions such as running a linter or blocking unsafe file writes.

**Why:** Reusable workflows become more valuable as models improve. The user-supplied Claude Code screenshot makes this point clearly: skills like `pdf-extractor`, `paper-visualizer`, `summarize-papers`, `deep-research`, `run-parallel`, `web-app-designer`, and `mcp-builder` become a reusable operating layer. This means future Claude, Codex, or other agents can benefit from the same workflow patterns.

**How:** Create `.claude/skills/<skill-name>/SKILL.md` files for recurring tasks. Keep `CLAUDE.md` short and only include rules that apply broadly; use skills for domain-specific or occasional workflows. Use hooks when the action must always happen. Use subagents for tasks that would otherwise fill the main context window, such as broad codebase investigation, security review, documentation review, or automated code review.

**Important detail:** Scott Spence’s testing showed that skills do not always activate reliably just because they exist. His forced-evaluation hook improved activation compared with a simple passive instruction, because it made Claude explicitly evaluate, commit to, and then activate relevant skills before implementation.

**Sources:**
- https://code.claude.com/docs/en/best-practices
- https://scottspence.com/posts/how-to-make-claude-code-skills-activate-reliably
- Uploaded image: `image(6).png` — Claude Code skills/workflows screenshot.
- https://platform.claude.com/cookbook

---

## 4. Context engineering: make project knowledge persistent and reusable

**What:** Prompt engineering is no longer only about phrasing a single prompt. The DAIR Prompt Engineering Guide frames prompt engineering as a broader discipline for working with LLMs, including techniques, tools, RAG, agents, context engineering, and external knowledge.

**Why:** Agents fail when the right context is missing, noisy, stale, or hidden in chat history. Context engineering is about designing the information environment around the model: what files it sees, what examples it uses, what rules persist, what tools it can call, and what verification signal it gets.

**How:** For a serious AI-assisted project, create a small set of durable files:

- `README.md` — what the project is and how to run it.
- `CLAUDE.md` — project rules, commands, testing instructions, style conventions.
- `AI_CONTEXT.md` — domain background and important decisions.
- `research.md` — Claude’s current understanding of the relevant code/system.
- `plan.md` — reviewed implementation plan and task checklist.
- `VALIDATION.md` — checks that must pass before output is trusted.
- `.claude/skills/` — reusable workflows for repeated project tasks.

**Note:** The supplied DAIR link `https://academy.dair.ai/blog/agentic-context-engineering` appears to be relevant as an example of agentic workflows that read sources, generate a visual, annotate it, and iterate.

**Sources:**
- https://www.promptingguide.ai/
- https://github.com/dair-ai/Prompt-Engineering-Guide
- https://academy.dair.ai/blog/agentic-context-engineering

---

## 5. Orchestration and multi-agent work

**What:** The next layer is orchestration: running multiple agents, assigning tasks, reviewing outputs, coordinating file access, and keeping audit trails. The `ntm` project appears to be a local control plane for multi-agent software development using tmux, with session orchestration, work triage, safety policies, approvals, checkpoints, timelines, REST/WebSocket APIs, and robot-readable surfaces.

**Why:** Once agents can work for longer periods, the bottleneck shifts from “can the model write code?” to “can I coordinate, supervise, verify, and safely merge the work?” This is especially relevant when using Claude Code, Codex, Gemini, or multiple agents in parallel.

**How:** Use worktrees, tmux sessions, labels, checkpoints, task queues, code-review agents, and clear assignment protocols. Keep agents isolated when needed. Use one agent for implementation, another for review, another for test generation, and another for documentation or security review. Avoid letting several agents edit the same files without coordination.

**Sources:**
- https://github.com/Dicklesworthstone/ntm
- https://platform.claude.com/cookbook
- Uploaded image: `image(6).png`

---

## 6. Remote/mobile continuation of local Claude Code sessions

**What:** The provided X post announced Claude Code **Remote Control**, where a local terminal session can be continued from a phone or browser.

**Why:** This matters because it turns long-running Claude Code work into something you can supervise away from your desk. The local filesystem, MCP servers, tools, and project configuration can remain available because execution starts from a local machine/session.

**How:** The announcement text says to try it with `/remote-control`: start local sessions from the terminal, then continue them from your phone without losing flow. This is useful for long-running agentic coding sessions where you want to check progress, approve actions, or redirect the session while away from the computer.

**Sources:**
- https://x.com/noahzweben/status/2026371260805271615

---

## 7. Visual, multimodal, and diagram workflows

**What:** Several resources point toward visual and multimodal agent workflows. The Claude Cookbook includes practical examples, and Fireworks Tech Graph is a GitHub project related to AI/development tooling and technical graph/diagram generation.

**Why:** Visual structure is useful for architecture, papers, workflows, and debugging. Diagrams help humans review what the agent thinks the system is doing. Screenshots and images also give the model grounding that pure text sometimes misses.

**How:** Use diagram tools to turn architecture descriptions, agent workflows, and paper concepts into visuals. Use Claude Code with image-generation or playground-style review loops when you want to generate, annotate, and refine visual outputs.

**Sources:**
- https://github.com/yizhiyanhua-ai/fireworks-tech-graph
- https://academy.dair.ai/blog/agentic-context-engineering
- https://platform.claude.com/cookbook

---

## 8. Reasoning models and “societies of thought”

**What:** The Omar Sar X link is likely related to reasoning models, agentic workflows, or prompt/context engineering.

**Why:** This source fits the broader theme that AI systems can benefit from structured reasoning, multiple perspectives, and explicit orchestration. Whether inside one model or across several agents, the practical idea is the same: separate roles often produce better results than one vague instruction.

**How:** In practice, set up explicit role separation. For example: one Claude session investigates, one writes the plan, one implements, one reviews, and one verifies tests. Avoid one monolithic “do everything” prompt for complex work.

**Sources:**
- https://x.com/omarsar0/status/2015079909048422735

---

## 9. Learning resources

**Claude Code for Everyone** is a DAIR.AI course aimed at learning Claude Code and related workflows.

**Claude Cookbook** is useful for implementation examples: agent patterns, tools, RAG/retrieval, multimodal workflows, skills, context management, prompt caching, evals, and orchestration patterns.

**Prompt Engineering Guide** is the broader reference for prompting, RAG, agents, context engineering, function calling, ReAct, prompt chaining, multimodal prompting, and prompt risks.

**Sources:**
- https://dair-ai.thinkific.com/courses/claude-code-for-everyone-2
- https://platform.claude.com/cookbook
- https://github.com/dair-ai/Prompt-Engineering-Guide
- https://www.promptingguide.ai/

---

## Practical checklist for applying this

1. **Create a project memory layer**
   - `README.md`
   - `CLAUDE.md`
   - `AI_CONTEXT.md`
   - `VALIDATION.md`

2. **Use persistent planning artifacts**
   - `research.md`
   - `plan.md`
   - `todo.md` or a checklist inside `plan.md`

3. **Build reusable workflows**
   - `.claude/skills/`
   - custom commands
   - hooks
   - subagents
   - MCP tools

4. **Force verification**
   - tests
   - linting
   - type checks
   - screenshots
   - output diffs
   - reviewer subagent

5. **Use orchestration for larger work**
   - git worktrees
   - tmux / NTM
   - separate agents for planning, implementation, review, and validation
   - checkpoints and audit logs

6. **Use visual/multimodal tools where useful**
   - diagrams for architecture and workflows
   - screenshots for UI review
   - annotated visual feedback loops

7. **Keep context clean**
   - avoid overloading `CLAUDE.md`
   - move occasional workflows into skills
   - clear or compact context when needed
   - use subagents for broad investigation

---

## Complete source list

### Uploaded images/files

- `image(5).png` — screenshot/figure for **From Entropy to Epiplexity**, value of data, structural information, and OOD transfer.
- `image(6).png` — screenshot of Claude Code skills and commentary on reusable workflows, skills, orchestration, multimodality, and compounding agent productivity.

### Links provided

- https://arxiv.org/abs/2601.03220
- https://arxiv.org/html/2601.03220v2
- https://dair-ai.thinkific.com/courses/claude-code-for-everyone-2
- https://platform.claude.com/cookbook
- https://code.claude.com/docs/en/best-practices
- https://github.com/Dicklesworthstone/ntm
- https://academy.dair.ai/blog/agentic-context-engineering
- https://boristane.com/blog/how-i-use-claude-code/
- https://scottspence.com/posts/how-to-make-claude-code-skills-activate-reliably
- https://x.com/noahzweben/status/2026371260805271615
- https://github.com/dair-ai/Prompt-Engineering-Guide
- https://github.com/yizhiyanhua-ai/fireworks-tech-graph
- https://x.com/omarsar0/status/2015079909048422735
- https://www.promptingguide.ai/
