import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf
import time
import random
import math
import tweepy

from PIL import Image,ImageFont,ImageDraw, ImageOps, ImageChops


import os
import webbrowser


UI_INFO = """
<ui>
  <menubar name='menuBar'>
    <menu action='archivo'>
      <menuitem action='cargarImagen' />
      <menuitem action='guardarASCII' />
      <separator />
      <menuitem action='FileQuit' />
    </menu>
    <menu action='Twitter'>
      <menuitem action='SignIn' />
      <menuitem action='LogOut' />
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
		Gtk.Window.__init__(self, title='ASCII art')

		self.carga = 'No' #Para controlar cuando hay una imagen en ASCII art
		self.sesion = 'No' #Para controlar cuando hay credenciales validas
		self.state = False #Para controlar el invertir la imgen
		self.img = Gtk.Image()
		self.imgRes = Gtk.Image()
		self.imgPIL = Image.Image
		self.imgPILASCII = Image.Image
		st = '"$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,^.' #Escala de grises inicial
		self.charsList = list(st)
		self.chars = self.charsList

		#Credenciales de twiiter
		self.APIkey = ''
		self.APIkeyS = ''
		self.AccessToken = ''
		self.AccessTokenS = ''

		#Widget de la ventana
		btnConvertir = Gtk.Button(label='Convertir')
		btnConvertir.connect('clicked', self.convertir)
		btnInvertir = Gtk.ToggleButton(label='Invertir')
		btnInvertir.connect('toggled', self.invertir,'1')
		self.btnGuardar = Gtk.Button(label='Guardar')
		self.btnGuardar.connect('clicked', self.guardar)
		self.btnGuardar.set_sensitive(False)#Para desabilidar el boton guardar en el inicio del programa
		self.btnSubir = Gtk.Button(label='Subir')
		self.btnSubir.connect('clicked', self.subir)
		self.btnSubir.set_sensitive(False)#Para desabilidar el boton guardar en el inicio del programa
		btnGrises = Gtk.Button(label='Grises')
		btnGrises.connect('clicked', self.grises)

		btnPrueba = Gtk.Button(label='Prueba') #Boton de para probar cosas (No esta en la ventana)
		btnPrueba.connect('clicked', self.prueba)

		#Tamaño de la ventana
		self.set_default_size(700,00)
		#Para el barmenu
		self.action = Gtk.ActionGroup(name='action')
		self.menuArchivo(self.action)
		self.menuConfig(self.action)
		self.menuAyuda(self.action)
		self.uimanager = self.create_ui_manager()
		self.uimanager.insert_action_group(self.action)
		menubar = self.uimanager.get_widget('/menuBar')
		#Para desabilidar el boton guardar en el inicio del programa
		l = self.action.list_actions()
		for i in l:
			if i.get_name() == 'guardarASCII':
				i.set_sensitive(False)

		self.buffer = Gtk.TextBuffer()
		display = Gtk.TextView(buffer=self.buffer)
		display.set_justification(Gtk.Justification.LEFT)
		display.set_size_request(350, 550)

		#Grid donde estara toda la interfaz
		container = Gtk.Grid()
		container.set_row_spacing(5)
		container.set_column_spacing(5)
		container.attach(menubar, 0, 0, 150, 1)
		container.attach(self.img, 0, 1, 73, 95)
		container.attach(self.imgRes, 77, 1, 73, 95)
		container.attach(btnConvertir, 74, 25, 3, 1)
		container.attach(btnInvertir, 74, 26, 3, 1)
		container.attach(self.btnGuardar, 74, 27, 3, 1)
		container.attach(self.btnSubir, 74, 28, 3, 1)
		container.attach(btnGrises, 74, 29, 3, 1)
		#container.attach(btnPrueba, 74, 30, 3, 1)
		self.add(container)

		self.set_default_size(-1,500)
		self.set_resizable(False)

		self.verificarSesion()


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


	def resize(self,img, new_width=100):
		'''
		Toma como parametro el nuevo ancho deseado y redimensiona la imagen dada a
		las nuevas dimensiones
		'''
		im = img
		w,h = im.size
		new_height = math.ceil(new_width * h / w)
		return im.resize((new_width, new_height))

	def imGris(self,img):
		'''
		Convierte la imagen a escala de grises (creo que al final no use esta cosa)
		'''
		return  img.convert('L')

	def ASCII(self, img,chars):
		'''
		Una vez convertida la imagen convertida a escala de grises recorre todo pixel en la imagen
		y da el caracter correspondiente a dicha tonalidad de gris del pixel
		'''
		rango = math.ceil(255/len(chars))
		im = list(img.getdata())
		pixels_ascii=[]
		for pixel in im:
			temp = math.floor(pixel / rango)
			pixels_ascii.append(chars[temp])
		return ''.join(pixels_ascii)


	def convertir(self,widget):
		'''
		Agarra la imagen dada, convierte la imagen a escala de grises luego nos da todos los pixeles
		en ASCII en un string y luego convierte ese string a imagen, luego de que ya tenemos la imagen
		ASCII la ponemos en el canvas correspondiente
		'''
		w1,h1=self.imgPIL.size
		img = self.resize(self.imgPIL.convert('L'),new_width=w1)
		img = self.imGris(img)

		if self.state == True:
		#Ya que la tonalidad de gris se decide por los caracteres dados para poder invertir 
		#su escala de grises basta con invertir la cadena de caracteres dados
			self.chars = self.charsList[::-1]
		else:
			self.chars = self.charsList


		w,h = img.size
		caract = self.ASCII(img,self.chars)
		font = ImageFont.load_default()
		outImage = Image.new('RGB',(10*w,12*h),color=(255,255,255))
		drawImage = ImageDraw.Draw(outImage)

		for i in range(h):
			for j in range(w):
				drawImage.text((10*j,12*i),caract[j+i*w],font=font, fill=(0, 0, 0))

		nombregenerico = 'hola.jpg'
		outImage.save(nombregenerico)

		ruta=os.getcwd()
		ruta+='/'+nombregenerico

		pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
			filename=ruta,
			width=350,
			height=550,
			preserve_aspect_ratio=True)
		self.imgRes.set_from_pixbuf(pixbuf)
		self.imgPILASCII = Image.open(ruta)
		os.remove(ruta)

		#Esto activa los bonotes de guardado
		l = self.action.list_actions()
		for i in l:
			if i.get_name() == 'guardarASCII':
				i.set_sensitive(True)
		self.btnGuardar.set_sensitive(True)
		self.carga='Si'
		#Verifica si hay credenciales validas de Twitter y de ser asi habilita el boton de subida a twitter
		if self.sesion == 'Si':
			self.btnSubir.set_sensitive(True)
		if self.sesion == 'No':
			self.btnSubir.set_sensitive(False)

	def invertir(self,widget,name):
		#Controla el toggle button
		#Presionado significa que se tiene que invertir la imagen
		#Sin presionar es que la imagen tiene que estar normal
		if widget.get_active():
			self.state = True
		else:
			self.state = False

	def verificarSesion(self):
		#Verifica si hay credenciales guardadas de Twitter 
		#Osea, si anteriormente se ingresaron credenciales validas de twitter y no se cerro sesion entonces
		#Se mantienen guardadas y esto verifica las que se guardaron y se guardan las credenciales como atributos
		#para su uso posterior
		ruta = os.getcwd()
		ruta+='/InicioSesion.txt'
		if os.path.isfile(ruta):
			file = open('InicioSesion.txt', 'r')
			ver = file.readline()[:-1]
			self.sesion = ver
			lista = []
			if ver == 'Si':
				for i in range(4):
					lista.append(file.readline()[:-1])

				self.APIkey = lista[0]
				self.APIkeyS = lista[1]
				self.AccessToken = lista[2]
				self.AccessTokenS = lista[3]
			elif ver == 'No':
				self.btnSubir.set_sensitive(False)

		else:
			wr = open('InicioSesion.txt', 'w')
			wr.write('No')
			wr.close()
			file = open('InicioSesion.txt', 'r')
			ver = file.readline()[:-1]
			self.sesion = ver
			lista = []
			if ver == 'Si':
				for i in range(4):
					lista.append(file.readline()[:-1])

				self.APIkey = lista[0]
				self.APIkeyS = lista[1]
				self.AccessToken = lista[2]
				self.AccessTokenS = lista[3]
			elif ver == 'No':
				self.btnSubir.set_sensitive(False)



	def guardar(self,widget):
		'''
		Hace lo mismo que convertir pero me da el texto plano, con la diferencia que esto no lo muestra
		tan detallado, si no que lo hace con una anchura de 100 para que pueda ser facilmente visible en un *.txt
		:param widget:
		:return:
		'''
		img = self.resize(self.imgPIL.convert('L'))
		img = self.imGris(img)

		if self.state == True:
			self.chars = self.charsList[::-1]
		else:
			self.chars = self.charsList

		w, h = img.size
		caract = self.ASCII(img, self.chars)

		l = len(caract)

		imageAscii = [caract[i: i + w] for i in
					  range(0, l, w)]


		cadenaASCII = ''
		for i in range(len(imageAscii)):
			cadenaASCII += imageAscii[i] + '\n'

		fo = open('result.txt', 'w')
		fo.write(cadenaASCII)
		fo.close()

	def subir(self,widget):
		#Usa las credenciales guardadas en los atributos para poder subir la imagen a 
		#Twiiter junto con el hashtag #ASCIIArtPM1
		auth = tweepy.OAuthHandler(self.APIkey,self.APIkeyS)
		auth.set_access_token(self.AccessToken,self.AccessTokenS)
		api = tweepy.API(auth)
		#Redimensiona la imagen a 1000 de anchura para que no tenga tanto peso la imagen y pueda subirse la imagen
		temp = self.resize(self.imgPILASCII, new_width=1000) 
		temp.save('temp.png')
		ruta = os.getcwd()
		ruta+='/temp.png'
		header = '#ASCIIArtPM1'
		api.update_with_media(ruta,header)
		print('ASCIIArt subido correctamente')
		os.remove(ruta)

		dialog = Gtk.MessageDialog(
			transient_for=self,
			flags=0,
			message_type=Gtk.MessageType.INFO,
			buttons=Gtk.ButtonsType.OK,
			text="Correcto!",
		)
		dialog.format_secondary_text(
			"ASCIIArt subido correctamente"
		)
		dialog.run()
		dialog.destroy()

	def prueba(self,widget):
		pass

	def grises(self,widget):
		#Abre una ventana para poder modificar la escalaa de grises
		def clicked(button):
			self.charsList = list(textBox.get_text())
			self.chars = self.charsList
			b.close()
			return self.chars
		b = Gtk.Window()
		textBox = Gtk.Entry()
		btnOk = Gtk.Button(label='Ok')
		btnOk.connect('clicked', clicked)
		label = Gtk.Label(label="Ingrese la escala de grises deseada")
		container = Gtk.Grid()
		container.set_row_spacing(5)
		container.set_column_spacing(5)
		container.attach(label, 0, 0, 1, 1)
		container.attach(textBox, 0, 1, 1, 1)
		container.attach(btnOk, 1, 0, 2, 2)
		b.add(container)
		b.set_default_size(-1, -1)
		b.set_resizable(False)
		b.show_all()

	def signIn(self,widget):
		#Abre una ventana en la cual podemos ingresar credenciales para poder subir cosas
		#y verificar si son correctas, en caso de ser correctas las guarda como atributos
		#ademas de guardarlo en un *.txt para poder ser incializadas la proxima vez que se abre el programa
		#Si no son correctas cierra la ventana y no guarda nada
		def ok(button):
			self.APIkey = textBoxAPI.get_text()
			self.APIkeyS = textBoxAPIS.get_text()
			self.AccessToken = textBoxAccess.get_text()
			self.AccessTokenS = textBoxAccessS.get_text()

			auth = tweepy.OAuthHandler(self.APIkey, self.APIkeyS)
			auth.set_access_token(self.AccessToken, self.AccessTokenS)
			api = tweepy.API(auth)
			try:
				api.verify_credentials()
				self.sesion = 'Si'
				wr = open('InicioSesion.txt', 'w')
				wr.write('Si\n')
				wr.write(textBoxAPI.get_text() + '\n')
				wr.write(textBoxAPIS.get_text() + '\n')
				wr.write(textBoxAccess.get_text() + '\n')
				wr.write(textBoxAccessS.get_text() + '\n')

				if self.carga == 'Si' and self.sesion == 'Si':
					self.btnSubir.set_sensitive(True)

				dialog = Gtk.MessageDialog(
					transient_for=self,
					flags=0,
					message_type=Gtk.MessageType.INFO,
					buttons=Gtk.ButtonsType.OK,
					text="Correcto!",
				)
				dialog.format_secondary_text(
					"Credenciales correctas"
				)
				dialog.run()
				dialog.destroy()

			except:
				dialog = Gtk.MessageDialog(
					transient_for=self,
					flags=0,
					message_type=Gtk.MessageType.INFO,
					buttons=Gtk.ButtonsType.OK,
					text="Error!",
				)
				dialog.format_secondary_text(
					"Credenciales invalidas\nVuelva a intentar"
				)
				dialog.run()
				dialog.destroy()

		def cancelar(widget):
			signIn.close()

		signIn = Gtk.Window()
		labelAPI = Gtk.Label(label='API key: ')
		labelAPIS = Gtk.Label(label='API key secret: ')
		labelAccess = Gtk.Label(label='Access token: ')
		labelAccessS = Gtk.Label(label='Access token secret: ')
		textBoxAPI = Gtk.Entry()
		textBoxAPIS = Gtk.Entry()
		textBoxAccess = Gtk.Entry()
		textBoxAccessS = Gtk.Entry()
		btnOk = Gtk.Button(label='Ok')
		btnOk.connect('clicked', ok)
		btnCancel = Gtk.Button(label='Cancelar')
		btnCancel.connect('clicked', cancelar)

		container = Gtk.Grid()
		container.set_row_spacing(5)
		container.set_column_spacing(5)
		container.attach(labelAPI, 0, 0, 1, 1)
		container.attach(labelAPIS, 0, 1, 1, 1)
		container.attach(labelAccess, 0, 2, 1, 1)
		container.attach(labelAccessS, 0, 3, 1, 1)
		container.attach(textBoxAPI, 4, 0, 1, 1)
		container.attach(textBoxAPIS, 4, 1, 1, 1)
		container.attach(textBoxAccess, 4, 2, 1, 1)
		container.attach(textBoxAccessS, 4, 3, 1, 1)
		container.attach(btnCancel, 0, 4, 2, 2)
		container.attach(btnOk, 3, 4, 2, 2)
		signIn.add(container)
		signIn.set_default_size(-1, -1)
		signIn.set_resizable(False)
		signIn.show_all()

	def logOut(self,widget):
		#Limpia los atributos de las credenciales y borra las credenciales guardadas en el *.txt
		#Y abre la ventana para ingresar nuevas credenciales
		self.APIkey = ''
		self.APIkeyS = ''
		self.AccessToken = ''
		self.AccessTokenS = ''
		wr = open('InicioSesion.txt', 'w')
		wr.write('No\n')

		self.sesion = 'No'
		self.btnSubir.set_sensitive(False)

		dialog = Gtk.MessageDialog(
			transient_for=self,
			flags=0,
			message_type=Gtk.MessageType.INFO,
			buttons=Gtk.ButtonsType.OK,
			text="Exito!",
		)
		dialog.format_secondary_text(
			"Sesion Cerrada con exito."
		)
		dialog.run()
		dialog.destroy()
		self.signIn(widget)

	def menuArchivo(self, action_group):
		'''
		Pestaña 'Archivo'
		:param action_group:
		:return:
		'''
		action_group.add_actions(
			[
				("archivo", None, "Archivo"),
				("cargarImagen", None, 'Cargar', '<control>N', None, self.cargaImagen),
				("guardarASCII", None, 'Guardar ASCII', "<control>G", None, self.guardar),
			]
		)

		action_filequit = Gtk.Action(name="FileQuit", stock_id=Gtk.STOCK_QUIT)
		action_filequit.connect("activate", self.cerrarVentana)
		action_group.add_action(action_filequit)

	def menuConfig(self, action_group):
		'''
		Pestaña 'Twitter'
		:param action_group:
		:return:
		'''
		action_group.add_actions(
			[
				("Twitter", None, "Twitter"),
				("SignIn", None, 'SignIn', None, None, self.signIn),
				("LogOut", None, 'Cerrar Sesion', None, None, self.logOut),
			]
		)

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




	def cargaImagen(self, widget):
		'''
		Selecciona un archivo para convertir a ASCII art y lo pone en el canvas correspondiente,
		ademas cada vez que se carga una imagen inhabilida los botones subir y guardar
		:param widget:
		:return:
		'''
		dialog = Gtk.FileChooserDialog(
			title='Seleccione una imagen', parent=self, action=Gtk.FileChooserAction.OPEN,
		)
		dialog.add_buttons(
			Gtk.STOCK_CANCEL,
			Gtk.ResponseType.CANCEL,
			Gtk.STOCK_OPEN,
			Gtk.ResponseType.OK
		)
		response = dialog.run()
		if response == Gtk.ResponseType.OK:
			self.ruta = dialog.get_filename()
			self.imgPIL = Image.open(self.ruta)
			pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
				filename=self.ruta,
				width=350,
				height=550,
				preserve_aspect_ratio=True)
			self.img.set_from_pixbuf(pixbuf)
		elif response == Gtk.ResponseType.CANCEL:
			pass

		l = self.action.list_actions()
		for i in l:
			if i.get_name() == 'guardarASCII':
				i.set_sensitive(False)
		self.btnGuardar.set_sensitive(False)
		self.btnSubir.set_sensitive(False)
		self.imgRes.clear()
		dialog.destroy()



	def cerrarVentana(self, widget):
		#Cierra ventana
		Gtk.main_quit()

	def acercaDe(self, widget):
		#Abre una ventana
		acercaDe = Gtk.AboutDialog()
		acercaDe.set_program_name('ASCIIArt')
		acercaDe.set_authors(['Jsfgefge/AngelMarroquin'])
		acercaDe.set_comments('Herramientas usadas:\n'
			'-Python v3.8.5\n'
			'-Gtk v3.0\n'
			'-Tweepy v3.9.0\n')
		acercaDe.set_title('Acerca De')
		acercaDe.run()
		acercaDe.destroy()

	def codigoVida(self, widget):
		webbrowser.open_new_tab("https://github.com/Jsfgefge/ProgramacionMatematica1/blob/master/ProyectoFinal/Main.py")









win = ventana()
win.connect("destroy", Gtk.main_quit)
win.show_all()

Gtk.main()
