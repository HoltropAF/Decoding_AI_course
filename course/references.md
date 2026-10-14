# References

Everything the course draws on, in one place: the scientific papers behind
the explanations, the policy documents behind the privacy rules, and the
sources for the parts that describe current events. Each entry says *why*
it is worth reading and which module it belongs to, and links straight to
the source. Use the search box to find a paper, an author or a topic.

> **How these were checked.** Every DOI below was verified against
> Crossref and every arXiv ID against the arXiv API (8 October 2026):
> the paper exists, with this title and year. Still, practise what
> Module 1 teaches: open the paper before you cite it. arXiv versions can
> differ slightly from the published conference or journal version.

The list follows the course: Module 1 first, then the later modules, then
biology, policy and law. Within each part, the ★ marks the ones to read if
you read only a few.

---

---

## Module 1 · The ideas behind today's AI

- **McCarthy J, Minsky ML, Rochester N, Shannon CE (1955).** A proposal for
  the Dartmouth summer research project on artificial intelligence.
  [PDF](http://jmc.stanford.edu/articles/dartmouth/dartmouth.pdf)
  The document that gave the field its name (Module 1, *What do we mean by
  "AI"?*).
- **Legg S, Hutter M (2007).** A collection of definitions of intelligence.
  *Advances in Artificial General Intelligence*, 17–24.
  [arXiv:0706.3639](https://arxiv.org/abs/0706.3639)
  About seventy definitions of intelligence side by side, and the authors'
  own summary: an agent's ability to achieve goals in a wide range of
  environments.
- **Russell S, Norvig P.** *Artificial Intelligence: A Modern Approach.*
  Pearson (4th edition 2020). [aima.cs.berkeley.edu](https://aima.cs.berkeley.edu)
  The standard AI textbook; defines AI as the study of agents that perceive
  their environment and act on it.
- **OECD (2024).** Explanatory memorandum on the updated OECD definition of
  an AI system. [OECD](https://www.oecd.org/en/publications/explanatory-memorandum-on-the-updated-oecd-definition-of-an-ai-system_623da898-en.html)
  The formal definition for policy makers (updated November 2023) that the
  EU AI Act's definition closely follows.
- **Rumelhart DE, Hinton GE, Williams RJ (1986).** Learning
  representations by back-propagating errors. *Nature* 323:533–536.
  [doi:10.1038/323533a0](https://doi.org/10.1038/323533a0)
  The classic paper on backpropagation, the method that still trains
  every neural network today (see "So what is a neural network?" in AI
  basics). Short, and surprisingly readable.
- **Hochreiter S, Schmidhuber J (1997).** Long short-term memory.
  *Neural Computation* 9(8):1735–1780.
  [doi:10.1162/neco.1997.9.8.1735](https://doi.org/10.1162/neco.1997.9.8.1735)
  The LSTM: the "word-by-word" recurrent design that dominated language
  modelling until transformers replaced it. Useful context for why
  Vaswani et al. mattered.
- ★ **Vaswani A, et al. (2017).** Attention is all you need. *NeurIPS.*
  [arXiv:1706.03762](https://arxiv.org/abs/1706.03762)
  The transformer architecture behind all current LLMs. Written by eight
  Google researchers for machine translation, it replaced word-by-word
  (recurrent) models with attention alone, which made training parallel
  and scalable. GPT, BERT, Claude, Gemini, Llama and AlphaFold 2 all build
  on it. Read sections 1–3 for the attention mechanism; Module 1
  (*What's inside?*) explains the background in plain language.
- **Devlin J, et al. (2019).** BERT: pre-training of deep bidirectional
  transformers for language understanding. *NAACL.*
  [arXiv:1810.04805](https://arxiv.org/abs/1810.04805)
  One of the first big successes of the transformer, for understanding
  rather than generating text; the basis of many biomedical text-mining
  tools.
- **Brown T, et al. (2020).** Language models are few-shot learners.
  *NeurIPS.* [arXiv:2005.14165](https://arxiv.org/abs/2005.14165)
  GPT-3; showed that in-context examples (few-shot prompting) change
  behaviour without retraining.
- **Kaplan J, et al. (2020).** Scaling laws for neural language models.
  [arXiv:2001.08361](https://arxiv.org/abs/2001.08361)
  Why bigger models and more data help, and why small local models lag on
  complex reasoning.

## Module 1 · How language models behave

- ★ **Liu NF, et al. (2024).** Lost in the middle: how language models use
  long contexts. *Transactions of the ACL* 12:157–173.
  [doi:10.1162/tacl_a_00638](https://doi.org/10.1162/tacl_a_00638) ·
  [arXiv:2307.03172](https://arxiv.org/abs/2307.03172)
  Evidence that information in the middle of long contexts is used less
  reliably. Basis for "bigger context ≠ better answers".
- ★ **Ji Z, et al. (2023).** Survey of hallucination in natural language
  generation. *ACM Computing Surveys* 55(12).
  [doi:10.1145/3571730](https://doi.org/10.1145/3571730) ·
  [arXiv:2202.03629](https://arxiv.org/abs/2202.03629)
  Taxonomy of hallucination types and mitigation strategies.
- **Bender EM, Gebru T, McMillan-Major A, Shmitchell S (2021).** On the
  dangers of stochastic parrots: can language models be too big?
  *FAccT '21.* [doi:10.1145/3442188.3445922](https://doi.org/10.1145/3442188.3445922)
  Critical perspective on data, cost and the limits of "understanding".
- ★ **Ouyang L, et al. (2022).** Training language models to follow
  instructions with human feedback. *NeurIPS.*
  [arXiv:2203.02155](https://arxiv.org/abs/2203.02155)
  The InstructGPT paper: instruction tuning plus RLHF, the recipe behind
  ChatGPT and the "post-training" step in Module 1, part 2.
- **Bai Y, et al. (2022).** Constitutional AI: harmlessness from AI
  feedback. [arXiv:2212.08073](https://arxiv.org/abs/2212.08073)
  Anthropic's approach of training with written principles and AI
  feedback instead of only human ratings.
- **Sharma M, et al. (2023).** Towards understanding sycophancy in language
  models. [arXiv:2310.13548](https://arxiv.org/abs/2310.13548)
  Why assistants tend to agree with you, even when you're wrong: a side
  effect of training on human preferences.

## Module 1 · Watermarks and detecting AI output

- ★ **Dathathri S, et al. (2024).** Scalable watermarking for identifying
  large language model outputs. *Nature* 634:818–823.
  [doi:10.1038/s41586-024-08025-4](https://doi.org/10.1038/s41586-024-08025-4)
  Google DeepMind's SynthID-Text, the method Claude's watermark is based
  on.
- **Kirchenbauer J, et al. (2023).** A watermark for large language
  models. *ICML.* [arXiv:2301.10226](https://arxiv.org/abs/2301.10226)
  The first widely used open text-watermarking method.
- **Kirchenbauer J, et al. (2023).** On the reliability of watermarks for
  large language models. [arXiv:2306.04634](https://arxiv.org/abs/2306.04634)
- **Sadasivan VS, et al. (2023).** Can AI-generated text be reliably
  detected? [arXiv:2303.11156](https://arxiv.org/abs/2303.11156)
  Shows how paraphrasing defeats both watermarks and detectors.
- ★ **Liang W, et al. (2023).** GPT detectors are biased against non-native
  English writers. *Patterns* 4(7).
  [doi:10.1016/j.patter.2023.100779](https://doi.org/10.1016/j.patter.2023.100779)
  Why you should never use "AI checkers" to judge someone's work.
- **Nemecek A, Chaudhary V, Ayday E (2026).** Watermarks without
  verification: AI text watermarking after the EU AI Act.
  [arXiv:2609.09604](https://arxiv.org/abs/2609.09604)
  A first look at the deployed systems, and why nobody can check them yet.
- **Watermark under Fire (2024).** A robustness evaluation of LLM watermarking.
  [arXiv:2411.13425](https://arxiv.org/abs/2411.13425)
  How well watermarks survive paraphrasing and other attacks.

### Current sources: watermarks and EU rules (checked 8 October 2026)

**Regulation**

- European Commission: [Code of Practice on Transparency of AI-Generated Content](https://digital-strategy.ec.europa.eu/en/policies/code-practice-ai-generated-content) and [news on its signatories](https://digital-strategy.ec.europa.eu/en/news/strong-backing-code-practice-transparency-ai-generated-content)
- [Article 50 of the EU AI Act](https://artificialintelligenceact.eu/article/50/) (AI Act Explorer)
- Morrison Foerster: [Organizations sign EU Code of Practice on AI transparency](https://www.mofo.com/resources/insights/260911-full-transparency-organizations-sign-eu-code) (Sept 2026)

**Companies (primary sources)**

- Anthropic: [How Claude's text watermarking works](https://www.anthropic.com/news/claude-text-watermark) and [How Claude marks AI-generated content](https://support.claude.com/en/articles/16266773-how-claude-marks-ai-generated-content)
- Google DeepMind: [SynthID](https://deepmind.google/models/synthid/); Hugging Face: [Introducing SynthID Text](https://huggingface.co/blog/synthid-text); Google: [Pixel and C2PA Content Credentials](https://blog.google/security/pixel-android-trusted-images-c2pa-content-credentials/)
- OpenAI: [Our approach to EU text provenance rules](https://openai.com/index/eu-text-provenance/), [Provenance signals in OpenAI-generated content](https://help.openai.com/en/articles/8912793-provenance-signals-in-openai-generated-content), [textGrain technical report](https://cdn.openai.com/pdf/e9508624-d767-41b6-a26d-e34ca798ada6/textgrain-entropy-calibrated-watermarking-for-language-model-text.pdf)
- Microsoft: [Content Credentials in Azure OpenAI](https://learn.microsoft.com/azure/ai-services/openai/concepts/content-credentials)
- C2PA: [OpenAI joins C2PA steering committee](https://www.businesswire.com/news/home/20240507424798/en/OpenAI-Joins-C2PA-Steering-Committee) (May 2024)

**Independent coverage**

- TechCrunch: [Anthropic says it will watermark text generated by its AI models](https://techcrunch.com/2026/08/11/anthropic-says-it-will-watermark-text-generated-by-its-ai-models/) (Aug 2026)
- BleepingComputer: [How Anthropic plans to watermark Claude's AI-generated text](https://www.bleepingcomputer.com/news/artificial-intelligence/how-anthropic-plans-to-watermark-claudes-ai-generated-text/)
- Maginative: [Meta releases Video Seal](https://www.maginative.com/article/meta-releases-video-seal-an-open-source-watermarking-tool-for-ai-video/); The Decoder: [Meta's "Imagined with AI" labels](https://the-decoder.com/meta-introduces-imagined-with-ai-labels-for-ai-generated-content-on-its-social-media-platforms/)

## Module 1 · The AI tools you'll meet

### Current sources: the AI tools (checked 8 October 2026)

**Official documentation**

- Microsoft Learn: [Enterprise data protection in Microsoft Copilot and Copilot Chat](https://learn.microsoft.com/en-us/copilot/microsoft-365/enterprise-data-protection) (updated August 2026)
- GitHub Docs: [Supported AI models in GitHub Copilot](https://docs.github.com/en/copilot/reference/ai-models/supported-models)
- Adobe: [Firefly, commercially safe](https://www.adobe.com/cc-shared/fragments/products/firefly/commercially-safe)
- Google DeepMind: [SynthID](https://deepmind.google/models/synthid/)
- Anthropic: [How Claude's text watermarking works](https://www.anthropic.com/news/claude-text-watermark)

**Journal policy**

- Nature Portfolio: [Editorial policy on artificial intelligence](https://www.nature.com/nature-portfolio/editorial-policies/ai); coverage: [The Decoder, "Nature bans AI images and videos"](https://the-decoder.com/nature-bans-ai-images-and-videos-citing-lack-of-transparency/)

**Comparisons and coverage (secondary; they don't always agree)**

- [TeamDay: Best AI models 2026](https://www.teamday.ai/blog/best-ai-models-2026)
- [Fello AI: Best AI models in October 2026](https://felloai.com/best-ai-models/)
- [Kingy AI: Frontier AI models compared](https://kingy.ai/blog/frontier-ai-models-gemini-4-argon-gpt-6-astra-sol-claude/)
- [TechTarget: Copilot Pro vs Copilot for Microsoft 365](https://www.techtarget.com/searchenterprisedesktop/tip/Comparing-Copilot-Pro-vs-Copilot-for-Microsoft-365)
- [PromptZone: Midjourney vs GPT Image 2 vs Flux 2](https://www.promptzone.com/tara_suzuki/best-ai-image-generator-in-2026-midjourney-vs-gpt-image-2-vs-flux-2-4ebn.md)
- [Maginative: Running OpenAI's open-weight gpt-oss models locally](https://www.maginative.com/article/how-to-run-openais-new-open-weight-gpt-oss-models-on-your-own-computer/)
- [Waimakers: Mistral AI and GDPR](https://www.waimakers.com/en/resources/gdpr-compliance/mistral-ai)
- [FreeAcademy: What NotebookLM is and why it is different](https://freeacademy.ai/lessons/what-is-notebooklm)

## Module 2 · Prompting and structured output

- ★ **Schulhoff S, et al. (2024).** The Prompt Report: a systematic survey of
  prompt engineering techniques.
  [arXiv:2406.06608](https://arxiv.org/abs/2406.06608)
  The map of the field: 58 text-prompting techniques and a shared vocabulary.
  Start here if you want to go deeper than the chapter.
- ★ **Sclar M, et al. (2023).** Quantifying language models' sensitivity to
  spurious features in prompt design. *ICLR 2024.*
  [arXiv:2310.11324](https://arxiv.org/abs/2310.11324)
  Formatting changes that keep the meaning can shift accuracy by up to 76
  points. Why the prompt is part of the method.
- **Lu Y, et al. (2022).** Fantastically ordered prompts and where to find
  them: overcoming few-shot prompt order sensitivity. *ACL.*
  [arXiv:2104.08786](https://arxiv.org/abs/2104.08786)
  The order of few-shot examples alone can make or break performance.
- **Zheng M, et al. (2024).** When "a helpful assistant" is not really
  helpful: personas in system prompts do not improve performances of large
  language models. *Findings of EMNLP.*
  [arXiv:2311.10054](https://arxiv.org/abs/2311.10054)
  162 personas, 2,410 questions: adding a role doesn't make answers more accurate.
- ★ **Wei J, et al. (2022).** Chain-of-thought prompting elicits reasoning
  in large language models. *NeurIPS.*
  [arXiv:2201.11903](https://arxiv.org/abs/2201.11903)
- **Kojima T, et al. (2022).** Large language models are zero-shot
  reasoners. *NeurIPS.* [arXiv:2205.11916](https://arxiv.org/abs/2205.11916)
  The "let's think step by step" effect.
- **Wang X, et al. (2023).** Self-consistency improves chain of thought
  reasoning in language models. *ICLR.*
  [arXiv:2203.11171](https://arxiv.org/abs/2203.11171)
  Sampling several answers and taking the majority; related to the
  consistency measurements in the Module 2 experiment.
- **Zhou D, et al. (2023).** Least-to-most prompting enables complex
  reasoning in large language models. *ICLR.*
  [arXiv:2205.10625](https://arxiv.org/abs/2205.10625)
  Break a problem into simpler sub-questions first; the idea behind prompt chaining.
- **Dhuliawala S, et al. (2023).** Chain-of-verification reduces
  hallucination in large language models.
  [arXiv:2309.11495](https://arxiv.org/abs/2309.11495)
  Draft, ask verification questions, answer them independently, revise.
- **Zhou Y, et al. (2023).** Large language models are human-level prompt
  engineers. *ICLR.* [arXiv:2211.01910](https://arxiv.org/abs/2211.01910)
  Automatic Prompt Engineer: letting a model search for better prompts.
- **Khattab O, et al. (2023).** DSPy: compiling declarative language model
  calls into self-improving pipelines.
  [arXiv:2310.03714](https://arxiv.org/abs/2310.03714)
  A framework that optimises prompts against a test set and a metric.
- ★ **Greshake K, et al. (2023).** Not what you've signed up for:
  compromising real-world LLM-integrated applications with indirect prompt
  injection. *AISec '23.* [arXiv:2302.12173](https://arxiv.org/abs/2302.12173)
  Why external documents are untrusted input.
- **DAIR.AI Prompt Engineering Guide.**
  [promptingguide.ai](https://www.promptingguide.ai/)
  Practical reference for techniques.

- **White J, et al. (2023).** A prompt pattern catalog to enhance prompt
  engineering with ChatGPT. *PLoP 2023.*
  [arXiv:2302.11382](https://arxiv.org/abs/2302.11382)
  Reusable prompting patterns, including the flipped interaction, where
  the model interviews you.
- **Yin Z, et al. (2024).** Should we respect LLMs? A cross-lingual study
  on the influence of prompt politeness on LLM performance.
  [arXiv:2402.14531](https://arxiv.org/abs/2402.14531)
  Rude prompts made answers worse; extra politeness didn't make them
  better.
- **Dobariya O, Kumar A (2025).** Mind your tone: investigating how prompt
  politeness affects LLM accuracy.
  [arXiv:2510.04950](https://arxiv.org/abs/2510.04950)
  On ChatGPT-4o, blunt prompts scored slightly higher than polite ones;
  one model and 50 questions.
- **Hong K, Troynikov A, Huber J (2025).** Context rot: how increasing input
  tokens impacts LLM performance. *Chroma technical report.*
  [research.trychroma.com/context-rot](https://research.trychroma.com/context-rot)
  Eighteen models get worse as the input grows, even on simple tasks.
  Written by a company that sells retrieval tools, so read it with that in
  mind.
- **Davis K, Mahmoud Q (2026).** Citation constraints and reference
  hallucinations in large language models. *PMLR* 318:464–475.
  [proceedings.mlr.press](https://proceedings.mlr.press/v318/davis26a.html)
  Stricter citation demands went with more invalid references.
- **The Transmitter.** Boost your writing with AI personas.
  [thetransmitter.org](https://www.thetransmitter.org/from-bench-to-bot/boost-your-writing-with-ai-personas/)
  Practical guide for scientists to getting feedback from AI readers.

### Current sources: dictation tools (checked 13 October 2026)

- Wispr Flow: [pricing and plans](https://wisprflow.ai/pricing) (official)
- [Zack Proser: Wispr Flow pricing guide 2026](https://zackproser.com/blog/wisprflow-pricing-guide-2026) (secondary)
- [Voibe: Wispr Flow pricing 2026](https://www.getvoibe.com/resources/wispr-flow-pricing/) (secondary; written by a competitor)

## Modules 3 and 5 · Reproducibility and research software

- ★ **van Kampen AHC, et al. (2024).** ENCORE: a practical implementation
  to improve reproducibility and transparency of computational research.
  *Nature Communications* 15.
  [doi:10.1038/s41467-024-52446-8](https://doi.org/10.1038/s41467-024-52446-8)
  The project structure audited by Themis.
- **Sandve GK, Nekrutenko A, Taylor J, Hovig E (2013).** Ten simple rules
  for reproducible computational research. *PLoS Comput Biol*
  9(10):e1003285. [doi:10.1371/journal.pcbi.1003285](https://doi.org/10.1371/journal.pcbi.1003285)
- **Wilson G, et al. (2017).** Good enough practices in scientific
  computing. *PLoS Comput Biol* 13(6):e1005510.
  [doi:10.1371/journal.pcbi.1005510](https://doi.org/10.1371/journal.pcbi.1005510)
- **Wilkinson MD, et al. (2016).** The FAIR Guiding Principles for
  scientific data management and stewardship. *Scientific Data* 3:160018.
  [doi:10.1038/sdata.2016.18](https://doi.org/10.1038/sdata.2016.18)

## Modules 4 and 5 · Tools, retrieval and agents

- ★ **Lewis P, et al. (2020).** Retrieval-augmented generation for
  knowledge-intensive NLP tasks. *NeurIPS.*
  [arXiv:2005.11401](https://arxiv.org/abs/2005.11401)
  The original RAG paper (Track B, D).
- ★ **Yao S, et al. (2023).** ReAct: synergizing reasoning and acting in
  language models. *ICLR.* [arXiv:2210.03629](https://arxiv.org/abs/2210.03629)
  The reason → act → observe loop that coding agents build on.
- **Schick T, et al. (2023).** Toolformer: language models can teach
  themselves to use tools. *NeurIPS.*
  [arXiv:2302.04761](https://arxiv.org/abs/2302.04761)
- **Jimenez CE, et al. (2024).** SWE-bench: can language models resolve
  real-world GitHub issues? *ICLR.*
  [arXiv:2310.06770](https://arxiv.org/abs/2310.06770)
  How coding agents are benchmarked; useful model for Track C evaluation.
- **Model Context Protocol specification.**
  [modelcontextprotocol.io](https://modelcontextprotocol.io)
- **Anthropic. Claude Code best practices.**
  [code.claude.com/docs/en/best-practices](https://code.claude.com/docs/en/best-practices)

## Biology and biomedicine (all modules, hackathon)

- ★ **Jumper J, et al. (2021).** Highly accurate protein structure
  prediction with AlphaFold. *Nature* 596:583–589.
  [doi:10.1038/s41586-021-03819-2](https://doi.org/10.1038/s41586-021-03819-2)
  AlphaFold 2: attention applied to amino acids (see the protein-shape
  example in Module 1, part 1).
- **Abramson J, et al. (2024).** Accurate structure prediction of
  biomolecular interactions with AlphaFold 3. *Nature* 630:493–500.
  [doi:10.1038/s41586-024-07487-w](https://doi.org/10.1038/s41586-024-07487-w)
  AlphaFold 3: a diffusion-based model for proteins together with DNA,
  RNA and small molecules.
- ★ **Walters WH, Wilder EI (2023).** Fabrication and errors in the
  bibliographic citations generated by ChatGPT. *Scientific Reports*
  13:14045. [doi:10.1038/s41598-023-41032-5](https://doi.org/10.1038/s41598-023-41032-5)
  Measured fabricated references; the model for the Module 1 experiment.
- **Singhal K, et al. (2023).** Large language models encode clinical
  knowledge. *Nature* 620:172–180.
  [doi:10.1038/s41586-023-06291-2](https://doi.org/10.1038/s41586-023-06291-2)
  Benchmarking LLMs on medical questions, including human evaluation of
  harms.
- **Jin Q, et al. (2024).** GeneGPT: augmenting large language models with
  domain tools for improved access to biomedical information.
  *Bioinformatics* 40(2).
  [doi:10.1093/bioinformatics/btae075](https://doi.org/10.1093/bioinformatics/btae075)
  LLMs calling NCBI APIs; tool use vs memory (Module 4 experiment).
- **Hou W, Ji Z (2024).** Assessing GPT-4 for cell type annotation in
  single-cell RNA-seq analysis. *Nature Methods* 21.
  [doi:10.1038/s41592-024-02235-4](https://doi.org/10.1038/s41592-024-02235-4)
  An example of evaluating LLM annotation against expert labels; read the
  evaluation design as much as the results.

## Policy, ethics and law

- **ICMJE.** Recommendations for the Conduct, Reporting, Editing, and
  Publication of Scholarly Work in Medical Journals (section on
  AI-assisted technology). [icmje.org](https://www.icmje.org)
  AI tools cannot be authors; use must be disclosed.
- **Nature Portfolio editorial policy on AI.**
  [nature.com/…/editorial-policies/ai](https://www.nature.com/nature-portfolio/editorial-policies/ai)
  Example of a journal policy on LLM use and AI-generated images.
- **Regulation (EU) 2024/1689 (EU AI Act).**
  [EUR-Lex](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
  Risk-based regulation of AI systems in the EU. Article 50
  (transparency and marking of AI output) applies from 2 August 2026; see
  Module 1, part 4.
- **European Commission (2026).** Code of Practice on Transparency of
  AI-Generated Content.
  [digital-strategy.ec.europa.eu](https://digital-strategy.ec.europa.eu/en/policies/code-practice-ai-generated-content)
- **Regulation (EU) 2016/679 (GDPR)**, in particular Art. 9 (special
  categories, including health and genetic data).
  [EUR-Lex](https://eur-lex.europa.eu/eli/reg/2016/679/oj)
- Your institution's research data management and AI-use policy (ask your
  data steward or DPO for the current version).
