#..../BME5320-project/project_files/scripts/amalgamateFxNames.py

import os
import sys
import subprocess

def amalgamate():
    exit_code = 0;
    
    #get path to data/faa-split directory relative to this location
    pwd1 = os.getcwd();
    grand_parent_dir = os.path.split(pwd1)[0];
    faa_split_path = os.path.join(grand_parent_dir,'data','faa-split'); #    hardcoded
    
    #initializing some lists to append matches, their fx names, and the original query accession ids
    matches = [];
    mqueries = [];
    fxnames = [];
    
    for(dirpath, dirnames, filenames) in os.walk(faa_split_path):
        for filename in filenames:
            if('.fxname' in filename):
#                 print('append contents to fxnames');
                with open(os.path.join(faa_split_path,filename), 'r') as infile:
                    for line in infile:
                        line_strip = line.strip('\n');
                        if(line_strip):
                            fxnames.append(line_strip);
            elif('.matches' in filename):
#                 print('append contents to matches');
                with open(os.path.join(faa_split_path,filename), 'r') as infile:
                    for line in infile:
                        line_strip = line.strip('\n');
                        if(line_strip):
                            matches.append(line_strip);
            elif('.mqueries' in filename):
#                 print('append contents to matches');
                with open(os.path.join(faa_split_path,filename), 'r') as infile:
                    for line in infile:
                        line_strip = line.strip('\n');
                        if(line_strip):
                            mqueries.append(line_strip);
    
    #concatenate the 3 lists' contents into single tab delim file
    with open(os.path.join(grand_parent_dir,'data','proteome_annotated.txt'), 'w') as outfile:
        outfile.write('MGG Query' + '\t' + 'Matched Targets' + '\t' + 'Functional Names' + '\n');   #    header row
        for i, fxname in enumerate(fxnames):
            outfile.write(mqueries[i] + '\t' + matches[i] + '\t' + fxname + '\n');
    
    return(exit_code);

if __name__ == "__main__":
    exit_code = amalgamate();
    sys.exit(exit_code);