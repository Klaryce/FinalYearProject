import sys
import time
import os
from array import array
from glob import globs, setGlobals


def fileLen(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def init(buffer, inputQCN_dir, operator, otpt):
    # create spatial variables of specified number
    temp = buffer.pop(0)
    Vars = int(temp.split()[0].strip())+2
    TypeId = temp.split()[1].strip()

    # initialize constraints
    N = fileLen("allen.relations")
    setGlobals("size", N)
    Id = 0
    from bitcoding import B_dict
    with open("allen.identity") as f:
        Id = B_dict[f.readline().strip()]
    if N <= 8:
        ConMatrix = tuple([array('B',[B_dict['DALL'] if i != j else Id for i in range(Vars)]) for j in range(Vars)])
        ConMatrixS = tuple([array('B',[0 if i != j else Id for i in range(Vars)]) for j in range(Vars)])
    elif N <= 16:
        ConMatrix = tuple([array('H',[B_dict['DALL'] if i != j else Id for i in range(Vars)]) for j in range(Vars)])
        ConMatrixS = tuple([array('H',[0 if i != j else Id for i in range(Vars)]) for j in range(Vars)])
    else:
        ConMatrix = tuple([array('I',[B_dict['DALL'] if i != j else Id for i in range(Vars)]) for j in range(Vars)])
        ConMatrixS = tuple([array('I',[0 if i != j else Id for i in range(Vars)]) for j in range(Vars)])

    # parse spatial CSP
    from parsecsp import parsecsp
    parsecsp(ConMatrix, buffer, TypeId, Vars, inputQCN_dir, operator, otpt)

    return TypeId, ConMatrix, ConMatrixS

# main function
def main(argv=None):

    if argv is None:
        argv = sys.argv

    # set some sys useful stuff
    sys.setrecursionlimit(1<<30)
    sys.setcheckinterval(10000)

    from optparse import OptionParser

    # initialize parser for command line arguments
    parser = OptionParser()
    
    # set parsing options
    # parser.add_option("-c", "--calculus", type="string", dest="calc", default="rcc8", help="interaction mode: rcc8, or allen [default: %default]")
    # parser.add_option("-m", "--method", type="string", dest="method", default="iterative", help="interaction mode: recursive, or iterative [default: %default]")
    # parser.add_option("-p", "--pcheuristic", type="string", dest="pcheuristic", default="none", help="interaction mode: none, or weighted [default: %default]")
    # parser.add_option("-s", "--split", type="string", dest="split", default="horn", help="interaction mode: base, or horn [default: %default]")
    # parser.add_option("-d", "--print", action="store_true", dest="printsol", help="print solution to output")
    # parser.add_option("-z", "--pc", action="store_true", dest="pc", help="path consistency only")
    # parser.add_option("-t", "--trivial", action="store_true", dest="trivial", help="extra path consistency on the initial graph")
    # parser.add_option("-e", "--heuristic", type="string", dest="heuristic", default="global", help="interaction mode: global, local, or none [default: %default]")
    parser.add_option("-f", "--file", action="store", type="string", dest="filename", default="size16-edges8-9QCNs-consistent")
    parser.add_option("-o", "--operator", action="store", type="string", dest="operator", default="crossConsB", help="crossConsA, crossConsB, crossConsC, crossConsD, crossVarsA, crossVarsB, or crossVarsC")
    parser.add_option("-p", "--cardP", action="store", type="int", dest="cardP", default=50)
    parser.add_option("-b", "--cardBest", action="store", type="int", dest="cardBest", default=20)
    parser.add_option("-d", "--divT", action="store", type="int", dest="divT", default=50)
    parser.add_option("-t", "--timeout", action="store", type="int", dest="timeout", default=1800)
    parser.add_option("-n", "--name", action="store", type="string", dest="pname", default="default")
    parser.add_option("-c", "--consC", action="store", type="int", dest="consC", default=7)
    parser.add_option("-i", "--singleFile", action="store_true", dest="singleFile")
    parser.add_option("-r", "--triangle", action="store_true", dest="triangle")

    # parse command line arguments
    options, args = parser.parse_args()

    filename = "QCN-files/" + options.filename
    operator = options.operator
    cardP = options.cardP
    cardBest = options.cardBest
    divT = options.divT
    timeout = options.timeout
    name = options.pname
    consC = options.consC
    setGlobals("otpt", options.singleFile)

    if not os.access(filename, os.F_OK):
        print("File %s does not exist." % filename)
        return

    print("***** EAMQ with the Original Version of Composition Handling")
    print("***** QCNs read from: %s" % filename)
    print("***** Operator: %s" % operator)
    if operator == "crossConsC":
        print("***** Parameter of crossConsC: %d" % consC)
    print("***** cardP: %s" % cardP)
    print("***** cardBest: %s" % cardBest)
    print("***** divT: %s" % divT)
    print("***** Timeout: %s" % timeout)
    print("***** Experiment Name: %s" % name)

    all_ppc_time = 0.0
    all_ppc_num = 0
    all_cross_time = 0.0
    all_cross_num = 0

    setGlobals("timeout", timeout)
    setGlobals("process_total", 0.0)
    setGlobals("process_num", 0)
    setGlobals("fcomp_total", 0.0)
    setGlobals("fcomp_num", 0)
    setGlobals("all_cross_explore_time", 0.0)
    setGlobals("all_cross_explore_num", 0)
    setGlobals("first_ite", 0.0)
    setGlobals("last_ite", 0.0)
    setGlobals("select_time", 0.0)
    setGlobals("ite_select_time", 0.0)
    setGlobals("initial_time", 0.0)
    setGlobals("total_loops", 0)

    with open(filename) as f:
        total = 0
        meter = 0
        buffer = []
        Sp = []
        setGlobals("qcnNo", 0)
        
        start = time.clock()
        for i in f:
            buffer.append(i)

            if i.strip() == '.':
                globs["qcnNo"] += 1

                if "QCN-files/" in filename:
                    filename = filename[10:]
                fn = ""
                for c in filename:
                    if c is not ".":
                        fn = fn + c
                    else:
                        break

                if globs["qcnNo"] == 1:
                    if operator == "crossConsC":
                        results_dir = "Results/" + str(name) + "/" + str(timeout) + "s-"  + str(cardP) + "-" + str(cardBest) + "-" + str(divT) + "/"+ fn + "/" + str(operator) + "-" + str(consC) + "/" 
                        loopsInfo_dir = "LoopsInfo/" + str(name) + "/" + str(timeout) + "s-"  + str(cardP) + "-" + str(cardBest) + "-" + str(divT) + "/"+ fn + "/" + str(operator) + "-" + str(consC) + "/"
                        triangle_dir = "Triangulations/" + str(name) + "/" + str(timeout) + "s-"  + str(cardP) + "-" + str(cardBest) + "-" + str(divT) + "/"+ fn + "/" + str(operator) + "-" + str(consC) + "/"
                        inputQCN_dir = "Input_singleQCNs/" + str(name) + "/" + str(timeout) + "s-"  + str(cardP) + "-" + str(cardBest) + "-" + str(divT) + "/"+ fn + "/" + str(operator) + "-" + str(consC) + "/"
                    else:
                        results_dir = "Results/" + str(name) + "/" + str(timeout) + "s-"  + str(cardP) + "-" + str(cardBest) + "-" + str(divT) + "/"+ fn + "/" + str(operator) + "/" 
                        loopsInfo_dir = "LoopsInfo/" + str(name) + "/" + str(timeout) + "s-"  + str(cardP) + "-" + str(cardBest) + "-" + str(divT) + "/"+ fn + "/" + str(operator) + "/"
                        triangle_dir = "Triangulations/" + str(name) + "/" + str(timeout) + "s-"  + str(cardP) + "-" + str(cardBest) + "-" + str(divT) + "/"+ fn + "/" + str(operator) + "/"
                        inputQCN_dir = "Input_singleQCNs/" + str(name) + "/" + str(timeout) + "s-"  + str(cardP) + "-" + str(cardBest) + "-" + str(divT) + "/"+ fn + "/" + str(operator) + "/"

                    if not os.path.exists(results_dir):
                        os.makedirs(results_dir)
                    if not os.path.exists(loopsInfo_dir):
                        os.makedirs(loopsInfo_dir)
                    if not os.path.exists(triangle_dir) and options.triangle:
                        os.makedirs(triangle_dir)
                    if not os.path.exists(inputQCN_dir) and options.singleFile:
                        os.makedirs(inputQCN_dir)

                    # if options.singleFile:
                    #     setGlobals("inputQCN_dir", inputQCN_dir)

                TypeId, ConMatrix, ConMatrixS = init(buffer, inputQCN_dir, operator, options.singleFile)

                
                buffer = [] # example文件里的每一行是两个节点和它们之间的relation，计算两个节点的复合关系的数字，存入ConMatrix里

                from triangulation import MCS, FIC
                from bitcoding import B_dict
                
                edjes = set([])

                neighbors = tuple([set([]) for i in range(len(ConMatrix))]) #tuple里的每个元素是conmatrix每一行组成的set

                DALL = B_dict['DALL']
                for i in range(len(ConMatrix)):
                    for j in range(i+1,len(ConMatrix)): #conmatrix对角线右上方 (为了不重复遍历)
                        if ConMatrix[i][j] != DALL: #如果不是全关系说明行和列对应的数字表示的节点是邻居
                            edjes.add((i,j))
                            neighbors[i].add(j)
                            neighbors[j].add(i)
    
                setGlobals("ppc_total", 0.0)
                setGlobals("ppc_num", 0)

                from ppc import pPC as ppc

                if (ppc(ConMatrix, neighbors)): #path consistency on the initial graph (partial)
                    
                    a, a_ = MCS(ConMatrix, neighbors)
                    fill = FIC(ConMatrix, neighbors, a, a_) #找到所有的要加进去的边（为了把图变成chordal的

                    neighbors = tuple([set([]) for i in range(len(ConMatrix))]) #哪一些变元是邻居，在chordal graph下
                    incident = [[] for i in range(len(ConMatrix))]

                    for i,j in fill:
                        incident[j].append(i) 

                    for m, i in enumerate(incident): 
                        fills = []
                        for n in i:
                            fills.append((n,m))
                            neighbors[m].add(n) 
                            neighbors[n].add(m)

                    if options.triangle:
                        from outputtri import outputTriangulation
                        outputTriangulation(TypeId, neighbors, triangle_dir, operator)

                    if_except = 0

                    from eamqfunc import EAMQ
                    
                    try:
                        print("QCN No.", globs["qcnNo"])
                        filename =  loopsInfo_dir + "LoopsInfo-" + str(globs["qcnNo"])
                        f = open(filename, "w")
                        EAMQ(operator, ConMatrix, neighbors, cardP, cardBest, divT, loopsInfo_dir, f, consC)
                        f.close()
                    except KeyboardInterrupt:
                        print("Interrupt")
                    except Exception as e:
                        print("Exception: ", e)
                        if_except = 1
                    
                    if if_except == 0:
                        print("+++++++++++++++++++++++after calling EAMQ, globs shown below")
                        if "passT" in globs.keys():
                            globs['process_total'] += globs["passT"]
                            globs['process_num'] += 1
                        if "nbloops" in globs.keys():
                            globs["total_loops"] += globs["nbloops"]
                        print(globs)
                        print("---------------------")
                        all_ppc_time += globs["ppc_total"]
                        all_ppc_num += globs["ppc_num"]
                        all_cross_time += globs["cross_total"]
                        all_cross_num += globs["cross_num"]
                        globs["all_cross_explore_time"] += globs["explore_aftcross_total"]
                        globs["all_cross_explore_num"] += globs["explore_aftcross_num"]
                        
                        from outputRes import outputResult
                        outputResult(results_dir, operator, TypeId, neighbors, timeout, cardP, cardBest, divT)
                else:
                    print("Input QCN inconsistent: No.%d" % globs["qcnNo"])
           
        if if_except == 0:
            total_time = time.clock() - start
            from outputInfo import outputInformation
            outputInformation(results_dir, operator, TypeId, timeout, cardP, cardBest, divT, total_time, all_ppc_time, all_ppc_num, all_cross_time, all_cross_num)
        
        
        '''        
        try:
            EAMQ(operator, ConMatrix, neighbors, cardP, cardBest, divT)
        except:
            KeyboardInterrupt
        '''
        '''
        EAMQ(operator, ConMatrix, neighbors, cardP, cardBest, divT)
        print("+++++++++++++++++++++++after calling EAMQ, globs shown below")
        print(globs)
        print("---------------------")
        '''
        # 调试selectbest
        '''
        print("ConMatrix is -------------------------------")
        print(ConMatrix)
        C1 = (array('H', [1, 4409, 2014, 6174, 4026, 4317, 2834, 2526, 2111, 2008, 8191]), array('H', [2265, 1, 2589, 6687, 6800, 6859, 6940, 7607, 7484, 8023, 8191]), array('H', [1982, 5147, 1, 4615, 3678, 444, 7127, 7129, 7449, 5402, 8191]), array('H', [6174, 7199, 3079, 1, 5711, 5423, 1758, 7259, 6670, 4636, 8191]), array('H', [6108, 7432, 5694, 3639, 1, 3033, 3005, 6448, 5839, 6555, 8191]), array('H', [2363, 7477, 474, 2775, 5561, 1, 1343, 4554, 3470, 7947, 8191]), array('H', [5260, 7322, 7599, 1854, 5595, 735, 1, 2332, 4669, 2321, 8191]), array('H', [4542, 7119, 7609, 6717, 6344, 2484, 4250, 1, 2004, 7946, 8191]), array('H', [4191, 6874, 6809, 7190, 3895, 5014, 3163, 1962, 1, 1981, 8191]), array('H', [1976, 7855, 2716, 3098, 6557, 7829, 4233, 7828, 4, 1, 8191]), array('H', [8191, 8191, 8191, 8191, 8191, 8191, 8191, 8191, 8191, 8191, 1]))
        C2 = (array('H', [1, 4409, 2014, 6174, 4026, 4317, 2834, 2526, 2111, 2008, 8191]), array('H', [2265, 1, 2589, 6687, 6800, 6859, 6940, 7607, 7484, 8023, 8191]), array('H', [1982, 5147, 1, 4615, 3678, 444, 7127, 7129, 7449, 5402, 8191]), array('H', [6174, 7199, 3079, 1, 5711, 5423, 1758, 7259, 6670, 4636, 8191]), array('H', [6108, 7432, 5694, 3639, 1, 3033, 3005, 6448, 5839, 6555, 8191]), array('H', [2363, 7477, 474, 2775, 5561, 1, 1343, 4554, 3470, 7947, 8191]), array('H', [5260, 7322, 7599, 1854, 5595, 735, 1, 2332, 4669, 2321, 8191]), array('H', [4542, 7119, 7609, 6717, 6344, 2484, 4250, 1, 10, 7946, 8191]), array('H', [4191, 6874, 6809, 7190, 3895, 5014, 3163, 1962, 1, 1981, 8191]), array('H', [1976, 7855, 2716, 3098, 6557, 7829, 4233, 7828, 4, 1, 8191]), array('H', [8191, 8191, 8191, 8191, 8191, 8191, 8191, 8191, 8191, 8191, 1]))
        C3 = (array('H', [1, 4409, 2014, 6174, 4026, 4317, 2834, 2526, 2111, 2008, 8191]), array('H', [2265, 1, 2589, 6687, 6800, 6859, 6940, 7607, 7484, 8023, 8191]), array('H', [1982, 5147, 1, 4615, 3678, 444, 7127, 7129, 7449, 5402, 8191]), array('H', [6174, 7199, 3079, 1, 5711, 5423, 1758, 7259, 6670, 4636, 8191]), array('H', [6108, 7432, 5694, 3639, 1, 3033, 3005, 6448, 5839, 6555, 8191]), array('H', [2363, 7477, 474, 2775, 5561, 1, 1343, 4554, 3470, 7947, 8191]), array('H', [5260, 7322, 7599, 1854, 5595, 32, 1, 2332, 4669, 2321, 8191]), array('H', [4542, 7119, 7609, 6717, 6344, 2484, 4250, 1, 10, 7946, 8191]), array('H', [4191, 6874, 6809, 7190, 3895, 5014, 3163, 1962, 1, 1981, 8191]), array('H', [1976, 7855, 2716, 3098, 6557, 7829, 4233, 7828, 4, 1, 8191]), array('H', [8191, 8191, 8191, 8191, 8191, 8191, 8191, 8191, 8191, 8191, 1]))
        C4 = (array('H', [1, 4409, 32, 6174, 4026, 4317, 2834, 2526, 2111, 2008, 8191]), array('H', [2265, 1, 2589, 6687, 6800, 6859, 6940, 7607, 7484, 8023, 8191]), array('H', [1982, 5147, 1, 4615, 3678, 444, 7127, 7129, 7449, 5402, 8191]), array('H', [6174, 7199, 3079, 1, 5711, 5423, 1758, 7259, 6670, 4636, 8191]), array('H', [6108, 7432, 5694, 3639, 1, 3033, 3005, 6448, 5839, 6555, 8191]), array('H', [2363, 7477, 474, 2775, 5561, 1, 1343, 4554, 3470, 7947, 8191]), array('H', [5260, 7322, 7599, 1854, 5595, 32, 1, 2332, 4669, 2321, 8191]), array('H', [4542, 7119, 7609, 6717, 6344, 2484, 4250, 1, 10, 7946, 8191]), array('H', [4191, 6874, 6809, 7190, 3895, 5014, 3163, 1962, 1, 1981, 8191]), array('H', [1976, 7855, 2716, 3098, 6557, 7829, 4233, 7828, 4, 1, 8191]), array('H', [8191, 8191, 8191, 8191, 8191, 8191, 8191, 8191, 8191, 8191, 1]))
        from selectbest import selectBestScenarios
        testset = []
        testset.append(C4)
        testset.append(C2)
        testset.append(C3)
        testset.append(C1)
        resultlist = selectBestScenarios(ConMatrix, testset, 2)
        print("result is -------------------")
        for k in resultlist:
            print(k)
            print()
        '''

        # 调试crossvarsA
        '''
        from random_scenario import randomScenario
        from exploreNeighbor import exploreNeighborhood
        for k in range(2):
            S = randomScenario(neighbors)
            # print("S is -------------------------")
            # print(S)
            bestNg = exploreNeighborhood(ConMatrix, S, neighbors)
            Sp.append(bestNg)
            # print(bestNg)
            # print()
  
        print("Neighbors of random scenarios are ----------------------------")
        print(Sp[0])
        print("and")
        print(Sp[1])
        from crossover import crossConsB
        crossS = crossConsB(ConMatrix, neighbors, Sp[0], Sp[1])
        print("crossS is -------------------------------")
        print(crossS)
        '''

        # 调试EAMQ
        '''
        print(ConMatrix)
        print("----------------------------")
        from eamqfunc import EAMQ
        result = EAMQ(ConMatrix, neighbors, 4, 2, 5, 5)
        from outputRes import outputResult
        outputResult(TypeId, result, neighbors)
        print("-------------result--------------")
        print(result)
        '''

if __name__ == '__main__':
   sys.exit(main())     
