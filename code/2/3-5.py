def print_line(s1,s2,r):
	for i in range (0,r):
		print s1,
		for j in range (0,4):
			print s2,
	print s1

def print_hline(r):
	print_line('+','-',r)

def print_vline(r):
	print_line('/',' ',r)

def print_grid(r,c):
	for i in range (0,c):
		print_hline(r)
		for j in range (0,4):
			print_vline(r)
	print_hline(r)

print_grid(4,5)