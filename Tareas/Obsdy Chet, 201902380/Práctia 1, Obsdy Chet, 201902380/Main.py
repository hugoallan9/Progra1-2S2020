import os  # Para la lectura del XML, para hallar directorios
import xml.etree.ElementTree as Et  # Para la lectura del XML
import csv  # Para escribir el CSV
from matplotlib import pyplot as plt  # Para la gráfica de histograma

print("Para todo el programa las preguntas con (Sí/No) pueden ser contestada considerando que:")
print("*) No importa si la entrada es o no con mayúsculas.")
print("*) Puede ser variante de: sí, si, yes, s, y para Sí y no, n para No")
print("*) Cualquier otra entrada es considerada negativa")
input("Presiona enter para continuar")
print(" ")


def primera_opcion_texto_input():
    """
    Esta función será será el primer menú que vea el usuario, está pensada para repetirse y poder usar sus valores
    para saber cual de las instrucciones que describe seguir.
    :return: el número de la opción que elija como una cadena.
    """
    print("Elige una de las siguienes opciones:")
    print("1) Escribir la ruta de archivos XML (archivos por separado)")
    print("2) Escribir la ruta de la carpeta con archivos XML (archivos en la misma carpeta)")
    opcion_carpeta_o_directo = input("Escribe aquí el número y presiona enter o escribe x para terminar: ")
    print("")
    return opcion_carpeta_o_directo


def primera_opcion_loop():
    """
    Esta función repetirá la función "primera_opcion_texto_input()" hasta que el usuario de una entrada válida.
    :return: la respuesta del usuario si esta se halla dentro de las opciones posibles.
    """
    respuesta_1 = "-1"
    while respuesta_1 not in ["1", "2", "x"]:
        respuesta_1 = primera_opcion_texto_input()
    return respuesta_1


def arreglar_direccion_espacios(ruta):
    """
    Cambia en la cadena una secuencia de escape de espacio en blanco por el mismo espacio en blanco.
    :param ruta: Suponiendo que se ingresa una ruta que ha sido copiada de la terminal o cualquier ruta que de
    problemas con la secuencia de escape de espacio.
    :return: la misma ruta que ya puede ser usada por las funciones open() de os y el método .parse() para el archivo
    XML.
    """
    lista_auxiliar = ruta.split("\\")
    direccion_arreglada = ""
    for n in lista_auxiliar:
        direccion_arreglada += n
    return direccion_arreglada


directorio_carpetas = []
directorio_archivos = []

respuesta_afirmativa = ["sí", "si", "y", "s"]
respuesta_negativa = ["no", "N", "n"]

eleccion = "x"

"""
---------------------------------------------------------------------------
Empieza el proceso de ingresar las direcciones
---------------------------------------------------------------------------
"""
while True:
    volver_2 = True
    eleccion = primera_opcion_loop()
    if eleccion == "2":  # Escribir la ruta de la carpeta con archivos XML (archivos en la misma carpeta)
        volver = True
        while volver:
            primer_ruta = input("Ingresa la dirección o escribe x para salir de esta opción: ")
            if primer_ruta == "x":
                break
            print("")
            segunda_ruta = arreglar_direccion_espacios(primer_ruta)
            directorio_actual = os.getcwd()
            try:
                os.chdir(segunda_ruta)
            except NotADirectoryError:
                print("Esta no es una ruta válida, tal vez te equivocaste de opción.\n")
                break
            except FileNotFoundError:
                print("Esta no es una ruta válida, tal vez te equivocaste de opción.\n")
                break
            hay_xml = False
            for documento in os.listdir(segunda_ruta):
                if documento[-1] == "l" and documento[-2] == "m" and documento[-3] == "x" and documento[-4] == ".":
                    print(documento)
                    hay_xml = True
            print("")
            if hay_xml:
                pregunta = input("¿Es correcto este listado de archivos? (Sí, No) ")
                if pregunta.lower() in respuesta_afirmativa:
                    volver = False
                    os.chdir(directorio_actual)
                    directorio_carpetas.append(segunda_ruta)
                    pregunta_2 = input("¿Te gustaría añadir otro directorio? (Sí, No) ")
                    print(" ")
                    if pregunta_2.lower() in respuesta_negativa:
                        volver_2 = False
                    elif pregunta_2.lower() in respuesta_afirmativa:
                        pass
                    else:
                        print("Lo tomaré como un No")
                        volver_2 = False
                    break
                else:
                    if pregunta.lower() in respuesta_negativa:
                        pass
                    else:
                        print("Lo tomaré como un No")
                    os.chdir(directorio_actual)
            else:
                print("La carpeta no tiene archivos XML, ingresa la ruta de una carpeta que sí tenga archivos XML.")
        if not volver_2:
            break
    elif eleccion == "1":  # Escribir la ruta de archivos XML (archivos por separado)
        volver = True
        while volver:
            primer_ruta = input("Ingresa la dirección o escribe x para salir de esta opción: ")
            if primer_ruta == "x":
                break
            print("")
            documento = arreglar_direccion_espacios(primer_ruta)
            hay_xml = False
            if documento[-1] == "l" and documento[-2] == "m" and documento[-3] == "x" and documento[-4] == ".":
                arreglo = documento[::-1]
                valor = 0
                for i in range(len(arreglo)):
                    if arreglo[i] == "/":
                        valor = i
                        break
                arreglo = arreglo[0:valor]
                arreglo = arreglo[::-1]
                print(arreglo)
                hay_xml = True
            print("")
            if hay_xml:
                pregunta = input("¿Es correcto este archivo? (Sí, No) ")
                if pregunta.lower() in respuesta_afirmativa:
                    volver = False
                    directorio_archivos.append(documento)
                    pregunta_2 = input("¿Te gustaría añadir otro directorio? (Sí, No) ")
                    print(" ")
                    if pregunta_2.lower() in respuesta_negativa:
                        volver_2 = False
                    elif pregunta_2.lower() in respuesta_afirmativa:
                        pass
                    else:
                        print("Lo tomaré como un No")
                        volver_2 = False
                    break
                else:
                    if pregunta.lower() in respuesta_negativa:
                        pass
                    else:
                        print("Lo tomaré como un No")
            else:
                print("La dirección no es la de un archivo XML, ingresa la dirección de un archivo XML.")
        if not volver_2:
            break
    elif eleccion == "x":
        break

"""
---------------------------------------------------------------------------
Arreglamos las direcciones ingresadas
---------------------------------------------------------------------------
"""


def no_repetidos_en_lista(lista):
    """
    :param lista: Ingresa una lista que pueda tener elementos repetidos.
    :return: En caso de tener elementos repetidos los elimina.
    """
    limpio = False
    while not limpio:
        limpio = True
        for k in range(len(lista)):
            for h in range(k + 1, len(lista)):
                if lista[k] == lista[h]:
                    del lista[k]
                    limpio = False
                    break
    return lista


directorio_archivos = no_repetidos_en_lista(directorio_archivos)
directorio_carpetas = no_repetidos_en_lista(directorio_carpetas)

"""
Hasta aquí lo que llevamos es tener ya todos los archivos .xml a utilizar.
Ordenamos los directorios para solo tener la ruta del archivo en vez de rutas de carpetas enteras.
"""
directorios_finales = dict()
for direccion in directorio_carpetas:
    directorio_actual = os.getcwd()
    os.chdir(direccion)
    for documento in os.listdir(direccion):
        if documento[-1] == "l" and documento[-2] == "m" and documento[-3] == "x" and documento[-4] == ".":
            directorios_finales[documento] = direccion + "/" + documento
    os.chdir(directorio_actual)

for direccion in directorio_archivos:
    arreglo = direccion[::-1]
    valor = 0
    for i in range(len(arreglo)):
        if arreglo[i] == "/":
            valor = i
            break
    arreglo = arreglo[0:valor]
    arreglo = arreglo[::-1]
    directorios_finales[arreglo] = direccion


diccionario_referencia_numero_directorio = dict()
contador = 1
for x in directorios_finales:  # Con esto podremos acceder a cada lista por su número asignado
    diccionario_referencia_numero_directorio[str(contador)] = x
    contador += 1


def ver_listas():
    """
    :return: imprime las listas agregadas.
    """
    print("Las listas de reproducción agregadas son:\n ")
    contador_v = 1
    for y in directorios_finales:
        print(str(contador_v) + ") " + y[0:-4])
        contador_v += 1
    print("")


if eleccion != "x":
    ver_listas()  # Mostramos las listas que ingresó el usuario
    input("Presiona enter para continuar. ")
    print("")
"""
Empezamos a definir las funciones que usaremos en el segundo proceso
"""


def segunda_opcion_texto_input():
    print("Elige una de las siguienes opciones:")
    print("1) Detalles de lista en particular: nombre de cada canción, artista y duración.")
    print("2) Encontrar duplicados en las listas de reproducción.")
    print("3) Exportar lista de reproducción. (En formato CSV con Nombre, Artista y Duración)")
    print("4) Estadísticas. (De todas las listas o una en particular)")
    opcion_funcion = input("Escribe aquí el número y presiona enter o escribe x para terminar: ")
    print("")
    return opcion_funcion


def segunda_opcion_loop():
    respuesta_2 = "-1"
    while respuesta_2 not in ["1", "2", "3", "4", "x"]:
        respuesta_2 = segunda_opcion_texto_input()
    return respuesta_2


def datos_de_la_lista(ruta):
    """
    :param ruta: la ruta donde se halla el archivo .xml de la lista de reproducción.
    :return: los datos: Nombre, Artista, Duración de cada canción en una lista, en adelante la referencia estos nombres
    será NAD.
    """
    arbol = Et.parse(ruta)
    mi_raiz = arbol.getroot()

    def hallar_dict(raiz):
        for k in range(len(raiz[0])):
            if raiz[0][k].tag == "dict":
                return k

    def hallar_sub_dict(raiz, numero):
        sub_dicts = []
        for m in range(len(raiz[0][numero])):
            if raiz[0][numero][m].tag == "dict":
                sub_dicts.append(m)
        return sub_dicts

    def hallar_datos(raiz, numero_1, numero_2):
        datos = []
        nombre_1 = 0
        artista_2 = 0
        duracion_3 = 0
        for k in range(len(raiz[0][numero_1][numero_2])):
            if raiz[0][numero_1][numero_2][k].text == "Name":
                nombre = raiz[0][numero_1][numero_2][k+1].text
                datos.append(nombre)
                nombre_1 += 1
            elif raiz[0][numero_1][numero_2][k].text == "Artist":
                artista = raiz[0][numero_1][numero_2][k+1].text
                datos.append(artista)
                artista_2 += 1
            elif raiz[0][numero_1][numero_2][k].text == "Total Time":
                duracion = int(raiz[0][numero_1][numero_2][k+1].text)
                datos.append(duracion)
                duracion_3 += 1
        while len(datos) != 3:
            if nombre_1 != 1:
                datos.append("")
                for g in range(1, len(datos)):
                    datos[-g] = datos[-g-1]
                datos[0] = "Nombre no encontrado"
            elif artista_2 != 1:
                datos.append("")
                for g in range(1, len(datos) - 1):
                    datos[-g] = datos[-g - 1]
                datos[1] = "Artista no encontrado"
            elif duracion_3 != 1:
                datos.append("")
                for g in range(1, len(datos) - 2):
                    datos[-g] = datos[-g - 1]
                datos[2] = 0
        return datos

    num_dict = hallar_dict(mi_raiz)
    lista = hallar_sub_dict(mi_raiz, num_dict)

    todos_los_datos = []
    for r in lista:
        lista_resultado = hallar_datos(mi_raiz, num_dict, r)
        todos_los_datos.append(lista_resultado)

    return todos_los_datos


def convertir_tiempo_a_ms(lista):
    """
    :param lista: lista con los datos NAD.
    :return: Agregará a cada elemento de la lista el tiempo en minutos y segundos.
    """
    if len(lista[0]) < 4:
        for t in range(len(lista)):
            segundos = round(lista[t][2] / 1000)
            minutos = str(segundos // 60)
            segundos = str(segundos % 60)
            if len(segundos) == 1:
                segundos = "0" + segundos
            tiempo = minutos + ":" + segundos
            lista[t].append(tiempo)


def imprimir_datos_orden(lista, separacion=5):
    """
    :param lista: la lista con los datos de la lista de reproducción: Nombre, Artista, Duración.
    :param separacion: la separación usada entre cada columna de información.
    :return: imprime los datos de forma organizada.
    """
    largo_1 = 0
    largo_2 = 0
    for k in range(len(lista)):
        largo_eval = len(lista[k][0])
        if largo_eval > largo_1:
            largo_1 = largo_eval
    for k in range(len(lista)):
        largo_eval = len(lista[k][1])
        if largo_eval > largo_2:
            largo_2 = largo_eval
    largo_1 += separacion
    largo_2 += separacion

    impresion = "Nombre" + " " * (largo_1 - len("Nombre"))
    impresion += "Artista" + " " * (largo_2 - len("Artista"))
    impresion += "Duración"
    print(impresion)
    print("")
    for r in range(len(lista)):
        impresion = lista[r][0] + " " * (largo_1 - len(lista[r][0]))
        impresion += lista[r][1] + " " * (largo_2 - len(lista[r][1]))
        impresion += lista[r][3]
        print(impresion)
    print("")


def imprimir_repetidos_orden(lista, separacion=10):  # FALTA POR HACER
    """
    Función para imprimir los datos de la música repetida en las listas de forma organizada.
    :param lista: la lista con los datos de la lista de reproducción: Nombre, Artista, Duración.
    :param separacion: la separación usada entre cada columna de información.
    :return: imprime los datos de forma organizada.
    """
    if len(lista) == 0:
        return print("No hay canciones repetidas")
    largo_1 = 0
    largo_2 = 0
    largo_3 = 0
    for k in range(len(lista)):
        largo_eval = len(lista[k][0])
        if largo_eval > largo_1:
            largo_1 = largo_eval
    for k in range(len(lista)):
        largo_eval = len(lista[k][1])
        if largo_eval > largo_2:
            largo_2 = largo_eval
    for k in range(len(lista)):
        largo_eval = len(lista[k][3])
        if largo_eval > largo_3:
            largo_3 = largo_eval
    largo_1 += separacion
    largo_2 += separacion
    largo_3 += separacion

    impresion = "Nombre" + " " * (largo_1 - len("Nombre"))
    impresion += "Artista" + " " * (largo_2 - len("Artista"))
    impresion += "Duración" + " " * (largo_3 - len("Duración"))
    impresion += "Repetidos en listas"
    print(impresion)
    print("")
    for r in range(len(lista)):
        impresion = lista[r][0] + " " * (largo_1 - len(lista[r][0]))
        impresion += lista[r][1] + " " * (largo_2 - len(lista[r][1]))
        impresion += lista[r][3] + " " * (largo_3 - len(lista[r][3]))
        repetidos_en = ""
        for q in range(4, len(lista[r])):
            lista_numero = lista[r][q]
            repetidos_xml = diccionario_referencia_numero_directorio[lista_numero]
            repetidos_en += repetidos_xml[0:-4] + ", "
        repetidos_en = repetidos_en[0:-1]
        impresion += repetidos_en
        print(impresion)
    print("")


def datos_nad(numero_de_lista_elegida):
    """
    Resume el proceso de usar diccionarios y funciones que se describen y ven adelante.
    :param numero_de_lista_elegida: usando el diccionario con referencia en números a la lista elegida podemos usar
    dicho número para acceder al nombre de la lista, con ese nombre usamos otro diccionario para acceder a la ruta y
    con la ruta podemos obtener los datos de la lista.
    :return: los datos NAD.
    """
    lista_elegida = diccionario_referencia_numero_directorio[numero_de_lista_elegida]
    ruta_de_lista = directorios_finales[lista_elegida]
    datos = datos_de_la_lista(ruta_de_lista)
    return datos


def ordenar_datos(lista):
    """
    Haciendo uso del algoritmo quick sort ordenamos los datos de la lista.
    :param lista: Ingresamos una lista que puede estar desordenada.
    :return: la lista ordenada
    """

    def orden(nuestra_lista):
        """
        :param nuestra_lista: lista a evaluar si está o no ordenada .
        :return: True si está ordenada y False en caso contrario.
        """
        prueba = True
        for u in range(len(nuestra_lista)):
            if u == len(nuestra_lista) - 1:
                if int(nuestra_lista[u]) < int(nuestra_lista[u - 1]):
                    prueba = False
            elif int(nuestra_lista[u]) > int(nuestra_lista[u + 1]):
                prueba = False
                break
        if prueba:
            return True
        else:
            return False

    primer_valor = []
    indice_referencia = 0

    while not orden(lista):
        primer_valor_referencia = int(lista[indice_referencia])
        menores = []
        iguales = []
        mayores = []
        for v in range(indice_referencia + 1, len(lista)):
            if int(lista[v]) < primer_valor_referencia:
                menores.append(lista[v])
            elif int(lista[v]) > primer_valor_referencia:
                mayores.append(lista[v])
            else:
                iguales.append(lista[v])
        lista_referencia = [primer_valor_referencia]
        lista_anterior = lista
        lista = primer_valor + menores + iguales + lista_referencia + mayores

        if lista_anterior == lista:
            primer_valor.append(lista[indice_referencia])
            indice_referencia += 1

    return lista


def datos_grafica(datos_nad_ex):
    """
    Resume un proceso largo.
    :param datos_nad_ex: la lista con datos NAD a evaluar.
    :return: los datos para el eje x e y de la gráfica, la duración y repetición.
    """
    convertir_tiempo_a_ms(datos_nad_ex)
    lista_de_tiempos = []
    for NAD in datos_nad_ex:
        lista_de_tiempos.append(NAD[3])
    duracion_cancion = []
    for numero_l in range(len(lista_de_tiempos)):
        lista_de_tiempos[numero_l] = lista_de_tiempos[numero_l].split(":")
        lista_de_tiempos[numero_l][0] = int(lista_de_tiempos[numero_l][0])
        lista_de_tiempos[numero_l][1] = int(lista_de_tiempos[numero_l][1])
        if lista_de_tiempos[numero_l][1] > 30:
            lista_de_tiempos[numero_l][0] += 1
        del lista_de_tiempos[numero_l][1]
    for numero_l in range(len(lista_de_tiempos)):
        duracion_cancion.append(lista_de_tiempos[numero_l][0])
    duracion_cancion = ordenar_datos(duracion_cancion)
    repetidos_duracion = []
    i_2 = 0
    while i_2 < len(duracion_cancion):
        repetidos_2 = 1
        contador_2 = i_2 + 1
        while contador_2 <= len(duracion_cancion) - 1:
            if duracion_cancion[i_2] == duracion_cancion[contador_2]:
                repetidos_2 += 1
                del duracion_cancion[contador_2]
                contador_2 -= 1
            contador_2 += 1
        repetidos_duracion.append(repetidos_2)
        i_2 += 1
    return duracion_cancion, repetidos_duracion


"""
-------------------------------------------------
Empieza el proceso con las herramientas
-------------------------------------------------
"""
while True:
    eleccion = segunda_opcion_loop()
    if eleccion == "1":  # Detalles de lista en particular: nombre de cada canción, artista y duración.
        volver_1 = True
        while volver_1:
            ver_listas()
            numero_de_lista = input("Elige de cuál quieres ver los detalles escribiendo su número o x para salir: ")
            print("")
            while numero_de_lista not in diccionario_referencia_numero_directorio and numero_de_lista != "x":
                numero_de_lista = input("Elige un número de los que se te presentan o x para salir: ")
            if numero_de_lista != "x":
                datos_NAD = datos_nad(numero_de_lista)
                convertir_tiempo_a_ms(datos_NAD)
                imprimir_datos_orden(datos_NAD)
                segunda_opcion = input("¿Deseas ver datos de otra lista? (Sí/No) ")
                print("")
                if segunda_opcion in respuesta_afirmativa:
                    pass
                elif segunda_opcion in respuesta_negativa:
                    break
                else:
                    print("Tomaré eso como un no.\n")
                    break
    elif eleccion == "2":  # Encontrar duplicados en las listas de reproducción
        megalista = []
        repetidos = []
        # Ponemos todos los datos en una lista indicando la lista de reproducción a la que pertenece cada canción
        for i in diccionario_referencia_numero_directorio:
            datos_NAD = datos_nad(i)
            convertir_tiempo_a_ms(datos_NAD)
            for j in datos_NAD:
                j.append(i)
            for dato in datos_NAD:
                megalista.append(dato)
        # Evaluamos si hay repetidos, cada acierto se anotará.
        for i in range(len(megalista)):
            j = i + 1
            while j <= len(megalista) - 1:
                if megalista[i][0] == megalista[j][0] and megalista[i][2] == megalista[j][2]:
                    lista_en_que_se_repite = megalista[j][4]
                    megalista[i].append(lista_en_que_se_repite)
                    del megalista[j]
                    j -= 1
                j += 1
        i = 0
        while i <= len(megalista) - 1:
            if len(megalista[i]) < 6:
                del megalista[i]
                i -= 1
            i += 1
        imprimir_repetidos_orden(megalista)
        input("Presiona enter para continuar. ")
        print("")
    elif eleccion == "3":  # Exportar lista de reproducción. (En formato CSV con Nombre, Artista y Duración)
        ver_listas()
        numero_de_lista = input("Elige cuál quieres exportar en formato CSV o escribe x para salir: ")
        print("")
        while numero_de_lista not in diccionario_referencia_numero_directorio and numero_de_lista != "x":
            numero_de_lista = input("Elige un número de los que se te presentan: ")
        if numero_de_lista != "x":
            datos_NAD = datos_nad(numero_de_lista)
            nombre_para_csv = diccionario_referencia_numero_directorio[numero_de_lista][0:-4]
            print("Te gustaría guardar el archivo en:")
            print("1) La carpeta de la práctica")
            print("2) Otra carpeta")
            guardar = input("Elige una opción: ")
            print("")
            while guardar not in ["1", "2"]:
                guardar = input("Elige un número de los que se te presentan: ")
            directorio_actual = os.getcwd()
            segunda_ruta = ""
            if guardar == "2":
                ruta_guardado = input("Ingresa la dirección de la carpeta donde quieres guardar el archivo CSV: ")
                segunda_ruta = arreglar_direccion_espacios(ruta_guardado)
                hubo_error = False
                while True:
                    error = 0
                    if hubo_error:
                        ruta_guardado = input("Ingresa una dirección válida para guardar el archivo CSV: ")
                        segunda_ruta = arreglar_direccion_espacios(ruta_guardado)
                    try:
                        os.chdir(segunda_ruta)
                    except NotADirectoryError:
                        print("Esta no es una ruta válida.\n")
                        error += 1
                        hubo_error = True
                    except FileNotFoundError:
                        print("No encontré el archivo.\n")
                        error += 1
                        hubo_error = True
                    if error == 0:
                        break
            elif guardar == "1":
                segunda_ruta = os.getcwd()
                segunda_ruta += "/Listas de reproducción CSV"

            nombre_ya_guardado = nombre_para_csv + ".csv"

            with open(segunda_ruta + "/" + nombre_para_csv + ".csv", "w", ) as csv_file:
                csv_writer = csv.writer(csv_file, delimiter=",")

                for dato in datos_NAD:
                    csv_writer.writerow(dato)
            print("Lista exportada.")
            print(" ")
            input("Presiona enter para continuar. ")
            print("")
            os.chdir(directorio_actual)
    elif eleccion == "4":  # Estadísticas. (De todas las listas o una en particular)
        print("1) Gráfica para una lista en particular")
        print("2) Gráfica para todas las listas")
        una_o_todas = input("Escribe el número o x para salir: ")
        print("")
        while una_o_todas not in ["1", "2", "x"]:
            una_o_todas = input("Elige un número de los que se te presentan: ")
        if una_o_todas != "x":
            if una_o_todas == "1":
                ver_listas()
                numero_de_lista = input("Elige de cuál quieres ver las estadísticas: ")
                print("")
                while numero_de_lista not in diccionario_referencia_numero_directorio:
                    numero_de_lista = input("Elige un número de los que se te presentan: ")
                nombre_para_grafica = diccionario_referencia_numero_directorio[numero_de_lista]
                datos_NAD = datos_nad(numero_de_lista)
                eje_x, eje_y = datos_grafica(datos_NAD)

                plt.plot(eje_x, eje_y, marker="o")

                plt.xlabel("Duración en minutos (redondeado)")
                plt.ylabel("Cantidad con esa duración")
                plt.title(nombre_para_grafica[0:-4])

                plt.grid(True)
                plt.tight_layout()

                ruta_guardado = os.getcwd()
                ruta_guardado += "/Gráficas de estadística"
                ruta_guardado += "/" + nombre_para_grafica[0:-4]
                plt.savefig(ruta_guardado)
                print("Gráfica guardada.")
                print("")
                input("Presiona enter para continuar. ")
                print("")

            elif una_o_todas == "2":
                nombre_para_grafica = ""
                for i in directorios_finales:
                    nombre_para_grafica += i[0:-4] + ", "
                nombre_para_grafica = nombre_para_grafica[0:-1]
                if len(nombre_para_grafica) > 50:
                    nombre_para_grafica = "Todas las listas"

                megalista = []
                for i in diccionario_referencia_numero_directorio:
                    datos_NAD = datos_nad(i)
                    convertir_tiempo_a_ms(datos_NAD)
                    for j in datos_NAD:
                        j.append(i)
                    for dato in datos_NAD:
                        megalista.append(dato)
                eje_x, eje_y = datos_grafica(megalista)

                plt.plot(eje_x, eje_y, marker="o")

                plt.xlabel("Duración en minutos (redondeado)")
                plt.ylabel("Cantidad con esa duración")
                plt.title(nombre_para_grafica)

                plt.grid(True)
                plt.tight_layout()
                ruta_guardado = os.getcwd()
                ruta_guardado += "/Gráficas de estadística"
                ruta_guardado += "/" + nombre_para_grafica
                plt.savefig(ruta_guardado)
                print("Gráfica guardada.")
                print("")
                input("Presiona enter para continuar. ")
                print("")

    elif eleccion == "x":
        break
