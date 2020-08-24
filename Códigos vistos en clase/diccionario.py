#Creación de un diccionario
eng2sp = dict()

print(eng2sp)

#Agregar elementos al diccionarios

eng2sp['one']= 'uno'
print(eng2sp)

#Crear un diccionario no vacio

eng2sp = {'one':'uno', 'two':'dos', 'three': 'tres'}
print(eng2sp)

#Calcular el tamaño
print(len(eng2sp))

eng2sp['one'] = ''
print(eng2sp)

#averiguar si una cadena ya es una llave
print('Juan' in eng2sp)

#Averiguar si algo aparece como un valor
vals = eng2sp.values()
print('Juan' in vals)

def histogram(s):
    abecedario = dict()
    for c in s:
        if c not in abecedario:
            abecedario[c] =  1
        else:
            abecedario[c] += 1
    return abecedario

resultado = histogram('meme')

for x in resultado:
    print('|Letra|', '|Cantidad de veces|')
    print(x, '\t\t\t' , resultado[x])

#Búsqueda inversa dentro de diccionarios
def reverse_lookup(d,v):
    for k in d:
        if d[k] == v:
            return k
    raise ValueError

print(reverse_lookup(resultado, 2))


#Listas dentro de diccionarios
def invert_dict(d):
    inverso = dict()
    for k in d:
        val = d[k]
        if val not in inverso:
            inverso[val] = [k]
        else:
            inverso[val].append(k)
    return inverso

inverso_resultado = invert_dict(resultado)
print(inverso_resultado)









