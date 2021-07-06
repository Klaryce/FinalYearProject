
from helpfuncs import bitdecoding, B_dict_reverse
from glob import globs


def outputParent(operator, neighbors, S1, S2, nbloops):
    
    TypeId = globs["TypeId"]
    filename_x =  globs["parents_dir"] + "Parent-" + operator + TypeId + "-" + str(nbloops) + "-S1"
    filename_y =  globs["parents_dir"] + "Parent-" + operator + TypeId + "-" + str(nbloops) + "-S2"

    # output first parent
    f = open(filename_x, "w")

    print("Solution:", file=f)

    vnum = len(neighbors)
    vnum -= 2
    print("%d %s | GreedyFillIn" % (vnum, TypeId), file=f)
    for i in range(len(neighbors)):
        for j in neighbors[i]:
            if j > i:
                rstr = ""
                bsnum = S1[i][j]
                l = bitdecoding(bsnum)
                for num in l:
                    b = B_dict_reverse[num]
                    rstr = rstr + b
                print("%d %d (%s)" % (i, j, rstr), file=f)
    print(".", file=f)
    f.close()

    # output second parent
    f = open(filename_y, "w")

    print("Solution:", file=f)

    vnum = len(neighbors)
    vnum -= 2
    print("%d %s | GreedyFillIn" % (vnum, TypeId), file=f)
    for i in range(len(neighbors)):
        for j in neighbors[i]:
            if j > i:
                rstr = ""
                bsnum = S2[i][j]
                l = bitdecoding(bsnum)
                for num in l:
                    b = B_dict_reverse[num]
                    rstr = rstr + b
                print("%d %d (%s)" % (i, j, rstr), file=f)
    print(".", file=f)
    f.close()