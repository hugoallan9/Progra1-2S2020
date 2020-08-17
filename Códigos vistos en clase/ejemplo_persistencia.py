
#Abriendo un archivo

archivo = open('/home/hugo/Pop.xml')

#Leyendo la primera linea

print( archivo.readline() )

while True:
    linea = archivo.readline()
    if linea == '':
        break
    else:
        print(linea)


#Impresión del archivo en su totalidad
for line in archivo:
    print(line)


