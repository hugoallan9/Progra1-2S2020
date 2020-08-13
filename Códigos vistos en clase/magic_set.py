

def number_good_sequence(sequence,m):
    contador_multiplos = 0
    for x in sequence:
        if int(x)%m ==0:
            contador_multiplos+=1
    return 2**contador_multiplos-1

T = int(input())
for x in range(T):
    n, m = input().strip().split()
    sequence = input().strip().split()
    print(number_good_sequence(sequence,int(m)))




