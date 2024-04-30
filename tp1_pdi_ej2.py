import cv2
import numpy as np
import matplotlib.pyplot as plt

# definimos función genérica para mostrar imágenes
def imshow(img, new_fig=True, title=None, color_img=False, blocking=False, colorbar=True, ticks=False):
    if new_fig:
        plt.figure()
    if color_img:
        plt.imshow(img)
    else:
        plt.imshow(img, cmap='gray')
    plt.title(title)
    if not ticks:
        plt.xticks([]), plt.yticks([])
    if colorbar:
        plt.colorbar()
    if new_fig:        
        plt.show(block=blocking)

# definimos función para crear bloques de datos
def unir(image, window_size=(25,25)): 
    height, width = image.shape
    result = image.copy()
    pad_height = window_size[0] // 2
    pad_width = window_size[1] // 2

    umbral, imagen_binarizada = cv2.threshold(image, 200, 255, cv2.THRESH_BINARY) # aplicamos binarización

    # aplicamos relleno a la imagen para manejar bordes
    padded_image = cv2.copyMakeBorder(imagen_binarizada, pad_height, pad_height, pad_width, pad_width, borderType=cv2.BORDER_REPLICATE)

    for i in range(height):
        for j in range(width):
            roi = padded_image[i:i+window_size[0], j:j+window_size[1]] # definimos la región de interés (ROI) según el tamaño del kernel
            if np.any(roi == 0): # verificamos si algún vecino es 0
                result[i, j] = 0 # establecemos el píxel en la posición central de la ROI como 0

    return result

# definimos función para contar caracteres y palabras en una imagen
def find_blocks(image):  
    _, imagen_binarizada = cv2.threshold(image,10, 255, cv2.THRESH_BINARY_INV)  # aplicamos binarización
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(imagen_binarizada, 8, cv2.CV_32S) # aplicamos función connectedComponentsWithStats
    return num_labels, labels, stats, centroids

# definimos función para corrección
def respuestas(image): 
    imagen_unida=unir(image,(24,24))
    _, _, stats, _ = find_blocks(imagen_unida)  
    block_ans=[]

    # iteramos sobre las sublistas en stats
    for sublista in stats:
        area = sublista[4]
        if 120000 <= area <= 130000: # comprobamos si el área está dentro del rango deseado (120.000 - 130.000)
            block_ans.append((sublista[0], sublista[1])) # guardamos el primer y segundo valor de la sublista en la lista de resultados
            x,y = block_ans[0]
            x=x+11  #se corrige la posición inicial considerando el tamaño del kernel
            y=y+11  #se corrige la posición inicial considerando el tamaño del kernel

    lista_respuestas = []  # inicializamos lista de listas
    for i in range(25):    # iteramos sobre los índices i y j
        fila = []
        for j in range(5):
            r=y+31*i+i//12  #se añade i//12 para ajustar a un aumento de separación a partir de fila 12
            c=x+29*j
            recorte = image[r:r+21,c:c+21]
            # calculamos el promedio de los valores de grises en la imagen recortada
            promedio_gris = cv2.mean(recorte)[0]
            # agregamos 1 si el promedio es menor a 155, 0 en caso contrario
            if promedio_gris < 155:
                fila.append(1)
            else:
                fila.append(0)
        lista_respuestas.append(fila)
    return lista_respuestas

def check_ans_1(image):
    lista_respuestas=respuestas(image)
    lista_correctas = [
        [1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0],
        [0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 1, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [0, 0, 0, 1, 0],
        [1, 0, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0]
    ]

    for idx, (correcta, respuesta) in enumerate(zip(lista_correctas, lista_respuestas), start=1):
        if correcta == respuesta:
            print(f"Respuesta {idx}: OK")
        else:
            print(f"Respuesta {idx}: MAL")

def valida_header(imagen):
    # coordenadas de las subimágenes correspondientes a cada campo
    coordenadas = {
        'nombre': (98, 109, 278, 129),  # x1, y1, x2, y2
        'id': (330, 109, 429, 128),
        'code': (490, 109, 567, 129),
        'date': (651, 109, 763, 129)
    }

    th_area = 2 # umbral para filtrar componentes conectadas pequeñas

    # procesamos cada campo
    for campo, (x1, y1, x2, y2) in coordenadas.items():
        subimagen = imagen[y1:y2, x1:x2] # recortamos la subimagen correspondiente al campo
        _, subimagen_binaria = cv2.threshold(subimagen, 160, 255, cv2.THRESH_BINARY_INV) # binarizamos la subimagen utilizando un umbral
        _, _, stats_car, _ = cv2.connectedComponentsWithStats(subimagen_binaria, 8, cv2.CV_32S) # detectamos componentes conectadas en la subimagen binaria

        # detectamos componentes conectadas en la subimagen binaria transformada
        subimagen_binaria_pal=unir(subimagen,(3,3))
        _, _, stats_pal, _ = find_blocks(subimagen_binaria_pal)  

        # filtramos componentes conectadas pequeñas
        ix_area = stats_car[:, -1] > th_area
        stats_filtradas_car = stats_car[ix_area]

        # excluímos el fondo (primer componente)
        num_caracteres = len(stats_filtradas_car) - 1
        num_palabras = len(stats_pal) - 1

        # validamos el número de caracteres según el campo
        if campo == 'nombre':
            estado = "OK" if num_caracteres <= 25 and num_palabras >= 2 else "MAL"
        elif campo == 'id':
            estado = "OK" if num_caracteres == 8 and num_palabras == 1 else "MAL"
        elif campo == 'code':
            estado = "OK" if num_caracteres == 1 and num_palabras == 1 else "MAL"
        elif campo == 'date':
            estado = "OK" if num_caracteres == 8 and num_palabras == 1 else "MAL"
        print(f"{campo.capitalize()}: {estado}") # mostramos el estado del campo y el número de caracteres 

def corrector(image):
    imagen = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
    valida_header(imagen)
    check_ans_1(imagen)

def check_ans_2(image):
    lista_respuestas = respuestas(image)
    lista_correctas = [
        [1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0],
        [0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 1, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [0, 0, 0, 1, 0],
        [1, 0, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0]
    ]

    num_correctas = 0  # contador número de respuestas correctas

    for correcta, respuesta in zip(lista_correctas, lista_respuestas):
        if correcta == respuesta:
            num_correctas += 1

    return num_correctas

def procesar_examenes(file_list):
    resultados_examenes = {}  # diccionario contenedor de los resultados de los exámenes

    for file in file_list:
        imagen = cv2.imread(file, cv2.IMREAD_GRAYSCALE)  # cargamos la imagen
        num_correctas = check_ans_2(imagen)  # check_ans recibe la imagen
        nombre_alumno = file.split('.')[0]  # obtenemos nombre del alumno
        resultados_examenes[nombre_alumno] = num_correctas

    return resultados_examenes

# definimos para extraer los recortes de los nombres
def extract_names(file_list):
    cropped_names = []

    for file in file_list:
        image = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
        cropped_name = image[109:129, 98:278]  # recortamos la región del nombre
        cropped_names.append(cropped_name)

    return cropped_names

# definimos función para imprimir los recortes de los nombres y la condición de aprobado/desaprobado
def print_cropped_names_with_condition(cropped_names, resultados_examenes):
    # creamos imagen vacía
    height = len(cropped_names) * 20  # altura de la imagen basada en el número de nombres
    width = max([name.shape[1] for name in cropped_names]) + 200  # ancho de la imagen basado en el nombre más ancho y espacio para la condición
    output_image = np.zeros((height, width), dtype=np.uint8)

    # concatenamos los nombres recortados verticalmente en la nueva imagen
    y_offset = 0
    for name, (alumno, num_correctas) in zip(cropped_names, resultados_examenes.items()):
        h, w = name.shape[:2]
        output_image[y_offset:y_offset + h, :w] = name
        
        condicion = "Aprobado" if num_correctas >= 20 else "Desaprobado" # agregamos la condición 
        cv2.putText(output_image, condicion, (w + 10, y_offset + h//2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255, 1)
        y_offset += h

    # mostramos la imagen resultante
    plt.figure(figsize=(10, 8))
    plt.imshow(output_image, cmap='gray')
    plt.axis('off')
    plt.show()

def procesar_y_mostrar_resultados(file_list):
    resultados_examenes = procesar_examenes(file_list)
    cropped_names = extract_names(file_list)
    print_cropped_names_with_condition(cropped_names, resultados_examenes)


##########################################################################################################################################

#Apartado C
#corrector('multiple_choice_1.png')
#corrector('multiple_choice_2.png')
#corrector('multiple_choice_3.png')
#corrector('multiple_choice_4.png')
#corrector('multiple_choice_5.png')

##########################################################################################################################################

#Apartado D 
#file_list = ['multiple_choice_1.png', 'multiple_choice_2.png', 'multiple_choice_3.png', 'multiple_choice_4.png', 'multiple_choice_5.png']
#procesar_y_mostrar_resultados(file_list)

