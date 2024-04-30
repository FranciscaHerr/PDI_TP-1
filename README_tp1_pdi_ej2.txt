Corrección de Exámenes multiple choice

Este programa proporciona un conjunto de funciones para procesar imágenes de exámenes multiple choice. 
Utiliza las bibliotecas OpenCV, Numpy y Matplotlib para llevar a cabo diversas tareas de procesamiento de imágenes. 
Además de mostrar por pantalla cuáles de las respuestas son correctas y cuáles incorrectas, valida la información del encabezado, que contiene los datos personales del alumno (nombre, identificación, código y fecha). 
El programa también evalúa si los alumnos aprueban o no el examen, según el número de respuestas correctas de cada persona. Se establece que un examen es aprobado si el estudiante tiene veinte respuestas correctas o más.


Funcionalidades

Función para corregir exámenes multiple choice:
La función corrector toma como entrada una imagen de un examen multiple choice y verifica las respuestas marcadas por el alumno. 
Utiliza una serie de criterios para determinar si las respuestas son correctas o incorrectas y las imprime en la consola.

Función para procesar y mostrar resultados de exámenes:
La función procesar_y_mostrar_resultados procesa una lista de imágenes de exámenes multiple choice y muestra los nombres de los alumnos junto con su estado de aprobación o desaprobación, basado en el número de respuestas correctas. 


Uso

Instalación de dependencias: Instala las bibliotecas OpenCV, Numpy y Matplotlib en tu entorno de Python.
Ejecución del programa: Ejecuta el archivo tp1_pdi_ej2.py. 


Ejemplo de Uso

import cv2
import numpy as np
import matplotlib.pyplot as plt

# Correcciones individuales

corrector('multiple_choice_1.png')
corrector('multiple_choice_2.png')
corrector('multiple_choice_3.png')
corrector('multiple_choice_4.png')
corrector('multiple_choice_5.png')

# Procesamiento de resultados de la clase

file_list = ['multiple_choice_1.png', 'multiple_choice_2.png', 'multiple_choice_3.png', 'multiple_choice_4.png', 'multiple_choice_5.png']
procesar_y_mostrar_resultados(file_list)






