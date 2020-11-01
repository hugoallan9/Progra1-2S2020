El programa tiene 2 bugs importantes
1) Por defecto tiene cargado que genere una cuadricula 10x10 y por lo tanto al cargarle una matriz de dimension superior o inferios genera
error, esto podia arreglarlo haciendo que al pulsar el boton de random o cargar estado me abriera una ventana donde estuviera
exclusivamente la figura de matplotlib pero opte por no hacerlo ya que no me gustaba como quedaba, un ejemplo de esto es iniciar el codigo
y cargando el archivo 'Prueba (otra copia).pm2', sin embargo esto se arregla cambiando el valor del atributo 'dimensionMatriz' al valor de
la dimension de la matriz que queremos cargar (cosa que obviamente no deberia de ser asi)
**Para el random simplemente se genera la cuadricula random, y la dimension de esa cuadricula esta dada por el atributo 'dimensionMatriz'
2) Al cargar archivos se solapan uno con otro, por ejemplo, si carga el archivo 'Prueba.pm2' y luego 'Prueba (copia).pm2' se puede ver claramente como se solapa

Por el resto del programa creo que esta bien hecho, lo unico que puede dar problemas puede ser el apartado guardar por como entendi que tenia que funcionar esa parte
