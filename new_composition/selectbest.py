from bitcoding import B_dict

def alpha(N, S):
    if len(N) != len(S):
        return -1
    summ = 0
    for i in range(len(N)):
        for j in range(len(N[i])):
            #print("%d & %d = %d" % (N[i][j], S[i][j], N[i][j] & S[i][j]))
            if N[i][j] & S[i][j] == 0 and N[i][j] != B_dict["="]:
                summ += 1
                #print("summ is %d" % summ)
    a = 0.5 * summ
    return a

def selectBestScenarios(N, SSet, n):
    aList = []
    for i in range(len(SSet)):
        S = SSet[i]
        a = alpha(N, S)
        aList.append((S, a))
    sorted_aList = sorted(aList, key=lambda x: x[1])
    # print("sorted_aList is -----------------")
    # for item_ in sorted_aList:
    #     print(item_[1])
    # print("-----------------------------")
    if n > len(SSet):
        n = len(SSet)
    SList = []
    for i in range(n):
        Si, ai = sorted_aList[i]
        SList.append(Si)
    return SList
