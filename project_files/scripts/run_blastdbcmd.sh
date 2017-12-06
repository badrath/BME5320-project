#	BME5320
#	Robert Marini
#	project
#	filters and runs blastdbcmd with the given input blast -fmt 7 output file (...faa.out)

BLASTDBCMD='/Shared/class-BME5320-dkristensen/bin/blastdbcmd'

DB='/Shared/class-BME5320-dkristensen/database/refseq_protein'

DBTYPE='prot'

BATCH_FILE=$1

OUTPUT_FILE="$1.GO.out" #	suspect and untested

NUM_ALIGNMENTS_DESCR=500

TAB_FORMAT=7 #6 without header, 7 with header and final line for completion validation check

E_VALUE=0.001


#$BLASTP -query $QUERY_FILE -out $OUTPUT_FILE -db $DB -num_alignments $NUM_ALIGNMENTS_DESCR -num_descriptions $NUM_ALIGNMENTS_DESCR -outfmt $TAB_FORMAT

$BLASTDBCMD -db $DB -dbtype $DBTYPE -entry_batch BATCH_FILE