from math import sqrt

def distancia(x1,y1,x2,y2):
    dx = x1-x2
    dy = y1-y2
    d2 = dx**2 + dy**2
    d = sqrt(d2)
    return d

print(distancia(1,2,2,4))


