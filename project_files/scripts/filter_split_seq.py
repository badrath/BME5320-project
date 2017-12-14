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
    
    input_arguments = input_args; #    0 = file path
    
    #this section is essentially hardcoding the paths for project purposes and needs to be revisited to generalize it
    #the file paths are essentially hardcoded here
    input_file = input_arguments[1].replace('../','');   #hardcoding
    match_file = input_file + ".matches";
    matched_query_file = input_file + ".mqueries";
    
    pwd1 = os.getcwd();
    grand_parent_dir = os.path.split(pwd1)[0];
    sys.stdout.write('[DEV]    grand_parent_dir: ' + grand_parent_dir + '\n');
    input_file_path = os.path.join(grand_parent_dir, input_file);   #got the paths localized
    match_file_path = os.path.join(grand_parent_dir, match_file);    #got the paths localized
    matched_query_file_path = os.path.join(grand_parent_dir, matched_query_file);    #got the paths localized
    sys.stdout.write("[INFO] input_file_path from filter_split_seq.py: " + input_file_path + '\n');
    
    #read in MGG.txt with the MGG accession numbers and sequence length into dictionary. Use this dictionary for filtering
    MGG = {};
    MGG_path = os.path.join(grand_parent_dir, 'data', 'MGG.txt');
    with open(MGG_path,'r') as infile: #hardcoded
        for line in infile:
            line_split = line.strip('\n').split(',');
            MGG[line_split[0]] = float(line_split[1]);
    
    completion_line = str(subprocess.check_output(['tail','-2',input_file_path]));  #    gets last line to check for completed blast run
#     sys.stdout.write("[DEV]    Completion Line: " + completion_line + '\n');
#     sys.stdout.write("[DEV] completion_line from filter_split_seq.py: " + completion_line + '\n');
    returned_accID = [];
    query_accID = [];
#     newSeqLine = '';
    if ('# BLAST processed ' in completion_line):
        #    blast run of the file completed successfully.
        sys.stdout.write("[INFO] " + input_file + "completed BLASTP as expected." + '\n');
        #    filter and split
        with open (input_file_path, 'r') as infile:
            newSeq = False; #    Toggle for recognizing new query sequence results
            for line in infile:
                if('#' in line):
                    newSeq = True;
#                     newSeqLine = line;
                elif(newSeq and ('#' not in line)):
                    #    actual sequence results here
                    filter_result = filter(line, MGG);   #    filter function underconstruction
                    if(filter_result is not None):
                        newSeq = False; #resets toggle because adequate match was found
                        returned_accID.append(filter_result);
                        query_accID.append(line.strip("\n").split("\t")[0]);
                               
                    
    else:
        #    blast run of the file completed UNsuccessfully. skips this file with an error message.
        sys.stdout.write("[ERROR] " + input_file + "did not complete BLASTP as expected. \n\tExcluded file from split and Name finding" + '\n');
        match_file = input_file + ".matches.err";
        returned_accID.append("[ERROR] " + input_file + "did not complete BLASTP as expected. \n\tExcluded file from split and Name finding");
    
    with open(match_file_path, 'w') as outfile:
        for match in returned_accID:
            outfile.write(match + "\n");
            
    with open(matched_query_file_path, 'w') as outfile:
        for qmatch in query_accID:
            outfile.write(qmatch + "\n");
    
    return(match_file_path);

if __name__ == "__main__":
    #sys.stdout.write(sys.argv);
    result = find_filtered_matches(sys.argv);
    sys.exit(result); #returns the result value to shell as value (stored automatically within the $? variable)
