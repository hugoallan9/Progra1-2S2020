#Creación de una lista
nombres = ['Ana', 'Pedro', 'Juan']

#Listas en python almacenar elementos de distinto tipo
varios = [10, 20, 'Ana', 15.5, [1,5]]

#Función print para imprimir una lista
print(nombres)

#Iterador for para imprimir todos los elementos de una lista
for x in varios:
    print(x)

#Acceso a los elementos de la lista
print(varios[-2])

#Agregar un elemento a a lista
varios.append('Santa María')

print(varios)

#Slicing
print(varios[:])

#Concatenar listas
nombres.extend(varios)
print(nombres)

#ordenar listas
numeros = [12, 2,343, 12, 123, -15]
numeros.sort()
print(numeros)


matrix = [[1,2],[3,4],[4,5]]

print(matrix[-1][0])

def nested_sum(lista):
    total = 0
    for row in lista:
        for x in row:
            total += x
    return total

print(nested_sum(matrix))

#Borrar elementos de la lista
x = nombres.pop(5)
print(nombres)
print(x)

del(nombres[1])
print(nombres)

#Borrar sin conocer el índice
nombres.append('Ana')
print(nombres)
print(nombres)

def borrar_coincidencias(lista,valor):
    lista_auxiliar = lista.copy()
    while True:
        try:
            lista.remove(valor)
        except:
            pass
        if lista_auxiliar == lista:
            break
        else:
            lista_auxiliar = lista.copy()

nombres = ['Ana', 'Pedro', 'Juan', 'Ana', 'María']

borrar_coincidencias(nombres, 'Ana')
print(nombres)



