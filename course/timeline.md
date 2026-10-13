# Timeline: how we got here

The course tells a lot of small history stories, scattered over the
modules. Here they are in one line, from the first ideas to the tools we
use today. Each event says where the course talks about it, and links to a
source, so you can check it yourself.

## 1. The early ideas (1948–1979)

### 1948 · Predicting the next word, by hand

Claude Shannon, the founder of information theory, generates "English" by
picking each next word based on the word before it, using an ordinary book.
The result reads like English and means nothing. The recipe behind today's
language models, seventy years early.

*In the course:* Module 1, *How does it write?*

*Source:* [A Mathematical Theory of Communication (Wikipedia)](https://en.wikipedia.org/wiki/A_Mathematical_Theory_of_Communication)

### 1955 · The name "artificial intelligence"

John McCarthy and three colleagues propose a summer workshop at Dartmouth
College, held in 1956, with the starting idea that every aspect of learning
and intelligence could be described precisely enough for a machine to
simulate it.

*In the course:* Module 1, *What do we mean by "AI"?*

*Source:* [the 1955 proposal](http://jmc.stanford.edu/articles/dartmouth/dartmouth.pdf) · [Dartmouth workshop (Wikipedia)](https://en.wikipedia.org/wiki/Dartmouth_workshop)

### 1958 · The perceptron

The psychologist Frank Rosenblatt builds a single artificial neuron that
can learn simple patterns. The New York Times reports the US Navy's
expectation that such machines will one day walk, talk and even be
conscious. They didn't.

*In the course:* Module 1, *How we got here*

*Source:* [Perceptron (Wikipedia)](https://en.wikipedia.org/wiki/Perceptron)

### 1966 · ELIZA, the first chatbot

Joseph Weizenbaum's tiny program plays a therapist by turning your
sentences into questions. It understands nothing, yet people confide in
it, including his own secretary.

*In the course:* Module 1, *What is it good and bad at?* (the myths)

*Source:* [ELIZA (Wikipedia)](https://en.wikipedia.org/wiki/ELIZA)

### Around 1970 · "Intelligence is whatever machines haven't done yet"

Larry Tesler's remark, usually misquoted as "AI is whatever hasn't been
done yet", names the *AI effect*: once a computer can do something, we
stop calling it AI.

*In the course:* Module 1, *What do we mean by "AI"?*

*Source:* [AI effect (Wikipedia)](https://en.wikipedia.org/wiki/AI_effect) · [Larry Tesler (Wikipedia)](https://en.wikipedia.org/wiki/Larry_Tesler)

### 1970s · MYCIN and the first AI winter

At Stanford, the expert system MYCIN uses about 600 hand-written rules to
suggest antibiotics, about as well as specialists, but is never used in
hospitals. Promises outrun results, and funding dries up: the first *AI
winter*.

*In the course:* Module 1, *How we got here*

*Source:* [Mycin (Wikipedia)](https://en.wikipedia.org/wiki/Mycin) · [AI winter (Wikipedia)](https://en.wikipedia.org/wiki/AI_winter)

### 1978 · Good Laboratory Practice

After labs such as Industrial Bio-Test Laboratories turned out to have
badly run or invented safety studies, the US FDA introduces Good Laboratory
Practice: write down how the work is done, follow it, keep records. The
ancestor of every instruction file for AI.

*In the course:* Module 3, *Why does chat knowledge evaporate?*

*Source:* [Good laboratory practice (Wikipedia)](https://en.wikipedia.org/wiki/Good_laboratory_practice) · [Industrial Bio-Test Laboratories (Wikipedia)](https://en.wikipedia.org/wiki/Industrial_Bio-Test_Laboratories)

## 2. Learning from data (1980–2011)

### 1986 · Backpropagation

David Rumelhart, Geoffrey Hinton and Ronald Williams show in *Nature* how
to train neural networks with several layers. It is still how every model
in this course is trained.

*In the course:* Module 1, *How we got here* and *How did it learn?*

*Source:* [the original paper](https://doi.org/10.1038/323533a0) · [Backpropagation (Wikipedia)](https://en.wikipedia.org/wiki/Backpropagation)

### Late 1980s · The second AI winter

Expert systems prove expensive to build and maintain, and interest and
funding collapse a second time.

*In the course:* Module 1, *How we got here*

*Source:* [AI winter (Wikipedia)](https://en.wikipedia.org/wiki/AI_winter)

### 1994 · Byte-pair encoding

A trick for compressing computer files, merging the most frequent pairs of
characters. Around 2016 it is borrowed to build the token vocabularies of
language models.

*In the course:* Module 1, *How does it write?*

*Source:* [Byte pair encoding (Wikipedia)](https://en.wikipedia.org/wiki/Byte_pair_encoding)

### 1995 · AI as the study of agents

Stuart Russell and Peter Norvig's textbook defines AI as building agents
that perceive their surroundings and act on them; it becomes the most
widely used AI textbook.

*In the course:* Module 1, *What do we mean by "AI"?*, and Module 5

*Source:* [Artificial Intelligence: A Modern Approach (Wikipedia)](https://en.wikipedia.org/wiki/Artificial_Intelligence:_A_Modern_Approach)

### 1996 · USB

One plug replaces a tangle of device-specific ports, the comparison
everyone uses for MCP today.

*In the course:* Module 4, *What does MCP add?*

*Source:* [USB (Wikipedia)](https://en.wikipedia.org/wiki/USB)

### 1997 · Deep Blue beats Kasparov

IBM's chess computer beats the world champion. A few years later, nobody
calls a chess program "AI" any more.

*In the course:* Module 1, *What do we mean by "AI"?*

*Source:* [Deep Blue versus Garry Kasparov (Wikipedia)](https://en.wikipedia.org/wiki/Deep_Blue_versus_Garry_Kasparov)

### 1999 · The first hackathons

The word "hackathon" is first used, at events by the OpenBSD developers and
by Sun Microsystems.

*In the course:* Module 6, *How the hackathon brings the course together*

*Source:* [Hackathon (Wikipedia)](https://en.wikipedia.org/wiki/Hackathon)

### 2007 · Seventy definitions of intelligence

Shane Legg and Marcus Hutter collect about seventy published definitions of
intelligence, a good illustration of why "AI" has no single definition.

*In the course:* Module 1, *What do we mean by "AI"?*

*Source:* [Legg & Hutter 2007 (arXiv)](https://arxiv.org/abs/0706.3639)

## 3. Deep learning takes off (2012–2021)

### 2012 · AlexNet

A deep neural network trained on two gaming graphics cards recognises
objects in photos far better than anything before it. Lots of data, cheap
computing power and better training methods come together, and the
deep-learning boom begins.

*In the course:* Module 1, *How we got here*

*Source:* [the original paper (Krizhevsky, Sutskever & Hinton 2012)](https://papers.nips.cc/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html) · [AlexNet (Wikipedia)](https://en.wikipedia.org/wiki/AlexNet)

### 2017 · The transformer

Eight Google researchers publish *Attention Is All You Need*, the
architecture inside every language model in this course.

*In the course:* Module 1, *What's inside?*

*Source:* [the original paper (arXiv)](https://arxiv.org/abs/1706.03762) · [Attention Is All You Need (Wikipedia)](https://en.wikipedia.org/wiki/Attention_Is_All_You_Need)

### 2020 · GPT-3 and in-context learning

OpenAI shows that a large enough language model can do a new task from a
description and a few examples in the prompt, without retraining. The
prompt becomes the way to "program" a model.

*In the course:* Module 1, *How did it learn?*, and Module 2, *Where did prompt engineering come from?*

*Source:* [Brown et al. 2020 (arXiv)](https://arxiv.org/abs/2005.14165) · [GPT-3 (Wikipedia)](https://en.wikipedia.org/wiki/GPT-3)

### 2020 · AlphaFold 2 solves protein folding

DeepMind's AlphaFold 2 wins the CASP protein-structure competition by a wide
margin, solving a fifty-year-old problem in biology.

*In the course:* Module 1, *Does it predict or create?*

*Source:* [AlphaFold (Wikipedia)](https://en.wikipedia.org/wiki/AlphaFold) · [CASP (Wikipedia)](https://en.wikipedia.org/wiki/CASP)

## 4. Language models for everyone (2022–today)

### September 2022 · Prompt injection gets its name

Riley Goodside shows that GPT-3 obeys instructions hidden in text it was
asked to translate; Simon Willison names the problem *prompt injection*.

*In the course:* Module 2, *How do I keep it honest?*

*Source:* [Willison 2022](https://simonwillison.net/2022/Sep/12/prompt-injection/) · [Prompt injection (Wikipedia)](https://en.wikipedia.org/wiki/Prompt_injection)

### 30 November 2022 · ChatGPT

A post-trained language model in a simple chat window. Within about two
months it has an estimated 100 million users, at the time the
fastest-growing consumer app ever.

*In the course:* Module 1, *How did it learn?*

*Source:* [ChatGPT (Wikipedia)](https://en.wikipedia.org/wiki/ChatGPT)

### Spring 2023 · AutoGPT and the first agent hype

Hobby projects wire GPT-4 into a loop and promise assistants that run whole
projects on their own. They mostly go round in circles, and the hype fades.

*In the course:* Module 5, *How is an agent different from a chatbot?*

*Source:* [AutoGPT (Wikipedia)](https://en.wikipedia.org/wiki/AutoGPT)

### Spring 2023 · The Samsung leak

Engineers paste confidential source code into ChatGPT; Samsung can't take
it back and temporarily bans generative AI tools. Many organisations write
their first AI policies around this time.

*In the course:* Module 1, *Where does my data go?*

*Source:* [CSO Online, 2023](https://www.csoonline.com/article/3695170/samsung-bans-staff-ai-use-over-data-leak-concerns.html)

### 2023 · Plugins and function calling

OpenAI lets ChatGPT use plugins (March) and gives developers function
calling (June); every company builds its own incompatible variant.

*In the course:* Module 4, *What does MCP add?*

*Source:* [OpenAI, June 2023](https://openai.com/index/function-calling-and-other-api-updates)

### 2024 · Nobel Prizes for AI

Geoffrey Hinton (with John Hopfield) receives the Nobel Prize in Physics for
the foundations of neural networks; Demis Hassabis and John Jumper share the
Nobel Prize in Chemistry for AlphaFold (with David Baker, for protein design).

*In the course:* Module 1, *How we got here* and *Does it predict or create?*

*Source:* [Physics 2024](https://www.nobelprize.org/prizes/physics/2024/summary/) · [Chemistry 2024](https://www.nobelprize.org/prizes/chemistry/2024/summary/)

### 2024 · The EU AI Act

The European Union adopts the first broad law on AI, with a definition of
an "AI system" that closely follows the OECD's.

*In the course:* Module 1, *What do we mean by "AI"?* and *Can you tell what AI made?*

*Source:* [the regulation (EUR-Lex)](https://eur-lex.europa.eu/eli/reg/2024/1689/oj) · [Artificial Intelligence Act (Wikipedia)](https://en.wikipedia.org/wiki/Artificial_Intelligence_Act)

### November 2024 · The Model Context Protocol

Anthropic publishes MCP as an open standard for connecting AI tools to data
and services. Within a year OpenAI, Google and Microsoft adopt it, and in
December 2025 it moves to an independent foundation.

*In the course:* Module 4, *What does MCP add?*

*Source:* [Model Context Protocol (Wikipedia)](https://en.wikipedia.org/wiki/Model_Context_Protocol) · [MCP joins the Agentic AI Foundation](https://blog.modelcontextprotocol.io/posts/2025-12-09-mcp-joins-agentic-ai-foundation/)

### 2025 · Coding agents become everyday tools

Models are now reliable enough at each small step for agents such as
Claude Code to work inside real projects, with a person approving what
they change.

*In the course:* Module 5, *How is an agent different from a chatbot?*

### 2 August 2026 · AI output gets marked

The transparency rules of the EU AI Act apply: providers of generative AI
must mark their output in a machine-readable way, and Claude, Gemini and
(in the EU) ChatGPT text starts carrying invisible watermarks.

*In the course:* Module 1, *Can you tell what AI made?*

*Source:* [the regulation, Article 50 (EUR-Lex)](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
