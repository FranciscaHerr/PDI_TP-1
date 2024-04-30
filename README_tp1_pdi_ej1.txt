Ecualización Local del Histograma

Este programa sirve para aplicar ecualización local del histograma a imágenes en escala de grises utilizando la biblioteca OpenCV en Python. 
Además, para mostrar las imágenes de entrada y salida, hace uso de la biblioteca Matplotlib.


Descripción

La ecualización local del histograma es una técnica que realza el contraste y la definición de los detalles en imágenes al ajustar la distribución de las intensidades de los píxeles en áreas específicas de la imagen.


Funcionalidades

Función para ecualización local del histograma: 
La función ecual_local_hist toma una imagen en escala de grises y un tamaño de kernel como entrada, y devuelve la imagen ecualizada localmente.

Función para mostrar imágenes: 
La función imshow permite mostrar imágenes de forma interactiva, con opciones para configurar aspectos como la escala de grises, el título, la barra de colores y los ejes.


Uso

Instalación de dependencias: Instala las bibliotecas OpenCV y Matplotlib en tu entorno de Python.
Ejecución del programa: Ejecuta el archivo tp1_pdi_ej1.py. La imagen original y la imagen ecualizada resultante se mostrarán en una ventana emergente.


Ejemplo de Uso

import cv2
import matplotlib.pyplot as plt

f1 = cv2.imread('Imagen_con_detalles_escondidos.tif', cv2.IMREAD_GRAYSCALE) # leemos la imagen original
kernel = (20, 20) # definimos tamaño kernel 
result_image = ecual_local_hist(f1, kernel) # aplicamos ecualización local del histograma y guardamos imagen mejorada

# mostramos la imagen original y la imagen resultante
plt.figure()
ax1 = plt.subplot(121)
imshow(f1, new_fig=False, title="Imagen Original")
plt.subplot(122, sharex=ax1, sharey=ax1)
imshow(result_image, new_fig=False, title="Imagen resultante")
plt.show()



