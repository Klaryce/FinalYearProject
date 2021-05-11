import random
from array import array
import copy
from glob import globs, setGlobals
from helpfuncs import inv, bitdecoding
from triangulation import MCS, FIC
from ppc import pPC as ppc

def fileLen(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def randomScenario(neighbors):

    # initialize constraints
    N = globs["size"]
    Id = 0
    from helpfuncs import B_dict
    with open("allen.identity") as f:
        Id = B_dict[f.readline().strip()]
    if N <= 8:
        ConMatrix = tuple([array('B',[B_dict['DALL'] if i != j else Id for i in range(len(neighbors))]) for j in range(len(neighbors))])
        ConMatrixS = tuple([array('B',[0 if i != j else Id for i in range(neighbors)]) for j in range(neighbors)])
    elif N <= 16:
        ConMatrix = tuple([array('H',[B_dict['DALL'] if i != j else Id for i in range(len(neighbors))]) for j in range(len(neighbors))])
        ConMatrixS = tuple([array('H',[0 if i != j else Id for i in range(len(neighbors))]) for j in range(len(neighbors))])
    else:
        ConMatrix = tuple([array('I',[B_dict['DALL'] if i != j else Id for i in range(len(neighbors))]) for j in range(len(neighbors))])
        ConMatrixS = tuple([array('I',[0 if i != j else Id for i in range(len(neighbors))]) for j in range(len(neighbors))])

    unsele_edges = []
    for i in range(len(neighbors)):
        for j in neighbors[i]:  # traverse each edge
            baselist = bitdecoding(ConMatrix[i][j])
            if j > i and len(baselist) > 1:
                unsele_edges.append((i, j))

    while unsele_edges:  # there are edges need to be handled
        ran_e = random.randint(0, len(unsele_edges)-1)  # randomly select an edge
        u, v = unsele_edges[ran_e]
        baselist = bitdecoding(ConMatrix[u][v])
        
        ran_b = random.randint(0, len(baselist)-1) # randomly select a base relation
        b = baselist[ran_b]
        ConMatrix[u][v] =  b  # substitute the constraint
        ConMatrix[v][u] = inv(b)

        unsele_edges.remove(unsele_edges[ran_e])  # after handling an edge, remove it
                
        # G-consistent
        if not ppc(ConMatrix, neighbors):
            ConMatrix = randomScenario(neighbors)
            print("inconsistency occurs: ppc in random scenario")
            return ConMatrix
    return ConMatrix

