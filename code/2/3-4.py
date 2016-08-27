def do_four(f,v):
	do_twice(f,v)
	do_twice(f,v)

def do_twice(f,v):
	f(v)
	f(v)

def print_spam(v):
	print v

do_four(print_spam, 'spam')