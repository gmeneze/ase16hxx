# Coding Home Work 3 Submission

Run SA_schafer.py and provide parameters for kmax, seed, emax and s0 if you wish to use non-default values.

Example:-
python SA_Schafer.py 1000 1 -1 0

How to Interpret results? :-
The initial values of kmax, seed, emax and s0 (initial state) being used by the model are printed before minimization begins.
This is followed by iterations over values of temperature from 1000 to 0025. In each line - the temperature, the current minimum and the jumps (., ?, !) are printed for 25 iterations, this is same as what is mentioned in the assignment doc :-
https://github.com/txt/ase16/blob/master/doc/hw4.md

At the end, the best values of state and energy (minimum) denoted by sb and eb are printed.

Some results :-

with kmax = 1000, seed = 1, emax = -1 and s0 = 0 :-
![alt code-execution-results-SA-schafer-1](https://github.com/gmeneze/ase16hxx/blob/master/code/4/.images/Capture2.png)

with kmax = 1000, seed = 10, emax = -1 and s0 = 0 :-
![alt code-execution-results-SA-schafer-2](https://github.com/gmeneze/ase16hxx/blob/master/code/4/.images/Capture1.png)

with kmax = 1000, seed = 100, emax = -1 and s0 = 0 :-
![alt code-execution-results-SA-schafer-3](https://github.com/gmeneze/ase16hxx/blob/master/code/4/.images/Capture3.png)
