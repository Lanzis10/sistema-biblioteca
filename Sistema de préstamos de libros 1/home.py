import tkinter as tk
from libros import gestionar_libros
from prestamos import ver_prestamos
from devoluciones import registrar_devolucion


tema_fondo = "#ffffff"  
tema_rojo = "#c0392b"  
tema_texto = "#c0392b"  

def mostrar_home(id_usuario, nombre_usuario):
    ventana = tk.Tk()
    ventana.title("Sistema de Biblioteca")
    ventana.geometry("600x400")

    tk.Label(ventana, text=f"Bienvenido {nombre_usuario}", font=("Arial", 20)).pack(pady=10)

    tk.Button(ventana, text="Gestionar Libros", width=20, border=7, command=lambda: gestionar_libros(ventana, id_usuario, nombre_usuario)).pack(pady=10)
    tk.Button(ventana, text="Gestionar Préstamos", width=20, border=7, command=lambda: ver_prestamos(ventana, id_usuario, nombre_usuario)).pack(pady=10)
    tk.Button(ventana, text="Registrar Devolución", width=20, border=7, command=lambda: registrar_devolucion(ventana, id_usuario, nombre_usuario)).pack(pady=10)

    ventana.mainloop()

