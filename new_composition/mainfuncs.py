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

    # output the input information
    print("***** EAMQ with the New Version of Composition Handling")
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

    # initialize global variables
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

                # if it is the first QCN
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

                    # if the directory has not been created yet
                    if not os.path.exists(results_dir):
                        os.makedirs(results_dir)
                    if not os.path.exists(loopsInfo_dir):
                        os.makedirs(loopsInfo_dir)
                    if not os.path.exists(triangle_dir) and options.triangle:
                        os.makedirs(triangle_dir)
                    if not os.path.exists(inputQCN_dir) and options.singleFile:
                        os.makedirs(inputQCN_dir)

                # load the input QCN
                TypeId, ConMatrix, ConMatrixS = init(buffer, inputQCN_dir, operator, options.singleFile)

                
                buffer = []

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
                    fill = FIC(ConMatrix, neighbors, a, a_)  # find all edges need to be added

                    neighbors = tuple([set([]) for i in range(len(ConMatrix))])  # find neighbors in the chordal graph
                    incident = [[] for i in range(len(ConMatrix))]

                    for i,j in fill:
                        incident[j].append(i) 

                    for m, i in enumerate(incident): 
                        fills = []
                        for n in i:
                            fills.append((n,m))
                            neighbors[m].add(n) 
                            neighbors[n].add(m)  # add neighbors

                    if options.triangle:
                        from outputtri import outputTriangulation
                        outputTriangulation(TypeId, neighbors, triangle_dir, operator)  # output chordal graphs

                    if_except = 0

                    from eamqfunc import EAMQ
                    
                    try:
                        print("QCN No.", globs["qcnNo"])  # output the QCN nubmer which is started to be processed
                        filename =  loopsInfo_dir + "LoopsInfo-" + str(globs["qcnNo"])
                        f = open(filename, "w")
                        EAMQ(operator, ConMatrix, neighbors, cardP, cardBest, divT, loopsInfo_dir, f, consC)  # the main algorithm EAMQ
                        f.close()
                    except KeyboardInterrupt:
                        print("Interrupt")
                    except Exception as e:
                        print("Exception: ", e)
                        if_except = 1
                    
                    if if_except == 0:  # if no exception is catched, record the data
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
            from outputInfo import outputInformation  # after all QCNs are processed, output the information of total QCNs
            outputInformation(results_dir, operator, TypeId, timeout, cardP, cardBest, divT, total_time, all_ppc_time, all_ppc_num, all_cross_time, all_cross_num)

if __name__ == '__main__':
   sys.exit(main())     
