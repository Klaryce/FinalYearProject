from bitcoding import B_dict, B_dict_reverse, B_dict_store
from helpfuncs import bitdecoding
from comptab import fcomp

# ##直接用数字
# # 根据复合关系数字返回由该复合关系所包含的所有基本关系组成的列表
# def comp_relations_decode(comp): # comp:复合关系数字
#     base_rs = []
#     l = bitdecoding(comp) #该复合关系包含的基本关系对应的数字组成的列表
#     for base_num in l:
#         r = B_dict_reverse[base_num] # 由基本关系数字找出基本关系
#         base_rs.append(r)
#     return base_rs

# 返回代表复合关系的数字
# 参数：求 i 和 j 的复合关系
def complex_relations(i, j):
    # 点i到点j的relation: ConMatrix[i][j]数字对应的基本关系集合： (r1, r2, r3)
    # 点j到点k的relation: ConMatrix[j][k]数字对应的基本关系集合： (r4, r5)
    # 求 ConMatrix[i][j] 和 ConMatrix[j][k]的复合关系
    # 即(r1, r2, r3)和(r4, r5)的复合关系
    ij = 0

    #将数字转换为基本关系集合
    i_base_rs = bitdecoding(i) # i的基本关系集合
    j_base_rs = bitdecoding(j) # j的基本关系集合
    
    for r_i in i_base_rs: # 对于ij中的每个base relation
        for r_j in j_base_rs: # 对于jk中的每个base relation
            # 该 jk base relation 的数字
            num_r = fcomp[B_dict_store[B_dict_reverse[r_i]]][B_dict_store[B_dict_reverse[r_j]]] # 这两个 base relation 的复合关系
            ij = ij | num_r # 取或，将这两个 base relation 构成的复合关系添加到 ij, jk 的复合关系中
    return ij

# testvalue = complex_relations(1339, 2332)
# print(testvalue)
# print(bitdecoding(1339))
# print(bitdecoding(4669))