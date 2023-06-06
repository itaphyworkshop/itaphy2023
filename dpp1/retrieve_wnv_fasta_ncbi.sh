#!/bin/bash

# Run sequence retrieval script
Rscript retrieve_wnv_fasta_ncbi.R | tee -a out.o

# Log
head -n -2 out.o > temp.txt ; mv temp.txt out.o
final_numseq=$(grep -c ">" wnv.fasta)
echo -e "\n A total number of $final_numseq sequences were downloaded." >> out.o

# Remove spaces in the final fasta file:
sed -i '/^$/d' wnv.fasta

# Get list of IDs from fasta file
grep ">" wnv.fasta | cut -d " " -f 1 | sed 's/>//g' > wnv.ids
