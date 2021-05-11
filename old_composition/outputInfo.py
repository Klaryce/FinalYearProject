from __future__ import division
import os
from glob import globs


def outputInformation(results_dir, operator, TypeId, timeout, cardP, cardBest, divT, total_time, all_ppc_time, all_ppc_num, all_cross_time, all_cross_num):

    filename =  results_dir + "Info"
    f = open(filename, "w")

    if all_ppc_num != 0:
        ppc_ave = all_ppc_time / all_ppc_num
        print("ppc time in average: %f. (total time: %f, number: %d)" % (ppc_ave, all_ppc_time, all_ppc_num), file=f)
    if all_cross_num != 0:
        cross_ave = all_cross_time / all_cross_num
        print("crossover time in average: %f. (total time: %f, number: %d)" % (cross_ave, all_cross_time, all_cross_num), file=f)
    if globs["all_cross_explore_num"] != 0:
        cross_explore_ave = globs["all_cross_explore_time"] / globs["all_cross_explore_num"]
        print("Neighbors exploring time in crossover step in average: %f. (total time: %f, number: %d)" % (cross_explore_ave, globs["all_cross_explore_time"], globs["all_cross_explore_num"]), file=f)
    if globs["fcomp_num"] != 0:
        fcomp_ave = globs["fcomp_total"] / globs["fcomp_num"]
        print("fcomp time in average: %f. (total time: %d, number: %d)" % (fcomp_ave, globs["fcomp_total"], globs["fcomp_num"]), file=f)
    if globs["process_num"] != 0:
        print("Total time: %f, number: %d, average: %f" % (total_time, globs["process_num"], total_time / globs["process_num"]), file=f)
        first_ave = globs["first_ite"] / globs["process_num"]
        last_ave = globs["last_ite"] / globs["process_num"]
        print("Total time of the first iteration: %f. Average time of the first iteration: %f" % (globs["first_ite"], first_ave), file=f)
        print("Total time of the last iteration: %f. Average time of the last iteration: %f" % (globs["last_ite"], last_ave), file=f)
        loops_ave = globs["total_loops"] / globs["process_num"]
        print("Total loops: %d. Average number of loops: %f." % (globs["total_loops"], loops_ave), file=f)
    
    print("Selection time: %f." % globs["select_time"], file=f)
    print("Selection step (before crossingover) in the first iteration: %f." % globs["ite_select_time"], file=f)
    print("Initialization time: %f." % globs["initial_time"], file=f)
    
    f.close()
