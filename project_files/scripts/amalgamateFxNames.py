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
            if(('.faa.out' in filename) and ('.fxname' not in filename) and ('.matches' not in filename) and ('.mqueries' not in filename)):
                #3 at a time!
                fxname_path = os.path.join(faa_split_path,filename + '.fxname');
                match_path = os.path.join(faa_split_path,filename + '.matches');
                mquery_path = os.path.join(faa_split_path,filename + '.mqueries');
                with open(fxname_path, 'r') as infile:
                    for line in infile:
                        line_strip = line.strip('\n');
                        if(line_strip):
                            fxnames.append(line_strip);
                with open(match_path, 'r') as infile:
                    for line in infile:
                        line_strip = line.strip('\n');
                        if(line_strip):
                            matches.append(line_strip);
                with open(mquery_path, 'r') as infile:
                    for line in infile:
                        line_strip = line.strip('\n');
                        if(line_strip):
                            mqueries.append(line_strip);
                            
#             if('.fxname' in filename):
# #                 print('append contents to fxnames');
#                 with open(os.path.join(faa_split_path,filename), 'r') as infile:
#                     for line in infile:
#                         line_strip = line.strip('\n');
#                         if(line_strip):
#                             fxnames.append(line_strip);
#             elif('.matches' in filename):
# #                 print('append contents to matches');
#                 with open(os.path.join(faa_split_path,filename), 'r') as infile:
#                     for line in infile:
#                         line_strip = line.strip('\n');
#                         if(line_strip):
#                             matches.append(line_strip);
#             elif('.mqueries' in filename):
# #                 print('append contents to mqueries');
#                 with open(os.path.join(faa_split_path,filename), 'r') as infile:
#                     for line in infile:
#                         line_strip = line.strip('\n');
#                         if(line_strip):
#                             mqueries.append(line_strip);
    
    #check for missing (possibly filtered out) MGG queries (and therefore no fx names)
    MGG = [];
    MGG_path = os.path.join(grand_parent_dir, 'data', 'MGG.txt');
    with open(MGG_path,'r') as infile: #hardcoded
        for line in infile:
            line_split = line.strip('\n').split(',');
            MGG.append(line_split[0]);
    miss_annote_path = os.path.join(grand_parent_dir,'data','filtered_out_queries.txt');
    with open(miss_annote_path, 'w') as miss_outfile:
        for gene in MGG:
            in_mquery = False;
            for mquery in mqueries:
                if ( gene in mquery ):
                    in_mquery = True;
                    break;
            if( not in_mquery ):
                miss_outfile.write(gene + "\n");
                in_mquery = False;
    
    #concatenate the 3 lists' contents into single tab delim file
    with open(os.path.join(grand_parent_dir,'data','proteome_fx_annotations.txt'), 'w') as outfile:
        outfile.write('MGG Query' + '\t' + 'Matched Targets' + '\t' + 'Functional Names' + '\n');   #    header row
        for i, fxname in enumerate(fxnames):
            outfile.write(mqueries[i] + '\t' + matches[i] + '\t' + fxnames[i] + '\n');
        if(len(matches) == len(mqueries) and len(matches) == len(fxnames) and len(mqueries) == len(fxnames)):
            outfile.write("#    Function annotation completed successfully. Number of annotations: " + str(len(matches)));
        else:
            outfile.write("#    Function annotation completed unsuccessfully. Unequal number of queries, matched targets, and functional names: " + ",".join([str(len(mqueries)),str(len(matches)),str(len(fxnames))]));
    
    return(exit_code);

if __name__ == "__main__":
    exit_code = amalgamate();
    sys.exit(exit_code);