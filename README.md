# FinalYearProject

Maximizing Satisfiability of Qualitative Constraint Networks (QCNs)

Keywords: Qualitative Spatial and Temporal Reasoning (QSTR), evolutionary algorithm

The content below was updated in 2023.

This is the final year project of the author's bachelor's degree. Thank Professor Michael Sioutis for his auxiliary code (below in 1) and the code for consistency checking (ppc.py). The contribution is fourfold.

(1) The auxiliary code structure has been reorganized (helpfuncs.py, glob.py, inverse.py, parsecsp.py).

(2) The algorithm from https://dl.acm.org/doi/abs/10.1145/3200947.3201021 has been reproduced.

(3) The new composition handling processes pre-calculation in a new way. It only pre-calculates the binary composition of basic relations so that the matrix is 13 by 13 instead of 2^13 by 2^13 in the original version.

(4) The new crossover operator (crossConsC and crossConsD) has been proposed. A new parameter -c is introduced to control crossConsC.
  
	a). Modified based on crossConsB.
  
	b). crossConsC considers the better QCN more often.
  
	c). crossConsD considers the first input QCN more often.
  


![image](https://user-images.githubusercontent.com/45749073/225372356-0f59745f-2855-48b9-8c4a-dd11abcaab7a.png)

<img src="https://user-images.githubusercontent.com/45749073/225385051-671b9707-b818-4946-b920-d37789caee46.png" width="600px">
<img src="https://user-images.githubusercontent.com/45749073/225372185-e574f2f9-8c00-4c02-bb39-7b0615a015cb.png" width="400px">

<img src="https://user-images.githubusercontent.com/45749073/225385284-0752c83b-d3be-44a4-9ea7-6a0d4760811a.png" width="600px">
<img src="https://user-images.githubusercontent.com/45749073/225372266-fc3b0a01-82d2-4329-831e-81243d5fe8e8.png" width="400px">

![image](https://user-images.githubusercontent.com/45749073/225372786-88268836-4c92-40a5-a7e2-c1292ebc2d64.png)

<img src="https://user-images.githubusercontent.com/45749073/225376099-caf06b4c-1eef-4137-84af-954ddcf57c6f.png" width="500px">

**Motivation of the Improvement on Crossover Operators (June 2021)**

All three new crossovers operators change the way of assigning $S_x$ and $S_y$ to $S_1$ and $S_2$ in crossConsB. Firstly the operator crossConsB will be reviewed again in the view of the inheritance from two parents. Then the idea to create crossConsC and crossConsD will be explained comparing with crossConsB.

The constraint of an edge in a scenario needs to be a singleton relation. However, as all constraints in the child QCN is initialized as the universe relation $B$ in crossConsB, there must exist some $(v, v') \in E$ and $|S[v, v']|>1$ which should be singleton relations. In each iteration, the constraint of such a pair $v, v'$ is handled. When selecting the singleton constraint for it, the operator always considers $S_\text{1}$ in priority, and only considers $S_\text{2}$ if the constraint in $S_\text{1}$ does not meet the requirement. Therefore, in each iteration where a new pair $v, v'$ is selected, $S[v, v']$ tends more likely to be assigned with the constraint $S_\text{1}[v, v']$ rather than $S_\text{2}[v, v']$. However, in crossConsB, the two parent QCNs are assigned to $S_\text{1}$ and $S_\text{2}$ randomly, which means that in general cases, around half of the constraints in $S$ will come from $S_\text{1}$, whereas the other half will come from $S_\text{2}$. Although both $S_\text{1}$ and $S_{\text{2}}$ are $_G^\diamond$\- consistent, their combinations may be not. 

When designing the operator crossConsC, it is analyzed that focusing on the better scenario more often rather than picking them randomly may increase the performance. However, focusing on one scenario which is not necessarily the best one may also increase the performance. Moreover, if the result of choosing the second better scenario is not worse than choosing the best one, then the comparison of the two scenarios, and all operations for reassigning $S_\text{1}$ and $S_\text{2}$ in each iteration can only waste time. In addition, although in each iteration there might be different parents passed to crossConsC, since there is still a probability that some parents are repeatedly selected in different iterations, it means that the relatively better scenarios among the best individuals tend to be considered much more often. Based on these points of view, crossConsD is come up with.

Concisely, both two methods lose some extent of diversification for the sake of a faster speed of convergence. This is because the diversification and the convergence speed always check and balance. The introduction of diversification will increase the possibility to obtain global minimality, since some better elements are likely to be found. However, it is also more likely to get worse elements and generate a worse result. Therefore, it is a trade-off to prevent the diversification from influencing the convergence speed while avoiding obtaining the local minimality.

-----------------------------------------------------------------------------

The content below was updated in June 2021.

The folder new_composition is the code package using the new version of composition handling, while the old_composition is the code package using the original (old) version of compositin handling.

Enter the command "python mainfuncs.py" to run the code. The version of the code is Python 3. The command "python 3" is expected to be used if the default version of the command "python" is 2.


Available parameters:

-f: filename of the input QCNs. String. Default: size16-edges8-9QCNs-consistent.

-o: crossover operator. String. Default: crossConsB.

-p: cardP, the size of the population. Integer. Default: 50.

-b: cardBest, the number of best individuals selected. Integer. Default: 20. 

-d: divT, number of loops to enter the diversification step. Integer. Default: 50. 

-t: timeoutL, the time out limit of the algorithm EAMQ. Integer. Default: 1800. 

-n: name of the experiment. String. Default: default. 

-c: the parameter c in the operator crossConsC. Integer. Default: 7. 

-r: output chordal graphs. 

-i: output each input QCN to a single file.


The folder QCN-files contains the input files of the algorithm. When using the -f command to specify a input file, the algorithm will search the filename within this folder. 

The algorithm will create a folder Results which contains the solutions and some information.

The algorithm will also create folder LoopsInfo containing information of each loop.

If the parameter -r is set, the folder Triangulation will be created to contain chordal graphs.

If the parameter -i is set, the folder Input_SingleQCNs will be created to contain the seperate files of the input QCNs.


In each folder, a folder named using the parameter -n will be created. Then, sub-directories named using configurations of QCNs, or parameters of the algorithm will be created to contain the results and information of corresponding QCNs.

If a folder has been created already, it will not be created again. And the results will be put into it.

There are different versions of the code package and the current package is the last one where the code structure has been changed a lot. Please contact the author immediately if the current version of the code package cannot run successfully. Many thanks. Email: klarycehappy@gmail.com.

Note that the running time may be much longer when the code is processed on a different computer, especially the pre-calculations in the original version of composition handling. If there is not enough time to wait for the new version to process large QCNs, adding the argument "-f size8-edges4-1QCNs-consistent" may be helpful. The output results can be checked from the folder LoopsInfo and Results.
