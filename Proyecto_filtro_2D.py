import numpy as np
import matplotlib.pyplot as plt
import cv2
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
from scipy.fft import fft2, ifft2, fftshift, ifftshift

# Estructura global para almacenar la imagen cargada y su espectro
imagen_actual = {'img': None, 'color': None, 'titulo': "", 'fft_img': None, 'magnitud': None}

# Convertir imagen NumPy a formato Tkinter
def convertir_para_tk(img_np):
    img_np = (img_np - img_np.min()) / (img_np.max() - img_np.min()) * 255
    img_np = img_np.astype(np.uint8)
    img_pil = Image.fromarray(img_np)
    return ImageTk.PhotoImage(img_pil.resize((256, 256)))

# Cargar imagen desde archivo
def cargar_archivo():
    archivo = filedialog.askopenfilename(title="Selecciona una imagen", filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.bmp")])
    if archivo:
        img_color = cv2.imread(archivo, cv2.IMREAD_COLOR)
        if img_color is not None:
            img_gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)
            preparar_imagen(img_gray, f"Imagen: {archivo}", img_color)
        else:
            messagebox.showerror("Error", "No se pudo cargar la imagen.")

# Generar imagen patrón
def usar_patron():
    x = np.linspace(-5, 5, 256)
    y = np.linspace(-5, 5, 256)
    X, Y = np.meshgrid(x, y)
    img = np.sin(X * 2 + Y * 2) + np.cos(0.5 * X) + np.sin(0.5 * Y)
    img = (img - img.min()) / (img.max() - img.min()) * 255
    img_uint8 = img.astype(np.uint8)
    img_color = cv2.merge([img_uint8, img_uint8, img_uint8])
    preparar_imagen(img_uint8, "Imagen de prueba (patrón)", img_color)

# Procesar imagen y calcular su FFT
def preparar_imagen(img_gris, titulo, img_color):
    imagen_actual['img'] = img_gris
    imagen_actual['color'] = cv2.cvtColor(img_color, cv2.COLOR_BGR2RGB)
    imagen_actual['titulo'] = titulo
    imagen_actual['fft_img'] = fftshift(fft2(img_gris))
    imagen_actual['magnitud'] = np.log(np.abs(imagen_actual['fft_img']) + 1)

# Aplicar filtro y mostrar resultado
def aplicar_filtro(tipo):
    img = imagen_actual['img']
    fft_img = imagen_actual['fft_img']
    magnitud = imagen_actual['magnitud']
    
    if img is None or fft_img is None:
        messagebox.showerror("Error", "Primero debes cargar o generar una imagen.")
        return

    try:
        divisor = int(entry_amplitud.get())
        if divisor <= 0 or divisor > 300:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Ingresa un número entero entre 1 y 300 como divisor de radio.")
        return

    rows, cols = img.shape
    crow, ccol = rows // 2, cols // 2
    radio = max(1, min(rows, cols) // divisor)

    # Crear máscara
    if tipo == "bajo":
        mascara = np.zeros((rows, cols), np.uint8)
        cv2.circle(mascara, (ccol, crow), radio, 1, -1)
        titulo_filtro = "Filtro pasa bajas"
    elif tipo == "alto":
        mascara = np.ones((rows, cols), np.uint8)
        cv2.circle(mascara, (ccol, crow), radio, 0, -1)
        titulo_filtro = "Filtro pasa altas"
    elif tipo == "banda":
        mascara = np.ones((rows, cols), np.uint8)
        cv2.circle(mascara, (ccol, crow), radio, 0, -1)
        cv2.circle(mascara, (ccol, crow), radio // 2, 1, -1)
        titulo_filtro = "Filtro elimina banda"
    else:
        return

    # Filtrado y reconstrucción
    fft_filtrado = fft_img * mascara
    magnitud_filtrada = np.log(np.abs(fft_filtrado) + 1)
    img_filtrada = np.real(ifft2(ifftshift(fft_filtrado)))
    img_filtrada = (img_filtrada - img_filtrada.min()) / (img_filtrada.max() - img_filtrada.min()) * 255
    img_filtrada = img_filtrada.astype(np.uint8)

    # Mostrar resultados en dos filas
    fig = plt.figure(figsize=(15, 8))
    fig.suptitle(f"{imagen_actual['titulo']} - {titulo_filtro}", fontsize=14)

    # Fila 1: Imagen original y magnitud
    ax1 = plt.subplot(2, 3, 1)
    ax1.imshow(imagen_actual['color'])
    ax1.set_title("Imagen original")
    ax1.axis('off')

    ax2 = plt.subplot(2, 3, 2)
    ax2.imshow(magnitud)
    ax2.set_title("Espectro original")
    ax2.axis('off')

    # Fila 2: Filtros
    ax3 = plt.subplot(2, 3, 4)
    ax3.imshow(mascara, cmap='gray')
    ax3.set_title("Máscara de filtro")
    ax3.axis('off')

    ax4 = plt.subplot(2, 3, 5)
    ax4.imshow(magnitud_filtrada)
    ax4.set_title("Espectro filtrado")
    ax4.axis('off')

    ax5 = plt.subplot(2, 3, 6)
    ax5.imshow(img_filtrada, cmap='gray')
    ax5.set_title("Imagen filtrada")
    ax5.axis('off')

    plt.tight_layout()
    plt.show()

# ====================
# VENTANA PRINCIPAL
# ====================
ventana = tk.Tk()
ventana.title("Filtro de Imagen por Fourier 2D")
ventana.geometry("350x380")

# Título
tk.Label(ventana, text="Filtro de Imagen por Fourier 2D", font=("Segoe UI", 12)).pack(pady=10)

# Sección de carga de imagen
frame_carga = tk.LabelFrame(ventana, text="Carga de Imagen", padx=10, pady=5)
frame_carga.pack(fill="x", padx=15, pady=5)

tk.Button(frame_carga, text="Usar imagen de prueba", command=usar_patron).pack(fill="x", pady=2)
tk.Button(frame_carga, text="Cargar imagen desde archivo", command=cargar_archivo).pack(fill="x", pady=2)

# Sección de filtros
frame_filtros = tk.LabelFrame(ventana, text="Configuración de Filtro", padx=10, pady=5)
frame_filtros.pack(fill="x", padx=15, pady=10)

tk.Label(frame_filtros, text="Divisor de radio (1-300)", font=("Segoe UI", 10)).pack()
entry_amplitud = tk.Entry(frame_filtros, justify="center")
entry_amplitud.insert(0, "16")
entry_amplitud.pack(pady=5)

tk.Button(frame_filtros, text="Filtro pasa bajas", width=25, command=lambda: aplicar_filtro("bajo")).pack(pady=3)
tk.Button(frame_filtros, text="Filtro pasa altas", width=25, command=lambda: aplicar_filtro("alto")).pack(pady=3)
tk.Button(frame_filtros, text="Filtro elimina banda", width=25, command=lambda: aplicar_filtro("banda")).pack(pady=3)

# Botón salir
tk.Button(ventana, text="Salir", command=ventana.destroy).pack(pady=5)
ventana.mainloop()
