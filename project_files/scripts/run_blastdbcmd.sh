#	BME5320
#	Robert Marini
#	project
#	filters and runs blastdbcmd with the given input blast -fmt 7 output file (...faa.out)

BLASTDBCMD='/Shared/class-BME5320-dkristensen/bin/blastdbcmd'

DB='/Shared/class-BME5320-dkristensen/database/refseq_protein'

DBTYPE='prot'

BATCH_FILE=$1
#QUERY=$1

OUTPUT_FILE=$2 

OUTPUT_FORMAT="%t" #%a gives accession, %t gives sequence title 

#$BLASTP -query $QUERY_FILE -out $OUTPUT_FILE -db $DB -num_alignments $NUM_ALIGNMENTS_DESCR -num_descriptions $NUM_ALIGNMENTS_DESCR -outfmt $TAB_FORMAT

#below command is untested
$BLASTDBCMD -db $DB -dbtype $DBTYPE -entry_batch $BATCH_FILE -out $OUTPUT_FILE -outfmt $OUTPUT_FORMAT -target_only
#$BLASTDBCMD -db $DB -dbtype $DBTYPE -entry $QUERY -out $OUTPUT_FILE -outfmt $OUTPUT_FORMAT -target_only