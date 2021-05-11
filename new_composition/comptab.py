from functools import reduce
import time
from bitcoding import B_dict, B_dict_store
from baserels import B
from glob import globs

DALL = B_dict['DALL']
N = 13

# calculate and store compositions formed by base relations
def start(i, fcomp):
   relations, composition = i.split('::')
   relA, relB = relations.strip().split(':')
   composition = composition.replace(')','').replace('(','').strip().split()
   fcomp[B_dict_store[relA.strip()]][B_dict_store[relB.strip()]] = reduce(lambda x, y: x | y, [B_dict[i] for i in composition])

# initialize matrix to hold compositions between all 256 possible relations
startT = time.time()
with open("allen.comp") as f:

   from array import array
   if N <= 8:
      fcomp = [array('B',[0 for i in range(N)]) for j in range(N)]
   elif N <= 16:
      fcomp = [array('H',[0 for i in range(N)]) for j in range(N)]
   else:
      fcomp = [array('I',[0 for i in range(N)]) for j in range(N)]
  
   for i in f:
      start(i,fcomp)

passT = time.time() - startT
globs["fcomp_total"] += passT
globs["fcomp_num"] += 1



