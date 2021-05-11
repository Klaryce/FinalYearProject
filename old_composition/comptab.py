from functools import reduce
from helpfuncs import B_dict, B, bsplit
from glob import globs
import time

DALL = B_dict['DALL']
N = globs["size"]

# 存储两个基本关系组成的复合关系所对应的数字
def start(i, fcomp):
   relations, composition = i.split('::')
   relA, relB = relations.strip().split(':')
   composition = composition.replace(')','').replace('(','').strip().split()
   '''
   print(relA.strip())
   print(relB.strip())
   print(B_dict[relA.strip()]-1)
   print(B_dict[relB.strip()]-1)
   print(fcomp)
   print(fcomp[0][1])
   print(fcomp[0][15])
   print(fcomp[B_dict[relA.strip()]-1][B_dict[relB.strip()]-1])
   '''
   fcomp[B_dict[relA.strip()]-1][B_dict[relB.strip()]-1] = reduce(lambda x, y: x | y, [B_dict[i] for i in composition])

# 完善所有可能的复合关系
def complete(fcomp):
   for i in range((2**N)-1):
      for j in range((2**N)-1): # 用 i 和 j 遍历所有关系的两两搭配 （包括复合关系
         comp = 0 
   
         for m in bsplit[i][1]:  # bsplit返回每个数字代表的关系中的基本关系代表的数字的集合. m是i代表的关系中的每个基本关系对应的数字
            for n in bsplit[j][1]: # n是j代表的关系中的每个基本关系对应的数字
               comp |= fcomp[m-1][n-1] # comp = comp|fcomp[m-1][n-1]. fcomp[m-1][n-1] 是 m与n的复合关系所代表的数字（m和n作或运算的结果
               if comp == DALL: 
                  break # stop calculating if the global relation
            else:
               continue  # executed if the loop ended normally (no break)
            break  # executed if 'continue' was skipped (break)
           
         fcomp[i][j] = comp

startT = time.time()
# initialize matrix to hold compositions between all 256 possible relations
with open("allen.comp") as f:

   from array import array
   if N <= 8:
      fcomp = [array('B',[0 for i in range((2**N)-1)]) for j in range((2**N)-1)]
   elif N <= 16:
      fcomp = [array('H',[0 for i in range((2**N)-1)]) for j in range((2**N)-1)]
   else:
      fcomp = [array('I',[0 for i in range((2**N)-1)]) for j in range((2**N)-1)]
  
   for i in f:
      # print(i)
      start(i,fcomp)

   complete(fcomp)

passT = time.time() - startT
globs["fcomp_total"] += passT
globs["fcomp_num"] += 1

