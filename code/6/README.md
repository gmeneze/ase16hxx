# Coding Home Work 5 Submission

The threshold value was chosen after running MaxWalkSat with 100 retries and 100 chances with seed = 0,
threshold = 0.068868980963

How to run?
Run Osyczka2_MaxWalkSat.py and provide parameters for seed, max_retries and max_chances if you wish to use non-default values.
The default values are :-
seed = 1
max_retries = 1000
max_chances = 1000

Example:-
python Osyczka2_MaxWalkSat.py 1 1000 1000

How to Interpret results? :-
The program outputs the values of seed, best solution, threshold value (stated above) and the energy computed using the best solution found. 
It implements the algorithm specified here:-
https://github.com/txt/ase16/blob/master/doc/mws.md

Some results :-
with seed = 100, max_retries = 1000 and max_chances = 1000 :-
![alt code-execution-results-Osyczka2-MaxWalkSat-1](https://github.com/gmeneze/ase16hxx/blob/master/code/6/.images/capture_1.png)

with seed = 1, max_retries = 1000 and max_chances = 1000 :-
![alt code-execution-results-Osyczka2-MaxWalkSat-2](https://github.com/gmeneze/ase16hxx/blob/master/code/6/.images/capture_2.png)

with seed = 2, max_retries = 1000 and max_chances = 1000 :-
![alt code-execution-results-Osyczka2-MaxWalkSat-3](https://github.com/gmeneze/ase16hxx/blob/master/code/6/.images/capture_3.png)
