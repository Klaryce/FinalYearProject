import time
from comptab import fcomp
from bitcoding import B_dict
from inverse import inv
from collections import deque
from glob import globs
# from counters import counter

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

   for i in range(Vars):
      for j in range(i+1,Vars):
         if ConMatrix[i][j] != DALL:
            task = (i, j)
            add_task(task)

   # as long as the queue is not empty, process it
   while pq:
      # print("enter while")
      (i,j) = pop_task() # grab the appropriate relation
      
      #counter['arcs'] += 1 # increment visited arcs counter 
  
      # create all triplets to be checked for path consistency
      for k in neighbors[i] & neighbors[j]: #对于节点i和节点j的每个共同邻居k

          temp = fcomp[ConMatrix[k][i]-1][ConMatrix[i][j]-1] #节点k和i之间的约束与节点i和j之间的约束的复合约束
          if temp != DALL:

             #counter['cons'] += 1 # increment checked constraints counter
  
             # constrain arc (k,i,j)
             temp = temp & ConMatrix[k][j] #对kiij复合关系和kj之间的关系进行AND运算
             if temp != ConMatrix[k][j]: #存在某个kj约束不在这个ki和ij的复合关系中
                if not temp: # 如果kj关系和kiij复合关系完全不同
                   passT = time.time() - startT
                   globs["ppc_total"] += passT
                   globs["ppc_num"] += 1
                  #  print("false case 1")
                   return False # inconsistency
                ConMatrix[k][j] = temp #如果有重合，就把不重合的那些关系去掉
                ConMatrix[j][k] = inv[temp-1]
                if k < j:
                   add_task((k, j)) #更新了k和j之间的约束之后再对k和j的共同邻居与它们之间的约束进行更新
                else:
                   add_task((j, k))

          temp = fcomp[ConMatrix[i][j]-1][ConMatrix[j][k]-1] #ij与jk的复合约束
          if temp != DALL:

             #counter['cons'] += 1 # increment checked constraints counter
          
             # constrain arc (i,j,k) 
             temp = temp & ConMatrix[i][k] #更新i和k之间的约束
             if temp != ConMatrix[i][k]:
                if not temp: 
                   passT = time.time() - startT
                   globs["ppc_total"] += passT
                   globs["ppc_num"] += 1
                  #  print("false case 2")
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
