import time
from comptab import fcomp
from helpfuncs import B_dict, inv
from collections import deque
from glob import globs

DALL = B_dict['DALL']

# path consistency using van Beek weights
def pPC(ConMatrix, neighbors):
   startT = time.time()
   pq = deque([])                         # list of entries arranged in a heap
   entry_finder = set([])               # mapping of tasks to entries
   Vars = len(ConMatrix) #conmatrix行数

   def add_task(task):
       'Add a new task or update the priority of an existing task'
       if task not in entry_finder:
          entry_finder.add(task)
          pq.append(task)
          
   def pop_task():
       'Remove and return the lowest priority task. Raise KeyError if empty.'
       task = pq.popleft()
       entry_finder.discard(task)
       return task

   # initialize the queue
   for i in range(Vars):
      for j in range(i+1,Vars):
         if ConMatrix[i][j] != DALL:
            task = (i, j)
            add_task(task)

   # as long as the queue is not empty, process it
   while pq:

      (i,j) = pop_task() # grab the appropriate relation
  
      # create all triplets to be checked for path consistency
      for k in neighbors[i] & neighbors[j]:  # for each common neighbors of i and j

          temp = fcomp[ConMatrix[k][i]-1][ConMatrix[i][j]-1]  # composition of ki and ij
          if temp != DALL:
  
             # constraint arc (k,i,j)
             temp = temp & ConMatrix[k][j]  # (ki comp ij) & kj
             if temp != ConMatrix[k][j]:  # there is a relation in kj which is not in the composition of ki and ij
                if not temp:   # kj and the composition of ki ij totally different
                   passT = time.time() - startT
                   globs["ppc_total"] += passT
                   globs["ppc_num"] += 1
                   return False  # inconsistency
                ConMatrix[k][j] = temp  # remove inconsistent relation
                ConMatrix[j][k] = inv[temp-1]
                if k < j:
                   add_task((k, j)) # after updating the constraint of kj, update the constraint between their neighbors and them
                else:
                   add_task((j, k))

          temp = fcomp[ConMatrix[i][j]-1][ConMatrix[j][k]-1]  # composition of ij and jk
          if temp != DALL:
          
             # constraint arc (i,j,k) 
             temp = temp & ConMatrix[i][k] 
             if temp != ConMatrix[i][k]:
                if not temp: 
                   passT = time.time() - startT
                   globs["ppc_total"] += passT
                   globs["ppc_num"] += 1
                   return False # inconsistency
                ConMatrix[i][k] = temp
                ConMatrix[k][i] = inv[temp-1]
                if i < k:
                   add_task((i, k)) 
                else:
                   add_task((k, i))

   # the network is concistent and can't be refined further
   passT = time.time() - startT
   globs["ppc_total"] += passT
   globs["ppc_num"] += 1
   return True    
