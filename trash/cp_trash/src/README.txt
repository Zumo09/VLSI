Before running the MiniZinc model, .dzn files with the data have to be created. To do so I wrote a python script 
'modify_instances.py' that receives as input the path of the folder containing the .txt files with the data in the 
format specified by the pdf project.
It creates for each 'ins-i.txt' a new file 'ins_i.txt' that has to be copy in the MiniZinc IDE as data file.

'no_rotation.mzn' containes the model in which circuits are not allowed to rotate.
'rot_allowed.mzn' containes the model in which circuits are allowed to rotate.

To plot the solution, the optimal solution has to be copied in a txt file and then passed to the script 'solution_plot.py'.

However, all the solutions found are already present in the folder 'out' for the first model and in the folder 'out_rot' 
for the second model. 
Some files in these folders are marked with #, it means that these solutions aren't the optimal ones but the best found 
within the time limit.


 