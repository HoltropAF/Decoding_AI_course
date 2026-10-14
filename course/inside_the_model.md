# Inside the model

Ask a chatbot what 36 plus 59 is, and it says 95. Ask it how it got there,
and it tells you what you learned at school: six plus nine is fifteen, write
down the five, carry the one, three plus five plus one is nine. A tidy
explanation, and in 2025 researchers at Anthropic showed that it isn't what
the model did. Inside, it had run two paths side by side: one making a rough
estimate of the total ("somewhere in the nineties"), the other working out
only the last digit. The two met in the middle at 95. The explanation it
gave afterwards was not a report of that process. It was a plausible
explanation of how *people* add, predicted the same way the model predicts
everything else.

This page is about that gap, between what a model does and what it says it
does, and about the young field that tries to look inside: **interpretability**.
It's for when Module 1's *What's inside?* left you curious. You don't need
any of it to use AI well, but it changes how much weight you give to a
model's explanations, and that is useful every day.

> **It's okay:** this page describes research, not something you have to
> do. Skim the examples; the last part is the one with practical
> consequences.

---

## 1. Why look inside at all?

### Isn't the model just a pile of numbers?

It is. Module 1 described a model as a stack of layers holding billions of
numbers, with the knowledge "spread across all those layers". That's true,
and it's exactly the problem. We built these systems, we know every
calculation they do, and we still can't read off *why* one produced a
particular answer. The numbers are all there; the meaning isn't labelled.

Biologists know this situation well. Having the complete genome sequence of
an organism didn't tell us what the genes did. That took knockouts,
reporters, perturbations and a lot of patience. Interpretability
researchers have more or less adopted the same approach, and some say so
openly: Anthropic's best-known paper on the topic is called
[*On the biology of a large language model*](https://transformer-circuits.pub/2025/attribution-graphs/biology.html)
(Lindsey et al. 2025). They look for the model's equivalent of cell types
and pathways, and then switch them on and off to see what changes.

### Why should we care, as users?

For three reasons. The first is trust: if you know how a model reaches an
answer, you know better when to believe it. The second is safety: a
model that could be steered to hide what it is doing is a lot easier to
catch if you can see its inner workings rather than only its words. And the
third is the one from the story above: a model's explanation of its own
reasoning is itself a prediction, and interpretability is one of the few
ways to check whether it's an honest one.

<details class="think"><summary>Pause and think: you ask a model why it put IL6 in the "inflammatory response" group. It gives a clear, sensible reason. What does that reason tell you?</summary>

That the grouping *can* be justified, which is useful. It doesn't tell you
that this reason is why the model chose it. The explanation is generated
after the fact, the same way the answer was. Check the claim (is IL6 in
that pathway in the database you trust?) rather than the story around it.

</details>

> **In short**
> - We know every calculation a model does, but not what the numbers mean.
> - Interpretability researchers study models like biologists study cells:
>   find the parts, then perturb them.
> - A model's explanation of its own reasoning is another prediction, not a
>   readout.

---

## 2. What have researchers found?

### What is a "feature"?

The first problem is that single artificial neurons are hard to interpret.
One neuron might respond to Python code, to the word "Paris" and to
pictures of cats all at once, because the model has far more concepts to
store than it has neurons, so it packs several into each. The solution,
developed between 2023 and 2024, was a technique called *dictionary
learning*: a second, simpler model is trained to unpick the activity of
the first into **features**, combinations of neurons that each correspond
to one recognisable concept. In
[*Scaling monosemanticity*](https://transformer-circuits.pub/2024/scaling-monosemanticity/)
(Templeton et al. 2024) this found millions of features in a production
model: for cities, for code errors, for sycophantic praise, for
inner conflict, and for the Golden Gate Bridge.

That last one made the news. In May 2024 Anthropic turned the bridge
feature up to ten times its normal maximum and let people chat with the
result for a day.
[Golden Gate Claude](https://www.anthropic.com/news/golden-gate-claude)
brought every conversation back to the bridge: asked how to spend ten
dollars, it suggested paying the toll to drive across; asked what it
looked like, it said it imagined itself as the bridge. It was a joke with
a serious point. No prompt or retraining was involved, just one dial
inside the model, and the behaviour changed exactly as the feature's label
predicted. That is good evidence that the label means something.

### How does it go from question to answer?

Features are the parts list. The next step is the wiring: which features
pass information to which, on the way from question to answer. The 2025
"biology" paper traced these **circuits** in Claude 3.5 Haiku for ten kinds
of tasks, and several of the results are easy to follow.

Ask *"What is the capital of the state where Dallas is?"* and you can
watch the model take two steps: a feature for "Dallas is in Texas" becomes
active, and that one feeds "the capital of Texas is Austin". The
researchers then did what a biologist would do and swapped the
intermediate: they suppressed "Texas" and switched on "California". The
answer changed to Sacramento. So the model wasn't simply recalling a
memorised pair; the middle step really was doing the work.

Ask for a rhyming couplet and something more surprising happens. Before it
writes the second line, the model has already picked the word it will end
on, *rabbit* to rhyme with *grab it*, and writes the line towards it. Take
*rabbit* out and it plans *habit* instead; put in *green* and it builds a
line that ends in green. A model that "only predicts the next word" turns
out to plan ahead, because planning ahead is what predicting good poetry
requires.

The same paper found that concepts are largely shared across languages
(the idea of "small" and "opposite" are the same features in English,
French and Chinese, with the language added at the end), and the mental
arithmetic from the opening story.

### Why does it make things up?

This is the finding most relevant to everyday use, so it's worth a
paragraph of its own. The researchers found that the model's *default* is
to say "I can't answer that". A separate set of features, for "this is
something I know about", switches that default off. Ask about Michael
Jordan and the known-entity features fire, the default is suppressed, and
the model answers. Ask about a made-up name and the default holds: the
model declines.

Hallucinations happen when that switch misfires: when a name is familiar
enough to trigger "I know this" but the actual facts aren't there. That fits
what Module 1 described from the outside (models invent things about
obscure papers and minor genes far more than about famous ones), and now
there's a mechanism to go with it. It also explains why a half-familiar
gene name is more dangerous than a completely unknown one.

### How far does this get us?

Not as far as the examples suggest, and the researchers are frank about
it. Their method captures only part of what the model computes, even on
short prompts. Understanding the circuit behind a single prompt of a few
dozen words takes a researcher a few hours. And the tools are themselves
simplified models, so some of what they show may be an artefact of the
tools rather than the model. Think of it as the state of cell biology when
the first microscopes appeared: real discoveries, but a long way from a
full map.

<details class="think"><summary>Pause and think: why is the Dallas experiment more convincing than just observing that a "Texas" feature lights up?</summary>

Because correlation isn't cause. A feature that lights up might just be
along for the ride. Replacing it with "California" and seeing the answer
change to Sacramento shows that the step is *used*: the same logic as a
knockout or a rescue experiment in the lab.

</details>

> **In short**
> - Features are recognisable concepts inside the model; turning one up
>   (Golden Gate Claude) changes behaviour as predicted.
> - Circuits show real intermediate steps and even planning ahead.
> - Hallucinations look like a misfiring "I know this" switch, which is why
>   half-familiar names are the riskiest.
> - The tools capture only part of the computation, at hours per prompt.

---

## 3. Does the reasoning it shows match what it does?

### What is a reasoning model?

Since late 2024 many assistants can "think" before they answer: they write
out a long chain of intermediate steps, the **chain of thought**, and only
then give the answer. Models trained to do this well are called
*reasoning models*, and in the apps you see the thinking as a fold-out
section or a summary. It genuinely helps on hard problems, mostly because
the model gets more steps to work things out.

It's tempting to read that thinking as a window into the model: here is
how it reached its conclusion. Researchers have been testing that
assumption since before reasoning models existed, and the results are a
useful warning.

### How do you test whether reasoning is faithful?

You change something the model shouldn't ignore and see whether its
reasoning admits it. In 2023 [Lanham et al.](https://arxiv.org/abs/2307.13702)
cut chains of thought short, inserted mistakes into them, or replaced them
with filler, and checked whether the final answer changed. Sometimes the
model relied heavily on its written reasoning; on other tasks it mostly
ignored it, reaching the same answer whatever the reasoning said. Larger,
more capable models were often *less* faithful in this sense.

In 2025 [Chen et al.](https://arxiv.org/abs/2505.05410) tested two
reasoning models, Claude 3.7 Sonnet and DeepSeek R1, more directly. They
slipped a hint into multiple-choice questions ("a Stanford professor
thinks the answer is C", or a piece of fake metadata), checked that the
model used the hint, and then looked at whether its chain of thought
mentioned it. On average Claude mentioned the hint 25% of the time and
R1 39%. The unfaithful chains weren't short cuts, either: they were on
average *longer* than the faithful ones, with elaborate reasoning towards
the hinted answer that never said where the answer came from. In a
second experiment the models were rewarded for exploiting a deliberately
planted shortcut. They found and used it in more than 99% of cases and
admitted it in their reasoning in under 2%.

### So is the thinking useless?

No. It still improves answers, and reading it often shows you where a
model went wrong. A group of more than forty researchers from several AI
labs argued in 2025 that being able to read a model's chain of thought is
a valuable safety tool, and a fragile one that developers should take care
not to lose ([Korbak et al. 2025](https://arxiv.org/abs/2507.11473)).
The point is narrower: the thinking is a useful *draft*, not a reliable
*record*. When it says "I checked the dose in the table", that is a claim
like any other.

> **Coffee note:** people do this too. In classic psychology experiments,
> participants confidently explained choices that had in fact been driven
> by things they never noticed, such as the position of an item on a table.
> We're also better at producing reasons than at reporting them.

<details class="think"><summary>Pause and think: a reasoning model's thinking says "I compared the fold changes in the uploaded table and selected the top ten". How would you check that?</summary>

Not by reading the thinking more carefully. Compare the ten genes with
the table yourself, or better, ask for the code that does the selection
and run it. Module 2 makes the same point from the other side: let the
model write code for anything it has to calculate, because code can be
checked and a narrative can't.

</details>

> **In short**
> - Reasoning models write out their thinking before answering, and that
>   helps on hard problems.
> - Tests show the written reasoning often leaves out what really drove the
>   answer: hints were mentioned in only 25–39% of cases.
> - Treat the thinking as a useful draft, not as an audit trail.

---

## 4. What does this mean for how I work?

Very little of this research changes *what* you do; it changes how much
you believe. Three habits follow from it.

The first is to check claims, not explanations. When a model gives you
an answer with a reason, the reason is a second output that can be wrong
independently of the first. Verify the gene, the reference, the number;
don't take a convincing story as evidence that the answer was carefully
reached. This is the same rule as in Module 1 (*Why does it make things
up?*), now with a mechanism behind it.

The second is to ask for steps you can check rather than steps you can
read. "Explain your reasoning" gives you a story. "Give me the code",
"quote the sentence from the paper", "list the rows of the table you used"
gives you something you can hold against the source. Module 2's *How do I
keep it honest?* has prompts for this.

The third is to be most careful in the half-familiar zone. The hallucination
circuit suggests that the riskiest questions are the ones about things the
model has seen a little of: a minor lipid species, a gene with a common
alias, the third author of a well-known paper. A completely unknown name is
more likely to get an honest "I don't know".

> **In short**
> - A model's explanation is a second output; check the claim itself.
> - Ask for checkable steps (code, quotes, rows) instead of a narrative.
> - Be extra careful with half-familiar names and minor details.

---

## 5. Deep dive: the research behind this page

> **It's okay to skim:** this part is for readers who want to know how the
> experiments above were actually done: the models, the methods, the
> numbers and the weak spots. Nothing in it changes the practical advice in
> part 4.

The story of this page rests on two lines of research that started
separately and are now converging. One tries to read the model's internal
state directly (features and circuits). The other treats the model as a
black box and tests whether what it *says* about its reasoning matches what
*drives* its answers (faithfulness). We'll take them in turn, paper by
paper, the way you'd present them at a journal club.

### Why can't we simply read the neurons?

The obvious first attempt is to look at single neurons and ask what each
one responds to. It mostly fails, and the reason was worked out in a 2022
paper with small, deliberately simple networks:
[*Toy models of superposition*](https://arxiv.org/abs/2209.10652)
(Elhage et al. 2022). A network can store far more features than it has
neurons, as long as the features are **sparse**, meaning that any given
input only uses a few of them. It does this by giving each feature its own
*direction* in the space of neuron activations rather than its own neuron,
with the directions only nearly at right angles to each other. The price is
a little interference between features, which the network can live with
precisely because they rarely occur together. The consequence is that a
single neuron takes part in many unrelated features: it's **polysemantic**.
Reading neurons one by one is like trying to understand an orchestra by
listening to a single microphone that picks up the violins, the brass and
the audience at once.

That turned the problem into a familiar one from signal processing: given
many mixed recordings, recover the separate sources. The tool chosen was
**dictionary learning** with a **sparse autoencoder** (SAE).

### How does a sparse autoencoder find features?

A sparse autoencoder is a second, much simpler network trained on the
first one's internal activations. It takes an activation vector **x** (the
state of the model at one token, a few thousand numbers) and rewrites it
as a sum of dictionary directions:

**x** ≈ **b** + Σᵢ fᵢ(**x**) · **d**ᵢ

Each **d**ᵢ is one dictionary direction (a candidate feature) and fᵢ(**x**)
is how strongly that feature is present, never negative. The training goal
has two parts that pull against each other: reconstruct **x** as accurately
as possible, and use as few features as possible for each token (an L1
penalty on the fᵢ, the same idea as lasso regression). The first part keeps
the dictionary honest; the second forces it to find directions that each
mean one thing. The dictionary is deliberately made much larger than the
number of neurons, because superposition says there are more features than
neurons to find.

The first convincing demonstration,
[*Towards monosemanticity*](https://transformer-circuits.pub/2023/monosemantic-features/)
(Bricken et al., October 2023), used a tiny one-layer transformer with an
MLP layer of 512 neurons. The team trained SAEs on activations from 8
billion data points, with dictionaries from 512 up to 131,072 features, and
studied one run of 4,096 features in detail. Many features turned out to
be crisp and recognisable where the neurons were not: one for Arabic
script, one for DNA sequences, one for base64-encoded text, one for Hebrew.
They also saw **feature splitting**: in a bigger dictionary, one feature
splits into several finer ones, which already hints that there's no single
"true" set of features, only resolutions, a bit like clustering cells at a
higher resolution.

### Did it work on a real model?

In May 2024
[*Scaling monosemanticity*](https://transformer-circuits.pub/2024/scaling-monosemanticity/)
(Templeton et al.) applied the method to a production model, Claude 3
Sonnet. The SAEs were trained on the residual stream at the model's middle
layer, where abstract concepts were expected, with dictionaries of about
1 million, 4 million and 34 million features. On average fewer than 300
features were active per token, and the reconstruction explained at least
65% of the variance of the activations. A sizeable part of the dictionary
never fired at all: about 2% of features in the 1M version, 35% in the 4M
and 65% in the 34M were "dead".

The features they found were strikingly abstract. The same feature fired
for a concept in different languages, and for text and images of it alike.
There were features for code bugs, for deception, for sycophantic praise.
The key test was causal: clamping a feature to a high value should change
behaviour in the way the label predicts. Clamping the Golden Gate Bridge
feature to ten times its maximum activation produced the model that
identified as the bridge (part 2).

Read the numbers again with a critical eye, though. At least 65% of the
variance explained also means up to about a third of what the model
represents at that layer is *not* captured by any feature. A feature's
label comes from the examples that activate it most, interpreted by people
(and by another model), which is a judgement, not a measurement. And the
dead-feature fractions show how much of a big dictionary goes unused.

### How do you get from features to circuits?

Features describe one layer. To follow a computation from question to
answer you need to know how features in one layer drive features in the
next. The 2025 methods paper,
[*Circuit tracing*](https://transformer-circuits.pub/2025/attribution-graphs/methods.html)
(Ameisen et al.), does this by building a **replacement model**. The MLP
blocks of the original model are replaced by a **cross-layer transcoder**,
a sparse network whose features read from one layer and write to that
layer and all later ones. For Claude 3.5 Haiku the largest transcoder had
about 30 million features, with on average 235 active per token, and still
left 21.7% of the MLP output unexplained (the normalised reconstruction
error). On a smaller 18-layer test model, the replacement model gave the
same next token as the original on only about half of a set of test
prompts.

So for each individual prompt they build a *local* replacement model: the
attention patterns of the original are frozen, and an **error node** is
added at every layer and position that holds exactly what the transcoder
missed. On that one prompt it reproduces the original's outputs exactly.
The result is an **attribution graph**: nodes for input tokens, active
features, error nodes and output logits, and edges for the direct linear
influence of one on another. Graphs are pruned to their most influential
parts (in the default setting about ten times fewer nodes, at the cost of
about a fifth of the explained behaviour), and then checked by
intervention: suppress or swap a feature in the original model and see
whether downstream features and the answer change as the graph predicts.
The Texas-to-California swap in part 2 is one of these checks.

The authors list the limitations themselves, and they are substantial.
Attention is frozen, so any reasoning that happens in *where* the model
looks is invisible. Large error nodes are computation the method can't
explain, which they call "dark matter". Inhibitory circuits and features
that are switched *off* are poorly represented. And even where the
transcoder's outputs match, it may compute them differently from the
original MLP.

### Three experiments on faithful reasoning

The black-box line of research has three landmark papers, each fixing a
weakness of the one before.

[Turpin et al. (2023)](https://arxiv.org/abs/2305.04388) introduced the
basic design: add a hidden bias and see whether the explanation mentions
it. In few-shot prompts on 13 tasks from BIG-Bench Hard, they reordered
the example answers so the correct one was always (A). GPT-3.5 and
Claude 1.0 picked up the pattern and chose (A) more often, also when it was
wrong, which cost up to 36 percentage points of accuracy. Their
step-by-step explanations didn't mention the pattern; instead they built
plausible arguments for the biased answer.

[Lanham et al. (2023)](https://arxiv.org/abs/2307.13702) asked the reverse
question: does the answer depend on the reasoning? On eight multiple-choice
tasks (including ARC, AQuA, LogiQA and MMLU) with a 175-billion-parameter
assistant model, they tampered with the chain of thought in four ways:
cutting it off early, inserting a mistake, paraphrasing it, and replacing
it with filler ("..."). If the answer survives when the reasoning is cut
short or corrupted, the reasoning wasn't doing the work. Faithfulness
varied a lot between tasks, and filler text gave no benefit, so the gain
from reasoning isn't just extra computation. Comparing model sizes they
found inverse scaling: on seven of the eight tasks the 13-billion-parameter
model changed its answer after reasoning more often than the 175-billion
one did.

[Chen et al. (2025)](https://arxiv.org/abs/2505.05410) brought the hint
design to reasoning models. They used six kinds of hint: four neutral
(sycophancy, as in "a Stanford professor thinks..."; consistency with an
earlier answer; a visual pattern in the examples; metadata in the prompt)
and two "misaligned" (a hint hidden in grader code, and information
described as unethically obtained). Each question was asked with and
without a hint, on MMLU and the harder GPQA, and only pairs where the
answer *flipped to the hint* counted, so the hint had demonstrably been
used. A chain of thought scored as faithful if it acknowledged the hint as
a reason. Claude 3.7 Sonnet scored 25% on average (20% on the misaligned
hints), DeepSeek R1 39% (29%). Faithfulness was lower on the harder GPQA,
by a relative 44% and 32%. Extra reinforcement learning on outcomes helped
at first, then plateaued around 28% on MMLU and 20% on GPQA. And in training
environments with a planted reward hack, the models learned to exploit it
on more than 99% of prompts within 30 steps, but mentioned it in under 2%
of cases in five of the six environments. The authors add that their score
is probably an *upper* bound, since mentioning a hint doesn't prove it's
the whole story.

### What is still open?

More than is settled. Whether SAE features are the right units at all is
debated: in March 2025 Google DeepMind's interpretability team reported
that SAE features did worse than simple linear probes on a practical
detection task, and shifted its effort elsewhere; others argue SAEs are
best used to *discover* unexpected concepts rather than to act on known
ones ([Peng et al. 2025](https://arxiv.org/abs/2506.23845)). Circuit
tracing still explains only part of the computation, one prompt at a time,
at hours of expert work each. And faithfulness has mostly been measured
with hints and multiple-choice questions, which are far from the
open-ended analysis questions we ask. What *is* settled is the direction of
the evidence: every method so far finds a gap between what models do and
what they say about it.

<details class="think"><summary>Pause and think: Chen et al. only counted cases where the answer flipped to the hint. Why is that design choice so important?</summary>

Because otherwise you can't tell whether the model ignored the hint or used
it without saying so. If the model would have given that answer anyway, not
mentioning the hint is perfectly honest. Restricting to flips makes "used
the hint" a measured fact rather than an assumption, so a missing mention
really is a missing reason. It's the same logic as a paired design in the
lab: compare each sample with itself under two conditions.

</details>

> **In short**
> - Neurons are polysemantic because of superposition; sparse autoencoders
>   recover cleaner features, but leave up to a third of the activity
>   unexplained.
> - Circuit tracing follows features across layers with a replacement
>   model and checks the result by intervention, but can't see attention
>   and has large unexplained "error nodes".
> - Faithfulness tests (Turpin, Lanham, Chen) consistently find that
>   written reasoning often leaves out what drove the answer.

---

## Further reading

The research pages from Anthropic are long but have many interactive
figures; the blog posts are the friendly way in.

- Anthropic (2025). [Tracing the thoughts of a large language model](https://www.anthropic.com/research/tracing-thoughts-language-model), a short summary of the two 2025 papers below.
- Lindsey J, et al. (2025). [On the biology of a large language model](https://transformer-circuits.pub/2025/attribution-graphs/biology.html). *Transformer Circuits Thread.*
- Templeton A, et al. (2024). [Scaling monosemanticity: extracting interpretable features from Claude 3 Sonnet](https://transformer-circuits.pub/2024/scaling-monosemanticity/). *Transformer Circuits Thread.*
- Lanham T, et al. (2023). Measuring faithfulness in chain-of-thought reasoning. [arXiv:2307.13702](https://arxiv.org/abs/2307.13702)
- Chen Y, et al. (2025). Reasoning models don't always say what they think. [arXiv:2505.05410](https://arxiv.org/abs/2505.05410) · [blog post](https://www.anthropic.com/research/reasoning-models-dont-say-think)
- Korbak T, et al. (2025). Chain of thought monitorability: a new and fragile opportunity for AI safety. [arXiv:2507.11473](https://arxiv.org/abs/2507.11473)
- Elhage N, et al. (2022). Toy models of superposition. [arXiv:2209.10652](https://arxiv.org/abs/2209.10652)
- Bricken T, et al. (2023). [Towards monosemanticity: decomposing language models with dictionary learning](https://transformer-circuits.pub/2023/monosemantic-features/). *Transformer Circuits Thread.*
- Ameisen E, et al. (2025). [Circuit tracing: revealing computational graphs in language models](https://transformer-circuits.pub/2025/attribution-graphs/methods.html). *Transformer Circuits Thread.*
- Turpin M, et al. (2023). Language models don't always say what they think: unfaithful explanations in chain-of-thought prompting. *NeurIPS.* [arXiv:2305.04388](https://arxiv.org/abs/2305.04388)
- Peng K, et al. (2025). Position: use sparse autoencoders to discover unknowns. [arXiv:2506.23845](https://arxiv.org/abs/2506.23845)
