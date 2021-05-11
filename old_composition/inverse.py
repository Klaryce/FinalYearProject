from bitcoding import B_dict
from helpfuncs import bitdecoding
from functools import reduce
from basesplit import bsplit
from glob import globs

inverseDict = {}
N = globs["size"]

# initialize list with the inverses of all possible relations
with open("allen.conv") as f:
   for i in f:
      rel, irel = i.split('::')
      inverseDict[B_dict[rel.strip()]] = B_dict[irel.strip()]  # inverseDict[num] = num_of_inverse
   
inv = [(reduce(lambda x, y: x | y, [inverseDict[i] for i in bsplit[j][1]])) for j in range((2**N)-1)]


'''
def inv(relsnum):
   l = bitdecoding(relsnum)
   l_inv = []

   inverseDict = {}

   # initialize list with the inverses of all possible relations
   with open("allen.conv") as f:
      for i in f:
         rel, irel = i.split('::')
         inverseDict[B_dict[rel.strip()]] = B_dict[irel.strip()]  # inverseDict[num_base] = num_invbase

   for j in l:
      j_inv = inverseDict[j]
      l_inv.append(j_inv)
   
   relsnum_inv = reduce(lambda x, y: x | y, l_inv)
   #print(relsnum_inv)
   return relsnum_inv
'''