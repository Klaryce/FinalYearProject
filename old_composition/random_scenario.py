import random
from array import array
import copy
from glob import globs, setGlobals
from triangulation import MCS, FIC
from ppc import pPC as ppc
from inverse import inv
from helpfuncs import bitdecoding

def fileLen(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def randomScenario(ini_neighbors):

    neighbors = copy.deepcopy(ini_neighbors)
    # initialize constraints
    # ConMatrix = tuple([array('B',[B_dict['DALL'] if i != j else Id for i in range(len(neighbors))]) for j in range(len(neighbors))])

    # initialize constraints
    N = globs["size"]
    Id = 0
    from bitcoding import B_dict
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

    # constraint of each edge is set as a random base relation
    unsele_edges = []
    # print(neighbors)
    for i in range(len(neighbors)):
        for j in neighbors[i]: #遍历每条边（有重合，如ab和ba
            # print("(i, j) is (%d, %d)" % (i, j))
            baselist = bitdecoding(ConMatrix[i][j])
            # print(baselist)
            if j > i and len(baselist) > 1:
                # print("Yes")
                unsele_edges.append((i, j))

    while unsele_edges:  # 当未选择的边不为空时
        ran_e = random.randint(0, len(unsele_edges)-1) # 随机选一条边
        u, v = unsele_edges[ran_e]
        baselist = bitdecoding(ConMatrix[u][v])
        
        ran_b = random.randint(0, len(baselist)-1) # 在B中随机选择一个约束
        b = baselist[ran_b]
        ConMatrix[u][v] =  b # 将随机选择的约束作为 u, v 之间的约束
        ConMatrix[v][u] = inv[b-1]

        # print(unsele_edges[ran_e])
        # print(ConMatrix[u][v])
        unsele_edges.remove(unsele_edges[ran_e])  # 从未选择的边中去掉 (u, v)
                
        # G-consistent
        if not ppc(ConMatrix, neighbors): #path consistency on the initial graph (partial)
            ConMatrix = randomScenario(neighbors)
            print("inconsistency occurs: ppc in random scenario")
            return ConMatrix
    # print(ConMatrix)
    return ConMatrix
