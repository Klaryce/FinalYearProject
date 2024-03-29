import random
import time
from ppc import pPC as ppc
from array import array
from glob import globs
from helpfuncs import bitdecoding, inv
from selectbest import alpha

def crossVarsA(N, neighbors, S1, S2):
    startT = time.time()
    V1 = [i for i in range(len(N))]
    V2 = []
    while len(V1) > len(V2):
        ran_v = random.randint(0, len(V1)-1) # randomly choose a variable
        V2.append(V1[ran_v])
        V1.remove(V1[ran_v])

    n = globs["size"]
    Id = 0
    from helpfuncs import B_dict
    with open("allen.identity") as f:
        Id = B_dict[f.readline().strip()]
    if n <= 8:
        S = tuple([array('B',[B_dict['DALL'] if i != j else Id for i in range(len(neighbors))]) for j in range(len(neighbors))])
    elif n <= 16:
        S = tuple([array('H',[B_dict['DALL'] if i != j else Id for i in range(len(neighbors))]) for j in range(len(neighbors))])
    else:
        S = tuple([array('I',[B_dict['DALL'] if i != j else Id for i in range(len(neighbors))]) for j in range(len(neighbors))])
        
    for i in range(len(S)):
        for j in range(i+1, len(S)):
            if i in V1 and j in V1:
                S[i][j] = S1[i][j]
                S[j][i] = S1[j][i]
            elif i in V2 and j in V2:
                S[i][j] = S2[i][j]
                S[j][i] = S2[j][i]

    unsele_edges = []
    for i in range(len(neighbors)):
        for j in neighbors[i]:  # traverse each edge
            baselist = bitdecoding(S[i][j])
            if j > i and len(baselist) > 1:
                unsele_edges.append((i, j))

    while unsele_edges:  # if there exist some edges need to be handled
        ran_e = random.randint(0, len(unsele_edges)-1)  # randomly choose an edge
        u, v = unsele_edges[ran_e]

        if S[u][v] & N[u][v] != 0:
            rel = S[u][v] & N[u][v]
        else:
            rel = S[u][v]

        rellist = bitdecoding(rel)
        ran_b = random.randint(0, len(rellist)-1)  
        S[u][v] = rellist[ran_b] 
        S[v][u] = inv(rellist[ran_b])

        unsele_edges.remove(unsele_edges[ran_e]) 
                
        # G-consistent
        if not ppc(S, neighbors): #path consistency on the initial graph (partial)
            print("Inconsistency occurs in crossConsB")
            return None

    passT = time.time() - startT
    globs["cross_total"] = globs["cross_total"] + passT
    globs["cross_num"] += 1
        
    return S


def crossVarsB(N, neighbors, S1, S2):
    startT = time.time()
    V1 = [i for i in range(len(N))]
    V2 = []
    while len(V1) > len(V2):
        ran_v = random.randint(0, len(V1)-1) 
        V2.append(V1[ran_v])
        V1.remove(V1[ran_v])

    n = globs["size"]
    Id = 0
    from helpfuncs import B_dict
    with open("allen.identity") as f:
        Id = B_dict[f.readline().strip()]
    if n <= 8:
        N1 = tuple([array('B',[B_dict['DALL'] if i != j else Id for i in range(len(neighbors))]) for j in range(len(neighbors))])
        N2 = tuple([array('B',[B_dict['DALL'] if i != j else Id for i in range(len(neighbors))]) for j in range(len(neighbors))])
    elif n <= 16:
        N1 = tuple([array('H',[B_dict['DALL'] if i != j else Id for i in range(len(neighbors))]) for j in range(len(neighbors))])
        N2 = tuple([array('H',[B_dict['DALL'] if i != j else Id for i in range(len(neighbors))]) for j in range(len(neighbors))])
    else:
        N1 = tuple([array('I',[B_dict['DALL'] if i != j else Id for i in range(len(neighbors))]) for j in range(len(neighbors))])
        N2 = tuple([array('I',[B_dict['DALL'] if i != j else Id for i in range(len(neighbors))]) for j in range(len(neighbors))])
        
    for i in range(len(N1)):
        for j in range(i+1, len(N1)):
            if i in V1 and j in V1:
                N1[i][j] = S1[i][j]
                N1[j][i] = S1[j][i]
                N2[i][j] = S2[i][j]
                N2[j][i] = S2[j][i]
            elif i in V2 and j in V2:
                N1[i][j] = S2[i][j]
                N1[j][i] = S2[j][i]
                N2[i][j] = S1[i][j]
                N2[j][i] = S1[j][i]

    a1 = alpha(N, N1)
    a2 = alpha(N, N2)
    if a1 <= a2:
        S = N1
    else:
        S = N2

    unsele_edges = []
    for i in range(len(neighbors)):
        for j in neighbors[i]:
            baselist = bitdecoding(S[i][j])
            if j > i and len(baselist) > 1:
                unsele_edges.append((i, j))

    while unsele_edges:  # if there exist some edges need to be handled
        ran_e = random.randint(0, len(unsele_edges)-1) 
        u, v = unsele_edges[ran_e]

        if S[u][v] & N[u][v] != 0:
            rel = S[u][v] & N[u][v]
        else:
            rel = S[u][v]

        rellist = bitdecoding(rel)
        ran_b = random.randint(0, len(rellist)-1)
        S[u][v] = rellist[ran_b] 
        S[v][u] = inv(rellist[ran_b])

        unsele_edges.remove(unsele_edges[ran_e])
                
        # G-consistent
        ppc(S, neighbors) #path consistency on the initial graph (partial)
        
    return S

def crossVarsC(N, neighbors, S1, S2):
    startT = time.time()
    V1 = [i for i in range(len(N))]
    V2 = []
    for i in range(len(neighbors)):
        for j in neighbors[i]:
            if N[i][j] & S1[i][j] == 0 and j > i:

                if i in V1:
                    V1.remove(i)
                    V2.append(i)
                if j in V1:
                    V1.remove(j)
                    V2.append(j)

    n = globs["size"]
    Id = 0
    from helpfuncs import B_dict
    with open("allen.identity") as f:
        Id = B_dict[f.readline().strip()]
    if n <= 8:
        S = tuple([array('B',[B_dict['DALL'] if i != j else Id for i in range(len(neighbors))]) for j in range(len(neighbors))])
    elif n <= 16:
        S = tuple([array('H',[B_dict['DALL'] if i != j else Id for i in range(len(neighbors))]) for j in range(len(neighbors))])
    else:
        S = tuple([array('I',[B_dict['DALL'] if i != j else Id for i in range(len(neighbors))]) for j in range(len(neighbors))])
        
    for i in range(len(S)):
        for j in range(i+1, len(S)):
            if i in V1 and j in V1:
                S[i][j] = S1[i][j]
                S[j][i] = S1[j][i]
            elif i in V2 and j in V2:
                S[i][j] = S2[i][j]
                S[j][i] = S2[j][i]

    unsele_edges = []
    for i in range(len(neighbors)):
        for j in neighbors[i]: 
            baselist = bitdecoding(S[i][j])
            if j > i and len(baselist) > 1:
                unsele_edges.append((i, j))

    while unsele_edges:  # if there exist some edges need to be handled
        ran_e = random.randint(0, len(unsele_edges)-1) 
        u, v = unsele_edges[ran_e]

        if S[u][v] & N[u][v] != 0:
            rel = S[u][v] & N[u][v]
        else:
            rel = S[u][v]

        rellist = bitdecoding(rel)
        ran_b = random.randint(0, len(rellist)-1) 
        S[u][v] = rellist[ran_b] 
        S[v][u] = inv(rellist[ran_b])

        unsele_edges.remove(unsele_edges[ran_e]) 
                
        # G-consistent
        if not ppc(S, neighbors): #path consistency on the initial graph (partial)
            print("Inconsistency occurs in crossConsB")
            return None

    passT = time.time() - startT
    globs["cross_total"] = globs["cross_total"] + passT
    globs["cross_num"] += 1
        
    return S

def crossConsA(N, neighbors, S1, S2):
    startT = time.time()
    n = globs["size"]
    Id = 0f
    from helpfuncs import B_dict
    with open("allen.identity") as f:
        Id = B_dict[f.readline().strip()]
    if n <= 8:
        S = tuple([array('B',[B_dict['DALL'] if i != j else Id for i in range(len(neighbors))]) for j in range(len(neighbors))])
    elif n <= 16:
        S = tuple([array('H',[B_dict['DALL'] if i != j else Id for i in range(len(neighbors))]) for j in range(len(neighbors))])
    else:
        S = tuple([array('I',[B_dict['DALL'] if i != j else Id for i in range(len(neighbors))]) for j in range(len(neighbors))])

    # constraint of each edge is set as a random base relation
    unsele_edges = []
    for i in range(len(neighbors)):
        for j in neighbors[i]:  # each edge
            baselist = bitdecoding(S[i][j])
            if j > i and len(baselist) > 1:
                unsele_edges.append((i, j))

    while unsele_edges:  # if there exist some edges need to be handled
        ran_e = random.randint(0, len(unsele_edges)-1) 
        u, v = unsele_edges[ran_e]

        ran_s = random.randint(0, 1)
        if ran_s == 0:
            S_1 = S1
            S_2 = S2
        else:
            S_1 = S2
            S_2 = S1
        if S[u][v] & N[u][v] != 0:
            rel = S[u][v] & N[u][v]
        else:
            rel = S[u][v]

        if S_1[u][v] & rel != 0:
            rel = S_1[u][v] & rel
        elif S_2[u][v] & rel != 0:
            rel = S_2[u][v] & rel

        baselist = bitdecoding(rel)
        ran_b = random.randint(0, len(baselist)-1) 
        b = baselist[ran_b]
        S[u][v] =  b 
        S[v][u] = inv(b)

        unsele_edges.remove(unsele_edges[ran_e]) 
                
        # G-consistent
        if not ppc(S, neighbors): 
            print("Inconsistency occurs in crossConsB")
            return None

    passT = time.time() - startT
    globs["cross_total"] = globs["cross_total"] + passT
    globs["cross_num"] += 1
    return S

def crossConsB(N, neighbors, S1, S2):
    startT = time.time()
    n = globs["size"]
    Id = 0
    from helpfuncs import B_dict
    with open("allen.identity") as f:
        Id = B_dict[f.readline().strip()]
    if n <= 8:
        S = tuple([array('B',[B_dict['DALL'] if i != j else Id for i in range(len(neighbors))]) for j in range(len(neighbors))])
    elif n <= 16:
        S = tuple([array('H',[B_dict['DALL'] if i != j else Id for i in range(len(neighbors))]) for j in range(len(neighbors))])
    else:
        S = tuple([array('I',[B_dict['DALL'] if i != j else Id for i in range(len(neighbors))]) for j in range(len(neighbors))])

    # constraint of each edge is set as a random base relation

    unsele = []
    unsele_not0 = []
    unsele_0 = []
    
    for i in range(len(neighbors)):
        for j in neighbors[i]: 
            baselist = bitdecoding(S[i][j])
            if j > i and len(baselist) > 1:
                unsele.append((i, j))

    for (i, j) in unsele:
        if N[i][j] & S[i][j] == 0:
            unsele_0.append((i, j))
        else:
            unsele_not0.append((i, j))

    while unsele:  # while there exist unhandled edges

        if unsele_not0:  # if there exist some edges need to be handled which has common relation with the target QCN
            ran_e = random.randint(0, len(unsele_not0)-1) 
            u, v = unsele_not0[ran_e]

            ran_s = random.randint(0, 1)
            if ran_s == 0:
                S_1 = S1
                S_2 = S2
            else:
                S_1 = S2
                S_2 = S1
            
            if S[u][v] & N[u][v] != 0:
                rel = S[u][v] & N[u][v]
            else:
                rel = S[u][v]

            if S_1[u][v] & rel != 0:
                rel = S_1[u][v] & rel
            elif S_2[u][v] & rel != 0:
                rel = S_2[u][v] & rel

            baselist = bitdecoding(rel)
            if len(baselist) > 1:
                ran_b = random.randint(0, len(baselist)-1) 
            elif len(baselist) > 0:
                ran_b = 0
            else:
                print(rel)
                print(baselist)
                print("crossover baselist 0 elements in unsele_not0")
                return None
            b = baselist[ran_b]
            S[u][v] =  b 
            S[v][u] = inv(b)

            unsele.remove(unsele[ran_e]) 
            unsele_not0.remove(unsele_not0[ran_e]) 
                    
            # G-consistent
            if not ppc(S, neighbors): 
                print("Inconsistency occurs in crossConsB")
                return None

            for (i, j) in unsele_not0:
                if N[i][j] & S[i][j] == 0:
                    unsele_0.append((i, j))
                    unsele_not0.remove((i, j))

        elif unsele_0:  # if there exist some edges need to be handled
            ran_e = random.randint(0, len(unsele_0)-1) 
            u, v = unsele_0[ran_e]

            ran_s = random.randint(0, 1)
            if ran_s == 0:
                S_1 = S1
                S_2 = S2
            else:
                S_1 = S2
                S_2 = S1
            
            if S[u][v] & N[u][v] != 0:
                rel = S[u][v] & N[u][v]
            else:
                rel = S[u][v]

            if S_1[u][v] & rel != 0:
                rel = S_1[u][v] & rel
            elif S_2[u][v] & rel != 0:
                rel = S_2[u][v] & rel

            baselist = bitdecoding(rel)
            if len(baselist) > 1:
                ran_b = random.randint(0, len(baselist)-1) 
            elif len(baselist) > 0:
                ran_b = 0
            else:
                print("crossover baselist 0 elements")
                return None
            b = baselist[ran_b]
            S[u][v] =  b 
            S[v][u] = inv(b)

            unsele.remove(unsele[ran_e])
            unsele_0.remove(unsele_0[ran_e])
                
            # G-consistent
            if not ppc(S, neighbors): 
                print("Inconsistency occurs in crossConsB")
                return None

    passT = time.time() - startT
    globs["cross_total"] = globs["cross_total"] + passT
    globs["cross_num"] += 1
    
    return S

def crossConsC(N, neighbors, S1, S2, d):
    startT = time.time()
    n = globs["size"]
    Id = 0
    from helpfuncs import B_dict
    with open("allen.identity") as f:
        Id = B_dict[f.readline().strip()]
    if n <= 8:
        S = tuple([array('B',[B_dict['DALL'] if i != j else Id for i in range(len(neighbors))]) for j in range(len(neighbors))])
    elif n <= 16:
        S = tuple([array('H',[B_dict['DALL'] if i != j else Id for i in range(len(neighbors))]) for j in range(len(neighbors))])
    else:
        S = tuple([array('I',[B_dict['DALL'] if i != j else Id for i in range(len(neighbors))]) for j in range(len(neighbors))])

    # constraint of each edge is set as a random base relation

    nbloops = 0

    a1 = alpha(N, S1)
    a2 = alpha(N, S2)

    if a1 <= a2:
        S_fst = S1
        S_scd = S2
    else:
        S_fst = S2
        S_scd = S1

    unsele = []
    unsele_not0 = []
    unsele_0 = []
    
    for i in range(len(neighbors)):
        for j in neighbors[i]: 
            baselist = bitdecoding(S[i][j])
            if j > i and len(baselist) > 1:
                unsele.append((i, j))

    for (i, j) in unsele:
        if N[i][j] & S[i][j] == 0:
            unsele_0.append((i, j))
        else:
            unsele_not0.append((i, j))

    while unsele:  # while there exist unhandled edges
        if unsele_not0:  # if there exist some edges need to be handled which has common relation with the target QCN
            ran_e = random.randint(0, len(unsele_not0)-1)
            u, v = unsele_not0[ran_e]

            nbloops += 1

            if nbloops % d == 0:
                S_1 = S_scd
                S_2 = S_fst
            else:
                S_1 = S_fst
                S_2 = S_scd
            
            if S[u][v] & N[u][v] != 0:
                rel = S[u][v] & N[u][v]
            else:
                rel = S[u][v]

            if S_1[u][v] & rel != 0:
                rel = S_1[u][v] & rel
            elif S_2[u][v] & rel != 0:
                rel = S_2[u][v] & rel

            baselist = bitdecoding(rel)
            if len(baselist) > 1:
                ran_b = random.randint(0, len(baselist)-1) 
            elif len(baselist) > 0:
                ran_b = 0
            else:
                print(rel)
                print(baselist)
                print("crossover baselist 0 elements in unsele_not0")
                return None
            b = baselist[ran_b]
            S[u][v] =  b 
            S[v][u] = inv(b)

            unsele.remove(unsele[ran_e]) 
            unsele_not0.remove(unsele_not0[ran_e]) 
                    
            # G-consistent
            if not ppc(S, neighbors): 
                print("Inconsistency occurs in crossConsC")
                return None
            
            for (i, j) in unsele_not0:
                if N[i][j] & S[i][j] == 0:
                    unsele_0.append((i, j))
                    unsele_not0.remove((i, j))
    
        elif unsele_0:  # if there exist some edges need to be handled which has no common relation with the target QCN
            ran_e = random.randint(0, len(unsele_0)-1) 
            u, v = unsele_0[ran_e]

            nbloops += 1

            if nbloops % d == 0:
                S_1 = S_scd
                S_2 = S_fst
            else:
                S_1 = S_fst
                S_2 = S_scd
            
            if S[u][v] & N[u][v] != 0:
                rel = S[u][v] & N[u][v]
            else:
                rel = S[u][v]

            if S_1[u][v] & rel != 0:
                rel = S_1[u][v] & rel
            elif S_2[u][v] & rel != 0:
                rel = S_2[u][v] & rel

            baselist = bitdecoding(rel)
            if len(baselist) > 1:
                ran_b = random.randint(0, len(baselist)-1) 
            elif len(baselist) > 0:
                ran_b = 0
            else:
                print("crossover baselist 0 elements")
                return None
            b = baselist[ran_b]
            S[u][v] =  b 
            S[v][u] = inv(b)

            unsele.remove(unsele[ran_e])
            unsele_0.remove(unsele_0[ran_e])
                    
            # G-consistent
            if not ppc(S, neighbors): #path consistency on the initial graph (partial)
                print("Inconsistency occurs in crossConsC")
                return None

    passT = time.time() - startT
    globs["cross_total"] = globs["cross_total"] + passT
    globs["cross_num"] += 1

    return S


def crossConsD(N, neighbors, S1, S2):
    startT = time.time()
    n = globs["size"]
    Id = 0
    from helpfuncs import B_dict
    with open("allen.identity") as f:
        Id = B_dict[f.readline().strip()]
    if n <= 8:
        S = tuple([array('B',[B_dict['DALL'] if i != j else Id for i in range(len(neighbors))]) for j in range(len(neighbors))])
    elif n <= 16:
        S = tuple([array('H',[B_dict['DALL'] if i != j else Id for i in range(len(neighbors))]) for j in range(len(neighbors))])
    else:
        S = tuple([array('I',[B_dict['DALL'] if i != j else Id for i in range(len(neighbors))]) for j in range(len(neighbors))])

    # constraint of each edge is set as a random base relation
    unsele = []
    unsele_not0 = []
    unsele_0 = []
    
    for i in range(len(neighbors)):
        for j in neighbors[i]: 
            baselist = bitdecoding(S[i][j])
            if j > i and len(baselist) > 1:
                unsele.append((i, j))

    for (i, j) in unsele:
        if N[i][j] & S[i][j] == 0:
            unsele_0.append((i, j))
        else:
            unsele_not0.append((i, j))


    while unsele:  # while there exist unhandled edges

        if unsele_not0:  # if there exist some edges need to be handled which has common relation with the target QCN
            ran_e = random.randint(0, len(unsele_not0)-1) 
            u, v = unsele_not0[ran_e]

            if S[u][v] & N[u][v] != 0:
                rel = S[u][v] & N[u][v]
            else:
                rel = S[u][v]

            if S1[u][v] & rel != 0:
                rel = S1[u][v] & rel
            elif S2[u][v] & rel != 0:
                rel = S2[u][v] & rel

            baselist = bitdecoding(rel)
            if len(baselist) > 1:
                ran_b = random.randint(0, len(baselist)-1) 
            elif len(baselist) > 0:
                ran_b = 0
            else:
                print("crossover baselist 0 elements")
                return None
            b = baselist[ran_b]
            S[u][v] =  b 
            S[v][u] = inv(b)

            unsele.remove(unsele[ran_e]) 
            unsele_not0.remove(unsele_not0[ran_e]) 
                    
            # G-consistent
            if not ppc(S, neighbors): 
                print("Inconsistency occurs in crossConsD")
                return None
            
            for (i, j) in unsele_not0:
                if N[i][j] & S[i][j] == 0:
                    unsele_0.append((i, j))
                    unsele_not0.remove((i, j))
    
        elif unsele_0: 
            ran_e = random.randint(0, len(unsele_0)-1) 
            u, v = unsele_0[ran_e]
            
            if S[u][v] & N[u][v] != 0:
                rel = S[u][v] & N[u][v]
            else:
                rel = S[u][v]

            if S1[u][v] & rel != 0:
                rel = S1[u][v] & rel
            elif S2[u][v] & rel != 0:
                rel = S2[u][v] & rel

            baselist = bitdecoding(rel)
            if len(baselist) > 1:
                ran_b = random.randint(0, len(baselist)-1) 
            elif len(baselist) > 0:
                ran_b = 0
            else:
                print("crossover baselist 0 elements")
                return None
            b = baselist[ran_b]
            S[u][v] =  b 
            S[v][u] = inv(b)

            unsele.remove(unsele[ran_e])
            unsele_0.remove(unsele_0[ran_e])
                    
            # G-consistent
            if not ppc(S, neighbors):
                print("Inconsistency occurs in crossConsD")
                return None

    passT = time.time() - startT
    globs["cross_total"] = globs["cross_total"] + passT
    globs["cross_num"] += 1

    return S

