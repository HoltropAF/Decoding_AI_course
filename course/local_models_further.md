# Local models, one step further

Here's a situation from our own lab. A colleague runs `llama3.1:8b` in
Ollama, as in the Module 1 exercise, and pastes in a long protocol: twelve
pages of an LC-MS method, followed by the question *"Which column
temperature do we use?"* The answer is confident and wrong. Asked again, the
model doesn't seem to know the protocol mentions a column at all. Nothing
crashed, no warning appeared. The model simply never saw the first pages.

Module 1 (*How big is "big"?* and *Local models: Ollama and LM Studio*)
explained what a local model is, what quantisation does and roughly how
much memory you need. This page is for when you start using local models
for real work. It covers the choices Module 1 skipped: which version of a
model to download, why memory is about more than the model file (and how
that explains the protocol above), which model you're actually allowed to
use, and how to find out whether it's good enough for your task.

> **It's okay:** this page assumes you've installed Ollama or LM Studio
> once. If you haven't, the Module 1 exercise walks you through it; come
> back later.

---

## 1. Which version should I download?

### What do all those letters in the name mean?

Look up a model in the Ollama library or on Hugging Face and you'll find
not one download but a dozen: `q4_0`, `q4_K_M`, `q5_K_M`, `q6_K`, `q8_0`,
`fp16`. These are the same model, quantised to different levels. Module 1
described quantisation as rounding every number to fewer bits; the name
tells you how much rounding was done and how.

The number after the `q` is roughly the bits per weight, so `q4` is about 4
bits and `q8` about 8. The `K` marks the newer "k-quant" method, which
works in small blocks with their own scale and, importantly, doesn't treat
all parts of the model the same: the parts that matter most for quality
keep more precision than the rest. The letter at the end (`S`, `M`, `L`
for small, medium, large) says how generous it is with that extra
precision. And `fp16` is the unrounded original, 16 bits per weight.

### How much quality do I lose?

Less than you might fear, down to a point. The measurements published
alongside llama.cpp, the engine inside Ollama and LM Studio, and repeated
in many comparisons since, show a consistent pattern. At 8 bits, a model is
practically indistinguishable from the original. At 5 and 6 bits the loss
is barely measurable. At 4 bits with the k-quant method (`q4_K_M`) it is
small, and that is why it's the default most libraries give you. The old
`q4_0` method loses several times more at the same size, and below 4 bits
quality drops noticeably: models start to lose track of instructions and
facts.

Those measurements are mostly of how well the model predicts ordinary
text, which isn't the same as how well it does *your* task. Precise tasks
(extracting numbers from a table, following a strict output format, code)
tend to suffer first. So the rule of thumb is simple: take `q4_K_M` as the
default, choose `q5_K_M`, `q6_K` or `q8_0` if your memory allows and the
task is precise, and stay away from anything below 4 bits unless nothing
else fits.

> **Tip:** `ollama show llama3.1:8b` tells you which quantisation you
> actually have, together with the model's maximum context length. Other
> versions are pulled by tag, for example
> `ollama pull llama3.1:8b-instruct-q8_0`.

<details class="think"><summary>Pause and think: would you rather run a 14B model at 4 bits or an 8B model at 8 bits, if both fit?</summary>

Usually the bigger model at 4 bits: a larger model loses less from
quantisation than a smaller model gains from extra precision. The
exception is a task where exactness matters more than knowledge, such as
copying numbers faithfully; there it's worth testing both on a few real
examples. Part 3 shows how.

</details>

> **In short**
> - The tag says how the model was rounded: `q4_K_M` is the usual default,
>   `q8_0` practically the original.
> - Below 4 bits, quality drops noticeably.
> - Precise tasks suffer first; test before you trust a low-bit version.

---

## 2. Why is memory about more than the model?

### What else needs memory?

Module 1 gave rules of thumb for how much memory a model needs. Those cover
the model file. But while it runs, a model needs a second chunk of memory
that grows with the length of the conversation: the **KV cache**. For
every token in the context window, every layer keeps two lists of numbers
(the "keys" and "values" its attention step looks back at). That's what
lets the model consult the start of your text without recalculating it for
every new word.

It adds up quickly. For Llama 3.1 8B the cache takes about 128 KB per
token. A context of 8,000 tokens therefore costs about 1 GB on top of the
model, 32,000 tokens about 4 GB, and the model's full 128,000 tokens about
16 GB: three times the model itself. And the runtime reserves that memory
up front for the context length you set, whether you use it or not.

### Why did the model miss the start of the protocol?

Because, to keep memory in check, local runtimes start with a context
window much shorter than the model's maximum: 4,096 tokens by default in
Ollama, about five pages of text. When your text is longer, the
beginning is quietly dropped. There is no error message; the model just
answers from what it can still see. That is what happened with the
protocol: twelve pages is easily more than the default window, so the
first pages, with the column details, were gone before the question was
asked. The "lost in the middle" effect in Module 2 was about a model paying less
attention to parts of a long text; this is worse, because the part simply
isn't there.

The fix is to set the context length yourself. In an Ollama chat, type
`/set parameter num_ctx 16384`; in a script, pass `num_ctx` in the
request options; in LM Studio, it's the context length slider when you
load a model. Then do the arithmetic from above to make sure it fits in
your memory, or the model will slow to a crawl or fail to load.

> **In practice: a long document in a local model.** Situation: you want a
> local model to answer questions about a long protocol or paper. What to
> do: estimate the length (a page of dense text is roughly 700 to 900 tokens),
> set `num_ctx` comfortably above it, and ask one question about the first
> page before anything else. What to check: if it can't answer that one,
> the start is being cut off.

> **In short**
> - The KV cache grows with the context window and can outgrow the model.
> - Local runtimes use a short default window and silently drop the start
>   of longer texts.
> - Set the context length yourself, and check it fits in memory.

---

## 3. Which model may I use, and is it good enough?

### Is "open" the same as "open source"?

Not quite. Most models you can download are **open-weight**: you get the
trained numbers, but usually not the training data or the full recipe, and
always under a licence. Those licences differ more than people expect.
OpenAI's gpt-oss models and many Qwen models come under Apache 2.0, a
standard permissive licence. Meta's Llama models have their own community
licence with an acceptable-use policy and extra conditions for very large
companies, which is why the Open Source Initiative doesn't call them open
source. Licences can even differ between sizes of the same family. For
research use in our lab these are rarely a problem, but if a tool you build
might be shared, sold or used in a clinical setting, read the licence on the
model card first, and note it in your project.

### How do I know it's good enough for my task?

Leaderboards won't tell you. They test general knowledge and reasoning on
public benchmark questions, which the models may well have seen during
training, and they rarely include anything that looks like a lipid table or
a methods section. The only reliable test is your own task. Module 2's
*How do I test a prompt?* describes the method; for choosing a model it
comes down to this. Collect ten real examples where you know the right
answer (made-up or public data, of course), run them through two or three
candidate models with the same prompt, and score the answers. Ten examples
take an afternoon and tell you more than any leaderboard.

Write down what you used while you're at it: the model name, the exact
tag (`llama3.1:8b-instruct-q4_K_M`, not just "Llama"), the context length
and the date. `ollama list` shows an ID for every model you have; that ID
changes if the model file changes, so it pins the exact version. Module 1
mentioned that a local model never changes unless you change it. That's
only an advantage for reproducibility if you record which one it was.

> **Coffee note:** speed depends mostly on memory bandwidth, not on how
> clever your processor is. That's why a laptop with a fast graphics card,
> or an Apple Silicon Mac with its shared memory, runs a model many times
> faster than an ordinary office laptop with the same amount of RAM.

<details class="think"><summary>Pause and think: two local models score 9/10 and 8/10 on your ten test examples. Is the first one better?</summary>

Not necessarily. With ten examples, one answer difference is well within
chance. Look at *which* examples each got wrong: if the second model's
mistake is harmless and the first model's mistake is a wrong number in a
results table, the scores are telling you the wrong story. Add more
examples if the choice matters.

</details>

> **In short**
> - Downloadable models are open-weight, under licences that differ; read
>   the model card if your tool will be shared.
> - Test candidate models on ten of your own examples, not on leaderboards.
> - Record the exact tag, context length and date for reproducibility.

---

## Further reading

- Ollama documentation: [FAQ](https://docs.ollama.com/faq) (context length, where models are stored) and the [model library](https://ollama.com/library), where each model lists its tags.
- llama.cpp: [quantisation tool and its README](https://github.com/ggml-org/llama.cpp/tree/master/tools/quantize), the source of most quantisation measurements.
- Hugging Face: [GGUF documentation](https://huggingface.co/docs/hub/gguf), the file format behind Ollama and LM Studio models.
- Open Source Initiative: [the Open Source AI Definition](https://opensource.org/ai), on what "open" should mean for AI models.
