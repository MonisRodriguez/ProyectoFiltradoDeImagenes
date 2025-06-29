import numpy as np
import matplotlib.pyplot as plt
import cv2
from scipy.fft import fft2, ifft2, fftshift, ifftshift

def filtro_imagen_fourier():
    print("\n=== FILTRO DE IMAGEN POR FOURIER 2D ===")

    # Cargar imagen
    print("\nOpciones de imagen:")
    print("1. Usar imagen de prueba (patrón)")
    print("2. Cargar imagen desde archivo")
    
    opcion = input("Seleccione una opción (1-2): ")

    if opcion == "1":
        x = np.linspace(-5, 5, 256)
        y = np.linspace(-5, 5, 256)
        X, Y = np.meshgrid(x, y)
        img = np.sin(X*2 + Y*2) + np.cos(0.5*X) + np.sin(0.5*Y)
        img = (img - img.min()) / (img.max() - img.min()) * 255
        img = img.astype(np.uint8)
        titulo = "Imagen de prueba (patrón)"
    elif opcion == "2":
        archivo = input("Ingrese el nombre del archivo de imagen: ")
        try:
            img = cv2.imread(archivo, cv2.IMREAD_GRAYSCALE)
            if img is None:
                raise ValueError
            titulo = f"Imagen: {archivo}"
        except:
            print("Error al cargar la imagen. Usando imagen de prueba.")
            x = np.linspace(-5, 5, 256)
            y = np.linspace(-5, 5, 256)
            X, Y = np.meshgrid(x, y)
            img = np.sin(X*2 + Y*2) + np.cos(0.5*X) + np.sin(0.5*Y)
            img = (img - img.min()) / (img.max() - img.min()) * 255
            img = img.astype(np.uint8)
            titulo = "Imagen de prueba (patrón)"
    else:
        print("Opción no válida.")
        return

    # FFT
    fft_img = fftshift(fft2(img))
    magnitud = np.log(np.abs(fft_img) + 1)

    # Mostrar espectro
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    fig.suptitle(titulo)
    ax1.imshow(img, cmap='gray')
    ax1.set_title("Imagen original")
    ax1.axis('off')
    ax2.imshow(magnitud, cmap='viridis')
    ax2.set_title("Espectro de Fourier (magnitud)")
    ax2.axis('off')

    # Selección de filtro
    print("\nTipos de filtro:")
    print("1. Pasa bajas")
    print("2. Pasa altas")
    print("3. Elimina banda")
    tipo = input("Seleccione tipo de filtro (1-3): ")

    rows, cols = img.shape
    crow, ccol = rows // 2, cols // 2
    radio = min(rows, cols) // 4

    if tipo == "1":
        mascara = np.zeros((rows, cols), np.uint8)
        cv2.circle(mascara, (ccol, crow), radio, 1, -1)
        titulo_filtro = "Filtro pasa bajas"
    elif tipo == "2":
        mascara = np.ones((rows, cols), np.uint8)
        cv2.circle(mascara, (ccol, crow), radio, 0, -1)
        titulo_filtro = "Filtro pasa altas"
    elif tipo == "3":
        mascara = np.ones((rows, cols), np.uint8)
        cv2.circle(mascara, (ccol, crow), radio, 0, -1)
        cv2.circle(mascara, (ccol, crow), radio//2, 1, -1)
        titulo_filtro = "Filtro elimina banda"
    else:
        print("Opción no válida. Usando filtro pasa bajas.")
        mascara = np.zeros((rows, cols), np.uint8)
        cv2.circle(mascara, (ccol, crow), radio, 1, -1)
        titulo_filtro = "Filtro pasa bajas"

    # Aplicar filtro
    fft_filtrado = fft_img * mascara
    magnitud_filtrada = np.log(np.abs(fft_filtrado) + 1)

    # Reconstruir imagen
    img_filtrada = np.real(ifft2(ifftshift(fft_filtrado)))
    img_filtrada = (img_filtrada - img_filtrada.min()) / (img_filtrada.max() - img_filtrada.min()) * 255
    img_filtrada = img_filtrada.astype(np.uint8)

    # Mostrar resultado
    fig2, (ax3, ax4, ax5) = plt.subplots(1, 3, figsize=(15, 5))
    fig2.suptitle(titulo_filtro)
    ax3.imshow(mascara, cmap='gray')
    ax3.set_title("Máscara de filtro")
    ax3.axis('off')
    ax4.imshow(magnitud_filtrada, cmap='viridis')
    ax4.set_title("Espectro filtrado")
    ax4.axis('off')
    ax5.imshow(img_filtrada, cmap='gray')
    ax5.set_title("Imagen filtrada")
    ax5.axis('off')

    plt.show()

# Puedes probarlo llamando directamente:
# filtro_imagen_fourier()