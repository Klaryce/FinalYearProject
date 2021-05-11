import time
from collections import deque
from helpfuncs import B_dict, inv
from comp_relations import complex_relations
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
      #  print("enter task")
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

         temp = complex_relations(ConMatrix[k][i], ConMatrix[i][j])  # composition of ki and ij
         if temp != DALL:

            # constraint arc (k,i,j)
            temp = temp & ConMatrix[k][j] # (ki comp ij) & kj

            if temp != ConMatrix[k][j]:  # there is a relation in kj which is not in the composition of ki and ij
               if not temp:  # kj and the composition of ki ij totally different
                  passT = time.time() - startT
                  globs["ppc_total"] += passT
                  globs["ppc_num"] += 1
                  return False # inconsistency
               ConMatrix[k][j] = temp  # remove inconsistent relation
               ConMatrix[j][k] = inv(temp)
               if k < j:
                   add_task((k, j))  # after updating the constraint of kj, update the constraint between their neighbors and them
               else:
                   add_task((j, k))


         temp2 = complex_relations(ConMatrix[i][j], ConMatrix[j][k])  # composition of ij and jk

         if temp2 != DALL:

            # constraint arc (i,j,k) 
            temp2 = temp2 & ConMatrix[i][k] 
            if temp2 != ConMatrix[i][k]:
               if not temp2:
                  passT = time.time() - startT
                  globs["ppc_total"] += passT
                  globs["ppc_num"] += 1
                  return False # inconsistency
               ConMatrix[i][k] = temp2
               ConMatrix[k][i] = inv(temp2)
               if i < k:
                   add_task((i, k)) 
               else:
                   add_task((k, i))
   # the network is concistent and can't be refined further
   passT = time.time() - startT
   globs["ppc_total"] = globs["ppc_total"] + passT
   globs["ppc_num"] += 1
   return True    
