#!/bin/bash

COLECT=$1
YYYY=$2
MM=$3
DD=$4


####
DIR_OUT="/home/peng/Documents/ris/$YYYY.$MM/"
BASE_IN="http://data.ris.ripe.net/$COLECT/"
LIST_HH=("0000" "1200")
####


if [[ ! -d $DIR_OUT ]] 
then
	mkdir -p $DIR_OUT
fi

for hh in "${LIST_HH[@]}";
do
	#echo $hh
	ldate=$YYYY$MM$DD.$hh
	rv_url="$BASE_IN/$YYYY.$MM/updates.$ldate.gz"
	
	base_file=$(basename $rv_url)
	parse_file="$DIR_OUT/updates.$ldate"
        file="$DIR_OUT$base_file"
	file_unzip="$DIR_OUT/updatesunzip.$ldate"
	file_parse="$DIR_OUT/updates.$ldate"	
	curl -o $file $rv_url
	
	gzip -dc $file > $file_unzip
	rm $file
	bgpdump -m $file_unzip > $file_parse
	rm $file_unzip
	gzip -9 $file_parse
done









