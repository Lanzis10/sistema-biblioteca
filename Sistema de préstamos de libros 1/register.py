import tkinter as tk
from tkinter import messagebox
import sqlite3
from db import conectar


tema_fondo = "#ffffff"  
tema_rojo = "#c0392b"  
tema_texto = "#c0392b"  

def estilo_boton(boton):
    boton.configure(bg=tema_rojo, fg="white", activebackground="#e74c3c", activeforeground="white", borderwidth=0, font=("Arial", 12, "bold"))
    boton.bind("<Enter>", lambda e: boton.config(bg="#e74c3c"))
    boton.bind("<Leave>", lambda e: boton.config(bg=tema_rojo))

def estilo_ventana(ventana):
    ventana.configure(bg=tema_fondo)

def estilo_label(label):
    label.configure(bg=tema_fondo, fg=tema_texto, font=("Arial", 12))

def registrar_usuario():
    ventana = tk.Toplevel()
    ventana.title("Registro")
    ventana.geometry("400x300")
    estilo_ventana(ventana)

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

    label_usuario = tk.Label(ventana, text="Usuario")
    estilo_label(label_usuario)
    label_usuario.pack()

    entry_usuario = tk.Entry(ventana)
    entry_usuario.pack()

    label_contrasena = tk.Label(ventana, text="Contraseña")
    estilo_label(label_contrasena)
    label_contrasena.pack()

    entry_contrasena = tk.Entry(ventana, show="*")
    entry_contrasena.pack()

    btn_registrar = tk.Button(ventana, text="Registrar", command=registrar)
    estilo_boton(btn_registrar)
    btn_registrar.pack(pady=5)

    
    def volver_al_menu():
        ventana.destroy()
        from main import mostrar_menu_principal
        mostrar_menu_principal()

    btn_volver = tk.Button(ventana, text="Volver", command=volver_al_menu)
    estilo_boton(btn_volver)
    btn_volver.pack(pady=5)

