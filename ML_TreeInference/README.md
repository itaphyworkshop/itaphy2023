### System: Protein set coming from 4 Diptera species

[Aste](https://en.wikipedia.org/wiki/Anopheles_stephensi).  
[Aaeg](https://it.wikipedia.org/wiki/Aedes_aegypti).  
[Cqui](https://en.wikipedia.org/wiki/Culex_quinquefasciatus).  
[Llon](https://en.wikipedia.org/wiki/Lutzomyia_longipalpis).  

### Prepare working environment with conda

Install required programs using conda, clone the repo and create a meaningfull directory structure.

```
conda create --name Day_1
conda activate Day_1
conda install -c bioconda orthofinder trimal amas
```

### Prepare working environment without conda

Download IQ-TREE (http://www.iqtree.org/) TRIMAL(http://trimal.cgenomics.org/downloads), put them in a correct path and create directory structures

```
git clone https://github.com/itaphyworkshop
cd ML_TreeInference/
mkdir -p Analyses/{Aln,Orthofinder,Species_Tree}
mkdir IQTREE
mv ../../Downloads/iqtree-2.2.2.6-Linux/bin/iqtree2 IQTREE/
mkdir TRIMAL
mv ../../Downloads/trimAl/* TRIMAL/
cd TRIMAL
make
```

Install AMAS

```
pip install amas --user
python /home/phyworkshop_039/.local/lib/python3.10/site-packages/amas/__pycache__/AMAS.cpython-310.pyc #path for AMAS. PLEASE REMEMBER THAT THE phyworkshop_039 path is different for each of you
```
Install MAFFT

```
cd Data/mafft-7.505-with-extensions/core/
make clean
make
make install
```

mafft binaries are under 
```
/home/phyworkshop_039/itaphy2023/ML_TreeInference/Data/mafft-7.505-with-extensions/scripts/mafft
```

Install TRIMAL (http://trimal.cgenomics.org/downloads)

```
cd trimal/source
make
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

If yu did not run orthofinder: 

```
mkdir -p Analyses/Orthofinder/Single_Copy_Orthologue_Sequences/
mv Data/OG/OG00000* Analyses/SingleCopy_OG/
```

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

Trimal in -gappyout mode will remove columns of the alignments based on gaps' distribution.

```
for i in Analyses/Aln/*mafft; do 
 trimal -gappyout -in "$i" -out "${i/.mafft/.gappyout.mafft}"; 
done
```
#### 4. [AMAS]([http://trimal.cgenomics.org/trimal](https://github.com/marekborowiec/AMAS))

```
AMAS.py concat -i Analyses/Aln/*gappyout.mafft -y nexus -f fasta -d aa -p Analyses/Aln/Partitions.nexus -t Analyses/Aln/Concat.fa
```

#### 5&6. [IQTREE (Model Selection and Tree Inference)](http://www.iqtree.org/)
```
iqtree2 -s Analyses/Aln/Concat.fa -m TESTNEW -p Analyses/Aln/Partitions.nexus -m MFP+MERGE -B 1000 --prefix Analyses/Species_Tree/ML_TreeInference
```

Where: 
* ```-s```: Alignment file
* ```-m MFP+MERGE```: Best-fit partitioning scheme search considering FreeRate heterogeneity model

**Don't esitate to use other ML software (e.g. RAxML)

