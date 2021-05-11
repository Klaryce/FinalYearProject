from __future__ import division
import os
from helpfuncs import bitdecoding
from bitcoding import B_dict_reverse
from glob import globs


def outputResult(results_dir, operator, TypeId, neighbors, timeout, cardP, cardBest, divT):
    
    filename =  results_dir + "Result-" + operator + TypeId
    f = open(filename, "w")

    if "best_a" in globs.keys():
        a = globs["best_a"]
        print("Alpha: %s" % a)
        print("Alpha: %s" % a, file=f)
    if "nbloops" in globs.keys():
        nbloops = globs["nbloops"]
        loopstr = str(nbloops)
        print("Number of loops: %s" % loopstr, file=f)
    if "passT" in globs.keys():
        passT = globs["passT"]
        passTstr = str(passT)
        print("Processing time: %s" % passTstr, file=f)
    if globs["process_num"] != 0:
        process_ave =  globs["process_total"] / globs["process_num"]
        print("Average processing time: %f. (total processing time: %f, number of QCNs: %d)" % (process_ave, globs["process_total"], globs["process_num"]), file=f)
    if globs["ppc_num"] != 0:
        ppc_ave = globs["ppc_total"] / globs["ppc_num"]
        print("ppc time in average: %f. (total time: %f, number: %d)" % (ppc_ave, globs["ppc_total"], globs["ppc_num"]), file=f)
    if globs["cross_num"] != 0:
        cross_ave = globs["cross_total"] / globs["cross_num"]
        print("crossover time in average: %f. (total time: %f, number: %d)" % (cross_ave, globs["cross_total"], globs["cross_num"]), file=f)
    if globs["explore_aftcross_num"] != 0:
        explore_aftcross_ave = globs["explore_aftcross_total"] / globs["explore_aftcross_num"]
        print("Neighbors exploring time in crossover step in average: %f. (total time: %f, number: %d)" % (explore_aftcross_ave, globs["explore_aftcross_total"], globs["explore_aftcross_num"]), file=f)
    if globs["fcomp_num"] != 0:
        fcomp_ave = globs["fcomp_total"] / globs["fcomp_num"]
        print("fcomp time in average: %f. (total time: %f, number: %d)" % (fcomp_ave, globs["fcomp_total"], globs["fcomp_num"]), file=f)

    vnum = len(neighbors)
    vnum -= 2
    if "best_scenario" in globs.keys():
        BestScenario = globs["best_scenario"]
        print("%d %s | GreedyFillIn" % (vnum, TypeId), file=f)
        for i in range(len(neighbors)):
            for j in neighbors[i]:
                if j > i:
                    rstr = ""
                    bsnum = BestScenario[i][j]
                    l = bitdecoding(bsnum)
                    for num in l:
                        b = B_dict_reverse[num]
                        rstr = rstr + b
                    print("%d %d (%s)" % (i, j, rstr), file=f)
        print(".", file=f)
    f.close()
