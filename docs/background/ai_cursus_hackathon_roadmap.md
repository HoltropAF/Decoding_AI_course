# AI Cursus & Hackathon Roadmap: Bioinformatics & Systems Immunology

This master curriculum and project specification is designed to take a computational biology team from fundamental LLM mechanics to advanced autonomous agent orchestration, local inference, and multi-omics hackathon applications.

---

## Curriculum Overview

```
Module 1: Foundations, Ecosystem & Cloud vs. Local
  └── Core mechanics, tokenization, cost models, Ollama setup, data classification.
Module 2: Prompting Architecture & Structured Context
  └── 5-part prompt framework, few-shotting, JSON/XML outputs, hallucination control.
Module 3: AI Skills & Operational Standardization
  └── System instructions, CLAUDE.md templates, team standards, versioning.
Module 4: Model Context Protocol (MCP) & Data Connections
  └── MCP architecture, file system & DB integration, API security, sandboxing.
Module 5: Autonomous Agents & Tool Execution
  └── Planning loops, function calling, code interpretation, Human-in-the-Loop.
Module 6: Systems Immunology & Multi-Omics Application (Hackathon)
  └── Applied bioinformatics workflows, multi-omics synthesis, hackathon tracks.
```

---

## Detailed Modules

### Module 1: Foundations, Ecosystem & Cloud vs. Local
**Goal:** Understand LLM mechanics, master model selection, and establish local privacy boundaries.

* **LLM Core Mechanics:** Next-token prediction, attention mechanisms ($Q, K, V$), and context windows. Why models excel at sequence patterns (text, biological FASTA strings, SMILES) but require external execution for precise arithmetic.
* **Model Selection Framework:**
  * **Cloud Flagships:** Claude (reasoning, code, complex analysis), ChatGPT/Codex (general purpose), Gemini (large-context document processing).
  * **Local Execution (Ollama / LM Studio):** Running open models (Llama 3, DeepSeek, Qwen) on local hardware.
* **Token Dynamics & Economics:** Tokenization behavior, input vs. output cost calculations, context window limits, and context rot.
* **🔒 Security & Data Privacy:** Consumer vs. Enterprise API privacy terms. What data can go to the cloud vs. what must stay strictly local on Ollama (e.g., patient datasets, pre-publication multi-omics results).

---

### Module 2: Prompting Architecture & Structured Context
**Goal:** Move from informal chatting to deterministic, reproducible execution for scientific analysis.

* **Anatomy of an Engineering Prompt:** Framing requests using **Role, Context, Instruction, Inputs, and Output Format**.
* **Deterministic Outputs for Pipelines:** Forcing strict JSON or XML schema outputs for direct consumption by downstream Python/R scripts.
* **Context Anchoring & RAG Mechanics:** Grounding prompts with reference documents (e.g., pathway databases like Reactome/KEGG) to eliminate biological hallucinations.
* **Advanced Patterns:**
  * **Few-Shot Prompting:** Providing input/output exemplars for complex formatting.
  * **Chain-of-Thought (CoT):** Forcing step-by-step reasoning for logic-heavy tasks.
* **🔒 Security Checkpoint:** Direct and indirect prompt injection defense when processing external text (e.g., automated paper summarization).

---

### Module 3: AI Skills & Operational Standardization
**Goal:** Convert high-performing prompts into persistent, version-controlled team instructions.

* **What is an AI Skill?** Moving beyond ephemeral chat sessions into persistent rule files (`CLAUDE.md`, system prompts, or workspace configurations).
* **Building Team Standards:**
  * Codifying coding style guides, unit testing rules, and bioinformatics pipeline conventions.
  * Creating domain-specific reference templates (e.g., standardized differential gene expression report formats).
* **Version Control for Prompts:** Storing and sharing skill templates in GitHub repositories for reproducible team usage.
* **🔒 Security Checkpoint:** Ensuring skills do not hardcode credentials, private API endpoints, or confidential keys.

---

### Module 4: Model Context Protocol (MCP) & Data Connections
**Goal:** Safely connect language models directly to local files, databases, and microservices.

* **Understanding MCP:** The open protocol that standardizes how LLMs talk to external tools and file systems ("USB-C for AI").
* **Connecting Data Sources:** Building local MCP connectors to interact with local directories, SQL/NoSQL databases, and internal REST APIs.
* **Automated Data Retrieval:** Allowing AI to dynamically query pathway APIs (e.g., HMDB, ENSEMBL) without writing bespoke wrapper code for every query.
* **🔒 Security Checkpoint:**
  * Least-privilege connections: Enforcing read-only access by default.
  * Credential hygiene: Storing API keys in environment variables, never in prompt context.
  * Isolated execution: Running local tools in sandboxed environments (e.g., Docker).

---

### Module 5: Autonomous Agents & Tool Execution
**Goal:** Combine Models, Skills, and MCP into multi-step, goal-oriented execution loops.

* **Agentic Architecture:** The loop of **Plan $\rightarrow$ Select Tool $\rightarrow$ Execute $\rightarrow$ Observe $\rightarrow$ Refine**.
* **Code Execution Environments:** Equipping agents with Python execution environments to run data transformations, inspect error tracebacks, and self-correct code iteratively.
* **Agent vs. Workflow:** Knowing when to use rigid, deterministic code scripts vs. flexible, non-linear agentic loops.
* **🔒 Security Checkpoint:**
  * Human-in-the-Loop (HITL): Inserting mandatory human confirmation steps before executing high-risk actions (e.g., committing code changes, modifying databases).
  * Circuit breakers and execution step limits to prevent infinite token loops.

---

### Module 6: Systems Immunology & Multi-Omics Application (Hackathon)
**Goal:** Bridge core AI concepts into active research challenges through hands-on project tracks.

* **Target Domains:**
  * **Transcriptomics (RNA-Seq):** Functional annotation of DEG clusters, mapping DEGs to dendritic cell maturation pathways in lymph nodes.
  * **Metabolomics & Lipidomics Integration:** Mapping raw lipid identification outputs to metabolic networks and cross-referencing multi-layer correlation matrices.
  * **Spatial Dynamics:** Assisting in parameterizing or debugging spatial/kinetic models of immune cell interactions.

---

## Hackathon Project Tracks

### Track A: Multi-Omics Synthesis Agent
* **Objective:** Build an agent that accepts a DEG list (RNA-Seq) and lipid change matrix (Lipidomics), queries local or online pathway databases via MCP, and synthesizes an interactive HTML report with biological interpretations.
* **Target Stack:** Python, Claude API or Ollama local model, MCP Server, Jinja2/HTML rendering.
* **Success Criteria:** Agent successfully links lipid class shifts (e.g., sphingolipids/ceramides) with transcriptomic markers of dendritic cell activation.

### Track B: Local Privacy-Preserving Literature RAG
* **Objective:** Build a fully offline Retrieval-Augmented Generation (RAG) system over a collection of domain PDFs (focusing on lymph node microenvironments and immune cell dynamics).
* **Target Stack:** Ollama (Llama 3 / DeepSeek / Qwen), ChromaDB / FAISS, Streamlit.
* **Success Criteria:** Precise citations from local PDFs without sending any data off the local machine.

### Track C: Automated Pipeline Debugger & Log Analyzer
* **Objective:** Develop an execution agent that monitors bioinformatics pipeline run logs (e.g., Nextflow, Snakemake, custom Python scripts), parses failure points, and outputs verified code patches.
* **Target Stack:** Python, Function Calling, System Process Monitoring.
* **Success Criteria:** Automatically diagnoses a broken matrix processing script, fixes the syntax or data alignment error, and re-runs the task.

### Track D: Hypothesis Engine for Immune Cell Modulation
* **Objective:** Create an interactive tool where users input an experimental perturbation (e.g., specific TLR agonist applied to dendritic cells); the agent predicts expected downstream transcriptomic and lipid membrane alterations based on literature grounding.
* **Target Stack:** Python, RAG Framework, Structured Output / Pydantic schemas.
* **Success Criteria:** Outputs structured hypotheses in JSON format containing target biological pathways, estimated kinetic trends, and suggested validation experiments.

---

## Suggested GitHub Repository Structure

If you wish to scaffold this project automatically in GitHub, use the following layout:

```text
ai-learning-automation/
├── README.md                          # Course overview and setup instructions
├── docs/
│   ├── 01_foundations_and_apis.md     # Module 1 guide
│   ├── 02_prompting_and_context.md    # Module 2 guide
│   ├── 03_ai_skills_and_standards.md  # Module 3 guide
│   ├── 04_mcp_and_data_connectors.md  # Module 4 guide
│   ├── 05_autonomous_agents.md        # Module 5 guide
│   └── 06_hackathon_guide.md          # Module 6 & Track descriptions
├── exercises/
│   ├── 01_api_and_ollama/             # Python scripts for Cloud API + Ollama inference
│   ├── 02_structured_prompting/       # Pydantic/JSON schema extraction examples
│   ├── 03_mcp_setup/                  # Starter code for custom MCP servers
│   └── 04_simple_agent/               # ReAct agent loop implementation
├── hackathon/
│   ├── track_a_multiomics/            # Starter files for Track A
│   ├── track_b_local_rag/             # Starter files for Track B
│   ├── track_c_log_debugger/          # Starter files for Track C
│   └── track_d_hypothesis_engine/     # Starter files for Track D
└── config/
    └── setup_env.sh                   # Script to install dependencies & set environment keys