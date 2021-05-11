import random
import copy
import sys
from helpfuncs import bitdecoding, B_dict, inv
from relaxation import relax
from selectbest import alpha
import copy

# explore the best neighbor of ini_S
def exploreNeighborhood(ini_N, ini_S,ini_G):
    N = copy.deepcopy(ini_N)
    S = copy.deepcopy(ini_S)
    G = copy.deepcopy(ini_G)
    bestNg = S
    besta = alpha(N, S)
    if besta <= 0.000001 and besta >= -0.000001:
        return bestNg
    for i in range(len(N)):
        relaxS = relax(S, i)   # relax the variables one by one, each time only one is relaxed
        bestNgtmp, bestatmp = exploreNeighborhoodAux(N, G, relaxS, bestNg, besta)
        if bestNgtmp is not None and bestatmp is not None:

            bestNg = bestNgtmp
            besta = bestatmp
            if besta <= 0.000001 and besta >= -0.000001:
                return bestNg

    return bestNg

# explore the best neighbor of the relaxation ini_N_
def exploreNeighborhoodAux(ini_N, ini_neighbors, ini_N_, ini_bestNg, besta):

    N = copy.deepcopy(ini_N)
    neighbors = copy.deepcopy(ini_neighbors)
    N_ = copy.deepcopy(ini_N_)
    bestNg = copy.deepcopy(ini_bestNg)

    # G-consistent
    from ppc import pPC as ppc
    if ppc(N_, neighbors): #path consistency on the initial graph (partial)
    
        a = alpha(N, N_)
        if a >= besta:
            return bestNg, besta
        
        unsele_edges = []
        for i in range(len(neighbors)):
            for j in neighbors[i]:  # traverse each edge
                baselist = bitdecoding(N_[i][j])
                if j > i and len(baselist) > 1:
                    unsele_edges.append((i, j))
        
        if len(unsele_edges) > 0:  # if there exist unhandled edges
            ran_e = random.randint(0, len(unsele_edges)-1)  # randomly choose one
            u, v = unsele_edges[ran_e]
            baselist = bitdecoding(N_[u][v])
            ran_b = random.randint(0, len(baselist)-1)  # random base relation

            removeblist = copy.deepcopy(baselist)
            r1 = baselist[ran_b]  # substitute to b
            removeblist.remove(removeblist[ran_b])  # remove b
            r2 = 0
            for k in removeblist:
                r2 = r2 | k
            N1 = copy.deepcopy(N_)
            N2 = copy.deepcopy(N_)
            N1[u][v] = r1
            N1[v][u] = inv(r1)
            N2[u][v] = r2
            N2[v][u] = inv(r2)

            bestNgtmp, bestatmp = exploreNeighborhoodAux(N, neighbors, N1, bestNg, besta)  # recursion
            if bestNgtmp is not None and bestatmp is not None:
                bestNg = bestNgtmp
                besta = bestatmp
                if besta <= 0.000001 and besta >= -0.000001:
                    return bestNg, besta

            bestNgtmp, bestatmp = exploreNeighborhoodAux(N, neighbors, N2, bestNg, besta)  # recursion
            if bestNgtmp is not None and bestatmp is not None:
                bestNg = bestNgtmp
                besta = bestatmp
        else:  # if there is no unhandled edge
            bestNg = N_
            besta = a

        return bestNg, besta

    else:
        return None, None
    