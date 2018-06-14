def test():
	a = 10
	b = 15
	c = a + b
	sub = b - a
	mult = a*b
	div = b/a

	print("Sum =" + str(c))
	print("sub =" + str(sub))
	print("mult =" + str(mult))
	print("div =" + str(div))

def test1():

	a=10
	b=5

	if a>b:
		print b
	else:
		print a


	a = "abcd"
	print len(a)

	for i in range(0,len(a)):
		print a[i]

def missing():
	a = [1,2,3,9,5,7,8,4,10]
	n = 10

	# o(n) complexity
	# 
	for i in range(0, len(a)-1):
	#	if a[i]+1 != a[i+1]:
	#		print a[i]+1

    #O(1) 
	sum1 = n * (n+1)
	sum1 = sum1 / 2

	sum2 = sum(a)
	missingnum = sum1 - sum2
	print (missingnum)


def main():
	#test()
	#test1()
	missing()

if __name__ == "__main__":
	main()