### Prepare working environment

```
git clone https://github.com/itaphyworkshop
cd ML_TreeInference/
mkdir -p Analyses/{Aln,Orthofinder,Species_Tree}
```
 
# Simple Phylogenetic Inference Inference under a ML Framework 

### Easy pipeline:

1. Identify orthologues genes.
2. Align genes.
3. Trim alignments (optional).
4. Concatenate single-genes alignments.
5. Model selection.
6. Tree inference.

#### 1. [Orthofinder](https://github.com/davidemms/OrthoFinder)

Most simple Orthofinder run:

```
orthofinder -f Data/
```

**NB:** Orthofinder has a lot of parameters, take a look at the help!

Move Orthofinder results in the correct directory.

```
mv Data/OrthoFinder/<RESULTS_DIR>/* Analyses/Orthofinder/
```

Rename fasta headers to keep only species name (necessary for concatenation)

```
for i in Analyses/Orthofinder/Single_Copy_Orthologue_Sequences/OG00000*; do 
 sed 's/>.*|/>/' "$i" > "${i/.fa/.renamed.fa}"; 
done;
```

#### 2. [MAFFT](https://mafft.cbrc.jp/alignment/server/)

Align single-copy orthologues genes

```
for i in Analyses/Orthofinder/Single_Copy_Orthologue_Sequences/*.renamed.fa; do 
 mafft --auto "$i" > "${i/.fa/.mafft}"; 
done;
```

Move mafft results in the correct directory.

```
mv Analyses/Orthofinder/Single_Copy_Orthologue_Sequences/*.mafft Analyses/Aln/
```

#### 3. [TRIM](https://mafft.cbrc.jp/alignment/server/)


