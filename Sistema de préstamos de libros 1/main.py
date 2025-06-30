from db import crear_tablas
import tkinter as tk

# Colores de la interfaz
tema_fondo = "#ffffff"  # blanco
tema_rojo = "#c0392b"  # rojo fuerte
tema_texto = "#c0392b"  # rojo para textos

def estilo_boton(boton):
    boton.configure(bg=tema_rojo, fg="white", activebackground="#e74c3c", activeforeground="white", borderwidth=0, font=("Arial", 12, "bold"))
    boton.bind("<Enter>", lambda e: boton.config(bg="#e74c3c"))
    boton.bind("<Leave>", lambda e: boton.config(bg=tema_rojo))

def mostrar_menu_principal():
    ventana = tk.Toplevel()
    ventana.title("Inicio")
    ventana.geometry("800x400")
    ventana.configure(bg=tema_fondo)

    from register import registrar_usuario
    from login import iniciar_sesion

    tk.Label(ventana, text="Bienvenido al sistema de biblioteca", font=("Arial", 16, "bold"), fg=tema_texto, bg=tema_fondo).pack(pady=20)
    btn_registrar = tk.Button(ventana, text="Registrarse", width=20, command=lambda: [ventana.destroy(), registrar_usuario()])
    estilo_boton(btn_registrar)
    btn_registrar.pack(pady=10)
    btn_login = tk.Button(ventana, text="Iniciar Sesión", width=20, command=lambda: [ventana.destroy(), iniciar_sesion()])
    estilo_boton(btn_login)
    btn_login.pack(pady=10)


    ventana.mainloop()

if __name__ == "__main__":
    crear_tablas()
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal real
    mostrar_menu_principal()
    root.mainloop()


#esta es una prueba de github para ver si se actualiza esto aaa.
