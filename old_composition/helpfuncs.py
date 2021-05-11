from bitcoding import B_dict, B_dict_reverse
from baserels import B

# translate a base relation from integer to its string representation
def translate(BR):
   return B_dict_reverse[BR]

# translate a base relation from its string representation to integer
def translateR(BR):
   return B_dict[BR]

# split a relation into its base relation representation
# 根据数字返回 base relations的数字列表
def bitdecoding(b):
   l = []

   if b in B: return [b]

   if b == B_dict['DALL']: return B[:]

   l = [i for i in B if b&i != 0 and i <=b]

   return l