### Prepare working environment

Install required programs using conda, clone the repo and create a meaningfull directory structure.
```
conda create --name Day_1
conda activate Day_1
conda install -c bioconda orthofinder trimal amas
```

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

#### 3. [TRIMAL](http://trimal.cgenomics.org/trimal)

Trimal in -gappyout mode will remove columns of the alignments based gaps' distribution.

```
for i in Analyses/Aln/*mafft; do 
 trimal -gappyout -in "$i" -out "${i/.mafft/.gappyout.mafft}"; 
done
```
#### 4. [AMAS]([http://trimal.cgenomics.org/trimal](https://github.com/marekborowiec/AMAS))

```
AMAS.py concat -i Analyses/Aln/*gappyout.mafft -y nexus -f fasta -d aa -p Analyses/Aln/Partitions.nexus -t Analyses/Aln/Concat.fa
```

#### 5. [IQTREE (Model Selection and Tree Inference)]([http://trimal.cgenomics.org/trimal](https://github.com/marekborowiec/AMAS))



