#!/bin/sh
mafft --thread 4 --auto  ../clean_seqs/wnv_formatted_10000_std_np10.fasta > wnv.aln
