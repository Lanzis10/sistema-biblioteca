import tkinter as tk
from tkinter import messagebox
import sqlite3
from db import conectar
from home import mostrar_home

def iniciar_sesion():
    ventana = tk.Toplevel()
    ventana.title("Login")
    ventana.geometry("400x300")

    def login():
        usuario = entry_usuario.get()
        contrasena = entry_contrasena.get()

        con = conectar()
        cur = con.cursor()
        cur.execute("SELECT * FROM usuario WHERE usuario=? AND contraseña=?", (usuario, contrasena))
        resultado = cur.fetchone()
        con.close()

        if resultado:
            id_usuario = resultado[0]
            nombre_usuario = resultado[1]
            messagebox.showinfo("Bienvenido", f"Hola {nombre_usuario}")
            ventana.destroy()
            mostrar_home(id_usuario, nombre_usuario)
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")

    tk.Label(ventana, text="Usuario").pack()
    entry_usuario = tk.Entry(ventana)
    entry_usuario.pack()

    tk.Label(ventana, text="Contraseña").pack()
    entry_contrasena = tk.Entry(ventana, show="*")
    entry_contrasena.pack()

    tk.Button(ventana, text="Iniciar sesión", command=login).pack(pady=5)

    def volver_al_menu():
        ventana.destroy()
        from main import mostrar_menu_principal
        mostrar_menu_principal()

    tk.Button(ventana, text="Volver", command=volver_al_menu).pack(pady=5)
