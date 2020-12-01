#!/usr/bin/env python
#!/usr/bin/python
import sys
from PIL import Image, ImageDraw, ImageFont
import math as m
import os
import shutil
import tweepy

import  gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import webbrowser

class PrincipalConNoteBook(Gtk.Window):
    def __init__(self):
        super(PrincipalConNoteBook, self).__init__(title="Arte ASCII")
        self.set_default_size(1900,950)
        self.set_resizable(False)

    #hacemos un notebook que no muestre las tabs para poder cambiar
    #de esta manera podremos tener espacio para ingresar credenciales o
    #el menu de modificaciones de usuario para el arte ascii

        notebook = Gtk.Notebook()
        notebook.set_show_tabs(False)
        self.add(notebook)
    #definimos las pags del notebook

    #P0 princial, inicio
        main = ArteAscii(notebook)
        notebook.append_page(main)
    #P1 pagina de Twitter
        ingreso_credenciales = VentanaTwitter(notebook)
        notebook.append_page(ingreso_credenciales)
    #P2 no hay archivo cargado
        no_hay_archivo_cargado = NoHayArchivoCargado(notebook)
        notebook.append_page(no_hay_archivo_cargado)
    #P3 archivo guardado en directorio
        archivo_guardad_en_cwd = DialogoGuardado(notebook)
        notebook.append_page(archivo_guardad_en_cwd)
    #P4 salir de cuenta mensaje
        salir_de_cuenta_mensaje = SalirCuentaMensaje(notebook)
        notebook.append_page(salir_de_cuenta_mensaje)
    #P5 tweet realizado mensaje
        tweet_realizado_mensaje = TweetRealizado(notebook)
        notebook.append_page(tweet_realizado_mensaje)
    #P6 credenciales no validas
        credenciales_no_validas = CredencialesNoValidas(notebook)
        notebook.append_page(credenciales_no_validas)
    #P7 n ha ingresado caracteres ascii
        no_hay_caracterse_ascii = NoHaIngresadoCaracteres(notebook)
        notebook.append_page(no_hay_caracterse_ascii)

class ArteAscii(Gtk.Box):
    # colocar como variable de clase para tener acceso a el en los metodos
    grid = Gtk.Grid()
    vbox = Gtk.VBox()
    img = Gtk.Image()
    im_ascii = Gtk.Image()
    text_buffer = Gtk.TextBuffer()
    display_para_buffer = Gtk.TextView(buffer=text_buffer)
    label_normal = Gtk.Label('IMAGEN NORMAL')
    label_arte_ascii = Gtk.Label('IMAGEN EN ARTE ASCII')
    contador_guardadas = 0  # para llevar una numeracion al guardar
    size = 600, 600
    label_espaciador = Gtk.Label('          ')  # para tener espacio entre la imagen y arte ascii
    label_espaciador_final = Gtk.Label('           ')

    entrada_caracteres = Gtk.Entry()
    espaciamiento_menu_config = Gtk.Label('\n'
                                          '\n'
                                          '\n')
    invertir = False
    # cuestiones que sirven en otras clases
    consumer_key_entrada = Gtk.Entry()
    consumer_secret_entry = Gtk.Entry()
    acces_token_entrada = Gtk.Entry()
    acces_token_secret_entrada = Gtk.Entry()

    def __init__(self, parent):
        super().__init__()
        self.__parent = parent
            # contenedores

        self.add(self.vbox)
        self.grid.set_column_spacing(1)
        self.grid.set_row_spacing(1)
        self.vbox.pack_start(self.grid, True, True, 0)

            # desarrollo del menu con opciones pedidas para el proyecto

        menu_bar = Gtk.MenuBar()

            # elementos del menu
        imagen = Gtk.MenuItem('Imagen')
        opciones_twitter = Gtk.MenuItem('Opciones de Twitter')
        ayuda = Gtk.MenuItem('Ayuda')

            # subelementos de los elementos del menu

            # submenu de imagen
        imagen_menu = Gtk.Menu()
        cargar_imagen_menu = Gtk.MenuItem('Cargar Imagen')
        imagen_menu.append(cargar_imagen_menu)
        guardar_arte = Gtk.MenuItem('Guardar Arte ASCII')
        imagen_menu.append(guardar_arte)
        imagen.set_submenu(imagen_menu)

            # acciones de las opciones del submenu de imagen
        cargar_imagen_menu.connect('activate', self.cargar_imagen_accion)
        guardar_arte.connect('activate', self.guardar_arte_accion)

            # submenu de opciones de twitter
        opciones_twitter_menu = Gtk.Menu()
        ingresar_credenciales = Gtk.MenuItem('Ingresar credenciales')
        opciones_twitter_menu.append(ingresar_credenciales)
        logout = Gtk.MenuItem('Salir de la cuenta')
        opciones_twitter_menu.append(logout)
        opciones_twitter.set_submenu(opciones_twitter_menu)

            # acciones de las opciones del submenu de twitter
        ingresar_credenciales.connect('activate', self.connect_accion)
        logout.connect('activate', self.logout_accion)

            # submenu de ayuda
        ayuda_menu = Gtk.Menu()
        acerca_de = Gtk.MenuItem('Acerca de')
        ayuda_menu.append(acerca_de)
        codigo_fuente = Gtk.MenuItem('Código fuente')
        ayuda_menu.append(codigo_fuente)
        ayuda.set_submenu(ayuda_menu)

            # acciones de las opciones del submenu de ayuda
        acerca_de.connect('activate', self.acerca_de_accion)
        codigo_fuente.connect('activate', self.codigo_fuente_accion)

            # agregar las ramas que se derivan del menu principal a este ultimo
        menu_bar.append(imagen)
        menu_bar.append(opciones_twitter)
        menu_bar.append(ayuda)
        self.grid.attach(menu_bar, 1, 0, 5, 1)

            # boton de guardar arte ascii que se muestra en la interfaz
            # este boton debera activarse solo cuando ya este cargada una imagen
        tool_bar = Gtk.Toolbar()  # recordar que estos botones tienen que tener accion cuando haya una imagen cargada
        tool_bar.set_style(2)
        guardar_tool_bar = Gtk.ToolButton(Gtk.STOCK_SAVE)
        separador_tool_bar = Gtk.SeparatorToolItem()
        subir_tool_bar = Gtk.ToolButton(Gtk.STOCK_ADD)
        tool_bar.insert(guardar_tool_bar, 0)
        tool_bar.insert(separador_tool_bar, 1)
        tool_bar.insert(subir_tool_bar, 2)
        tool_bar.set_halign(Gtk.Align.CENTER)
        self.vbox.pack_start(tool_bar, False, False, 20)

            # acciones para los botones del tool bar
        guardar_tool_bar.connect('clicked', self.guardar_arte_accion)
        subir_tool_bar.connect('clicked', self.connect_accion)

            # textbuffer, este dejara un mensaje cuando se haya cargado una imagen
            # tambien servira para pasarle la informacion al boton de guardado para que se habilite o no
        self.display_para_buffer.set_size_request(30, 30)
        self.grid.attach(self.display_para_buffer, 150,0, 1, 1)
            # label de imagen normal y con arte ascii
        self.grid.attach(self.label_normal, 10, 1, 1, 1)
        self.grid.attach(self.label_arte_ascii, 200, 1, 1, 1)

            # parte para cargar la imagen
        self.grid.attach_next_to(self.img, self.label_normal, Gtk.PositionType.BOTTOM, 1, 1)
        self.grid.attach_next_to(self.label_espaciador, self.img, Gtk.PositionType.RIGHT, 5, 1)
        self.grid.attach_next_to(self.im_ascii, self.label_arte_ascii, Gtk.PositionType.BOTTOM, 1, 1)
        self.grid.attach_next_to(self.label_espaciador_final, self.im_ascii, Gtk.PositionType.RIGHT, 5, 1)

#aca va la parte del menu de configuracion que va a estar en la ventana
        label_config = Gtk.Label('Ingrese sus caractéres ASCII:')
        label_invertir = Gtk.Label('¿Invertir imagen?')
        radio_boton_si = Gtk.RadioButton.new_with_label_from_widget(None, 'Sí')
        radio_boton_si.connect('toggled', self.si_invertir)
        radio_boton_no = Gtk.RadioButton.new_from_widget(radio_boton_si)
        radio_boton_no.set_label('No')
        radio_boton_no.connect('toggled', self.no_invertir)
    # algunos formatos para alinear los radio botones
        radio_boton_si.set_halign(Gtk.PositionType.BOTTOM)
        radio_boton_no.set_halign(Gtk.PositionType.BOTTOM)
        radio_boton_si.set_valign(Gtk.PositionType.RIGHT)
        radio_boton_no.set_valign(Gtk.PositionType.RIGHT)
        self.entrada_caracteres.set_halign(Gtk.Align.CENTER)
        self.entrada_caracteres.set_valign(Gtk.Align.CENTER)
#ponerlos en la ventana
        self.grid.attach(self.espaciamiento_menu_config, 2, 1, 1, 1)
        self.grid.attach_next_to(label_config, self.espaciamiento_menu_config, Gtk.PositionType.BOTTOM, 1,1)
        self.grid.attach_next_to(self.entrada_caracteres, label_config, Gtk.PositionType.BOTTOM, 1, 1)
        self.grid.attach_next_to(label_invertir, self.entrada_caracteres, Gtk.PositionType.BOTTOM, 1, 1)
        self.grid.attach_next_to(radio_boton_si, label_invertir, Gtk.PositionType.BOTTOM, 1, 1)
        self.grid.attach_next_to(radio_boton_no, radio_boton_si, Gtk.PositionType.BOTTOM, 1, 1)


    #configuracion metodo
    def si_invertir(self, widget):
        self.invertir = True
    def no_invertir(self, widget):
        self.invertir = False

    def config_imagen(self, widget):
        self.__parent.set_current_page(1)

    #metodos que se usan en el menu
    def cargar_imagen_accion(self, widget):
        #se abrira un file chooser dialog para elegir el archivo que tiene la imgen
        #a partir de esta carga tambien se obtiene el nombre del archivo para cargar en el buffer y habilidar el guardado
        global letras
        file_chooser_cargar_imagen = Gtk.FileChooserDialog('Seleccione una imagen', None, Gtk.FileChooserAction.OPEN,
                                       ('Cancelar', Gtk.ResponseType.CANCEL, 'Seleccionar', Gtk.ResponseType.OK))
        #agregar el filtro para que solo permita elegir imagenes
        file_chooser_cargar_imagen.set_default_response(Gtk.ResponseType.OK)
        filtro_file_chooser = Gtk.FileFilter()
        filtro_file_chooser.set_name('Imágenes')
        filtro_file_chooser.add_mime_type('Image/png')
        filtro_file_chooser.add_mime_type('Image/jpeg')
        filtro_file_chooser.add_mime_type('Image/jpg')
        filtro_file_chooser.add_pattern('*.png')
        filtro_file_chooser.add_pattern('*.jpeg')
        filtro_file_chooser.add_pattern('*.jpg')
        file_chooser_cargar_imagen.add_filter(filtro_file_chooser)

        respuesta = file_chooser_cargar_imagen.run()
        if respuesta == Gtk.ResponseType.OK:

            cadena_nombre_archivo = file_chooser_cargar_imagen.get_filename() #para obtener la ruta al archivo
            indice_diagonal = cadena_nombre_archivo[::-1].find('\\') #encontramos la ultima \ leyendo la cadena al reves
            indice_extension = cadena_nombre_archivo[::-1].find('.')
            texto_para_buffer = cadena_nombre_archivo[(len(cadena_nombre_archivo)-indice_diagonal):
                                                      (len(cadena_nombre_archivo)-indice_extension)-1]
            self.text_buffer.set_text('   {} ha sido cargado.'.format(texto_para_buffer))
    #ademas de decir en el buffer que hemos cargado la imagen, debemos cargar la imagen del lado izquierdo del window
    #al lado derecho aparecera la imagen en arte ascii, pero antes, debera mostrarse un dialogo para opciones de imagen
            ascii_pil = Image.open(cadena_nombre_archivo, 'r')
            ascii_pil.thumbnail(self.size)
            ascii_pil.save('NormalParaMostrar.png')
            self.img.set_from_file(os.path.abspath('NormalParaMostrar.png'))  # para ajustar el tamano

    #cargar el arte ascii a la par con las configuraciones que estan hasta el momento
            if os.path.exists(os.path.abspath('ImEnAscii.png')):
                os.remove('ImEnAscii.png')      #para no cargar otro archivo
                os.remove('AsciiParaMostrar.png')
            if self.invertir == False:
                letras = self.entrada_caracteres.get_text()
            elif self.invertir == True:
                letras = str(self.entrada_caracteres.get_text)[::-1]    #para invertir la imagen

            if len(letras) == 0:
                self.__parent.set_current_page(7)

            if len(letras) > 0:
                self.final_ascii(cadena_nombre_archivo, letras)     #pasar a ascii
                ascii_pil = Image.open(os.path.abspath('ImEnAscii.png'), 'r')
                ascii_pil.thumbnail(self.size)
                ascii_pil.save('AsciiParaMostrar.png')
                self.im_ascii.set_from_file(os.path.abspath('AsciiParaMostrar.png'))     #para ajustar el tamano

            self.show_all()

        elif respuesta == Gtk.ResponseType.CANCEL:
            pass

        file_chooser_cargar_imagen.destroy()

    def guardar_arte_accion(self, widget):
        #verifica si existe una ruta a un archivo ImEnAscii y guarda este que justamente es el que esta cargado
        if os.path.exists('ImEnAscii.png'):
            self.contador_guardadas += 1
            #cambiarle el nombre al archivo para guardarlo
            ruta_nombre_cambiado = str(os.path.abspath('ImEnAscii.png').strip('ImEnAscii.png')) + 'ArteAscii ' + str(self.contador_guardadas) + '.txt'
            os.rename(os.path.abspath('ImEnAscii.png'), ruta_nombre_cambiado)

        #damos un mensaje por un Gtk Dialog que indique que la imagen ha sido guardada
            self.__parent.set_current_page(3)
        else:
            self.__parent.set_current_page(2)

    def connect_accion(self, widget):
        self.__parent.set_current_page(1)

    def logout_accion(self, widget):
        self.__parent.set_current_page(4)
    def tuitear_accion(self, widget):
        self.__parent.set_current_page(2)

    def acerca_de_accion(self, widget):
        #aca saldra el dialogo con la informacion pedida
        vbox = Gtk.VBox()
        acerca_de_dialogo = Gtk.AboutDialog()
        acerca_de_dialogo.set_program_name('Arte ASCII')
        acerca_de_dialogo.set_version('Proyecto final PM1')
        acerca_de_dialogo.set_authors('MCM')
        acerca_de_dialogo.set_copyright('Desarrollo de interfaz gráfica en Gtk 3.0')
        acerca_de_dialogo.set_comments('Uso de Gtk 3.0, Tweepy y librerías estándar de Python 3.')        #agregar lo que me falta depues de hacer el proyecto
        acerca_de_dialogo.set_website('https://github.com/MariajoseChinchilla/Proyecto_final/blob/master/ProyectoFinalTerminado.py')
        vbox.pack_start(acerca_de_dialogo, False, False, 0)
        self.add(vbox)
        acerca_de_dialogo.run()
        acerca_de_dialogo.destroy()

    def codigo_fuente_accion(self, widget):
        webbrowser.open_new_tab('https://github.com/MariajoseChinchilla/Proyecto_final/blob/master/ProyectoFinalTerminado.py')

#ACA EMPIEZA TODA LA PARTE DE PASAR UNA IMAGEN A ARTE ASCII
    #varias metodos para eso definidos aca
    def dimensiones(self, imagen):
        (W, H) = imagen.size
        ratio = H / float(W)
        nueva_altura = int(ratio * 100)
        newImage = imagen.resize((100, nueva_altura))
        return newImage, nueva_altura

    def escala_grises(self, imagen):
        # convertir a escalas grises
        return imagen.convert('L')

    def pix_en_ascii(self, imagen, caracteres):
        rango = m.ceil(255 / len(caracteres))
        # elegir el mejor caracter para representar el pixel
        # el brillo esta entre 0 y 250, entonces se distribuye esto en la cantidad
        # total de caracteres
        # escoje en la lista de caracteres dependiendo del grupo de pixeles
        img = list(imagen.getdata())
        pixels_ascii = [caracteres[m.floor(pixel / rango)] for pixel in
                        img]

        return ''.join(pixels_ascii)

    def pasar_a_ascii(self, imagen, caracteres, na = 100):
        # pasar los caraceres elegidos a imagen
        imagen, alt = self.dimensiones(imagen)
        imagen = self.escala_grises(imagen)

        caracteres = self.pix_en_ascii(imagen, caracteres)

        # Crea la imagen y el archivo .txt con el asciiArt
        fnt = ImageFont.load_default()
        outputImage = Image.new('RGB', (10*na, 12 * alt), color=(0, 0, 0))
        drawImage = ImageDraw.Draw(outputImage)

        for i in range(alt):
            for j in range(na):
                drawImage.text((10 * j, 12 * i), caracteres[j + i * na], font=fnt, fill=(255, 255, 255))
        outputImage.save('ImEnAscii.png')
        l = len(caracteres)

        imageAscii = [caracteres[i: i + 100] for i in
                      range(0, l, na)]

        return "\n".join(imageAscii)

    def final_ascii(self, ruta, caracteres):
        image = Image.open(ruta)
        self.pasar_a_ascii(image, caracteres)


class DialogoGuardado(Gtk.VBox):
    def __init__(self, parent):
        super().__init__()
        self.__parent = parent
        label_espacio = Gtk.Label('\n'
                                  '\n'
                                  '\n'
                                  '\n'
                                  '\n'
                                  '\n'
                                  '\n'
                                  '\n'
                                  '\n')
        label = Gtk.Label('Su .txt fue guardado en el current working directory.')
        ok_boton = Gtk.Button('REGRESAR')
        ok_boton.connect("clicked", self.ok_accion)
        ok_boton.set_valign(Gtk.Align.CENTER)
        ok_boton.set_halign(Gtk.Align.CENTER)
        label.set_halign(Gtk.Align.CENTER)
        label.set_valign(Gtk.Align.CENTER)
        label_espacio.set_valign(Gtk.Align.CENTER)
        label_espacio.set_halign(Gtk.Align.CENTER)
        self.pack_start(label_espacio, False, False, 0)
        self.pack_start(label, False, False, 0)
        self.pack_start(ok_boton, False, False, 10)

    def ok_accion(self, widget):
        self.__parent.set_current_page(0)        #para regresar a la pagina principal

#esta es la clase para cuando no hay ningun archivo cargado
class NoHayArchivoCargado(Gtk.VBox):
    def __init__(self, parent):
        super().__init__()
        self.__parent = parent
        ok_boton = Gtk.Button("REGRESE Y CARGUE UNA IMAGEN.")
        ok_boton.connect("clicked", self.ok_accion)
        ok_boton.set_valign(Gtk.Align.CENTER)
        ok_boton.set_halign(Gtk.Align.CENTER)
        self.pack_start(ok_boton, True, True, 0)

    def ok_accion(self, widget):
        self.__parent.set_current_page(0)  # para regresar a la pagina principal

class VentanaTwitter(Gtk.VBox):
    def __init__(self, parent):
        super().__init__(spacing = 10)
        self.__parent = parent
        label_consumer_key = Gtk.Label('Consumer Key')
        label_consumer_key_secret = Gtk.Label('Consumer Secret')
        acces_token_label = Gtk.Label('Access Token')
        access_token_secret_label = Gtk.Label('Access Token Secret')
        label_titulo = Gtk.Label('INGRESE SUS CREDENCIALES DE TWITTER')
        boton_guardar_cambios = Gtk.Button('Guardar cambios y tweetear')
        boton_regresar = Gtk.Button('Regresar')
        label_espaciamiento = Gtk.Label('\n'
                                        '\n'
                                        '\n')

    #conectar los botones
        boton_guardar_cambios.connect('clicked', self.guardar_cambios_accion)
        boton_regresar.connect('clicked', self.regresar)

    #posicionar
        label_consumer_key.set_halign(Gtk.Align.CENTER)
        label_consumer_key.set_valign(Gtk.Align.CENTER)
        label_consumer_key_secret.set_halign(Gtk.Align.CENTER)
        label_consumer_key_secret.set_valign(Gtk.Align.CENTER)
        acces_token_label.set_halign(Gtk.Align.CENTER)
        acces_token_label.set_valign(Gtk.Align.CENTER)
        access_token_secret_label.set_halign(Gtk.Align.CENTER)
        access_token_secret_label.set_valign(Gtk.Align.CENTER)
        ArteAscii.consumer_key_entrada.set_halign(Gtk.Align.CENTER)
        ArteAscii.consumer_key_entrada.set_valign(Gtk.Align.CENTER)
        ArteAscii.consumer_secret_entry.set_halign(Gtk.Align.CENTER)
        ArteAscii.consumer_secret_entry.set_valign(Gtk.Align.CENTER)
        ArteAscii.acces_token_entrada.set_halign(Gtk.Align.CENTER)
        ArteAscii.acces_token_entrada.set_valign(Gtk.Align.CENTER)
        ArteAscii.acces_token_secret_entrada.set_halign(Gtk.Align.CENTER)
        ArteAscii.acces_token_secret_entrada.set_valign(Gtk.Align.CENTER)
        label_titulo.set_halign(Gtk.Align.CENTER)
        label_titulo.set_valign(Gtk.Align.CENTER)
        boton_guardar_cambios.set_halign(Gtk.Align.CENTER)
        boton_guardar_cambios.set_valign(Gtk.Align.CENTER)
        boton_regresar.set_halign(Gtk.Align.CENTER)
        boton_regresar.set_valign(Gtk.Align.CENTER)
        label_espaciamiento.set_halign(Gtk.Align.CENTER)
        label_espaciamiento.set_valign(Gtk.Align.CENTER)

    #agregar al box
        self.pack_start(label_espaciamiento, False, False, 0)
        self.pack_start(label_titulo, False, False, 50)
        self.pack_start(label_consumer_key, False, False, 10)
        self.pack_start(ArteAscii.consumer_key_entrada, False, False, 0)
        self.pack_start(label_consumer_key_secret, False, False, 10)
        self.pack_start(ArteAscii.consumer_secret_entry, False, False, 0)
        self.pack_start(acces_token_label, False, False, 10)
        self.pack_start(ArteAscii.acces_token_entrada, False, False, 0)
        self.pack_start(access_token_secret_label, False, False, 10)
        self.pack_start(ArteAscii.acces_token_secret_entrada, False, False, 0)
        self.pack_start(boton_guardar_cambios, False, False, 50)
        self.pack_start(boton_regresar, False, False, 35)

    #metodos para recuperar datos
    def guardar_cambios_accion(self, widget):
        consumer_key = ArteAscii.consumer_key_entrada.get_text()
        consumer_key_secret = ArteAscii.consumer_secret_entry.get_text()
        access_token = ArteAscii.acces_token_entrada.get_text()
        access_token_secret = ArteAscii.acces_token_secret_entrada.get_text()
        lista = [consumer_key, consumer_key_secret,  access_token, access_token_secret]

        auth = tweepy.OAuthHandler(consumer_key, consumer_key_secret)
        auth.set_access_token(access_token, access_token_secret)

        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        mensaje = '#ASCIIArtPM1.'
        if os.path.exists(os.path.abspath('ImEnAscii.png')):
            media = os.path.abspath('AsciiParaMostrar.png')
            try:
                api.update_with_media(media, mensaje)
                self.__parent.set_current_page(5)
            except:
                self.__parent.set_current_page(6)
        else:
            self.__parent.set_current_page(2)


    def regresar(self, widget):
        self.__parent.set_current_page(0)

class SalirCuentaMensaje(Gtk.VBox):
    def __init__(self, parent):
        super().__init__(spacing = 10)
        self.__parent = parent
        label_espaciamiento = Gtk.Label('\n'
                                        '\n'
                                        '\n'
                                        '\n'
                                        '\n'
                                        '\n'
                                        '\n'
                                        '\n'
                                        '\n'
                                        '\n'
                                        '\n'
                                        '\n'
                                        '\n')

        label_mensaje = Gtk.Label('¡Listo! Ninguna cuenta de Twitter está abierta.')
        salir_boton = Gtk.Button('REGRESAR')
        salir_boton.connect("clicked", self.ok_accion)
        salir_boton.set_valign(Gtk.Align.CENTER)
        salir_boton.set_halign(Gtk.Align.CENTER)
        label_mensaje.set_halign(Gtk.Align.CENTER)
        label_mensaje.set_valign(Gtk.Align.CENTER)
        label_espaciamiento.set_halign(Gtk.Align.CENTER)
        label_espaciamiento.set_valign(Gtk.Align.CENTER)

        self.pack_start(label_espaciamiento, False, False, 0)
        self.pack_start(label_mensaje, False, False, 0)
        self.pack_start(salir_boton, False, False, 0)

    def ok_accion(self, widget):
        self.__parent.set_current_page(0)  # para regresar a la pagina principal

class TweetRealizado(Gtk.VBox):
    def __init__(self, parent):
        super().__init__()
        self.__parent = parent
        label_espacio = Gtk.Label('\n'
                                  '\n'
                                  '\n'
                                  '\n')
        label_espacio.set_halign(Gtk.Align.CENTER)
        label_espacio.set_valign(Gtk.Align.CENTER)
        label_realizado = Gtk.Label('Su Tweet ha sido realizado.')
        label_realizado.set_halign(Gtk.Align.CENTER)
        label_realizado.set_valign(Gtk.Align.CENTER)
        boton_tweet_realizado = Gtk.Button('REGRESAR')
        boton_tweet_realizado.set_halign(Gtk.Align.CENTER)
        boton_tweet_realizado.set_valign(Gtk.Align.CENTER)
        boton_tweet_realizado.connect('clicked', self.tweet_realizado)
    #agregar el label y el boton
        self.pack_start(label_espacio, False, False, 0)
        self.pack_start(label_realizado, False ,False, 0)
        self.pack_start(boton_tweet_realizado, False, False, 15)

    def tweet_realizado(self, widget):
        self.__parent.set_current_page(0)

class CredencialesNoValidas(Gtk.VBox):
    def __init__(self, parent):
        super().__init__()
        self.__parent = parent
        label_no_valido = Gtk.Label('Credenciales no válidas.')
        boton_regresar = Gtk.Button('REGRESAR')
        label_espacio = Gtk.Label('\n'
                                  '\n'
                                  '\n'
                                  '\n')

        label_no_valido.set_halign(Gtk.Align.CENTER)
        label_no_valido.set_valign(Gtk.Align.CENTER)
        boton_regresar.set_halign(Gtk.Align.CENTER)
        boton_regresar.set_valign(Gtk.Align.CENTER)
        label_espacio.set_halign(Gtk.Align.CENTER)
        label_espacio.set_valign(Gtk.Align.CENTER)

        boton_regresar.connect('clicked', self.regresar)

        self.pack_start(label_espacio, False, False, 0)
        self.pack_start(label_no_valido, False, False, 15)
        self.pack_start(boton_regresar, False, False, 5)

    def regresar(self, widget):
        self.__parent.set_current_page(2)

class NoHaIngresadoCaracteres(Gtk.VBox):
    def __init__(self, parent):
        super().__init__()
        self.__parent = parent

        espacio = Gtk.Label('\n'
                            '\n'
                            '\n'
                            '\n'
                            '\n')

        label = Gtk.Label('             No ha ingresado carácteres para su ASCII. \n'
                          '\n'
                          'Regrese, ingrese sus caractéres y cargue la imagen nuevamente.')
        boton_regresar = Gtk.Button('REGRESAR')
        boton_regresar.connect('clicked', self.regresar)

        label.set_halign(Gtk.Align.CENTER)
        label.set_valign(Gtk.Align.CENTER)
        boton_regresar.set_halign(Gtk.Align.CENTER)
        boton_regresar.set_valign(Gtk.Align.CENTER)
        espacio.set_halign(Gtk.Align.CENTER)
        espacio.set_valign(Gtk.Align.CENTER)

        self.pack_start(espacio, False, False, 0)
        self.pack_start(label, False, False, 0)
        self.pack_start(boton_regresar, False, False, 15)
    def regresar(self, widget):
        self.__parent.set_current_page(0)

win = PrincipalConNoteBook()
win.connect('destroy', Gtk.main_quit)
win.show_all()
Gtk.main()