# Glossary

All the words in one place. Don't learn them by heart; come back here
whenever something sounds like jargon. The plain-language story behind
these is the first half of the Module 1 chapter.

## The basics

| Term | In plain language |
|------|-------------------|
| **Artificial intelligence (AI)** | Umbrella term for computers doing things we'd call "smart": recognising patterns, predicting, understanding or producing language and images. |
| **Machine learning (ML)** | A kind of AI that learns patterns from examples instead of following hand-written rules. Random forests and clustering are ML. |
| **Deep learning** | Machine learning with large neural networks (many layers). Good with images, sequences and language. |
| **Neural network** | Layers of simple calculations, loosely inspired by neurons, whose numbers are tuned during training. |
| **Generative AI** | AI that creates new content: text, images, code, structures. |
| **Predictive AI** | AI that puts a label or number on something ("is this a dendritic cell?"). |
| **Large language model (LLM)** | A generative model trained on huge amounts of text. ChatGPT, Claude, Gemini, Llama, Qwen are LLMs or apps built on them. |
| **Model** | The trained "brain": a very large file of numbers that turns input into output. |
| **Parameters / weights** | The numbers inside a model. "8B" = 8 billion parameters. More usually means smarter and hungrier. |
| **Training** | Building a model from huge amounts of data. Months of work in data centres. Not something we do. |
| **Inference** | Using a trained model to get an answer. What happens every time you press Enter. |
| **Training cutoff** | The date the model's knowledge stops. It doesn't know about anything after that unless you tell it. |
| **Prompt** | Everything you send to the model: question, instructions, pasted text, files. |
| **Chatbot** | An app you type into, like claude.ai or ChatGPT. |
| **API** | A way for code to talk to a model directly, without the chat app. |
| **Closed model** | Only usable through the company's app or API (e.g. Claude, GPT, Gemini). |
| **Multimodal** | Handles more than text: images, PDFs, audio. |
| **Tokeniser** | The component that chops text into tokens from a fixed vocabulary (Llama 3 has ~128,000) and turns each into an ID number. |
| **Pretraining** | The first and biggest training phase: the model learns to predict the next token on trillions of tokens of text. |
| **Base model** | A model straight out of pretraining: a superb text continuer, but not yet a helpful assistant. |
| **Post-training** | Training after pretraining that turns a base model into an assistant: instruction tuning plus preference training. |
| **Instruction tuning** | Training on example conversations (request → good answer) so the model learns to act as an assistant. |
| **Reinforcement learning** | Learning from feedback instead of from correct answers: the model tries something, gets a score, and is nudged towards what scored well. |
| **RLHF** | Reinforcement learning from human feedback: people compare answers, and the model is trained toward the preferred ones. |
| **Backpropagation / gradient descent** | The method that adjusts a model's parameters during training: measure the error, then nudge every parameter slightly to reduce it. |
| **Transformer** | The neural network design behind almost all LLMs: a stack of layers, each with an attention step and a feed-forward step. |
| **Sampling / top-p** | How the next token is chosen from the model's probabilities; top-p restricts the choice to the most likely tokens. Together with temperature, it is why answers vary. |
| **Stateless** | The model keeps no memory between requests; the app resends the whole conversation every time. |
| **Sycophancy** | The tendency of assistant models to agree with you too easily, a side effect of training toward answers people like. |
| **Fine-tuning** | Training an existing model a bit further on your own examples. Rarely needed. |

## AI concepts and techniques

| Term | Meaning | Module |
|------|---------|--------|
| **PCA (principal component analysis)** | A classic method that squeezes many measurements into a few summary axes; samples far from the rest on those axes are candidate outliers. | 1 |
| **Random forest** | A machine-learning method that combines many simple decision trees, each trained on a random part of the data; good for classification on tables. | 1 |
| **Support vector machine (SVM)** | A machine-learning classifier that finds the boundary that separates two groups of samples with the widest possible margin. | 1 |
| **Clustering** | Grouping samples by similarity without labels (for example k-means or hierarchical clustering); samples that fit no group stand out. | 1 |
| **Supervised / unsupervised learning** | Supervised: learning from labelled examples. Unsupervised: finding structure in data without labels. | 1 |
| **Autoencoder** | A neural network that learns to compress and rebuild its input; samples it can't rebuild well are unusual, which makes it useful for outlier detection. | 1 |
| **Agent** | A model running in a loop with tools: it plans, calls tools, observes results and continues until a goal is reached. | 5 |
| **AGENTS.md** | Cross-tool convention for a project instruction file, equivalent to `CLAUDE.md`. | 3 |
| **Attention** | The transformer mechanism that lets each token weigh every other token in the context. | 1 |
| **Baseline** | The result of the simplest alternative method (e.g. no retrieval, a human, classical enrichment), used to judge whether an AI method adds value. | 2, 6 |
| **Chain-of-thought (CoT)** | Prompting the model to reason step by step before answering. | 2 |
| **Circuit breaker** | A hard limit on steps, time or cost that stops an agent loop. | 5 |
| **`CLAUDE.md`** | Project instruction file that Claude Code loads at the start of every session in that folder. | 3 |
| **Cloud model** | A model running on a provider's servers; prompts and files are transmitted there. | 1 |
| **Constrained decoding** | Server-side restriction of generation so the output must match a grammar or JSON schema. | 2 |
| **Context engineering** | Designing everything the model sees (files, rules, examples, tools, history), not just the wording of one prompt. | 2, 3 |
| **Context rot** | Degradation of output quality as the context fills with long or irrelevant material. | 1 |
| **Context window** | Maximum number of tokens (input + output) a model can attend to at once. | 1 |
| **Data classification** | Sorting data into public / internal / confidential / restricted to decide which tools may process it. | 1 |
| **Embedding** | A numeric vector representing text meaning; used for similarity search in RAG. | Track B |
| **ENCORE** | ENhancing COmputational REproducibility: a standard project structure for computational research (van Kampen et al. 2024). | 5 |
| **Few-shot prompting** | Including worked input → output examples in the prompt. | 2 |
| **Ground truth** | Independently established correct answers against which outputs are scored. | all |
| **Grounding** | Supplying source material (documents, database results) and requiring the answer to rely on it. | 2, 4 |
| **Hallucination / fabrication** | Fluent output that is not supported by input or reality (e.g. invented citations, genes, pathways). | 1 |
| **Hook** | A deterministic command that the agent software runs automatically on an event (e.g. after each file edit). | 3 |
| **Human-in-the-loop (HITL)** | Requiring human approval before an agent performs an action with side effects. | 5 |
| **Jaccard similarity** | Size of the intersection divided by the size of the union of two sets; used to compare outputs between runs. | 2 |
| **Least privilege** | Giving a tool or agent only the permissions its task requires. | 4, 5 |
| **Local model** | A model running on your own hardware (e.g. via Ollama); no data leaves the machine. | 1 |
| **MCP (Model Context Protocol)** | Open protocol that standardises how AI applications connect to tools, data and prompts. | 4 |
| **MCP server / client / host** | Server: exposes tools/resources. Client/host: the AI application that connects to servers and executes tool calls. | 4 |
| **Next-token prediction** | The core operation of an LLM: estimating the probability distribution of the next token given all previous tokens. | 1 |
| **Ollama** | Software to download and run open-weight models locally with an HTTP API on `localhost:11434`. | 1 |
| **Open-weight model** | A model whose trained weights are downloadable (e.g. Llama, Qwen, Mistral, Gemma). | 1 |
| **Precision / recall** | Precision: fraction of reported items that are correct. Recall: fraction of correct items that were reported. | 4, 5 |
| **Prompt injection** | Instructions hidden in content the model processes (documents, web pages, tool results) that hijack its behaviour. | 2, 4 |
| **Provenance** | Recorded information on how an output was produced: model, version, prompt/template, inputs, parameters, date. | 2 |
| **Pydantic** | Python library to define data schemas and validate data (including LLM JSON output) against them. | 2 |
| **Quantisation** | Storing model weights at lower precision (e.g. 4-bit) to reduce memory; small quality cost. | 1 |
| **RAG (retrieval-augmented generation)** | Retrieve relevant passages from a document collection, then generate an answer from them. | 2, Track B |
| **Semantic check** | A validation rule about content that a schema cannot express (e.g. every gene in the output is in the input). | 2 |
| **Skill** | A packaged, named workflow (instructions plus optional scripts/templates) an agent loads when the task matches. | 3 |
| **Subagent** | A delegated agent with a scoped task, isolated memory, fixed instructions and restricted tools. | 5 |
| **System prompt** | Fixed instructions given to the model by the application, before the user's input. | 2, 3 |
| **Temperature** | Sampling parameter controlling randomness; low for extraction, higher for brainstorming. | 1, 2 |
| **Token** | The sub-word unit models read and write; roughly 0.75 English words. | 1 |
| **Tool / function calling** | The model emits a structured request to run a function; the application executes it and returns the result. | 4 |
| **Tool poisoning** | Malicious instructions placed in a tool's description or output. | 4 |
| **Transport (stdio / HTTP)** | How an MCP client and server communicate: local subprocess pipes or network HTTP. | 4 |
| **AlphaFold** | Google DeepMind's deep-learning model that predicts a protein's 3D structure from its amino-acid sequence; uses attention like LLMs, but is trained on protein structures and outputs atom coordinates, not text. | 1 |
| **pLDDT** | AlphaFold's per-residue confidence score (0–100); low-scoring regions of a predicted structure should not be trusted. | 1 |
| **Watermark (AI)** | A hidden statistical pattern a model builds into its output (for text: in its word choices) so that the company holding the key can later detect it. Survives copy-paste; weakens with editing. | 1 |
| **SynthID** | Google DeepMind's watermarking technology for AI-generated text, images, audio and video; its text version is open source and the basis of Claude's text watermark. | 1 |
| **C2PA / Content Credentials** | An open standard for signed metadata attached to a file that records where it came from and how it was edited (e.g. "AI-generated"). Stripped by screenshots. | 1 |
| **AI detector** | Software that guesses from writing style whether a text is AI-generated. Unreliable and biased against non-native writers; not the same as a watermark check. | 1 |
| **EU AI Act** | The EU regulation on AI (Regulation (EU) 2024/1689). Its Article 50 transparency rules, including machine-readable marking of AI output, apply from 2 August 2026. | 1 |
| **Prompt engineering** | Designing, testing and versioning prompts systematically so a model reliably does a task; treated in this course as part of the method. | 2 |
| **In-context learning** | A model picking up a task from instructions and examples in the prompt, without any change to its weights. | 2 |
| **Self-consistency** | Sampling several answers to the same prompt and taking the most common one; the agreement also shows how sure to be. | 2 |
| **Prompt chaining** | Splitting a big task into a sequence of small prompts, each checkable, where the output of one feeds the next. | 2 |
| **Persona / role prompting** | Telling the model who to act as ("you are an immunologist"); sets tone and vocabulary but does not reliably improve accuracy. | 2 |
| **ReAct** | A prompting pattern where the model alternates reasoning and tool use; the basis of agent loops. | 2, 5 |
| **Test set (for prompts)** | A small set of inputs with known good answers, used to compare prompt versions. | 2 |
| **Zero-shot prompting** | Asking the model to do a task without giving any examples (as opposed to few-shot). | 2 |
| **Diffusion model** | A generative technique that builds an output (image, structure) by gradually removing noise. Used by image generators and AlphaFold 3. | 1 |
| **Reasoning model** | A model that works through a problem step by step internally before answering; slower, better at multi-step problems. | 2 |
| **Vector store** | Database for embeddings supporting similarity search (e.g. ChromaDB, FAISS). | Track B |
| **ZDR (Zero Data Retention)** | Provider arrangement where inputs and outputs are not stored after processing; does not prevent transmission. | 1 |

## Lab and data terms

| Term | Meaning | Module |
|------|---------|--------|
| **BMDC** | Bone-marrow-derived dendritic cells: dendritic cells grown in the lab from (mouse) bone marrow; the model system in many course examples. | 2, 6 |
| **CCR7** | Chemokine receptor that mature dendritic cells switch on to find their way to the lymph node (following CCL19/CCL21). | 1, 6 |
| **DEG** | Differentially expressed gene: a gene whose expression differs significantly between conditions in an RNA-seq comparison. | 2 |
| **DESeq2** | Widely used R/Bioconductor package that tests RNA-seq counts for differential expression. | 2 |
| **Data use agreement (DUA)** | Contract that states how shared data may (and may not) be used, stored and processed. | 1 |
| **DPO** | Data protection officer: the person at your institution who advises on personal-data rules. | 1 |
| **Ensembl** | Genome annotation database; gives genes stable IDs such as `ENSG00000111640` (human) or `ENSMUSG…` (mouse). | 1, 4 |
| **FDR / padj** | False discovery rate, or the p-value adjusted for testing thousands of genes at once (usually Benjamini–Hochberg). `padj < 0.05` is the common cut-off. | 2 |
| **GDPR** | The EU's General Data Protection Regulation; health and genetic data are special categories with extra protection. | 1 |
| **GEO** | Gene Expression Omnibus: NCBI's public repository for gene expression data such as RNA-seq. | 6 |
| **HMDB** | Human Metabolome Database: reference database of metabolites with IDs and annotations. | Track A |
| **KEGG** | Kyoto Encyclopedia of Genes and Genomes: database of pathways, including metabolism and signalling. | 2, 4 |
| **LIPID MAPS** | Lipid classification and nomenclature resource; the source of shorthand names like `PC 34:1` or `Cer d18:1/16:0`. | 4, Track A |
| **log2 fold change (log2FC)** | How much expression changed, on a log2 scale: +1 means doubled, −1 means halved, 0 means no change. | 2 |
| **LPS** | Lipopolysaccharide: a component of bacterial cell walls that activates dendritic cells through TLR4. | 2, 6 |
| **MetaboLights** | EMBL-EBI's public repository for metabolomics (and lipidomics) studies. | 6 |
| **Pre-publication data** | Results not yet published: treat as confidential, so local tools only unless an approved contract says otherwise. | 1 |
| **Reactome** | Free, curated database of biological pathways with stable IDs (e.g. `R-MMU-…` for mouse). | 2, 4 |
| **TLR** | Toll-like receptors: sensors on immune cells that recognise microbial patterns (TLR4 sees LPS, TLR7/8 see R848, TLR3 sees poly(I:C)). | 6 |

## Computer and tool terms

| Term | Meaning | Module |
|------|---------|--------|
| **Research mode / deep research** | An agent inside a chat app (ChatGPT, Gemini, Claude) that plans searches, reads many web pages and writes a report with citations. Useful for orientation; check the claims you use. | 5 |
| **Custom instructions / Projects / Gems** | Places in chat apps (ChatGPT, Claude, Gemini) where you write standing instructions once, so they're added to every conversation; the chat-app version of `CLAUDE.md`. | 3 |
| **GPU / VRAM** | The graphics card (GPU) does thousands of calculations at once, which makes it fast at running models; VRAM is its own memory, where the model must fit. | 1 |
| **Connector** | A chat-app feature that lets the assistant read from another service, such as Google Drive, OneDrive or email; several are built on MCP. | 4 |
| **ChatGPT** | OpenAI's chat assistant, built on its GPT models; the all-rounder most people tried first. | 1, 2 |
| **Claude** | Anthropic's chat assistant and family of models, known for careful writing, long documents and code. | 1, 3, 5 |
| **Gemini** | Google's chat assistant and family of models, built into Google Workspace and strong with very long material. | 1 |
| **Llama** | Meta's family of open-weight models: you can download them and run them on your own computer, for example with Ollama. | 1, 2 |
| **Claude Code** | Anthropic's AI coding agent: works inside your project folder, reads files, runs commands and edits code (with your permission). | 3, 4, 5 |
| **Microsoft Copilot** | Microsoft's AI assistant built into Word, Excel, Outlook and Teams (formerly "Microsoft 365 Copilot"); with a work account it can fall under enterprise data protection. | 1 |
| **GitHub Copilot** | An AI coding assistant inside your code editor that suggests and writes code; lets you choose models from several companies. | 1 |
| **NotebookLM** | Google's research assistant that answers questions only from documents you upload, with citations. | 1 |
| **Docker** | Runs software in an isolated "container" so it can't touch the rest of your computer except what you allow. | 4 |
| **Environment variable** | A named setting stored outside your code (e.g. `NCBI_API_KEY`); the safe place for secrets. | 1, 3, 4 |
| **Git** | Version control: records every change to your files so you can see what changed and go back. | 3, 5 |
| **Pull request** | A proposed change to a shared repository that colleagues review and approve before it's accepted. | 3 |
| **GitHub** | Website that hosts Git repositories, like this course. | all |
| **JSON** | A structured text format of keys and values (`{"gene": "Ccr7"}`) that code reads easily. | 2 |
| **localhost** | Your own computer, as seen from a web address (`http://localhost:11434` is Ollama on your machine). | 1 |
| **Markdown** | Simple text formatting (`# heading`, `**bold**`, `- list`) used for all course files. | all |
| **Marp** | Tool that turns a Markdown file into slides; used for the course decks. | all |
| **Nextflow / Snakemake** | Workflow managers that run bioinformatics pipelines step by step, reproducibly. | Track C |
| **pip** | Python's package installer (`pip install requests`). | 1 |
| **Repository (repo)** | A project folder tracked by Git, including its full history. | all |
| **Terminal** | The text window where you type commands (PowerShell, Git Bash, macOS Terminal). | 1 |
| **Virtual environment (venv)** | A private folder of Python packages for one project, so projects don't break each other. | 1 |
| **VS Code** | Free code editor from Microsoft; used to read and present the course files. | all |

