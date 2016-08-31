from __future__ import division,print_function
import sys,re,traceback,random,string
sys.dont_write_bytecode=True

class Employee:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __repr__(self):
        return "name is: " + self.name + " age is: " + repr(self.age)

    def __lt__(self, other):
    	print("This is called")
    	return True if self.age < other.age else False


