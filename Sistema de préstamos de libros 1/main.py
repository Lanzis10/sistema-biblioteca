from db import crear_tablas
import tkinter as tk

def mostrar_menu_principal():
    ventana = tk.Toplevel()
    ventana.title("Inicio")
    ventana.geometry("800x400")

    from register import registrar_usuario
    from login import iniciar_sesion

    tk.Label(ventana, text="Bienvenido al sistema de biblioteca", font=("Arial", 16)).pack(pady=20)
    tk.Button(ventana, text="Registrarse", width=20, command=lambda: [ventana.destroy(), registrar_usuario()]).pack(pady=10)
    tk.Button(ventana, text="Iniciar Sesión", width=20, command=lambda: [ventana.destroy(), iniciar_sesion()]).pack(pady=10)


    ventana.mainloop()

if __name__ == "__main__":
    crear_tablas()
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal real
    mostrar_menu_principal()
    root.mainloop()


#esta es una prueba de github para ver si se actualiza eso.
#lmao
