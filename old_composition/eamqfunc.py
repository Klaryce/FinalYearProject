
import time
import random
import sys
import threading
from time import sleep
try:
    import thread
except ImportError:
    import _thread as thread
from random_scenario import randomScenario
from exploreNeighbor import exploreNeighborhood
from selectbest import selectBestScenarios
from crossover import *
from selectbest import alpha
from glob import globs, setGlobals


def exit_after(s):
    '''
    use as decorator to exit process if 
    function takes longer than s seconds
    '''
    def outer(fn):
        def inner(*args, **kwargs):
            timer = threading.Timer(s, callback_func, args=None)
            timer.start()
            try:
                result = fn(*args, **kwargs)
            finally:
                timer.cancel()
            return result
        return inner
    return outer


def callback_func():
    print('超时回调')
    print("--------")
    # result = selectBestScenarios(N, SBest, 1)
    # globs["best_scenario"] = result[0]
    # a = alpha(N, SBest[0])
    # globs["best_a"] = a
    thread.interrupt_main() # raises KeyboardInterrupt

@exit_after(globs["timeout"])
def EAMQ(operator, N, G, cardp, cardBest, divT, loopsInfo_dir, f, consC):

    print("Enter the main algorithm EAMQ")
    startT = time.time()
    
    # Initialization Step
    SP = []
    SBest = []
    nbloops = 0
    timeoutL = globs["timeout"]
    setGlobals("cross_total", 0.0)
    setGlobals("cross_num", 0)
    setGlobals("explore_aftcross_total", 0.0)
    setGlobals("explore_aftcross_num", 0)
    setGlobals("nbloops", 0)
    setGlobals("passT", 0.0)

    for i in range(cardp):
        S0 = randomScenario(G)
        while S0 is None:
            S0 = randomScenario(G)
            print("random scenario none")
        S = exploreNeighborhood(N, S0, G)
        while S is None:
            S = exploreNeighborhood(N, S0, G)
            print("explore neighbor none")
        SP.append(S)

    print("After initialization")
    passT = time.time() - startT
    globs["initial_time"] += passT

    ite_passT = 0

    # Main Loop
    while passT < timeoutL:

        # Selection Step
        select_startT = time.time()
        SBest = selectBestScenarios(N, SP, cardBest)
        setGlobals("best_scenario", SBest[0])
        select_passT = time.time() - select_startT
        globs["select_time"] += select_passT

        a = alpha(N, SBest[0])
        setGlobals("best_a", a)
        passT = time.time()-startT
        globs["passT"] = passT

        globs["nbloops"] = nbloops

        if nbloops > 0:
            ite_passT = time.time() - ite_startT

        if nbloops == 1:
            globs["first_ite"] += ite_passT
            globs["ite_select_time"] += ite_select_passT
        
        print("Loop %d, elapsed time is %f, timeout is %d, a is %f." % (nbloops, passT, timeoutL, a))
        print("Loop %d, elapsed time is %f, timeout is %d, a is %f." % (nbloops, passT, timeoutL, a), file=f)
        
        if a < 0.00001 and a > -0.00001:
            setGlobals("best_scenario", SBest[0])
            setGlobals("best_a", a)
            globs["last_ite"] += ite_passT
            return 0
        
        ite_startT = time.time()
        nbloops += 1
        print("nbloops: %d" % nbloops)

        # New Generation Step
        if nbloops % divT != 0:
            # Crossover Step
            SG = []
            for i in range(cardp-cardBest):

                ran_best1 = random.randint(0, len(SBest)-1) # 随机选一个scenario
                ran_best2 = random.randint(0, len(SBest)-1) # 随机选一个scenario

                while ran_best1 == ran_best2:
                    ran_best2 = random.randint(0, len(SBest)-1) # 随机选一个scenario
                    if ran_best2 != ran_best1:  # 两个随机数不同
                        break
                    print("reselect best scenario randomly")
                    
                S1 = SBest[ran_best1]
                S2 = SBest[ran_best2]
                ite_select_passT = time.time() - startT

                #print("operation beginning")
                if operator == "crossConsA":
                    # print("consA")
                    S = crossConsA(N, G, S1, S2)
                elif operator == "crossConsB":
                    #print("consB")
                    S = crossConsB(N, G, S1, S2)
                elif operator == "crossVarsA":
                    #print("varsA")
                    S = crossVarsA(N, G, S1, S2)
                elif operator == "crossVarsB":
                    #print("varsB")
                    S = crossVarsB(N, G, S1, S2)
                elif operator == "crossVarsC":
                    #print("varsC")
                    S = crossVarsC(N, G, S1, S2)
                elif operator == "crossConsC":
                    S = crossConsC(N, G, S1, S2, consC)
                elif operator == "crossConsD":
                    S = crossConsD(N, G, S1, S2)
                else:
                    print("Invalid operator %s" % operator)
                    sys.exit()

                explore_startT = time.time()
                S = exploreNeighborhood(N, S, G)
                explore_passT = time.time() - explore_startT

                globs["explore_aftcross_total"] += explore_passT
                globs["explore_aftcross_num"] += 1

                SG.append(S)
            SP = SBest + SG
        else:
            # Diversification Step
            print("Diversification Step")
            print("Diversification Step", file=f)
            SBest1 = selectBestScenarios(N, SBest, 1)
            SP = SBest1
            for i in range(cardp-1):
                S = randomScenario(G)
                S = exploreNeighborhood(N, S, G)
                SP.append(S)

        # select_startT = time.time()
        # theBest = selectBestScenarios(N, SBest, 1)
        # select_passT = time.time() - select_startT
        # globs["select_time"] += select_passT

        # a = alpha(N, theBest[0])

        # passT = time.time()-startT
        # ite_passT = time.time() - ite_startT
        # setGlobals("best_scenario", theBest[0])
        # setGlobals("best_a", a)
        # globs["nbloops"] = nbloops
        # globs["passT"] = passT

        # if a < 0.00001 and a > -0.00001:
        #     print(ite_passT)
        #     globs["last_ite"] += ite_passT
        #     return 0
        # bo = passT < timeoutL
        # print("Elapsed time is %f, timeout is %d, a is %f." % (passT, timeoutL, a))
        # print("Elapsed time is %f, timeout is %d, a is %f." % (passT, timeoutL, a), file=f)
        # if nbloops == 1:
        #     print(ite_passT)
        #     globs["first_ite"] += ite_passT
        #     globs["ite_select_time"] += ite_select_passT

    # bo = passT < timeoutL
    # print("Time out. Elapsed time is %f, timeout is %d. Result of passT < timeoutL is %d" % (passT, timeoutL, bo))
    
    # 调试
    '''
    ran_best1 = random.randint(0, len(SBest)-1) # 随机选一个scenario
    while True:
        ran_best2 = random.randint(0, len(SBest)-1) # 随机选一个scenario
        if ran_best2 != ran_best1:  # 两个随机数不同
            break
    S1 = SBest[ran_best1]
    S2 = SBest[ran_best2]
    print(S1)
    print()
    print(S2)
    print()
    S = crossVarsA(N, G, S1, S2)  ####
    print(S)
    print()
    S = exploreNeighborhood(N, S, G)
    print(S)
    print()
    ''' 
    return 0
