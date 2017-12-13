#../../project/project_files/filter_split_seq.py

#    filter_split_seq is incomplete, needs rethinking
#        should only return the best 1st result then move to next sequence.
#        DO NOT need to create composite score, or anything complicated.
#    dependent on filter function, of which is still underconstruction

import os
import sys
import subprocess
from filter import filter

def find_filtered_matches(input_args):

    exit_status = 0; #set to successful unless otherwise changed due to runtime failure
    
    input_arguments = input_args; #    0 = file path, 1 = directory to iterate through, 2 directory to output to
    
    #this section is essentially hardcoding the paths for project purposes and needs to be revisited to generalize it
    #the file paths are essentially hardcoded here
    input_file = input_arguments[1].replace('../','');   #hardcoding
    
    #read in MGG.txt with the MGG accession numbers and sequence length into dictionary. Use this dictionary for filtering
    MGG = {};
    with open('MGG.txt',r) as infile: #hardcoded
        for line in infile:
            line_split = line.strip('\n').split(',');
            MGG[line_split[0]] = line_split[1];
    
    pwd1 = os.getcwd();
    grand_parent_dir = os.path.split(pwd1)[0];
    filename_path = os.path.join(grand_parent_dir,input_file);   #got the paths localized
    print("filename_path from filter_split_seq.py: " + filename_path);
    
    completion_line = subprocess.check_output(['tail','-1',filename_path]);  #    gets last line to check for completed blast run
    print("completion_line from filter_split_seq.py: " + completion_line);
    returned_accID = [];
    if ('#' in completion_line[0]):
        #    blast run of the file completed successfully.
        sys.stdout.write("[INFO] " + filename + "completed BLASTP as expected.");
        #    filter and split
        with open (filename_path, 'r') as infile:
            newSeq = False; #    Toggle for recognizing new query sequence results
            for line in infile:
                if('#' in line):
                    newSeq = True;
                elif(newSeq):
                    newSet = False;
                    #    actual sequence results here
                    filter_result = filter(line, MGG);   #    filter function underconstruction
                    if(filter_result):
                        returned_accID.append(filter_result);
                        break; #found the 1 result that passed our filters, break loop and run it in blastdbcmd!
                               
                    
    else:
        #    blast run of the file completed UNsuccessfully. skips this file with an error message.
        sys.stdout.write("[ERROR] " + filename + "did not complete BLASTP as expected. \n\tExcluded file from split and Name finding");
        
    return(returned_accID);

if __name__ == "__main__":
    print(sys.argv);
    find_filtered_matches(sys.argv);

