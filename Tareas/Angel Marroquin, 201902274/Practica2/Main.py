import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import time
import random

import matplotlib.pyplot as plt #Para el grid
import matplotlib as mlp
from matplotlib import colors #Para los colores de las celulas
import matplotlib.animation as animation
import numpy as np #Tengo entendido que para el uso de matrices
from numpy import save

from matplotlib.backends.backend_gtk3agg import (
    FigureCanvasGTK3Agg as FigureCanvas)
from matplotlib.figure import Figure

import os
import webbrowser
from datetime import datetime


UI_INFO = """
<ui>
  <menubar name='menuBar'>
    <menu action='archivo'>
      <menuitem action='cargarInicio' />
      <menuitem action='guardarSimulacion' />
      <menuitem action='random' />
      <separator />
      <menuitem action='FileQuit' />
    </menu>
    <menu action='config'>
      <menuitem action='fronteraNorm' />
      <menuitem action='fronteraToro' />
      <separator />
      <menuitem action='actualizarIntervalo' />
    </menu>
    <menu action='help'>
      <menuitem action='about'/>
      <menuitem action='code'/>
    </menu>
  </menubar>
</ui>
"""

class ventana(Gtk.Window):
	def __init__(self):
		Gtk.Window.__init__(self, title='El juego de la vida')
		#Parametro de inicio utiles
		self.anim_running = False
		self.fronteras = 'Normal'
		self.intervaloActu = 100
		self.dimensionMatriz = 10
		self.conteo = 1
		self.ruta = ''

		#Para iniciar el programa con un grid 'muerto'
		self.grid = np.zeros((self.dimensionMatriz,self.dimensionMatriz), dtype=int)
		self.gridIni = np.zeros((self.dimensionMatriz,self.dimensionMatriz), dtype=int)

		#Inicializacion de lo necesario para la animacion
		self.figure = mlp.figure.Figure()
		self.canvas = FigureCanvas(self.figure)

		#Tamaño de la ventana
		self.set_default_size(700,00)
		#Para el barmenu
		self.action = Gtk.ActionGroup(name='action')
		self.menuArchivo(self.action)
		self.menuConfig(self.action)
		self.menuAyuda(self.action)
		uimanager = self.create_ui_manager()
		uimanager.insert_action_group(self.action)
		menubar = uimanager.get_widget('/menuBar')

		#Grid donde estara toda la interfaz
		container = Gtk.Grid()
		container.set_row_spacing(5)
		container.set_column_spacing(5)
		container.attach(menubar, 0, 0, 10, 1)
		self.add(container)

		#La parte donde estara el grid
		self.sw = Gtk.ScrolledWindow()
		container.attach(self.sw, 0, 1, 60, 90)
		self.sw.set_border_width(1)
		self.canvas1 = self.animacion()
		self.sw.add(self.canvas1)

		#Cosas extras
		self.buttonPausar = Gtk.Button(label='Pausar')
		self.buttonPausar.connect('clicked', self.onClick)
		container.attach_next_to(self.buttonPausar, self.sw, Gtk.PositionType.RIGHT, 5, 5)

		self.buttonCaptura = Gtk.Button(label='TomarCaptura')
		self.buttonCaptura.connect('clicked', self.imprimirCaptura)
		container.attach_next_to(self.buttonCaptura, self.buttonPausar, Gtk.PositionType.RIGHT,5,5)

		self.label = Gtk.Label()
		self.label.set_label('Turno: '+str(self.conteo))
		container.attach(self.label, 0, 91, 1, 5)

	def imprimirCaptura(self, event):
		'''
		Para tomar una foto del estado actual del ScrolledWindow
		:param event:
		:return:
		'''
		now = datetime.now()
		titulo = str(now.day) + '-' + str(now.month) + '-' + str(now.day) + '  ' + str(now.hour) + ':' + str(now.minute)
		self.figure.savefig(os.getcwd()+'/capturas/'+titulo+'.png')

	def create_ui_manager(self):
		'''
		Para el uso del barmenu
		:return:
		'''
		uimanager = Gtk.UIManager()
		uimanager.add_ui_from_string(UI_INFO)
		accelgroup = uimanager.get_accel_group()
		self.add_accel_group(accelgroup)
		return uimanager



	def menuArchivo(self, action_group):
		'''
		Pestaña 'Archivo'
		:param action_group:
		:return:
		'''
		action_group.add_actions(
			[
				("archivo", None, "Archivo"),
				("cargarInicio", None, 'Cargar', '<control>N', None, self.cargaEstado),
				("guardarSimulacion", None, 'Guardar Estado', "<control>G", None, self.guardarEstado),
				("random",None, 'Configuracion Random', "<control>R", None, self.random),
			]
		)

		action_filequit = Gtk.Action(name="FileQuit", stock_id=Gtk.STOCK_QUIT)
		action_filequit.connect("activate", self.cerrarVentana)
		action_group.add_action(action_filequit)

	def menuConfig(self, action_group):
		'''
		Pestaña 'Configuracion'
		:param action_group:
		:return:
		'''
		action_group.add_action(Gtk.Action(name="config", label="Configuracion"))

		action_group.add_radio_actions(
			[
				("fronteraNorm", None, "Normal", None, None, 1),
				("fronteraToro", None, "Toroidal", None, None, 2),
			],
			1,
			self.superficie,
		)
		intervalo = Gtk.Action(name='actualizarIntervalo', label='Intervalo')
		intervalo.connect('activate', self.intervalo)
		action_group.add_action(intervalo)

	def menuAyuda(self, action_group):
		'''
		Pestaña 'Ayuda'
		:param action_group:
		:return:
		'''
		action_group.add_actions(
			[
				("help", None, "Ayuda"),
				("about", None, 'Acerca de', None, None, self.acercaDe),
				("code", None, 'Codigo', None, None, self.codigoVida),
			]
		)

	def superficie(self, widget, current):
		'''
		Para diferenciar cual tipo de fronteras se esta usando
		:param widget:
		:param current:
		:return:
		'''
		if self.fronteras == 'Toro':
			self.fronteras = 'Normal'
		else:
			self.fronteras = 'Toro'

	def intervalo(self,widget):
		'''
		Abre una ventana para seleccionar el intervalo de actualizacion (por alguna razon despues de unas
		cuantas iteraciones se relentiza cuando el intervalo es muy pequeño)
		:param widget:
		:return:
		'''
		win = Gtk.Window()
		cosoGrid = Gtk.Grid()
		win.add(cosoGrid)
		def aceptar(event):
			inter = textBox.get_text()
			self.ani.event_source.interval = float(inter)*1000
			win.destroy()

		textBox = Gtk.Entry()
		cosoGrid.add(textBox)
		aceptarBtn = Gtk.Button(label='Aceptar')
		aceptarBtn.connect('clicked', aceptar)

		cosoGrid.add(aceptarBtn)
		win.connect("destroy", Gtk.main_quit)
		win.show_all()
		Gtk.main()

	def cargaEstado(self, widget):
		'''
		Selecciona un archivo para cargar en el ScrolledWindow
		:param widget:
		:return:
		'''
		dialog = Gtk.FileChooserDialog(
			title='Seleccione un estado a cargar', parent=self, action=Gtk.FileChooserAction.OPEN,
		)
		dialog.add_buttons(
			Gtk.STOCK_CANCEL,
			Gtk.ResponseType.CANCEL,
			Gtk.STOCK_OPEN,
			Gtk.ResponseType.OK
		)
		response = dialog.run()
		#self.onClick(response)
		#self.anim_running = False
		if response == Gtk.ResponseType.OK:
			self.ruta = dialog.get_filename()
			file = open(self.ruta, "r")
			line_count = 0
			for line in file:
				if line != "\n":
					line_count += 1
			file.close()
			skip = int(line_count)-(int(self.dimensionMatriz)+1)#Esto es para permitir leer archivos jvpm2 al tomar los
																#mismos datos que hay en un archivo pm2
			self.gridIni = np.genfromtxt(self.ruta, dtype='i', delimiter=' ', skip_header=1, skip_footer=skip)
			self.grid = np.genfromtxt(self.ruta, dtype='i', delimiter=' ', skip_header=1, skip_footer=skip)
			self.conteo = 1
			self.onClick(response) #Avanza un solo frame para cargar el estado en el ScrolledWindow
			self.anim_running = False
		elif response == Gtk.ResponseType.CANCEL:
			pass
		dialog.destroy()

	def guardarEstado(self, widget):
		coso1 = ''
		coso2 = ''
		turnosP = str(self.conteo)
		now = datetime.now()
		#Estos for recorden la matrix y luego cada fila y las concatena en una variable string para su posterior
		#almacenamiento
		for row in self.grid:
			for element in row:
				coso1+=str(element)+' '
			coso1+='\n'
		for row in self.gridIni:
			for element in row:
				coso2+=str(element)+' '
			coso2+='\n'
		titulo = str(now.day)+'-'+str(now.month)+'-'+str(now.day)+'  '+str(now.hour)+':'+str(now.minute)
		a_file = open(titulo+'.jvpm2', 'w+')
		a_file.write(str(self.dimensionMatriz)+'\n')
		contenido = coso1
		a_file.write(contenido)
		a_file.write('Turnos jugados: '+turnosP+'\n')
		a_file.write(coso2)
		a_file.close()

	def random(self, widget):
		#Genera una configuracion random
		temp = self.randomGrid(self.dimensionMatriz)
		self.gridIni = np.copy(temp)
		self.grid = np.copy(self.gridIni)
		self.onClick(widget)
		self.anim_running = False


	def cerrarVentana(self, widget):
		#Cierra ventana
		Gtk.main_quit()

	def acercaDe(self, widget):
		#Abre una ventana
		acercaDe = Gtk.AboutDialog()
		acercaDe.set_program_name('El juego de la vida')
		acercaDe.set_authors(['Jsfgefge/AngelMarroquin'])
		acercaDe.set_comments('Herramientas usadas:\n'
			'-Python v3.8.5\n'
			'-Gtk v3.0\n'
			'-Matplotlib v3.3.2\n'
			'-Numpy v1.19.2\n')
		acercaDe.set_title('uwu')
		acercaDe.run()
		acercaDe.destroy()

	def codigoVida(self, widget):
		webbrowser.open_new_tab("https://github.com/Jsfgefge/ProgramacionMatematica1/blob/master/Proyecto2/Main.py")

	def randomGrid(self,N):
		#Genera una matriz aleatoria
		return np.random.choice([1,0], N * N, p=[0.2, 0.8]).reshape(N,N)

	def onClick(self, event):
		#Al activarse el evento si esta en pausa se inicia y viceversa
		#self.anim:running ayuda para controlar esa accion
		if self.anim_running:
			self.ani.event_source.stop()
			self.anim_running = False
		else:
			self.ani.event_source.start()
			self.anim_running = True

	def onStart(self, event):
		#Ya que al inicio la animacion se inicia sola entonces esta funcion la detiene
		if self.anim_running == False:
			self.ani.event_source.stop()
		else:
			pass

	def iniConteo(self, event):
		#Para llevar el conteo de turnos
		if self.anim_running:
			self.conteo += 1
			self.label.set_label('Turno: '+str(self.conteo))

	def animacion(self):
		#Animacion
		N = self.dimensionMatriz
		def sumaToro(tabla, N):
			#Fronteras toroidales
			nTabla = self.grid
			for i in range(N):
				for j in range(N):
					total = int((tabla[i, (j - 1) % N] + tabla[i, (j + 1) % N] +
								 tabla[(i - 1) % N, j] + tabla[(i + 1) % N, j] +
								 tabla[(i - 1) % N, (j - 1) % N] + tabla[(i - 1) % N, (j + 1) % N] +
								 tabla[(i + 1) % N, (j - 1) % N] + tabla[(i + 1) % N, (j + 1) % N]))

					# Reglas del juego
					if tabla[i, j] == 0 and total == 3:
						nTabla[i, j] = 1
					elif tabla[i, j] == 1 and (total < 2 or total > 3):
						nTabla[i, j] = 0

			return nTabla

		def sumaNormal(tabla, N):
			#Fronteras normales
			nTabla = self.grid
			for i in range(0, N):
				for j in range(0, N):
					total = 0
					# **Verificacion de cada celda adyacente por su estado.
					# **En el caso que sea j==N, entonces j+1=N+1 por lo tanto da error, en ese caso se usa un try except para
					# considerar ese caso.
					# **En el caso que sea j==0, entonces j-1=0-1 por lo tanto me considera una celda que no es adyacente, en ese
					# caso devuelte una celula muerta.
					try:
						if j - 1 > -1 and int(tabla[i, (j - 1)]) == 1:
							total += 1
						else:
							total += 0
					except:
						total += 0
					try:
						if int(tabla[i, (j + 1)]) == 1: total += 1
					except:
						total += 0
					try:
						if i - 1 > -1 and int(tabla[(i - 1), j]) == 1:
							total += 1
						else:
							total += 0
					except:
						total += 0
					try:
						if int(tabla[(i + 1), j]) == 1: total += 1
					except:
						total += 0
					try:
						if i - 1 > -1 and j - 1 > -1 and int(tabla[(i - 1), (j - 1)]) == 1:
							total += 1
						else:
							total += 0
					except:
						total += 0
					try:
						if i - 1 > -1 and int(tabla[(i - 1), (j + 1)]) == 1:
							total += 1
						else:
							total += 0
					except:
						total += 0
					try:
						if j - 1 > -1 and int(tabla[(i + 1), (j - 1)]) == 1:
							total += 1
						else:
							total += 0
					except:
						total += 0
					try:
						if int(tabla[(i + 1), (j + 1)]) == 1: total += 1
					except:
						total += 0

					# Reglas del juego
					if tabla[i, j] == 0 and total == 3:
						nTabla[i, j] = 1
					elif tabla[i, j] == 1 and (total < 2 or total > 3):
						nTabla[i, j] = 0

			return nTabla

		def reglas(frame, img, tabla, N):
			#Funcion para la animacion
			if self.fronteras == 'Normal':
				nTabla = sumaNormal(tabla, N)
			if self.fronteras == 'Toro':
				nTabla = sumaToro(tabla, N)
			img.set_data(nTabla)
			tabla[:] = nTabla[:]
			return img,
		# Basicamente para colorear
		cmap = colors.ListedColormap(['blue', 'red'])  # Para seleccionar que color queremos
		bounds = [0, 1, 2]  # Para verificar que valores tienen que ser rojo y cuales azules (0=azul,1=rojo)
		norm = colors.BoundaryNorm(bounds, cmap.N)  # Para colorear el grid
		# Generacion del Grid y su animacion
		ax = self.figure.subplots()
		img = ax.imshow(self.grid, cmap=cmap, norm=norm)
		self.ani = animation.FuncAnimation(self.figure, reglas, fargs=(img, self.grid, self.dimensionMatriz),
										   frames=100,
										   interval=self.intervaloActu,
										   save_count=100,
										   repeat=True)

		#Estos eventos se activan al cumplirse la accion entre comillas
		self.figure.canvas.mpl_connect('button_press_event', self.onClick)
		self.figure.canvas.mpl_connect('draw_event', self.onStart)
		self.figure.canvas.mpl_connect('draw_event', self.iniConteo)

		return self.canvas




win = ventana()
win.connect("destroy", Gtk.main_quit)
win.show_all()

Gtk.main()
