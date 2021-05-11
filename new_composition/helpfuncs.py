from functools import reduce
from glob import globs

B_dict = {}
B_dict_reverse = {}
B_dict_store = {}

with open("allen.relations") as f:
   for i, j in enumerate(f):
      B_dict[j.strip()] = 2**i
      B_dict_reverse[2**i] =  j.strip()
      B_dict_store[j.strip()] = i

   B_dict['DALL'] = 2**(i+1) - 1 


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
N = globs["size"]
bsplit = [(len(bitdecoding(i+1)),bitdecoding(i+1)) for i in range((2**N)-1)]

# calculate compositions
def complex_relations(i, j):
    ij = 0  # initialize the composition of the constraint i and the constraint j

    i_base_rs = bitdecoding(i) # set of base relations of i
    j_base_rs = bitdecoding(j) # set of base relations of j
    
    for r_i in i_base_rs: 
        for r_j in j_base_rs: 
            # for each base relation in i and in j, calculate the composition
            num_r = fcomp[B_dict_store[B_dict_reverse[r_i]]][B_dict_store[B_dict_reverse[r_j]]]
            ij = ij | num_r  # add it to the composition of i and j

    return ij


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
   
   return relsnum_inv

