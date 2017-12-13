#	receives a file path from the array .job file
#	need to filter each match and run blastdbcmd on the match, need to only check the 1st match
#		since the MGG's have already been filtered out by the blastp run.
#	results should be appended to a single file (.Names). The separate .Names files will be concatenated in a later function

#	$1 is the .faa.out blastp result file to access for annotations
INPUT_FILE=$1
OUTPUT_FILE="$1.Name"

MATCH=($(python filter_split_seq.py $INPUT_FILE | tr -d '[],'))	#	filter_split_seq.py will search the argument file for exactly 1 query match that pass the filter.py filters.
#	returns a single accession id string of the pass match...or, if none found, it returns a warning message that none was found
#	legacy: filter_split_seq.py will return a python array (which needs to be converted to a UNIX array, see above) of the best matched accession.version ids.
#	legacy: each element of the array is then passed through the blastdbcmd function and the result is written to a ../data/GONames/*.Names file

echo "filter_split $OUTPUT";
#	legacy: below loop would run blastdbcmd for all matches that meet filter criteria
#for i in "${OUTPUT[@]}"
#do
#	if [ ! -f "$OUTPUT_FILE" ]; then
#		$i > $OUTPUT_FILE
#	else
#		$i >> $OUTPUT_FILE
#	fi 
#	echo $i;
#done

./run_blastdbcmd.sh $MATCH $OUTPUT_FILE
#	run blastdbcmd in a loop here