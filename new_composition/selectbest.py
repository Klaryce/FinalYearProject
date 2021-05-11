from helpfuncs import B_dict

def alpha(N, S):
    if len(N) != len(S):  # two QCNs have different number of variables
        return -1
    summ = 0
    for i in range(len(N)):
        for j in range(len(N[i])):
            if N[i][j] & S[i][j] == 0 and N[i][j] != B_dict["="]:
                summ += 1
    a = 0.5 * summ  # each constraint is calculated twice
    return a

def selectBestScenarios(N, SSet, n):
    aList = []
    for i in range(len(SSet)):
        S = SSet[i]
        a = alpha(N, S)
        aList.append((S, a))
    sorted_aList = sorted(aList, key=lambda x: x[1])  # sort
    if n > len(SSet):
        n = len(SSet)
    SList = []
    for i in range(n):
        Si, ai = sorted_aList[i]
        SList.append(Si)
    return SList
