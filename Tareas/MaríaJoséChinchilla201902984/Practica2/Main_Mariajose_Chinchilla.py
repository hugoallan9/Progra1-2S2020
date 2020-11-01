import matplotlib as mlp
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib import animation
from matplotlib.widgets import Button
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas
from datetime import datetime
import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk
from gi.repository import Gdk
import webbrowser
import numpy as np
import random
import time
import os


class JuegoDeLaVida(Gtk.Window):
    normal = True   #interruptor para saber que frontera quiere el usuario, los radio botones lo modifican
    TimeFrame = 1
    segundos = Gtk.SpinButton()
    guardado = True
    def __init__(self):
        super(JuegoDeLaVida, self).__init__(title='Juego de la vida, autómata celular')
    #Cuestiones basicas para la ventana y los contenedores
        self.set_default_size(400, 600)
        self.set_resizable(False)  # fijar el tamaño de la ventana
        vbox = Gtk.VBox()
        self.add(vbox)
        grid = Gtk.Grid()
        grid.set_row_spacing(2)
        grid.set_column_spacing(2)
        vbox.pack_start(grid, True, True, 0)
        self.pause = True
        self.now = datetime.now()
        self.cuenta = 0

    #Menu y todos sus items
        menubar = Gtk.MenuBar()  # barra de menu

        # elementos en el menu
        archivo = Gtk.MenuItem('Archivo')
        config = Gtk.MenuItem('Configuración')
        ayuda = Gtk.MenuItem('Ayuda')

        # SUBMENU DE LA OPCION ARCHIVO
        arch_menu = Gtk.Menu()
        config_inicial = Gtk.MenuItem('Cargar configuración inicial')
        arch_menu.append(config_inicial)
        generar = Gtk.MenuItem('Generar configuración aleatoria')
        arch_menu.append(generar)
        archivo.set_submenu(arch_menu)

        # ACCIONES DE LOS ITEMS DE ARCHIVO PARA PANTALLAS CORRESPONDIENTES SEGUN BOTON
        config_inicial.connect('activate', self.cargar_config_inicial)
        generar.connect('activate', self.generar_jugar_aleatorio)

        # SUBMENU DE AYUDA
        ayuda_menu = Gtk.Menu()
        acerca_de = Gtk.MenuItem('Acerca de')
        cod_fuente = Gtk.MenuItem('Código fuente GitHub')
        ayuda_menu.append(acerca_de)
        ayuda_menu.append(cod_fuente)
        ayuda.set_submenu(ayuda_menu)

        # ACCIONES DE MENU DE AYUDA
        acerca_de.connect('activate', self.acerca_de)
        cod_fuente.connect('activate', self.codigo_fuente)

        # agregar las opciones al menu
        menubar.append(archivo)
        menubar.append(ayuda)
        grid.attach(menubar, 0,0, 5, 1)
#el submenu de configuracion aparece siempre y no esta en la barra de menu para facilidad de modificacion de
        #las configuraciones

#Radio button para que el usuario deje seleccionado un tipo de frontera

        tipos_de_frontera = Gtk.Label('Tipo de frontera para el juego')
        grid.attach(tipos_de_frontera, 1, 1, 1, 3)
        radio_boton_normales = Gtk.RadioButton.new_with_label_from_widget(None, 'Fronteras normales')
        radio_boton_normales.connect('toggled', self.elegido_normal)
        grid.attach_next_to(radio_boton_normales, tipos_de_frontera, Gtk.PositionType.BOTTOM, 1, 1)

        radio_boton_toroidales = Gtk.RadioButton.new_from_widget(radio_boton_normales)
        radio_boton_toroidales.set_label('Fronteras toroidales')
        radio_boton_toroidales.connect('toggled', self.elegido_toroidal)
        grid.attach_next_to(radio_boton_toroidales, radio_boton_normales, Gtk.PositionType.RIGHT, 1, 1)

        # se usaran dos radio botones para guardar estado o no
        # si esta seleccionado si, entonces se guarda automaticamente en el directorio
        label_guardado = Gtk.Label('¿Guardar el estado de simulación en el directorio?')
        grid.attach_next_to(label_guardado, radio_boton_normales, Gtk.PositionType.BOTTOM, 1, 1)
        guardar_automatico = Gtk.RadioButton.new_with_label_from_widget(None, 'Guardar automáticamente')
        guardar_automatico.connect('toggled', self.si_automatico)
        grid.attach_next_to(guardar_automatico, label_guardado, Gtk.PositionType.BOTTOM, 1, 1)
        no_guardar = Gtk.RadioButton.new_from_widget(guardar_automatico)
        no_guardar.set_label('No guardar')
        no_guardar.connect('toggled', self.no_guardar)
        grid.attach_next_to(no_guardar, guardar_automatico, Gtk.PositionType.RIGHT, 1, 1)

        segundos_label = Gtk.Label('Segundos de espera entre turnos')
        grid.attach(segundos_label, 24, 1, 1, 3)
        self.segundos.set_digits(2)
        ajuste = Gtk.Adjustment(lower=0.00001, upper=5, step_increment=0.01, page_increment=0.01)
        self.segundos.set_adjustment(ajuste)
        grid.attach_next_to(self.segundos, segundos_label, Gtk.PositionType.BOTTOM, 1, 1)
        boton_elegir_tiempo = Gtk.Button('Ok')
        boton_elegir_tiempo.connect('clicked', self.tiempo_elegido)
        grid.attach_next_to(boton_elegir_tiempo, self.segundos, Gtk.PositionType.RIGHT, 1, 1)

#botones de pausar/jugar y el de tomar captura de pantalla
        pausa_jugar_boton = Gtk.Button('Jugar/Pausar')
        pausa_jugar_boton.connect('clicked', self.play_pause)
        grid.attach(pausa_jugar_boton, 24, 200, 1, 1)
        captura_boton = Gtk.Button('Captura de pantalla')
        captura_boton.connect('clicked', self.captura_de_pantalla)
        grid.attach_next_to(captura_boton, pausa_jugar_boton, Gtk.PositionType.BOTTOM, 1, 1)
        mensaje = Gtk.Label('Capturas serán guardadas en el directorio actual.')
        grid.attach_next_to(mensaje, captura_boton, Gtk.PositionType.BOTTOM, 1, 1)

            #ACCIONES DE LOS RADIO BOTONES, SABER CUAL ESTA ELEGIDO
# Acciones de los radio botones, esto servira para saber que tipo de forntera quiere el usuario,
# permanecera activado para todas las configuraciones al menos que el usuario lo cambie
    def si_automatico(self, widget):
        self.guardado = True

    def no_guardar(self, widget):
        self.guardado = False

    def elegido_normal(self, widget):
        self.normal = True

    def elegido_toroidal(self, widget):
        self.normal = False

#boton que guarda el tiempo de espera elegido por el usuario
    def tiempo_elegido(self, widget):
        self.TimeFrame = float(self.segundos.get_text())
        #no entiendo por que si cambie el self.TimeFrame y cuando hago la figura esta indicado que use eso
        #pero no lo cambia ya dentro de la figura

    #metodos para cada boton

    def cargar_config_inicial(self, widget):        #abre el dialogo para elegir un archivo a cargar
        dialogo = Gtk.FileChooserDialog('Select a File', None, Gtk.FileChooserAction.OPEN,
                                       ('Cancelar', Gtk.ResponseType.CANCEL, 'Seleccionar', Gtk.ResponseType.OK))
        respuesta = dialogo.run()
        if respuesta == Gtk.ResponseType.OK:
            # Lectura del archivo .pm2
            file = open(dialogo.get_filename(), 'r')
            global N
            N = int(file.readline())
            linea = [line.split() for line in file]
            global tablero
            tablero = np.zeros((N, N))
            for j in range(len(linea)):
                for i in range(len(linea)):
                    tablero[j, i] = eval(linea[j][i])
            dialogo.close()
            if self.normal == True:     #evaluar que frontera aplicar en las reglas del juego para el archivo cargado
                self.normales_cargado(tablero)
                if self.guardado == True:
                    self.guardar_estado(tablero)
            elif self.normal == False:
                self.toroidales_cargado(tablero)
                if self.guardado == True:
                    self.guardar_estado(tablero)
        elif respuesta == Gtk.ResponseType.CANCEL:
            pass
        dialogo.destroy()

    def guardar_estado(self,tablero):   #para guardar el estado del juego siguiendo las instrucciones de la practica
        estado = 'Estados_del_juego ' + str(self.now.year) + '-' + str(self.now.month) + '-' + str(self.now.day) + \
                 '-' + str(self.now.hour) + '-' + str(self.now.minute) + '-' + str(self.now.second) + '.jvpm2'
        arch = open(estado, 'w+')
        N = int(len(tablero))
        arch.write(str(N) + '\n')
        for i in range(N):
            linea = ''
            for j in range(N):
                linea = linea + str(tablero[j, i]) + ' '
            arch.write(linea + '\n')
        arch.close()

    def generar_jugar_aleatorio(self, widget):  #genera aleatoriamente un tablero con juego
        global N
        N = random.randint(3, 250)      #elige al azar una dimension para la cuadricula del juego
        global tablero
        tablero = np.zeros((N, N), dtype=int)
#generar el tablero a partir de la informacion anterior elegida aleatoriamente
        for i in range(N):
            for j in range(N):
                tablero[i, j] = random.randint(0, 1)
        if self.normal == True:
            self.normales_cargado(tablero)
            if self.guardado == True:
                self.guardar_estado(tablero)
        elif self.normal == False:
            self.toroidales_cargado(tablero)
            if self.guardado == True:
                self.guardar_estado(tablero)

# funciones para cargar un archivo inicial y poner pausa y demas

    def play_pause(self, widget):
        self.pause ^= True      #esto va a servir como un interruptor para normal_cargado funcion

    def captura_de_pantalla(self, widget):      #guardar captura de pantalla en el 'current working directory'
        plt.savefig(os.getcwd() + 'Juego en curso'+ str(self.now.year) + str(self.now.month) + str(self.now.day)
                    + str(self.now.hour) + str(self.now.minute) + str(self.now.second)+
                    '.png', dpi = 200, facecolor = 'w')
        cadena = str(os.getcwd())
        print('Su captura ha sido guardada en el current working directory:' + cadena)

# para evaluar que debe pasar con una celula, evaluar a sus 8 vecinas
#considerar "mover" las celulas en las 8 direcciones. Por cada movimiento, sumar el
#valor de la celula en esa posicion. El valor final que tome cada celula luego de los 8
#movimientos es el numero de celulas vecinas vivas.
    def normales_cargado(self, tablero):

        def conteo_normales(tablero):
            global vecindario
            vecindario = np.zeros((len(tablero), len(tablero)), dtype = int)
            for j in range(1, len(tablero) - 1):
                for i in range(1, len(tablero) - 1):
                    vecindario[j, i] = (
                            tablero[j + 1, i - 1] +  # Abajo - Izquierda
                            tablero[j + 1, i] +  # Abajo
                            tablero[j + 1, i + 1] +  # Abajo - Derecha
                            tablero[j, i + 1] +  # Derecha
                            tablero[j - 1, i + 1] +  # Arriba - Derecha
                            tablero[j - 1, i] +  # Arriba
                            tablero[j - 1, i - 1] +  # Arriba - Izquierda
                            tablero[j, i - 1]  # Izquierda
                    )
            for i in range(1, len(tablero) - 1):
                    vecindario[0, i] = (
                            tablero[0, i - 1] +  # Izquierda
                            tablero[1, i - 1] +  # Abajo - Izquierda
                            tablero[1, i] +  # Abajo
                            tablero[1, i + 1] +  # Abajo - Derecha
                            tablero[0, i + 1]  # Derecha
                    )
            for i in range(1, len(tablero) - 1):
                    vecindario[N - 1, i] = (
                            tablero[N - 1, i - 1] +  # Izquierda
                            tablero[N - 2, i - 1] +  # Arriba - Izquierda
                            tablero[N - 2, i] +  # Arriba
                            tablero[N - 2, i + 1] +  # Arriba - Derecha
                            tablero[N - 1, i + 1]  # Derecha
                    )
            for j in range(1, len(tablero) - 1):
                    vecindario[j, 0] = (
                            tablero[j - 1, 0] +  # Arriba
                            tablero[j - 1, 1] +  # Arriba - Derecha
                            tablero[j, 1] +  # Derecha
                            tablero[j + 1, 1] +  # Abajo - Derecha
                            tablero[j + 1, 0]  # Abajo
                    )
            for j in range(1, len(tablero) - 1):
                    vecindario[j, 0] = (
                            tablero[j - 1, N - 1] +  # Arriba
                            tablero[j - 1, N - 2] +  # Arriba - Izquierda
                            tablero[j, N - 2] +  # Izquierda
                            tablero[j + 1, N - 2] +  # Abajo - Izquierda
                            tablero[j + 1, N - 1]  # Abajo
                    )
            vecindario[0, 0] = (
                    tablero[0, 1] +  # Derecha
                    tablero[1, 1] +  # Abajo - Derecha
                    tablero[1, 0]  # Abajo
            )
            vecindario[0, N - 1] = (
                    tablero[0, N - 2] +  # Izquierda
                    tablero[1, N - 2] +  # Abajo - Izquierda
                    tablero[1, N - 1]  # Abajo
            )
            vecindario[N - 1, 0] = (
                    tablero[N - 2, 0] +  # Arriba
                    tablero[N - 2, 1] +  # Arriba - Derecha
                    tablero[N - 1, 1]  # Derecha
            )
            vecindario[N - 1, N - 1] = (
                    tablero[N - 2, N - 1] +  # Arriba
                    tablero[N - 2, N - 2] +  # Arriba - Izquierda
                    tablero[N - 1, N - 2]  # Izquierda
            )
            return vecindario

        def paso(tablero):
        # evaluacion de que pasara con la celula dependiendo de las reglas del juego
            v = conteo_normales(tablero)
            nuevo_tablero = tablero.copy()
            for i in range(nuevo_tablero.shape[0]):
                for j in range(nuevo_tablero.shape[1]):
                    if v[i, j] == 3 or (v[i, j] == 2 and tablero[i, j]):
                        nuevo_tablero[i, j] = 1
                        self.cuenta = self.cuenta + 1
                    else:
                        nuevo_tablero[i, j] = 0
                        self.cuenta = self.cuenta + 1
            return nuevo_tablero

#creacion de figura en matplotlib

        fig = plt.figure(figsize=(6, 6))
        ax = fig.add_subplot(111)
        titulo = f'Turno: {self.cuenta}'  # poner el numero de turno como titulo de la figura de matplotlib
        ax.set_title(titulo)  # agrega lo anterior como titulo de la figura
        imagen = ax.imshow(tablero, interpolation="none", aspect="equal", cmap=cm.bwr)
        plt.tick_params(
            axis='x',
            which='both',
            bottom=False,
            top=False,
            labelbottom=False)

        def animacion(i):
            global tablero
            if self.pause == False:
                tablero = paso(tablero)
                imagen.set_data(tablero)

            return imagen,

        anim = animation.FuncAnimation(fig, animacion,
                                       frames=100, blit=True, interval=(self.TimeFrame * 1000),
                                       repeat=True)
        plt.show()

#sospecho que se esta agregando al scrolled window pero este no esta agregado en la ventana principal

        #mostrar figura
    def toroidales_cargado(self, tablero):
        def vecindad(tablero):
#conteo de las vivas para ver si una celula tiene sobrepoblacion o esta en soledad
#np.roll podria hacerse la analogia que es como mover el tablero en las direcciones indicadas y a partir de eso, contar
            total = (
                np.roll(np.roll(tablero, 1, 1), 1, 0) +  # Abajo-derecha
                np.roll(tablero, 1, 0) +  # Abajo
                np.roll(np.roll(tablero, -1, 1), 1, 0) +  # Abajo-izquierda
                np.roll(tablero, -1, 1) +  # Izquierda
                np.roll(np.roll(tablero, -1, 1), -1, 0) +  # Arriba-izquierda
                np.roll(tablero, -1, 0) +  # Arriba
                np.roll(np.roll(tablero, 1, 1), -1, 0) +  # Arriba-derecha
                np.roll(tablero, 1, 1)  # Derecha
            )
            return total

        def paso(tablero):
#Aplicar las reglas del juego
            v = vecindad(tablero)
            nuevo_tablero = tablero.copy()  # Copia de la matriz para no sobreescribir
            for i in range(nuevo_tablero.shape[0]):
                for j in range(nuevo_tablero.shape[1]):
                    if v[i, j] == 3 or (v[i, j] == 2 and nuevo_tablero[i, j]):
                        nuevo_tablero[i, j] = 1
                        self.cuenta = self.cuenta + 1
                    else:
                        nuevo_tablero[i, j] = 0
                        self.cueta = self.cuenta + 1
            return nuevo_tablero

        fig = plt.figure(figsize=(4, 4))
        ax = fig.add_subplot(111)
        titulo = f'Turno: {self.cuenta}'  # poner el numero de turno como titulo de la figura de matplotlib
        ax.set_title(titulo)  # agrega lo anterior como titulo de la figura
        global imagen
        imagen = ax.imshow(tablero, interpolation="none", aspect="equal", cmap=cm.bwr)
        plt.tick_params(
            axis='x',
            which='both',
            bottom=False,
            top=False,
            labelleft=False,
            labelbottom=True)

        def animacion(i):
            global tablero
            if self.pause == False:
                tablero = paso(tablero)
                imagen.set_data(tablero)

            return imagen,

        anim = animation.FuncAnimation(fig, animacion, frames=100, blit=True, interval=(self.TimeFrame * 1000),
                                       save_count=1, repeat=True)
        plt.show()

    def segundos_espera(self,widget):
        pass

    def acerca_de(self, widget):
        #acerca de dialogo
        vbox = Gtk.VBox()
        acerca_de_dialogo = Gtk.AboutDialog()
        acerca_de_dialogo.set_program_name('El juego de la vida')
        acerca_de_dialogo.set_version('PM 1')
        acerca_de_dialogo.set_authors('MCM')
        acerca_de_dialogo.set_copyright('Desarrollo de interfaz gráfica en Gtk 3.0')
        acerca_de_dialogo.set_comments('Uso de Gtk 3.0, Numpy, MatplotLib')
        acerca_de_dialogo.set_website('https://github.com/MariajoseChinchilla/TestGit/blob/master/Main.py')
        vbox.pack_start(acerca_de_dialogo, False, False, 0)
        self.add(vbox)
        acerca_de_dialogo.run()
        acerca_de_dialogo.destroy()

    def codigo_fuente(self, widget):
        webbrowser.open_new_tab('https://github.com/MariajoseChinchilla/TestGit/blob/master/Main.py')

win = JuegoDeLaVida()
win.connect('destroy', Gtk.main_quit)
win.show_all()
Gtk.main()