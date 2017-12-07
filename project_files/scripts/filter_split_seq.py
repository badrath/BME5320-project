#../../project/project_files/filter_split_seq.py

#    filter_split_seq is complete
#    dependent on filter function, of which is still underconstruction

import os
import sys
import subprocess
from filter import filter

exit_status = 0; #set to successful unless otherwise changed due to runtime failure

input_arguments = sys.argv; #    0 = file path, 1 = directory to iterate through, 2 directory to output to

#this section is essentially hardcoding the paths for project purposes and needs to be revisited to generalize it
#the file paths are essentially hardcoded here
input_dir = input_arguments[1].replace('../','');   #hardcoding
output_dir = input_arguments[2].replace('../','');  #hardcoding

pwd1 = os.getcwd();
grand_parent_dir = os.path.split(pwd1)[0];
input_dir = os.path.join(grand_parent_dir,input_dir);   #got the paths localized
output_dir = os.path.join(grand_parent_dir,output_dir); #got the paths localized



for filename in os.listdir(input_dir):
    filename_path = os.path.join(input_dir,filename);
    if filename.endswith(".out"):
        #    only looking at the blast output files here
        completion_line = subprocess.check_output(['tail','-1',filename_path]);  #    gets last line to check for completed blast run
        if ('#' in completion_line[0]):
            #    blast run of the file completed successfully.
            sys.stdout.write("[INFO] " + filename + "completed BLASTP as expected.");
            #    filter and split
            with open (filename_path, 'r') as infile:
                for line in infile:
                    if('#' not in line):
                        #    actual sequence results here
                        filter_result = filter(line);   #    filter function underconstruction
                        if(filter_result):
                            #    the query match result passed the filter.
                            #    write the matched target id to the query seq's .batch4GO file
                            splitout_file = filename.replace(".faa.out",".batch4GO");
                            splitout_path = os.path.join(grand_parent_dir,"data","batch4GO",splitout_file)
                            try:
                                with open(splitout_path,'a') as outfile:
                                    outfile.write(filter_result);
                            except IOError:
                                try:
                                    with open(splitout_path,'w') as outfile:
                                        outfile.write(filter_result);
                                except:
                                    e = sys.exc_info()[0];
                                    sys.stdout.write(e);
                            except:
                                e = sys.exc_info()[0];
                                sys.stdout.write("[ERROR] Could not append or write to target: " + splitout_path);
                                sys.stdout.write(e);
                                
                                
                        
        else:
            #    blast run of the file completed UNsuccessfully. skips this file with an error message.
            sys.stdout.write("[ERROR] " + filename + "did not complete BLASTP as expected. \n\tExcluded file from split and GO Term finding");