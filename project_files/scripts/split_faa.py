#../../project/project_files/split_faa.py

import os
import sys

exit_status = 0; #set to successful unless otherwise changed due to runtime failure

input_arguments = sys.argv; #0 = file path, #1 = number of files, #2 = number of seqs per file

MGG_file = 'MGG.txt'; #    file to write MGG accession numbers to for later filtering

#    inputs for dev only
# input_arguments = ["filler","../data/uncompressed_input_file.faa",103,5];

faa_path = input_arguments[1];
num_files = int(input_arguments[2]);
num_seqs = int(input_arguments[3]);

pwd1 = os.getcwd();
grand_parent_dir = os.path.split(pwd1)[0];
MGG_path = os.path.join(grand_parent_dir,"data",MGG_file); #    path to MGG.txt file for later use in filtering out MGG genes and variants
MGG_acc_ids = [];
MGG_seq_len = [];
seqLen = 0; #init len counter for individual sequences
buffer = [];
seqs_num = 0;
filename_i = 1; #for job submission the file series cannot begin at 0
writing_records = [];
with open (faa_path, 'r') as infile:
    for line in infile:
        if('>' in line):
            #beginning of new sequence
            
            if(len(MGG_acc_ids) != 0):
                #append seq length to MGG_seq_len list
                MGG_seq_len.append(seqLen);
                seqLen = 0; #reset seqLen
                
            #save accession number to MGG_file and MGG_path
            MGG_acc_ids.append(line.strip('>').split(' ')[0].split('.')[0]);
            
            if(seqs_num == num_seqs):
                #sequence buffer filled
                
                # write to new file
                temp_filename = os.path.join(grand_parent_dir,"data","faa-split","file" + str(filename_i) + ".faa");
#                 print(temp_filename);
                with open(temp_filename, 'w+') as outfile:
                    for seq_line in buffer:
                        outfile.write(seq_line);
                
                filename_i += 1; #increment serial filename
                
                buffer = []; #clear buffer
                
                writing_records.append(seqs_num); #recording information about num of seqs written to each file.
                
                seqs_num = 0; #reset sequence counter of buffer
                
            seqs_num += 1;
        else:
            seqLen += len(line.strip('\n'));   
        buffer.append(line);
    
    # write last set of seqs to new file
    temp_filename = os.path.join(grand_parent_dir,"data","faa-split","file" + str(filename_i) + ".faa");
    print(temp_filename);
    with open(temp_filename, 'w+') as outfile:
        for seq_line in buffer:
            outfile.write(seq_line);
    
    MGG_seq_len.append(seqLen); #append last seq length to list
            
    writing_records.append(len(buffer)); #recording information of last file written

#write the MGG accession ids (MGG_acc_ids) to MGG_file at MGG_path
with open(MGG_path, 'w') as outfile:
    for i, id in enumerate(MGG_acc_ids):
        outfile.write(id + ',' + str(MGG_seq_len[i]) + '\n');

#testing to make sure correct information and write was successful
num_full_records = len(writing_records) - 1;
for seqs in writing_records[0:num_full_records]: #only iterates to n-1 items, indices 0 to len(writing_records) - 2
    if(seqs != num_seqs):
        exit_status = 1;    #number of seqs written to each file is incorrect
        break;

if(len(writing_records) != num_files):
    exit_status = 2;    #incorrect number of files, maybe a sequence got chopped up or skipped?
        
if(exit_status == 0):
    print("[INFO] " + faa_path + " split into " + str(num_files) + " files of " + str(num_seqs) + " sequences each. \n\tPlaced in following directory: " + os.path.join(grand_parent_dir,"data","faa-split"));
elif(exit_status == 1):
    print("[ERROR] number of sequences written to each file is inconsistent with the provided input");
elif(exit_status == 2):
    print("[ERROR] incorrect number of files, maybe a sequence got chopped up or skipped.");
else:
    print("[ERROR] an unknown error has occurred.");
    
sys.stdout.write(str(exit_status));
