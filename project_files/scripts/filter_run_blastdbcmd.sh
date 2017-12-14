#	receives a file path from the array .job file
#	need to filter each match and run blastdbcmd on the match, need to only check the 1st match
#		since the MGG's have already been filtered out by the blastp run.
#	results should be appended to a single file (.Names). The separate .Names files will be concatenated in a later function

#	$1 is the .faa.out blastp result file to access for annotations
INPUT_FILE=$1;
MATCHES_FILE="$1.matches";
OUTPUT_FILE="$1.fxname";
#BLASTDBCMD_FILE="$1.matches";

#MATCHES=($(python filter_split_seq.py $INPUT_FILE | tr -d '[],'))	#	filter_split_seq.py will search the argument file for exactly 1 query match that pass the filter.py filters.
#MATCHES_FILE=($(python filter_split_seq.py $INPUT_FILE))	#	filter_split_seq.py will search the argument file for exactly 1 query match that pass the filter.py filters. outputs the name of the matchlist file for blastdbcmd batch run
#MATCHES_FILE="arb";
python filter_split_seq.py $INPUT_FILE
#MATCHES_FILE=$? #this is set to the returned value from the filter_split_seq.py, for more information see: https://bytes.com/topic/python/answers/853377-return-value-shell-script
#MATCH="arb";
#python filter_split_seq.py $INPUT_FILE > $MATCH;
#	returns a single accession id string of the pass match...or, if none found, it returns a warning message that none was found
#	legacy: filter_split_seq.py will return a python array (which needs to be converted to a UNIX array, see above) of the best matched accession.version ids.
#	legacy: each element of the array is then passed through the blastdbcmd function and the result is written to a ../data/GONames/*.Names file

echo "[INFO]		filter_split of $INPUT_FILE complete"
echo "[INFO]		running blastdbcmd, in batch, for all matches in $MATCHES_FILE"
#	below loop would run blastdbcmd for all matches that meet filter criteria, contains 5 matches for 5 queries
#for i in "${MATCHES[@]}"
#do
#	if [ ! -f "$OUTPUT_FILE" ]; then
#		$i > $BLASTDBCMD_FILE
#	else
#		$i >> $OUTPUT_FILE
#	fi 
#	echo $i;
#done

./run_blastdbcmd.sh $MATCHES_FILE $OUTPUT_FILE #blastdbcmd gets run in batch
#	run blastdbcmd in a loop here