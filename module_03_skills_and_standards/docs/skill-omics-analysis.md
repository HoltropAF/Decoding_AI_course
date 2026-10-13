# Skill: omics analysis

What the skill makes the assistant do. How to start it is at the top
of this step; the skill file itself is the last part of this page.

## 1. What does the skill do?

### What it is

A skill is a recipe the assistant pulls out only when a task calls for it
(part 2 of the chapter). This one turns a general assistant into an
experienced computational bioinformatician for our kind of work: bulk and
single-cell RNA-seq, LC-MS lipidomics and metabolomics, and the integration
of the two. It's the skill most of us will use most often, because it
carries the lab's analysis habits into every session where you plan, write,
review or interpret an omics analysis.

### What it covers

Before it writes a line of code, the skill makes the assistant ask about
the experiment: organism and identifier type, the comparison and its
reference group, the number of biological replicates, pairing, and
batches. Those are exactly the details Module 2 showed a model guesses
when you leave them out. When it has to assume something, it says so at
the top of the answer.

Then come the lab's standards per data type. For RNA-seq it insists on
raw counts for differential expression, a design formula with batch or
donor where they apply, an explicit reference level, adjusted p-values,
and quality checks such as PCA and a sample-swap test before anyone
believes a result; for single-cell data, pseudobulk per sample. For
lipidomics and metabolomics it starts with pooled QC samples and drift
along the injection order, makes the missing-value choice explicit, and is
honest about annotation: the identification level, and whether a lipid is
known at sum-composition level (`PC 34:1`) or as a species
(`PC 16:0_18:1`). On top of that come the statistics (no
pseudo-replication, effect sizes, multiple testing), enrichment with the
right background, multi-omics integration that matches samples first,
readable figures, and reproducible code in the ENCORE layout.

### What you get back

Answers in a fixed order: the assumptions and open questions, the plan in a
few steps with a reason for each method, runnable and commented code in the
language you work in, the checks to run with what a good and a bad result
look like, and the caveats. The skill also tells the assistant to separate
what the data shows from what it suggests, to name an alternative
explanation for every finding, and never to invent gene names, pathway
members or lipid identifiers.

### Its limits

The skill holds good general practice and our lab's defaults, not the
answer to every design. It can't see your data unless you show it, and it
shouldn't: it works from column names, summaries and synthetic stand-ins,
and you run the code on the real data yourself. And like any skill, it's a
request to the model, not a guarantee (part 2 of the chapter): check the
code, the statistics and every identifier, especially in a result that
goes into a paper.
