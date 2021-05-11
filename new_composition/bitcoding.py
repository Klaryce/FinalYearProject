# bit codes for our base relations to speed up composition


B_dict = {}
B_dict_reverse = {}
B_dict_store = {}

with open("allen.relations") as f:
   for i, j in enumerate(f):
      B_dict[j.strip()] = 2**i
      B_dict_reverse[2**i] =  j.strip()
      B_dict_store[j.strip()] = i

   B_dict['DALL'] = 2**(i+1) - 1 
