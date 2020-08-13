def countdown(n):
    while n > 0:
        print(n)
        n = n-1
#Continuaria con el resto del código cuando ya no se satisface la condición del while


def sequence(n):
    while n != 1:
        if n%2 ==0:
            n = n/2
        else:
            n= 3*n+1

while True:
    line = input('>')
    if line == 'done':
        continue
    print(line)






