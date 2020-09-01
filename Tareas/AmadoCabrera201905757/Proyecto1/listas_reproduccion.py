from bs4 import BeautifulSoup
import os
import subprocess
import time
from datetime import datetime
from matplotlib import pyplot as plt

class Documento:
    # Atributos
    def __init__(self, archivo):
        self.archivo = archivo

    initial_directory = os.getcwd()
    playlist_name = ''
    save_name = ''
    posible_playlist = False
    songs = {}
    orden = []
    repeticion = []
    report = '' # 'Markdown' 'LaTeX' 'Pdf'
    existant_graph = False

    tex = """\\documentclass{article}
\\usepackage[utf8]{inputenc}
\\usepackage{graphicx}

\\title{Reporte lista de reproducción\\\\
NOMBRELISTAREPRO}
\\date{DATE}

\\begin{document}

\\maketitle
\\begin{center}
\\rule{30em}{0.1ex}
\\end{center}

\\section{Canciones}
SUSTITUCION1

\\end{document}"""

    md = """# Reporte lista de reproducción
# NOMBRELISTAREPRO
DATE

***

## Canciones
SUSTITUCION1"""

    # Metodos
    def nombre_playlist(self):
        """Nombres para guardar los archivos"""
        with open(self.archivo, 'r') as xml_file:
            soup = BeautifulSoup(xml_file, 'lxml')
            container = soup.find('array').find('dict').find_all('key')
            for x in container:
                if x.text == 'Name':
                    self.playlist_name = x.next_sibling.text
        tiempo = str(datetime.now()).replace(' ', '_')
        self.save_name = (f'{self.playlist_name}_{tiempo}')
        self.save_name = self.save_name.replace(' ', '_')

    def probability_playlist(self):
        """Define la probabilidad de que un documento sea playlist"""
        with open(self.archivo, 'r') as xml_file:
            contenido = xml_file.readlines()
            for i in contenido:
                if i.find('!DOCTYPE plist') == 1:
                    self.posible_playlist = True
                    return 0
                else:
                    pass

    def find_songs(self):
        """Parsea el XML y hace un diccionaro con los valores"""
        song_id = []
        nombre = []
        artista = []
        duracion = []
        with open(self.archivo, 'r') as xml_file:
            soup = BeautifulSoup(xml_file, 'lxml')
            container = soup.find('dict').find('dict').find_all('dict')
            for mini_container in container:
                llaves = mini_container.find_all('key')
                for i in llaves:
                    if i.text == 'Name':
                        nombre.append(i.next_sibling.text)
                    elif i.text == 'Artist':
                        artista.append(i.next_sibling.text)
                    elif i.text == 'Track ID':
                        song_id.append(i.next_sibling.text)
                    elif i.text == 'Total Time':
                        duracion.append(i.next_sibling.text)
                    else:
                        pass
        self.songs['nombre'] = nombre
        self.songs['song id'] = song_id
        self.songs['artista'] = artista
        self.songs['duracion'] = duracion

    def orden_canciones(self):
        """Guarda el orden de las canciones en una lista"""
        with open(self.archivo, 'r') as xml_file:
            soup = BeautifulSoup(xml_file, 'lxml')
            container = soup.find('array').find('array').find_all('integer')
            for i in container:
                self.orden.append(i.text)

    def find_repetidos(self):
        """Encuentra la repeticion de las canciones en una playlist y agrega
        estos valores al diccionario con los valores"""
        repeticiones = []
        auxiliar = self.orden.copy()
        while auxiliar:
            val = auxiliar[0]
            self.repeticion.append((val,auxiliar.count(val)))
            repeticiones.append(auxiliar.count(val))
            for _ in range(auxiliar.count(val)):
                auxiliar.remove(val)
        self.songs['repeticion'] = repeticiones

    def write_csv(self):
        """Recibe nombre para un documento le coloca la extensión CSV
        y guarda en el los valores de la playlist"""
        os.chdir(os.path.join(self.initial_directory, 'ListasCSV'))
        with open(f'{self.save_name}.csv', 'w') as csv_file:
            csv_file.write('Song ID, Nombre, Artista, Duración, Repetición\n')
            for i in range(len(self.songs.get('nombre'))):
                csv_file.write(self.songs.get('song id')[i] + ', "')
                csv_file.write(self.songs.get('nombre')[i] + '", "')
                csv_file.write(self.songs.get('artista')[i] + '", ')
                csv_file.write(self.songs.get('duracion')[i] + ', ')
                for j in self.repeticion:
                    if self.songs.get('song id')[i]==j[0]:
                        csv_file.write(str(j[1]) + '\n')

    def make_report(self):
        """Imprime en terminal un reporte de las canciones"""
        press("--REPORTE--", sty='bold')
        print(f'Las canciones en la lista de reproducción: {self.archivo}')
        for i in range(len(self.songs.get('nombre'))):
            print(f'\nCanción #{i+1}')
            print(f"{bl}Nombre: {self.songs.get('nombre')[i]}")
            print(f"{bl}Artista: {self.songs.get('artista')[i]}")
            print(f"{bl}Duración: {timet(self.songs.get('duracion')[i])}")
            for j in self.repeticion:
                    if self.songs.get('song id')[i]==j[0]:
                        print(f"{bl}Veces agregada: {j[1]}")
    
    def make_graph(self): # No funciona (ni se usa en el programa)
        """Hace un grafico de barras con canción y duración"""
        tiempo = [int(i) for i in self.songs.get('duracion')]
        nombrec = self.songs.get('nombre')
        plt.barh(nombrec, tiempo)
        plt.xlabel('Canciones')
        plt.ylabel('Duracion en ms')
        plt.title('Graficas de duración')
        os.chdir(os.path.join(self.initial_directory, 'Reportes'))
        plt.savefig(f'{self.save_name}.png')
        plt.show()
        self.existant_graph = True

    def make_histogram(self, bin_n):
        """Crea un histograma de la duración de las canciones"""
        tiempo = []
        for i in self.repeticion:
            for _ in range(i[1]):
                indice = self.songs.get('song id').index(i[0])
                tiempo.append(self.songs.get('duracion')[indice])
        tiempo.sort()
        tiempo = [int(i) for i in tiempo]
        plt.hist(tiempo, bins=bin_n, edgecolor='black')
        plt.xlabel('Duracion en ms')
        plt.title('Histograma de duración')
        os.chdir(self.initial_directory)
        os.chdir(os.path.join(self.initial_directory, 'Reportes'))
        plt.savefig(f'{self.save_name}.png')
        plt.show()
        self.existant_graph = True

    def save_report(self):
        """Crea un reporte en distintos formatos y lo guarda"""
        if (self.report == 'LaTeX' or self.report == 'Pdf'):
            self.tex = self.tex.replace('NOMBRELISTAREPRO', self.playlist_name)
            self.tex = self.tex.replace('DATE', str(datetime.now()))
            begin = "\\begin{enumerate}\n"
            for i in range(len(self.songs.get('nombre'))):
                begin += f'\t\\item Canción\n'
                begin += '\t\\begin{itemize}\n'
                begin += '\t\t\\item Nombre: '
                begin += self.songs.get('nombre')[i].replace('&', '\\&') + '\n'
                begin += '\t\t\\item Artista: '
                begin += self.songs.get('artista')[i] + '\n'
                begin += '\t\t\\item Duración: '
                begin += timet(self.songs.get('duracion')[i]) + '\n'
                begin += '\t\t\\item Repetición: '
                for j in self.repeticion:
                    if self.songs.get('song id')[i]==j[0]:
                        begin += str(j[1]) + '\n'
                begin += '\t\\end{itemize}\n'
            begin += '\\end{enumerate}\n\n'
            if self.existant_graph:
                begin += "\\section{Grafica}\n"
                begin += "\\begin{center}\n"
                begin += "\\includegraphics[scale=0.75]{" + self.save_name
                begin += ".png}\n"
                begin += "\\end{center}\n"
            else:
                pass
            self.tex = self.tex.replace('SUSTITUCION1', begin)
            os.chdir(os.path.join(self.initial_directory, 'Reportes'))
            with open(f'{self.save_name}.tex', 'w') as f:
                f.write(self.tex)
            if self.report == 'Pdf':
                subprocess.run(f'pdflatex --interaction=batchmode {self.save_name}.tex' ,shell=True)
                subprocess.run(f'rm {self.save_name}.log', shell=True)
                subprocess.run(f'rm {self.save_name}.aux', shell=True)
                subprocess.run(f'rm {self.save_name}.tex', shell=True)
            else:
                pass
        elif self.report == 'Markdown':
            self.md = self.md.replace('NOMBRELISTAREPRO', self.playlist_name)
            self.md = self.md.replace('DATE', str(datetime.now()))
            begin = ''
            for i in range(len(self.songs.get('nombre'))):
                begin += f'{i+1}. Canción\n'
                begin += '\t* Nombre: '
                begin += self.songs.get('nombre')[i] + '\n'
                begin += '\t* Artista: '
                begin += self.songs.get('artista')[i] + '\n'
                begin += '\t* Duración: '
                begin += timet(self.songs.get('duracion')[i]) + '\n'
                begin += '\t* Repetición: '
                for j in self.repeticion:
                    if self.songs.get('song id')[i]==j[0]:
                        begin += str(j[1]) + '\n'
            if self.existant_graph:
                begin += '\n## Grafica\n'
                begin += '![Image](' + self.save_name + '.png)'
            else:
                pass
            self.md = self.md.replace('SUSTITUCION1', begin)
            os.chdir(os.path.join(self.initial_directory, 'Reportes'))
            with open(f'{self.save_name}.md', 'w') as f:
                f.write(self.md)
        else:
            pass
    

    def restart(self):
        """Reinicia los valores de la clase"""
        #del self.initial_directory
        del self.playlist_name
        del self.save_name
        #del self.posible_playlist
        self.songs.clear()
        self.orden.clear()
        self.repeticion.clear()
        #del self.report
        self.existant_graph = False

bl = '\033[1;35m  • \033[0;m'

styles = {
    'nan' : 0, 'bold' : 1, 'weak' : 2, 'italic' : 3,
    'under' : 4, 'inv' : 5, 'cens' : 6, 'stk' : 7
}
color_txt = {
    'black' : 30, 'red' : 31, 'green' : 32, 'yellow' : 33,
    'blue' : 34, 'purple' : 35, 'cian' : 36, 'white' : 37,
    'nothing' : ''
}
color_bg = {
    'black' : 40, 'red' : 41, 'green' : 42, 'yellow' : 43,
    'blue' : 44, 'purple' : 45, 'cian' : 46, 'white' : 47,
    'nothing' : ''
}

def press(string, sty='nan', bg_color='nothing', bt_color='nothing'):
    """Imprime en consola con estilos personalizables"""
    estilo = styles.get(sty)
    txtcolor = color_txt.get(bt_color)
    bgcolor = color_bg.get(bg_color)
    string = str(string)
    if bgcolor == '':
        print(f'\033[{estilo};{txtcolor}m' + string + '\033[0;m')
    else:
        print(f'\033[{estilo};{txtcolor};{bgcolor}m' + string + '\033[0;m')

def timet(milisecs):
    """Recibe un entero en milisegundos y lo imprime en formato
    min:sec.mili_sec"""
    tiempo = str(milisecs)
    mili_segundos = tiempo[-3:]
    minutos = int(tiempo[0:-3])
    if minutos%60 < 10:
        return f'{minutos//60}:0{minutos%60}.{mili_segundos}'
    else:
        return f'{minutos//60}:{minutos%60}.{mili_segundos}'

def directorio_csvs():
    """Si existe directorio con ese nombre no hace nada, si no existe
    lo crea"""
    for i in os.listdir():
        if i == 'ListasCSV':
            return 1
    os.mkdir('ListasCSV')
    return 0

def directorio_repor():
    """Si existe directorio con ese nombre no hace nada, si no existe
    lo crea"""
    for i in os.listdir():
        if i == 'Reportes':
            return 1
    os.mkdir('Reportes')
    return 0

def barra_carga(archivo):
    """Crea una barra de carga y ejecuta las funciones necesarias para cada 
    clase"""
    carga="[                                                            ](0%)"
    print(carga)
    time.sleep(0.5)
    archivo.find_songs()
    subprocess.run('clear', shell=True)
    carga="[████████████████████                                        ](33%)"
    print(carga)
    time.sleep(0.5)
    archivo.orden_canciones()
    subprocess.run('clear', shell=True)
    carga="[████████████████████████████████████████                    ](66%)"
    print(carga)
    time.sleep(0.5)
    archivo.find_repetidos()
    subprocess.run('clear', shell=True)
    carga="[████████████████████████████████████████████████████████████](100%)"
    print(carga)
    time.sleep(0.5)
    subprocess.run('clear', shell=True)

header = """|--------------------------------------------------------------|
| LEER LISTAS DE REPRODUCIÓN CONSTRUIDAS DESDE ITUNES DE APPLE |
|--------------------------------------------------------------|
Con este script de python usted podrá leer listas de
reproducción que hayan sido construidas desde la 
herramienta Itunes de Apple.
"""

instrucciones = """
Ingrese la ruta absoluta del directorio donde se buscaran 
las listas de reproduccion a parsear, si no conoce la ruta 
absoluta arrastre el directorio que desea ingresar hacia a 
la terminal. Si coloca «quit()» el programa acabará"""

pregunta = ">>> "

cabecera_documentos = """Los documentos .xml que se han encontrado en su 
carpeta son:"""

mensaje_documentos = """\nLos documentos en \033[0;32m verde\033[0;m son posiblemente una 
lista de reproducción, los \033[0;31m rojos\033[0;m no.
"""

if __name__ == "__main__":
    amigos = 'Datos/To_parse.xml'
    intento1 = Documento(amigos)
    intento1.probability_playlist()
    print(intento1.posible_playlist, end='\n\n')
    intento1.find_songs()
    print(intento1.songs, end='\n\n')
    intento1.orden_canciones()
    print(intento1.orden)
    intento1.find_repetidos()
    print(intento1.repeticion)
    intento1.write_csv()
    press('hola mundo')
    timet(285178)
    print(intento1.playlist_name)
    print(intento1.save_name)
    intento1.nombre_playlist()
    intento1.make_histogram(5)
    intento1.save_report()