#!/bin/sh

while read -r line; do

	nameSEQ="$line"
	export  nameSEQ

	./download_metadata.py

done < wnv.ids > metadata.txt

sed -i '1 i\Accession\tCountry\tCollection_Date' metadata.txt
