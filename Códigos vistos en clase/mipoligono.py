
from math import pi




'''
#Dibujando un cuadrado
fd(bob,100)
lt(bob)
fd(bob,100)
lt(bob)
fd(bob,100)
lt(bob)
fd(bob,100)
'''
'''
#Dibujando un cuadrado con un for.
for x in range(4):
    fd(bob,100)
    lt(bob)
'''

def dibujar_poligono(tortuga, lado, n):
    for x in range(n):
        fd(bob,lado)
        lt(bob,360/n)

#dibujar_poligono(bob, 100,5)

def dibujar_circulo(tortuga,radio):
    dibujar_poligono(tortuga, 2*pi*radio/1000,1000 )

def arco(tortuga, r, theta):
    '''
    Esta función dibuja un arco de circunferencia de radio r y angulo theta.
    :param tortuga: Es un objeto de la clase Turtle de la biblioteca swampy
    :param r: Es un número positivo que denota el radio
    :param theta: Es un número positivo entre 0 y 360, denota
    :return: Una ventana gráfica con una tortuga que dibuja el arco de circunferencia dado. (No retorna nada)
    '''
    tam_arco = 2 * pi * r * theta / 360
    n = int(tam_arco / 3) + 1
    tam_paso = tam_arco  / n
    tam_angulo = float(theta) / n

    for i in range(n):
        fd(tortuga, tam_paso)
        lt(tortuga, tam_angulo)

#dibujar_circulo(bob, 100)









