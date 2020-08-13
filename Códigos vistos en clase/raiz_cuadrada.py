from math import fabs
from math import sqrt

def raiz_cuadrada(a, x, precision):
    while True:
        y = (x**2+a)/(2*x)
        print(y)
        if fabs(y-x) <= precision:
            return y
            break
        else:
            x = y


print(raiz_cuadrada(95,7,0.0001))
print(sqrt(95))