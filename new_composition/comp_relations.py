# from bitcoding import B_dict, B_dict_reverse, B_dict_store
from helpfuncs import B_dict, B_dict_reverse, B_dict_store, bitdecoding
from comptab import fcomp

# # calculate compositions
def complex_relations(i, j):
    ij = 0  # initialize the composition of the constraint i and the constraint j

    i_base_rs = bitdecoding(i) # set of base relations of i
    j_base_rs = bitdecoding(j) # set of base relations of j
    
    for r_i in i_base_rs: 
        for r_j in j_base_rs: 
            # for each base relation in i and in j, calculate the composition
            num_r = fcomp[B_dict_store[B_dict_reverse[r_i]]][B_dict_store[B_dict_reverse[r_j]]]
            ij = ij | num_r  # add it to the composition of i and j

    return ij
