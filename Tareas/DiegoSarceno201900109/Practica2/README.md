# Practica 2
## Juego de la vida
### Diego Sarceño
#### 201900109

El juego de la vida es un juego de 0 jugadores en el cual un conjunto de
células vivas o muertas interactuan mediante dos reglas.
	- Una célula muerta con, exactamente, 3 células vecinas vivas, nace.
	- Una célula viva con 2 ó 3 células vecinas vivas, sigue viva; sino, muere por soledad o sobrepoplación.

La animación fue hecha con el módulo matplotlib, y se tomaron en cuenta dos tipos de fronteras, la normal y la toroidal. 
La interfaz gráfica en la que se generaron el menú y los botones fue hecha con Gtk, del módulo Gi para Python.
