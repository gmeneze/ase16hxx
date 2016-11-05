def right_justify(s):
	spaces = 70
	n = len(s)
	spaces -= n
	fin = ""
	for i in range (0,spaces):
		fin += " "
	fin += s
	return fin

print right_justify('allen')