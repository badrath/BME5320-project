#                             #    the query match result passed the filter.
#                             #    write the matched target id to the query seq's .batch4GO file
#                             splitout_file = filename.replace(".faa.out",".batch4GO");
#                             splitout_path = os.path.join(grand_parent_dir,"data","batch4GO",splitout_file)
#                             try:
#                                 with open(splitout_path,'a') as outfile:
#                                     outfile.write(filter_result);
#                             except IOError:
#                                 try:
#                                     with open(splitout_path,'w') as outfile:
#                                         outfile.write(filter_result);
#                                 except:
#                                     e = sys.exc_info()[0];
#                                     sys.stdout.write(e);
#                             except:
#                                 e = sys.exc_info()[0];
#                                 sys.stdout.write("[ERROR] Could not append or write to target: " + splitout_path);
#                                 sys.stdout.write(e);

########################3