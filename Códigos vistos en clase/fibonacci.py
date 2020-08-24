import sys

# the setrecursionlimit function is
# used to modify the default recursion
# limit set by python. Using this,
# we can increase the recursion limit
# to satisfy our needs

sys.setrecursionlimit(  10 ** 6)

global known
known = {0:0,1:1}

def fibonacci(n):
    if n in known:
        return known[n]
    else:
        res = fibonacci(n-1) + fibonacci(n-2)
        known[n] = res
        return res
print(known)
f_10 = fibonacci(50)
print(f_10)
print(known)
f_11 = fibonacci(11)
print(known)



f_10000 = fibonacci(20000)
print(f_10000)