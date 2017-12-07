#	This file may be run on the login node

#~/Documents/SKOOL/Informatics/Fall2017\ Classes/BME_Bioinformatics\ Techniques/final\ project
#~/BME5320/project/project_files/scripts/get-split-MGG-genome.sh

#meant to be run on neon
module load python/3.3

#mainly for documenting command flow and NOT a runable shell script

data_dir="../data"
if [ -d $data_dir ]; then
	rm -rf $data_dir
fi
mkdir $data_dir

compressed_file="../data/compressed_input_file.faa.gz"
file="../data/uncompressed_input_file.faa"

#*******************************
#uncomment for production:
echo "[INFO] wget -O $compressed_file ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/027/325/GCF_000027325.1_ASM2732v1/GCF_000027325.1_ASM2732v1_protein.faa.gz"

wget -O $compressed_file ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/027/325/GCF_000027325.1_ASM2732v1/GCF_000027325.1_ASM2732v1_protein.faa.gz
#*******************************
$BLASTP -query $QUERY_FILE -out $OUTPUT_FILE -db $DB -num_alignments $NUM_ALIGNMENTS_DESCR -num_descriptions $NUM_ALIGNMENTS_DESCR -outfmt $TAB_FORMAsed_file ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/027/325/GCF_000027325.1_ASM2732v1/GCF_000027325.1_ASM2732v1_protein.faa.gz


gunzip -c $compressed_file > $file #the result is the uncompressed_input_file.faa

n=$(grep ">" $file | wc -l) #we know this to be 515, but this checks just to make sure

#finding factors
factors=$(./factor.sh $n) #returns 5 and 103 in an array

max_factor=0
max_factor_i=0
i=0
for factor in $factors
do
	if (($factor > $max_factor)); then
		max_factor=$factor
		max_factor_i=$i
	fi
	i=$(($i + 1))
done

num_of_files=$max_factor
num_of_seqs=$(($n / $max_factor))

#from here we can split the $compressed_file into 103 files with 5 sequences
echo "[INFO] Found best prime factors to split input file into: $num_of_seqs sequences per file of $num_of_files files."

#check if dir exists, if not, create it
if [ ! -d "../data/faa-split" ]; then
	mkdir "../data/faa-split"
fi

echo "[INFO] Creating files by running auxillary python script."
echo "[INFO] It is assumed that the python file is in the current working directory."
split_status=0
python split_faa.py $file $num_of_files $num_of_seqs > $split_status #5 seqences into each of the 103 files, it

if (($split_status > 0)); then
	exit 1
else
	echo "[INFO] File split successful."
fi

#	actual qsub here
#hold_blast_jid=$(qsub -terse -t 0-num_of_files:1 submit_blast_array.job)
echo "[INFO] Running blast array job."
hold_blast_jid=$(qsub -terse -t 1-2:1 submit_blast_array.job | awk -F. '{print $1}')	# runs only 2 files for dev only

#for blast results
#TODO:
hold_pyFilter_jid=$(qsub -hold_jid $hold_blastdbcmd_jid submit_filter_split_py.job | awk -F. '{print $1}') #	This will run a python script to process the blast results for the next step. incomplete
#TODO:
hold_blastdbcmd_jid=$(qsub -hold_jid $hold_pyFilter_jid filter_split_blastdbcmd_array.job | awk -F. '{print $1}') #This will run the blastdbcmd on all seq files in the data/batch4GO directory. not written

#for GO Terms
#TODO wait for the blastdbcmd's to finish then amalagmate them
qsub -hold_jid $hold_blastdbcmd_jid amalgamateGOTerms.job ##	This will combine the results of the individual sequence runs into 2 files, an Annotated_seq_simple.csv and Annotated_seqes_long.csv. not written
#TODO run a qsub to put together the GO Terms results into the final report
#TODO 	filter for unique GO Terms for each query sequence













