def MCS(ConMatrix, neighbors):

   a = [None for i in range(len(ConMatrix))]
   a_ = [None for i in range(len(ConMatrix))]     

   Set = [None for i in range(len(ConMatrix))]
   Size = [None for i in range(len(ConMatrix))] 

   for i in range(len(ConMatrix)): # i = 0, 1, 2, ..., len(ConMatrix)
      Set[i] = set([])     
      Size[i] = 0
      Set[0].add(i) # Set[0]:{0, 1, 2, ...}

   j = 0
   for i in range(len(ConMatrix)):
      v = Set[j].pop() # Set[j].pop(): 取出一个节点
      a[v] = i  # a[节点] = i
      a_[i] = v
      Size[v] = -1 # v与之前pop出的节点的Size值都为-1，后面没有pop的节点的Size值大于等于0
      for u in neighbors[v]:  # 遍历v的每个邻居
         if Size[u] >= 0:  # 邻居u在v之后
            Set[Size[u]].remove(u) # Set[Size[u]]中remove掉节点u
            Size[u] = Size[u] + 1
            Set[Size[u]].add(u) # 把节点u添加进Set[Size[u]+1]，表示已发现的u的邻居新增了1个？
      j = j + 1 # 如果Set[j+1]不为空就继续循环，回到前面从Set[j+1]中去取出节点
      while j >= 0 and not Set[j]: # Set[j]为空则一直执行j-1直到Set[j]中存在节点
         j = j - 1

   return a, a_


def FIC(ConMatrix, neighbors, a, a_ ):
   
   f = [None for i in range(len(ConMatrix))]
   index = [None for i in range(len(ConMatrix))]
   fill = list()

   for i in range(len(ConMatrix)-1,-1,-1): # 从len到0步长为-1
      w = a_[i]  # 节点
      f[w] = w
      index[w] = i
      for v in neighbors[w]:
         if a[v] > i:
            x = v
            while index[x] > i:
               index[x] = i
               fill.append((x,w) if x<w else (w,x))
               x = f[x]
            if f[x] == x: f[x] = w

   return fill
