import sys
import os
from helpfuncs import translateR, inv
# from inverse import inv
from glob import globs
from functools import reduce

# parse spatial CSP and fill in the constraint matrix
def parsecsp(ConMatrix, buffer, TypeId, Vars, otpt_dir, operator, otpt):
   
   if otpt:  # output each input QCN to a single file
      filename =  otpt_dir + "InputQCN-" + operator + TypeId
      if not os.path.exists(otpt_dir):
         os.makedirs(otpt_dir)
      f = open(filename, "w")

      if globs["qcnNo"] <= 9:
         no_str = "00" + str(globs["qcnNo"])
      elif globs["qcnNo"] <=99:
         no_str = "0" + str(globs["qcnNo"])
      else:
         no_str = str(globs["qcnNo"])
        
      new_typeid = "" + TypeId
      new_typeid = new_typeid.replace("P10-RandomConstraints", "R0.00-D11.00-IA-")
      new_typeid = str(Vars-2) + " " + new_typeid + no_str
      print(new_typeid, file=f)

   for line in buffer:

      l = line.strip().replace('(','').replace(')','').split()

      if otpt:
         print(line.strip(), file=f)

      # condition to end parsing
      if l == ['.']:
         break
 
      s = reduce(lambda x, y: x | y, [translateR(i) for i in l[2:]])
      a = int(l[0])
      b = int(l[1])
      #print("l[0] is %d, l[1] is %d" % (a, b))
      ConMatrix[int(l[0])][int(l[1])] = s
      ConMatrix[int(l[1])][int(l[0])] = inv(s)
      #print(ConMatrix[9])
   if otpt:
      f.close()
