import tkinter as tk
from tkinter import messagebox
import sqlite3
from db import conectar

def registrar_usuario():
    ventana = tk.Toplevel()
    ventana.title("Registro")
    ventana.geometry("400x300")

    def registrar():
        usuario = entry_usuario.get()
        contrasena = entry_contrasena.get()

        if usuario and contrasena:
            con = conectar()
            cur = con.cursor()
            try:
                cur.execute("INSERT INTO usuario (usuario, contraseña) VALUES (?, ?)", (usuario, contrasena))
                con.commit()
                messagebox.showinfo("Éxito", "Usuario registrado correctamente")
                ventana.destroy()
                from main import mostrar_menu_principal
                mostrar_menu_principal()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "El nombre de usuario ya existe")
            finally:
                con.close()
        else:
            messagebox.showwarning("Campos vacíos", "Debes completar todos los campos")

    tk.Label(ventana, text="Usuario").pack()
    entry_usuario = tk.Entry(ventana)
    entry_usuario.pack()

    tk.Label(ventana, text="Contraseña").pack()
    entry_contrasena = tk.Entry(ventana, show="*")
    entry_contrasena.pack()

    tk.Button(ventana, text="Registrar", command=registrar).pack(pady=5)

    # Botón "Volver"
    def volver_al_menu():
        ventana.destroy()
        from main import mostrar_menu_principal
        mostrar_menu_principal()

    tk.Button(ventana, text="Volver", command=volver_al_menu).pack(pady=5)

