def filter (queryMatch):
    #    this function checks the queryMatch argument to check if it meets the filter standards defined here
    #    this function returns the queryMatch as a string (same as it the input argument)
    
    #    filters
    filters = {
        max_e_val   :   0.001,  #filters out non-significant e value matches
        perc_id_perfect :   100.00, #filters against perfect self matches
        qt_len_perc   :   1.0,  #filters against short matches, query / target lengths must be around 1
        qt_len_perc_SE   : 0.25,    #wiggle room for query / target
        qa_len_perc :   1.0,    #filters against short matches, query / alignment lengths must be around 1
        qt_len_perc_SE  :   0.25,   #wiggle room for query / alignment
        min_bit_score   :   50  #minimum bit score accepted
        }
    
    