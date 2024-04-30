import cv2
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

# definimos función para ecualización local del histograma
def ecual_local_hist(image, kernel): 
    height, width = image.shape
    result = image.copy()
    pad_height = kernel[0] // 2
    pad_width = kernel[1] // 2

    # aplicamos relleno a la imagen para manejar los bordes
    padded_image = cv2.copyMakeBorder(image, pad_height, pad_height, pad_width, pad_width, borderType=cv2.BORDER_REPLICATE)

    for i in range(height):
        for j in range(width):
            roi = padded_image[i:i+kernel[0], j:j+kernel[1]] # definimos la región de interés (ROI) según el tamaño del kernel
            roi_equalized = cv2.equalizeHist(roi) # aplicamos la ecualización del histograma en la ROI
            result[i, j] = roi_equalized[pad_height, pad_width] # asignamos el resultado de la eq a la posición correspondiente en la imagen de salida
            # i y j son las coordenadas de fila y columna en la imagen de salida
            # roi_equalized[pad_height, pad_width] es el valor del pixel en el centro de la ROI ecualizada

    return result


#######################################################################################################################################################

#f1 = cv2.imread('Imagen_con_detalles_escondidos.tif', cv2.IMREAD_GRAYSCALE) # leemos la imagen original
#kernel = (20, 20) # definimos tamaño kernel 
#result_image = ecual_local_hist(f1, kernel) # aplicamos ecualización local del histograma y guardamos imagen mejorada

# mostramos la imagen original y la imagen resultante
#plt.figure()
#ax1 = plt.subplot(121)
#imshow(f1, new_fig=False, title="Imagen Original")
#plt.subplot(122, sharex=ax1, sharey=ax1)
#imshow(result_image, new_fig=False, title="Imagen resultante")
#plt.show()
