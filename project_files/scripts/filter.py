def filter (queryMatch):
    #    this function checks the queryMatch argument to check if it meets the filter standards defined here
    #    this function returns the queryMatch as a string (same as it the input argument)
    
    #    additionally, this function recieves MGG, a dictionary containing the original query accession id, and the sequence length queried
    
    
    #need to think of a way to filter out all matches with MGG...maybe in the batch step? (see notes from 11/7)
    
    #    filters
    filters = {
        max_e_val       :   0.0000000001,  # filters out non-significant e value matches, filter is 1e-10 because we are looking for homologous orthologs
        perc_id_min     :   35.00, # minimum percent identity threshold, minimum threshold above 'twilight zone' where BLAST struggles to be valid
        qt_len_perc     :   1.0,  # not implemented, filters against short matches, query / target lengths must be around 1
        qt_len_perc_SE  :   0.25,    # not implemented, wiggle room for query / target
        qa_len_perc     :   1.0,    # filters against short matches, query / alignment lengths must be around 1
        qa_len_perc_SE  :   0.25,   # wiggle room for query / alignment
        min_bit_score   :   50  # minimum bit score accepted, a verifying score to support the e_val
        };
    
    query_data = queryMatch.strip("\n").split("\t");
    match_data = {
        query       :   query_data[0],
        target      :   query_data[1],
        perc_id     :   float(query_data[2]),
        align_len   :   int(query_data[3]),
        mismatches  :   int(query_data[4]),
        gap_opens   :   int(query_data[5]),
        q_start     :   int(query_data[6]),
        q_end       :   int(query_data[7]),
        t_start     :   int(query_data[8]),
        t_end       :   int(query_data[9]),
        e_val       :   float(query_data[10]),
        bit_score   :   int(query_data[11])
        };
    
    target = None;
    if(match_data['target'] not in keys(MGG)): #filters out MGG self hits, either same as the query search or other MGG genes/variations
        
        qa_len_perc = MGG[match_data['query']] / match_data['align_len'];
        qa_pass = (qa_len_perc <= (filters['qa_len_perc'] + filters['qa_len_perc_SE'])) and (qa_len_perc <= (filters['qa_len_perc'] - filters['qa_len_perc_SE'])); # used to filter out matches of too low % coverage
        
        if(match_data["e_val"] <= filters["max_e_val"] and
           match_data["bit_score"] >= filters["min_bit_score"] and
           match_data["perc_id"] >= filters["perc_id_min"] and
           qa_pass # % coverage filtered for here
           ):
            target = match_data["target"];
    
    return(target);
    