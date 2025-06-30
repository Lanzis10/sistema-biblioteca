import tkinter as tk
from tkinter import messagebox
import sqlite3
from db import conectar
from home import mostrar_home


tema_fondo = "#ffffff" 
tema_rojo = "#c0392b"  
tema_texto = "#c0392b"  

def estilo_boton(boton):
    boton.configure(bg=tema_rojo, fg="white", activebackground="#e74c3c", activeforeground="white", borderwidth=0, font=("Arial", 12, "bold"))
    boton.bind("<Enter>", lambda e: boton.config(bg="#e74c3c"))
    boton.bind("<Leave>", lambda e: boton.config(bg=tema_rojo))

def iniciar_sesion():
    ventana = tk.Toplevel()
    ventana.title("Login")
    ventana.geometry("400x300")
    ventana.configure(bg=tema_fondo)

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

    tk.Label(ventana, text="Usuario", fg=tema_texto, bg=tema_fondo, font=("Arial", 12, "bold")).pack()
    entry_usuario = tk.Entry(ventana)
    entry_usuario.pack()

    tk.Label(ventana, text="Contraseña", fg=tema_texto, bg=tema_fondo, font=("Arial", 12, "bold")).pack()
    entry_contrasena = tk.Entry(ventana, show="*")
    entry_contrasena.pack()

    btn_login = tk.Button(ventana, text="Iniciar sesión", command=login)
    estilo_boton(btn_login)
    btn_login.pack(pady=5)

    def volver_al_menu():
        ventana.destroy()
        from main import mostrar_menu_principal
        mostrar_menu_principal()

    btn_volver = tk.Button(ventana, text="Volver", command=volver_al_menu)
    estilo_boton(btn_volver)
    btn_volver.pack(pady=5)
