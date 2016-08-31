from __future__ import division,print_function
import sys,re,traceback,random,string
sys.dont_write_bytecode=True

def has_duplicates(lst):
    """ Returns True if input list has any duplicates """
    seen = []
    for element in lst:
        if element in seen:
            return True
        else:
            seen.append(element)
    return False

def generate_list():
    """ Generates lists of length 23 containing random numbers between 1 to 365, which represents the days of the year """
    lst = []
    for i in range(23):
        lst.append(random.randint(1,365))
    return lst

success = 0
number_of_simulations = 1000
for i in range(1000):
    if has_duplicates(generate_list()):
        success += 1

print("number of simulations is:", number_of_simulations)
print("number of list instances with duplicates:", success)
print("probability of duplicates in a list:", success/number_of_simulations)
