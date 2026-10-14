# AI built for biology

Most of this course is about chatbots, because they are the AI you'll use
every day. But the AI that ends up in our methods sections usually looks
quite different. It reads protein sequences instead of sentences, single-cell
profiles instead of paragraphs, mass spectra instead of questions. Module 1
introduced the most famous example, AlphaFold, and said that plenty of AI
in biology "is not a chatbot at all". This page goes further: what these
models are, where the language-model idea has carried over into biology,
and, just as important, where it hasn't worked as well as the headlines
promised.

It's a page of examples from science, chosen to be close to our own work,
with a set of questions to ask when the next "foundation model for X"
paper lands in your inbox. For those who want the evidence in detail, the
last part reads four of the key papers closely.

> **It's okay:** you don't need to know how any of these models work to
> read on. The one idea to carry with you is the one from Module 1: a
> language model learns by predicting a hidden piece from its context.

---

## 1. What if the language is biology?

### Can you train a language model on proteins?

A protein sequence is a string of letters from an alphabet of twenty, and
evolution has been writing in it for billions of years. Sequences that
survive are "grammatical": the residues have to fit together into a
structure that folds and works. That makes protein databases a lot like a
huge library of text, and from about 2019 several groups asked the obvious
question: what happens if you train a language model on them?

The best-known answer is Meta's **ESM** family, now continued by the
company EvolutionaryScale. ESM-2 was trained on millions of protein
sequences with the same trick as BERT in Module 1: hide a fraction of the
residues, and learn to predict them from the rest. Nobody told the model
anything about structure. Yet to predict a hidden residue well, it pays to
know which other residues it touches in the folded protein, and the model
learned exactly that. [Lin et al. (2023)](https://doi.org/10.1126/science.ade2574)
used it to build **ESMFold**, which predicts a structure from a single
sequence, without the slow search for related sequences that AlphaFold 2
needs, and is many times faster for it. Fast enough, in fact, to predict
the structures of more than 600 million proteins from metagenomic
samples, most of them from organisms nobody has ever grown in a lab.

In 2025 the same team went a step further with ESM3, a model that reasons
over sequence, structure and function together
([Hayes et al. 2025](https://doi.org/10.1126/science.ads0018)). They asked
it to design a green fluorescent protein, and one of its designs, esmGFP,
glowed, despite sharing only 58% of its sequence with the closest known
fluorescent protein. The authors estimate that natural evolution would need
hundreds of millions of years to travel that far.

### What do biologists actually use them for?

Rarely to design glowing proteins. The everyday use is quieter: the
model's internal representation of a protein (its **embedding**, a long
list of numbers per residue or per protein) turns out to be a very good
starting point for other predictions. Feed embeddings into a small,
ordinary classifier and you can predict where a protein sits in the cell,
whether a variant is likely to be damaging, or which residues bind a
ligand, often with far less labelled data than you would otherwise need.
That is the pattern the field calls a **foundation model**: one large
model trained on everything, then adapted, or "fine-tuned", for many
smaller tasks.

<details class="think"><summary>Pause and think: ESM-2 was never shown a protein structure, yet it learned which residues touch. Why?</summary>

Because the training task rewards it. Residues that touch in the folded
protein mutate together over evolution: if one changes, the other often has
to change to keep the contact. A model that has to guess a hidden residue
does better if it has learned which positions co-vary, and those are
largely the positions in contact. Structure was hidden in the statistics of
the sequences all along.

</details>

> **In short**
> - Protein sequences can be treated as a language; ESM learned structure
>   just by predicting hidden residues.
> - ESMFold predicts structures fast enough to cover hundreds of millions of
>   metagenomic proteins; ESM3 designed a working, very unusual GFP.
> - The everyday use is embeddings: a strong starting point for small,
>   task-specific predictions.

---

## 2. And if the language is the cell?

### What is a single-cell foundation model?

If proteins can be a language, why not cells? A single-cell RNA-seq profile
is a list of genes and how strongly each is expressed, and public atlases
now hold tens of millions of them. **Geneformer**
([Theodoris et al. 2023](https://doi.org/10.1038/s41586-023-06139-9))
turned each cell into a "sentence" of gene names, ranked by expression,
and pretrained a transformer on about 30 million of these. Fine-tuned on
small datasets, it improved predictions on a range of tasks and pointed to
candidate therapeutic targets for cardiomyopathy. **scGPT**
([Cui et al. 2024](https://doi.org/10.1038/s41592-024-02201-0)) took a
similar route with a generative model. The promise was big: one model that
understands cells well enough to annotate cell types, remove batch effects
and even predict what happens when you knock a gene out, with little data
of your own.

For a lab that studies dendritic cells and their response to LPS, that
promise is easy to translate: could such a model tell us how our cells
would respond to a perturbation we haven't done yet?

### How well do they actually work?

This is where the story gets more interesting, and more useful. In 2025
[Kedzierska et al.](https://doi.org/10.1186/s13059-025-03574-x) tested
Geneformer and scGPT the way you would use them in discovery, without any
extra training (**zero-shot**), on clustering cells and correcting batch
effects. In many cases both were outperformed by much simpler approaches,
including simply taking the most variable genes. The good results in the
original papers had mostly come after fine-tuning, which hid how little
the pretrained models offered on their own.

The same year, [Ahlmann-Eltze, Huber and Anders (2025)](https://doi.org/10.1038/s41592-025-02772-6)
compared five foundation models and two other deep-learning models on the
headline task, predicting how the transcriptome changes after one or two
genes are perturbed, against deliberately simple baselines. None of the
deep-learning models did better than the baselines. Other benchmarks
reached similar conclusions, sometimes with titles that say it all: one
was subtitled *"one PCA still rules them all"*.

None of this means the idea is dead. Models and datasets keep improving,
and fine-tuned models do help on some tasks. But it is the clearest
example in our field of something the hackathon (Module 6) asks of every
team: before you believe a clever method, compare it with the simplest
thing that could possibly work.

<details class="think"><summary>Pause and think: why would a huge model trained on 30 million cells lose to "take the most variable genes"?</summary>

Several reasons are plausible. The pretraining task (predict hidden or
ranked genes) may not force the model to learn what clustering or
perturbation prediction needs. Technical variation between datasets may
dominate what it learns. And simple baselines are strong because decades
of method development went into them. The honest answer is that nobody
knows exactly yet, which is precisely why the comparison has to be made.

</details>

> **In short**
> - Single-cell foundation models treat cells as sentences of genes and
>   pretrain on tens of millions of them.
> - Independent tests found they often don't beat simple baselines, zero-shot
>   or for perturbation prediction.
> - The lesson for every method: compare with the simplest thing that works.

---

## 3. Closer to home: spectra and antigens

### Where does AI help with mass spectrometry?

In untargeted metabolomics and lipidomics, the hard step is annotation:
which molecule produced this MS/MS spectrum? The classic approach compares
your spectrum with a library of reference spectra using a similarity
score. Machine learning has entered at exactly that point. **Spec2Vec**
([Huber et al. 2021](https://doi.org/10.1371/journal.pcbi.1008724))
borrowed an idea from language models, word embeddings, and treated
fragment peaks as words that occur together; **MS2DeepScore**
([Huber et al. 2021](https://doi.org/10.1186/s13321-021-00558-4)) trained
a neural network to predict how structurally similar two molecules are
from their spectra alone. Both find related molecules that a classic score
misses. The **SIRIUS** software with CSI:FingerID
([Dührkop et al. 2019](https://doi.org/10.1038/s41592-019-0344-8)) goes the
other way: it predicts a molecular fingerprint from the spectrum and
searches structure databases for molecules that match, so it can suggest
candidates that are in no spectral library at all.

The same caution applies here as in part 2. In the same year,
[Li et al. (2021)](https://doi.org/10.1038/s41592-021-01331-z) showed that
a simple, carefully chosen similarity measure (spectral entropy, no
machine learning involved) beat the standard dot product for compound
identification. Better maths sometimes beats a bigger model.

### And in immunology?

Here AI has been at work for longer than the word "foundation model" has
existed. Predicting which peptides a given MHC molecule will present, the
question at the heart of what a dendritic cell shows to a T cell, has been
done with neural networks for twenty years. The current versions, such as
NetMHCpan-4.1 and NetMHCIIpan-4.0
([Reynisson et al. 2020](https://doi.org/10.1093/nar/gkaa379)), are trained
on binding data and on peptides actually eluted from MHC molecules and
identified by mass spectrometry. They are a good example of predictive AI
(Module 1, *What kinds of AI are there?*) that biologists use routinely
without thinking of it as AI. AlphaFold 3, introduced in Module 1, now
also predicts complexes such as antibodies with their antigens, though its
accuracy there is lower than for single proteins.

> **In short**
> - In MS/MS annotation, learned similarity scores and fingerprint
>   prediction find molecules that library matching misses.
> - A carefully chosen simple measure can still beat them.
> - Peptide–MHC prediction is long-established AI that many immunologists
>   use without calling it that.

---

## 4. How do I read the next "AI for biology" paper?

A new model in a high-profile journal, with impressive figures and a
memorable name, is now a weekly event. A handful of questions, most of
them familiar from Module 6's evaluation plan, sort the strong claims from
the weak ones.

Start with the baseline. What did the authors compare against, and was it
the strongest simple method or a convenient weak one? If the comparison
is only with other deep-learning models, you don't yet know whether any of
them is needed. Then ask how the model was used: zero-shot or fine-tuned,
and if fine-tuned, on how much data. A model that only shines after
fine-tuning on a large labelled set is less of a "foundation" than the
abstract suggests.

Next comes leakage, the classic trap in biology. Are the test proteins,
cells or spectra truly new, or are close relatives of them in the training
data? Proteins with 90% sequence identity to a training example are not
an independent test. Then look for independent evaluation: has anyone
outside the developing group benchmarked it, and on whose data? The
single-cell story in part 2 only came to light through independent groups.
And finally, check what it costs to run. A model that needs a cluster of
graphics cards to reproduce a result that PCA gets on a laptop has to be a
lot better to be worth it.

> **In practice: before you adopt a new model.** Situation: a colleague
> wants to use a new foundation model for your single-cell or lipidomics
> data. What to do: run it next to the simplest reasonable method (PCA plus
> clustering, a library search) on one dataset where you know the answer.
> What to check: does it find something the simple method misses, and is
> that something real?

> **In short**
> - Check the baseline, and whether it was strong.
> - Ask whether results are zero-shot or fine-tuned, and check for leakage
>   between training and test data.
> - Look for independent benchmarks before you believe the headline.

---

## 5. Deep dive: four papers up close

> **It's okay to skim:** this part reads four of the papers above the way
> you would at a journal club: what exactly was done, on which data, what
> came out (with the numbers), and where the weak spots are. Parts 1 to 4
> give you the conclusions; this is the evidence.

Two of the papers are about protein language models and show what the
approach can do. The other two are independent benchmarks of single-cell
foundation models and show how easily a field can fool itself. Read
together, they're a small course in judging AI methods in biology.

### ESM-2 and ESMFold: how good is "good"?

[Lin et al. (2023)](https://doi.org/10.1126/science.ade2574) trained ESM-2
in sizes from 8 million to 15 billion parameters. The training data came
from UniRef: sequences were sampled evenly across about 43 million UniRef50
clusters, drawing on about 138 million UniRef90 sequences, so the models
saw roughly 65 million distinct proteins. The task was masked language
modelling: each residue had a 15% chance of being hidden, and the model had
to predict it. As the models grew, they got better at that task (the
perplexity, roughly "how many residues is it still choosing between", fell
from 10.45 for the smallest to 6.37 for the largest).

The interesting claim is that structure *emerges* from this. To test it,
the authors trained a simple logistic regression to read contacts out of
the model's attention maps, using just 20 proteins for training and 14,842
for testing. With so little supervision, any structural information has to
come from the language model itself. Long-range contact precision rose
with model size, and how well a model did at the language task predicted
how well it captured structure almost perfectly across model sizes.

Then the head-to-head. ESMFold puts a folding module on top of the 15B
model and predicts a structure from a single sequence. On CAMEO, a
continuous benchmark of newly released structures, it reached an average
TM-score of 0.83 against 0.88 for AlphaFold 2 with its full search for
related sequences. On CASP14, the harder set of the 2020 competition, the
gap was bigger: 0.68 against 0.85. (A TM-score above 0.5 roughly means the
fold is right; 1 is a perfect match.) In exchange it was fast: 14.2 seconds
for a 384-residue protein on one graphics card, about six times faster
than one AlphaFold 2 model, and up to sixty times for short sequences, not
counting the sequence search AlphaFold needs first.

That speed made the ESM Metagenomic Atlas possible: about 617 million
metagenomic sequences folded in roughly two weeks on about 2,000 graphics
cards. About 365 million predictions had good confidence and about 225
million high confidence, and in a sample of a million high-confidence
structures, 12.6% resembled nothing in the Protein Data Bank. The honest
summary: a little less accurate than AlphaFold 2, much less on hard
targets, but fast enough to survey a part of protein space nobody had
looked at.

### ESM3 and esmGFP: what did the model actually design?

[Hayes et al. (2025)](https://doi.org/10.1126/science.ads0018) built ESM3,
which handles sequence, structure and function together by turning each
into tokens; structure, for instance, is encoded with a vocabulary of 4,096
structure tokens. The largest version has 98 billion parameters and was
trained on 2.78 billion natural proteins plus predicted structures and
synthetic sequences, 771 billion unique tokens in all. Because it is trained
to fill in any masked combination of tracks, you can prompt it with part
of a structure and a few key residues and let it complete the rest.

That is how esmGFP was made. The team prompted a 7-billion-parameter
version with six residues that form and hold the chromophore, plus the
backbone of part of a natural GFP, and let it generate structure first,
then sequence, then refine both. From tens of thousands of candidates they
tested 88 in the first round. One, B8, glowed, but about fifty times more
dimly than natural GFPs and only after a week of maturation. A second round
starting from B8 produced esmGFP, with brightness comparable to natural
GFPs. Its sequence is 58% identical to the nearest known fluorescent
protein (a designed variant, tagRFP) and 53% to the nearest natural one.

The famous "500 million years" deserves a careful read. It comes from a
simple model relating sequence identity to divergence time, calibrated on
six coral GFPs on a dated tree and then extrapolated to esmGFP's identity.
It's a vivid way to express "very far from anything natural", not a
measurement. And it took the experimental loop, two rounds and a lot of
filtering, to get from a model's suggestions to a protein that works.

### Zero-shot single-cell models: a close read of Kedzierska et al.

[Kedzierska et al. (2025)](https://doi.org/10.1186/s13059-025-03574-x)
asked a deceptively simple question: if you use Geneformer or scGPT the way
you'd use them on a new dataset without labels, are their cell embeddings
better than what we already have?

The two models encode cells differently. Geneformer (6 transformer layers,
pretrained on 27.4 million cells, excluding cancer and immortalised lines)
turns each cell into a list of genes ranked by expression and learns to
predict masked genes in that list. scGPT (12 layers, about three times as
many parameters) bins each gene's expression into 50 levels and learns to
predict masked bins, while also producing an embedding for the whole
cell. The baselines were deliberately ordinary: the 2,000 most variable
genes (HVG), and two established tools trained on each dataset, scVI and
Harmony. The five test datasets were real tissue data (pancreas, two PBMC
sets, a cross-tissue immune atlas and Tabula Sapiens), chosen to be the
*most favourable* setting for the models: tissues and technologies like
those they were pretrained on.

On separating known cell types, scored with the standard combination of
silhouette width, NMI and ARI, both models did worse than HVG, scVI and
Harmony; scGPT won only on one PBMC dataset. Simply taking the most
variable genes beat both models on every metric. On batch correction,
Geneformer came last everywhere, and its embeddings actually contained
*more* batch-driven variation than the raw data. scGPT beat scVI and
Harmony only on the immune atlas and Tabula Sapiens, which turned out to
have been part of its pretraining data, so that win may be memory rather
than understanding.

The most revealing analysis tested the models on the very task they were
trained for. scGPT, asked to predict masked expression without its cell
embedding, did worse than simply predicting the average; with the
embedding it improved only a little. Geneformer's predicted rankings
correlated with the real ones at a median of 0.56. And of three scGPT
versions pretrained on 0.8, 10.3 and 33 million cells, the 33-million one
was slightly *worse* than the blood-only one, even on non-blood tissues.
The authors' own limitations: two models, five datasets, transcriptomics
only, and some test data overlapping with pretraining, which is why they
call for benchmark datasets that are never used for training.

### Perturbation prediction: a close read of Ahlmann-Eltze et al.

[Ahlmann-Eltze, Huber and Anders (2025)](https://doi.org/10.1038/s41592-025-02772-6)
tested the most ambitious claim: that these models can predict what
happens to the transcriptome when you perturb genes, including
combinations you haven't measured.

For double perturbations they used a CRISPR-activation dataset in K562
cells with 100 single and 124 double perturbations, measured across 19,264
genes. Models were trained on all single perturbations and half of the
doubles, then asked to predict the other half, five times with different
random splits. The contenders were scGPT, scFoundation, GEARS and CPA,
plus scBERT, Geneformer and UCE with a simple decoder added. The baselines
were almost insultingly simple: "no change" (always predict the control)
and "additive" (predict the sum of the two single-gene log fold changes).
Every model had a larger prediction error than the additive baseline.

The authors then asked about genetic interactions, the cases where a
double perturbation does something the two singles don't predict, which is
exactly where a model that "understands" biology should shine. They found
5,035 such interactions in the data (out of 124,000 possible, at 5% FDR).
No model found them better than the "no change" baseline, which by
definition predicts no interactions at all. Looking closer, most models
barely varied their predictions between perturbations.

For unseen single perturbations (two CRISPR-interference datasets in K562
and RPE1 cells, and one more in K562), the baselines were the mean of the
training perturbations and a linear model built from a 10-component PCA of
the training data. No deep-learning model consistently beat either. Two
findings stand out. Taking scGPT's or scFoundation's learned gene
embeddings and plugging them into the simple linear model worked as well
as or better than the models' own decoders. And the only approach that
consistently won was the linear model with embeddings learned from
*perturbation data in another cell line*. Pretraining on atlases of
unperturbed cells added little; pretraining on perturbation data helped.

Two details are worth copying as good practice. The authors sent their
code to the developers of each model to check that they hadn't run it
wrongly, and reported the original results when a suggested fix made one
model worse. And they noticed that the linear baseline in the original
scGPT paper had been set up so that it predicted "no change" for any unseen
perturbation, an easy opponent to beat. Their own limitations: four
datasets, all from cancer cell lines, with the original quality control.

<details class="think"><summary>Pause and think: why is "the sum of the two single effects" such a strong baseline for double perturbations?</summary>

Because most gene pairs don't interact. In this dataset only a few percent
of gene–perturbation values deviated from the additive expectation, so a
model that gets the singles right and assumes independence is right most
of the time. A model has to beat additivity *on the interactions* to add
anything, which is a much harder target than "predict the expression
profile". It's the single-cell version of a well-known rule: know what the
null model already explains before you credit the fancy one.

</details>

> **In short**
> - ESM-2 learned protein contacts from sequence alone; ESMFold is close to
>   AlphaFold 2 on easy targets, clearly worse on hard ones, and far faster.
> - esmGFP is a real, very unusual fluorescent protein, reached through two
>   rounds of lab testing; "500 million years" is a rough extrapolation.
> - Used zero-shot, Geneformer and scGPT lost to simply taking the most
>   variable genes, and struggled even on their own training task.
> - For perturbation prediction, no deep-learning model beat an additive or
>   linear baseline; pretraining on perturbation data helped, atlas data
>   hardly.

---

## Further reading

- Lin Z, et al. (2023). Evolutionary-scale prediction of atomic-level protein structure with a language model. *Science* 379:1123–1130. [doi:10.1126/science.ade2574](https://doi.org/10.1126/science.ade2574)
- Hayes T, et al. (2025). Simulating 500 million years of evolution with a language model. *Science.* [doi:10.1126/science.ads0018](https://doi.org/10.1126/science.ads0018)
- Theodoris CV, et al. (2023). Transfer learning enables predictions in network biology. *Nature* 618:616–624. [doi:10.1038/s41586-023-06139-9](https://doi.org/10.1038/s41586-023-06139-9)
- Cui H, et al. (2024). scGPT: toward building a foundation model for single-cell multi-omics using generative AI. *Nature Methods.* [doi:10.1038/s41592-024-02201-0](https://doi.org/10.1038/s41592-024-02201-0)
- Kedzierska KZ, et al. (2025). Zero-shot evaluation reveals limitations of single-cell foundation models. *Genome Biology* 26:101. [doi:10.1186/s13059-025-03574-x](https://doi.org/10.1186/s13059-025-03574-x)
- Ahlmann-Eltze C, Huber W, Anders S (2025). Deep-learning-based gene perturbation effect prediction does not yet outperform simple linear baselines. *Nature Methods* 22:1657–1661. [doi:10.1038/s41592-025-02772-6](https://doi.org/10.1038/s41592-025-02772-6)
- Huber F, et al. (2021). Spec2Vec: improved mass spectral similarity scoring through learning of structural relationships. *PLOS Comput Biol.* [doi:10.1371/journal.pcbi.1008724](https://doi.org/10.1371/journal.pcbi.1008724)
- Huber F, et al. (2021). MS2DeepScore: a novel deep learning similarity measure to compare tandem mass spectra. *J Cheminform.* [doi:10.1186/s13321-021-00558-4](https://doi.org/10.1186/s13321-021-00558-4)
- Dührkop K, et al. (2019). SIRIUS 4: a rapid tool for turning tandem mass spectra into metabolite structure information. *Nature Methods.* [doi:10.1038/s41592-019-0344-8](https://doi.org/10.1038/s41592-019-0344-8)
- Li Y, et al. (2021). Spectral entropy outperforms MS/MS dot product similarity for small-molecule compound identification. *Nature Methods.* [doi:10.1038/s41592-021-01331-z](https://doi.org/10.1038/s41592-021-01331-z)
- Reynisson B, et al. (2020). NetMHCpan-4.1 and NetMHCIIpan-4.0. *Nucleic Acids Research.* [doi:10.1093/nar/gkaa379](https://doi.org/10.1093/nar/gkaa379)
