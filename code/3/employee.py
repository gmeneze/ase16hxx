from __future__ import division,print_function
import sys,re,traceback,random,string
sys.dont_write_bytecode=True

class Employee:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __repr__(self):
        return "name is:<" + self.name + "> age is:<" + repr(self.age) + ">"

    def __lt__(self, other):
    	return True if self.age < other.age else False

if __name__ == '__main__':
	emp1 = Employee("Glen", 26)
	emp2 = Employee("Deepak", 24)
	emp3 = Employee("Shweta", 22)

	print(emp1)

	lst = [emp1, emp2, emp3]

	print("unsorted list:", lst)

	lst.sort()

	print("sorted list:", lst)