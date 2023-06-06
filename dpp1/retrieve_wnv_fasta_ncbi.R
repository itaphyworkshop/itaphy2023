#!/usr/bin/env Rscript

# Set the working directory and load libraries
setwd("/home/silverja/tutorials/itaphy23/without_api_key")
library("rentrez")

# NCBI search
wnv_ncbi_search <- entrez_search(db="nucleotide", term="West Nile virus[Organism] & 11035:11360[SLEN]",retmax="10000", use_history=TRUE)

# Set the number of steps for download
nterms <- length(wnv_ncbi_search$ids)

if((nterms %% 2) == 0) {
    nsteps=3
} else {
    nsteps=2
}

# Log messages
cat("\nThe NCBI search resulted in", nterms, "terms")
cat("\nDownload in progress...\n")

# Download sequence records
for(seq_start in seq(0,nterms,nsteps)){
    Sys.sleep(0.1)
    recs <- entrez_fetch(db="nucleotide", web_history=wnv_ncbi_search$web_history,
                         rettype="fasta", retmax=nsteps, retstart=seq_start)
    cat(recs, file="wnv.fasta", append=TRUE)
    cat("\n", seq_start+nsteps, "sequences downloaded, please wait...\r")
}

# Store IDs retrieved in the NCBI search
write(wnv_ncbi_search$ids, file="wnv_ncbi_search.txt")
