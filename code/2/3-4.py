def do_four(f,v):
	do_twice(f,v)
	do_twice(f,v)
	return

def do_twice(f,v):
	f(v)
	f(v)
	return

def print_spam(v):
	print v
	return

do_four(print_spam, 'spam')