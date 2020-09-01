import os
from xml.etree.ElementTree import parse
import csv
import matplotlib.pyplot as plt

cwd = os.getcwd()
Listas = []
Canciones = dict()

def diferenciar(Lista):
    repetidas = []
    for cancion in Lista:
        if cancion[0:3] in diccionario:
            Canciones[cancion[0:3]].append(cancion[:4])
        else:
            Canciones[cancion[0:3]] = [cancion[:4]]
    return Canciones

def info(n):
    ruta = Listas[n][1]+'\\'+Listas[n][0]
    doc = parse(ruta)
    al = Listas[n][0]
    List = []
    ListAlb = []
    for item in doc.iterfind('dict/dict/dict'):
        Nombre, Artista, Duracin = item.findtext('./string[1]'), item.findtext('./string[2]'), item.findtext(
            './integer[3]')
        Album = al[:len(al)-3]
        t = Nombre, Artista, Duracin,Album
        List.append(t)

    return List

def menu():
    print('1) Agregar lista de reproduccion')
    print('2) Ver listas de reproduccion existentes')
    print('3) Encontrar canciones duplicadas')
    print('4) Exportar lista de reproduccion')
    print('5) Estadisticas de lista')
    print('6) Salir')
    x = input('Ingrese una opcion\n')
    if x == '1':
        agregar()
    if x == '2':
        ver()
    if x == '3':
        encontrar()
    if x == '4':
        exportar()
    if x == '5':
        estadisticas()
    if x == '6':
        exit()


def agregar():
    print('Agregue una ruta para buscar listas de reproduccion')
    ruta = input()
    cosas = os.listdir(str(ruta))
    tempLista = []
    tempReal = []
    for archivo in cosas:
        if os.path.isfile(os.path.join(ruta, archivo)) and archivo.endswith('.xml'):
            x, y = archivo, ruta
            ing = x, y
            tempLista.append(ing)
    for arcXML in tempLista:
        t = str(arcXML[1])+'\\'+str(arcXML[0])
        f = open(t, 'r')
        it = (linea for i, linea in enumerate(f) if i < 4)
        for linea in it:
            if 'plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN"' in linea:
                x, y = arcXML[0], arcXML[1]
                ing = x, y
                tempReal.append(ing)
                Listas.append(ing)
    for i in tempReal:
        print(i)
    print('¿Desea agregar otro directorio? Si/No')
    add = input()
    if add.lower() == 'si':
        agregar()
    else:
        menu()


def ver():
    count = 0
    if len(Listas) == 0:
        print('No hay listas agregadas, ¿Desea agregar listas? Si/No')
        de = input()
        if de.lower() == 'si':
            agregar()
        elif de.lower() == 'no':
            menu()
    else:
        for playlist in Listas:
            count += 1
            print(count,')',playlist[0])
        print('¿Desea ver la informacion de alguna lista? Si/No')
        de = input()
        if de.lower() == 'si':
            print('Ingrese el numero de lista a visualizar')
            de = input()
            listSelec = info(int(de)-1)
            print('{3}{0:70s}{3}{1:50s}{3}{2:10s}{3}'.format('nombre', 'artista', 'duracion', '|'))
            for it in listSelec:
                print('{3}{0:70s}{3}{1:50s}{3}{2:10s}{3}'.format(it[0], it[1], it[2], '|'))
            print('¿Desea ver alguna otra lista? Si/No')
            de = input()
            if de.lower() == 'si':
                ver()
            else:
                menu()
        elif de.lower() == 'no':
            menu()


def encontrar():
    todas = []
    repetidas = []
    if len(Listas) == 0:
        print('No hay listas agregadas, ¿Desea agregar listas? Si/No')
        de = input()
        if de.lower() == 'si':
            agregar()
        elif de.lower() == 'no':
            menu()
    else:
            for cada in range(len(Listas)):
                todas.append(info(cada))
            for i in todas:
                diferenciar(i)
            print(diccionario)
            for pa, cod in diccionario.items():
                if len(cod) > 1:
                    Nombre = cod[0][0]
                    Artista = cod[0][1]
                    Duracion = cod[0][2]
                    Album = []
                    for j in range(len(cod)):
                        Album.append(cod[j][3])
                    print(cod[0][3])
                    asd = Nombre, Artista, Duracion, Album
                    print(len(cod), cod)
                    repetidas.append(asd)
            print('Las listas repetidas son:')
            print('{4}{0:70s}{4}{1:50s}{4}{2:10s}{4}{3:15s}{4}'.format('nombre', 'artista', 'duracion','Albums', '|'))
            for it in repetidas:
                print('{3}{0:70s}{3}{1:50s}{3}{2:10s}{3}{4:15s}{3}'.format(it[0], it[1], it[2], '|', str(it[3])))
    menu()


def exportar():
    count = 0
    if len(Listas) == 0:
        print('No hay listas agregadas, ¿Desea agregar listas? Si/No')
        de = input()
        if de.lower() == 'si':
            agregar()
        elif de.lower() == 'no':
            menu()
    else:
        for playlist in Listas:
            count += 1
            print(count, ')', playlist[0])
        print('Ingrese el numero de lista a exportar')
        n = input()
        exp = [['Nombre','Artista','Duracion']]
        listSelec = info(int(n)-1)
        for playlist in listSelec:
            x,y,z = playlist[0],playlist[1],playlist[2]
            li = [x,y,z]
            exp.append(li)
        rutaExp = cwd+'\\Playlist.csv'
        myCSV = open(rutaExp,'w',newline='')
        with myCSV:
            writer = csv.writer(myCSV)
            writer.writerows(exp)
        print("Exportacion completa")
        print('Documento creoado en:',rutaExp)



def estadisticas():
    count = 0
    if len(Listas) == 0:
        print('No hay listas agregadas, ¿Desea agregar listas? Si/No')
        de = input()
        if de.lower() == 'si':
            agregar()
        elif de.lower() == 'no':
            menu()
    else:
        for playlist in Listas:
            count += 1
            print(count, ')', playlist[0])
        print('¿Que lista desea graficar?')
        n = input()
        lisSelec = info(int(n)-1)
        x = []
        for i in lisSelec:
            x.append(int(i[2]))
        n, bins, patches = plt.hist(x=x, bins='auto', color='#6414ff', alpha=0.7, rwidth=0.85)
        plt.grid(axis='y', alpha=0.75)
        plt.show()


menu()
