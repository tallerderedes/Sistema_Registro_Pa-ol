import tkinter as tk

# Crear una ventana
ventana = tk.Tk()
ventana.title("Mi primera interfaz")

# Agregar un label
etiqueta = tk.Label(ventana, text="¡Hola, mundo!")
etiqueta.pack()

# Iniciar el bucle principal
ventana.mainloop()