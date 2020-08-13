
def conteo(n):
    if n == 0:
        return 0
    else:
        conteo(n-1)
        print(n)

#conteo(10)

def fib(n):
    if (n == 1 or n == 2):
        return 1
    else:
        return fib(n-1) + fib(n-2)

#print(fib(6))

def suma_gauss(n):
    if n == 0:
        return 0
    else:
        return n + suma_gauss(n-1)

print(suma_gauss(10))