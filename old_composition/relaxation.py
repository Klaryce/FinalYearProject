from helpfuncs import B_dict
import copy

def relax(S, v):
    copyS = copy.deepcopy(S)
    for i in range(len(S)):
        if (i!=v):
            copyS[i][v] = B_dict['DALL']
            copyS[v][i] = B_dict['DALL']
    return copyS