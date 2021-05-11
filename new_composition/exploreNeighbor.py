import random
import copy
import sys
from helpfuncs import bitdecoding
from bitcoding import B_dict
from relaxation import relax
from selectbest import alpha
from inverse import inv
import copy

def exploreNeighborhood(ini_N, ini_S,ini_G):
    N = copy.deepcopy(ini_N)
    S = copy.deepcopy(ini_S)
    G = copy.deepcopy(ini_G)
    bestNg = S
    besta = alpha(N, S)
    if besta <= 0.000001 and besta >= -0.000001:
        return bestNg
    for i in range(len(N)):
        relaxS = relax(S, i) 
        bestNgtmp, bestatmp = exploreNeighborhoodAux(N, G, relaxS, bestNg, besta, 1)
        if bestNgtmp is not None and bestatmp is not None:

            bestNg = bestNgtmp
            besta = bestatmp
            if besta <= 0.000001 and besta >= -0.000001:
                return bestNg

    return bestNg

def exploreNeighborhoodAux(ini_N, ini_neighbors, ini_N_, ini_bestNg, besta, inde):

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
            for j in neighbors[i]: #遍历每条边（有重合，如ab和ba
                baselist = bitdecoding(N_[i][j])
                if j > i and len(baselist) > 1:
                    unsele_edges.append((i, j))
        
        if len(unsele_edges) > 0:  # 当未选择的边不为空时
            ran_e = random.randint(0, len(unsele_edges)-1) # 随机选一条边
            u, v = unsele_edges[ran_e]
            baselist = bitdecoding(N_[u][v])
            ran_b = random.randint(0, len(baselist)-1) # 随机选一个base relation

            removeblist = copy.deepcopy(baselist)
            r1 = baselist[ran_b] # 替换为b
            removeblist.remove(removeblist[ran_b]) # 去掉b
            r2 = 0
            for k in removeblist:
                r2 = r2 | k
            N1 = copy.deepcopy(N_)
            N2 = copy.deepcopy(N_)
            N1[u][v] = r1
            N1[v][u] = inv(r1)
            N2[u][v] = r2
            N2[v][u] = inv(r2)

            bestNgtmp, bestatmp = exploreNeighborhoodAux(N, neighbors, N1, bestNg, besta, 1)
            if bestNgtmp is not None and bestatmp is not None:
                bestNg = bestNgtmp
                besta = bestatmp
                if besta <= 0.000001 and besta >= -0.000001:
                    return bestNg, besta

            bestNgtmp, bestatmp = exploreNeighborhoodAux(N, neighbors, N2, bestNg, besta, 1)
            if bestNgtmp is not None and bestatmp is not None:
                bestNg = bestNgtmp
                besta = bestatmp
        else:
            bestNg = N_
            besta = a
        return bestNg, besta
    else:
        return None, None
    