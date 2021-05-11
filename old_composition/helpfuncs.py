from functools import reduce
from glob import globs

B_dict = {}
B_dict_reverse = {}

with open("allen.relations") as f:
   for i, j in enumerate(f):
      B_dict[j.strip()] = 2**i
      B_dict_reverse[2**i] =  j.strip()

   B_dict['DALL'] = 2**(i+1) - 1 

N = globs["size"]

B = sorted(B_dict.values())[:-1]

# translate a base relation from integer to its string representation
def translate(BR):
   return B_dict_reverse[BR]

# translate a base relation from its string representation to integer
def translateR(BR):
   return B_dict[BR]

# split a relation into its base relation representation
def bitdecoding(b):
   l = []

   if b in B: return [b]

   if b == B_dict['DALL']: return B[:]

   l = [i for i in B if b&i != 0 and i <=b]

   return l

# initialize and fill list for set based on base relations
bsplit = [(len(bitdecoding(i+1)),bitdecoding(i+1)) for i in range((2**N)-1)]

inverseDict = {}

# initialize list with the inverses of all possible relations
with open("allen.conv") as f:
   for i in f:
      rel, irel = i.split('::')
      inverseDict[B_dict[rel.strip()]] = B_dict[irel.strip()]  # inverseDict[num] = num_of_inverse
   
inv = [(reduce(lambda x, y: x | y, [inverseDict[i] for i in bsplit[j][1]])) for j in range((2**N)-1)]