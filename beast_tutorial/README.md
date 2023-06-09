# BEAST tutorial for the ITA\*PHY 2023 workshop
To make BEAST available on your computer, source the ```phyworkshop.sh``` file and export the ```java``` path:
```
source /usr/local/etc/phyworkshop.sh
export PATH=/usr/local/jdk1.8.0_102/bin:$PATH
```
1. Download the alignment:
```
wget https://raw.githubusercontent.com/itaphyworkshop/itaphy2023/main/beast_tutorial/beast_practical_wnvl2.fa
```
2. Run BEAUti and import the alignment (nucleotides) to setup the analysis:
```beauti```

3. Run the ```.xml``` file in BEAST:
```beast```

4. Inspect the ```.log``` file with Tracer:
```tracer```

5. Get the tree from the ```.trees``` file using TreeAnnotator (set a 10% burnin and select the "median heights" option):
```treeannotator```

6. Visualize the tree:
```figtree```

## Rate prior
<img src="./../images/mutation_rate_prior.png">

Duffy, S., Shackelton, L. & Holmes, E. Rates of evolutionary change in viruses: patterns and determinants. Nat Rev Genet 9, 267–276 (2008). https://doi.org/10.1038/nrg2323

## Webpage with more BEAST tutorials:
https://taming-the-beast.org/
