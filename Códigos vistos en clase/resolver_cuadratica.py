from math import sqrt

def resolver_cuadratica(a,b,c):
    if b**2-4*a*c <0:
        return -1,-1
    else:
        return (-b + sqrt(b**2-4*a*c))/(2*a), (-b - sqrt(b**2-4*a*c))/(2*a)

def menu():
    while True:
        entrada = input('Ingrese el valor de a, b y c separados por espacios o ingrese 0 '
                        'para terminar el programa \n')
        if entrada == '0':
            break
        else:
            a,b,c = entrada.strip().split()
            resolver_cuadratica(float(a),float(b),float(c))
            archivo = open('/home/hugo/PycharmProjects/ProgramaciónMatemática1_2020/salida_cuadrática.txt', 'a')
            archivo.write('La ecuación a resolver es:  {}x^2 + {}x + {}   = 0 \n'.format(a,b,c) )
            archivo.write('La solución es: \n ')
            x1 ,  x2 = resolver_cuadratica(float(a),float(b),float(c))
            archivo.write('x_1 = {0:f}, x_2 = {0:f}\n'.format( x1,x2 ))
            archivo.close()


menu()