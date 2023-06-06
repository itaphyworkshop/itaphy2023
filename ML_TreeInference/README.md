# Simple Phylogenetic Inference Inference under a ML Framework 

### Easy pipeline:

1. Identify orthologues genes.
2. Align genes.
3. Trim genes (optional).
4. Concatenate single-genes alignments.
5. Model selection.
6. Tree inference.

#### 1. [Orthofinder](https://github.com/davidemms/OrthoFinder)

Most simple Orthofinder run:

```
orthofinder -f ../../Data/
```

**NB:** Orthofinder has a lot of parameters, take a look at the help!
