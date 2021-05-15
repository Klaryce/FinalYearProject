# FinalYearProject
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

There are different versions of the code package and the current package is the last one where the code structure has been changed a lot. Please contact the student immediately if the current version of the code package cannot run successfully. Many thanks. Email: klaryce@qq.com.

* Note that the running time may be much longer when the code is processed on a different computer, especially the pre-calculations in the original version of composition handling. If there is not enough time to wait for it, adding the argument "-f size8-edges4-1QCNs-consistent" may be helpful. The output results can be checked from the folder LoopsInfo and Results.
