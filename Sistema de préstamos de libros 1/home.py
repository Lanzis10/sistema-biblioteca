import tkinter as tk
from libros import gestionar_libros
from prestamos import ver_prestamos
from devoluciones import registrar_devolucion


tema_fondo = "#ffffff"  
tema_rojo = "#c0392b"  
tema_texto = "#c0392b"  

def estilo_boton(boton):
    boton.configure(bg=tema_rojo, fg="white", activebackground="#e74c3c", activeforeground="white", borderwidth=0, font=("Arial", 12, "bold"))
    boton.bind("<Enter>", lambda e: boton.config(bg="#e74c3c"))
    boton.bind("<Leave>", lambda e: boton.config(bg=tema_rojo))

def mostrar_home(id_usuario, nombre_usuario):
    ventana = tk.Tk()
    ventana.title("Sistema de Biblioteca")
    ventana.geometry("600x400")
    ventana.configure(bg=tema_fondo)

    tk.Label(ventana, text=f"Bienvenido {nombre_usuario}", font=("Arial", 20, "bold"), fg=tema_texto, bg=tema_fondo).pack(pady=10)

    btn_libros = tk.Button(ventana, text="Gestionar Libros", width=20, command=lambda: gestionar_libros(ventana, id_usuario, nombre_usuario))
    estilo_boton(btn_libros)
    btn_libros.pack(pady=10)
    btn_prestamos = tk.Button(ventana, text="Gestionar Préstamos", width=20, command=lambda: ver_prestamos(ventana, id_usuario, nombre_usuario))
    estilo_boton(btn_prestamos)
    btn_prestamos.pack(pady=10)
    btn_devolucion = tk.Button(ventana, text="Registrar Devolución", width=20, command=lambda: registrar_devolucion(ventana, id_usuario, nombre_usuario))
    estilo_boton(btn_devolucion)
    btn_devolucion.pack(pady=10)

    ventana.mainloop()

