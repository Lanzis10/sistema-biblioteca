import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from db import conectar

# Colores de la interfaz
tema_fondo = "#ffffff"  # blanco
tema_rojo = "#c0392b"  # rojo fuerte
tema_texto = "#c0392b"  # rojo para textos

def estilo_boton(boton):
    boton.configure(bg=tema_rojo, fg="white", activebackground="#e74c3c", activeforeground="white", borderwidth=0, font=("Arial", 12, "bold"))
    boton.bind("<Enter>", lambda e: boton.config(bg="#e74c3c"))
    boton.bind("<Leave>", lambda e: boton.config(bg=tema_rojo))

def gestionar_libros(ventana_anterior, id_usuario, nombre_usuario):
    ventana_anterior.destroy()
    ventana = tk.Toplevel()
    ventana.title("Gestión de Libros")
    ventana.geometry("800x500")
    ventana.configure(bg=tema_fondo)

    # Función para cargar libros
    # ... (importaciones y encabezado igual)

    def cargar_libros():
        for row in tabla.get_children():
            tabla.delete(row)
        con = conectar()
        cur = con.cursor()
        cur.execute("""
            SELECT 
                l.id_libro, l.codigo, l.titulo, l.autor, l.editorial, l.descripcion, c.nombre_categoria,
                CASE
                    WHEN EXISTS (
                        SELECT 1 FROM prestamo p
                        WHERE p.id_libro_fk = l.id_libro AND p.estado = 'en préstamo'
                    )
                    THEN 'No'
                    ELSE 'Sí'
                END AS disponible
            FROM libro l
            LEFT JOIN categoria c ON l.id_categoria_fk = c.id_categoria
        """)
        for fila in cur.fetchall():
            tabla.insert("", "end", values=fila)
        con.close()


    # Función para agregar libro (solo esqueleto por ahora)
    def agregar_libro():
        ventana_agregar = tk.Toplevel(ventana)
        ventana_agregar.title("Agregar Libro")
        ventana_agregar.geometry("400x400")
        ventana_agregar.configure(bg=tema_fondo)

        tk.Label(ventana_agregar, text="Código", fg=tema_texto, bg=tema_fondo, font=("Arial", 12, "bold")).pack()
        entry_codigo = tk.Entry(ventana_agregar)
        entry_codigo.pack()

        tk.Label(ventana_agregar, text="Título", fg=tema_texto, bg=tema_fondo, font=("Arial", 12, "bold")).pack()
        entry_titulo = tk.Entry(ventana_agregar)
        entry_titulo.pack()

        tk.Label(ventana_agregar, text="Autor", fg=tema_texto, bg=tema_fondo, font=("Arial", 12, "bold")).pack()
        entry_autor = tk.Entry(ventana_agregar)
        entry_autor.pack()

        tk.Label(ventana_agregar, text="Editorial", fg=tema_texto, bg=tema_fondo, font=("Arial", 12, "bold")).pack()
        entry_editorial = tk.Entry(ventana_agregar)
        entry_editorial.pack()

        tk.Label(ventana_agregar, text="Descripción", fg=tema_texto, bg=tema_fondo, font=("Arial", 12, "bold")).pack()
        entry_descripcion = tk.Entry(ventana_agregar)
        entry_descripcion.pack()

        tk.Label(ventana_agregar, text="Categoría", fg=tema_texto, bg=tema_fondo, font=("Arial", 12, "bold")).pack()
        combo_categoria = ttk.Combobox(ventana_agregar, state="readonly")
        combo_categoria.pack()

        # Cargar categorías disponibles desde la BD
        con = conectar()
        cur = con.cursor()
        cur.execute("SELECT id_categoria, nombre_categoria FROM categoria")
        categorias = cur.fetchall()
        con.close()

        categorias_dict = {nombre: id_ for id_, nombre in categorias}
        combo_categoria["values"] = list(categorias_dict.keys())

        def guardar_libro():
            codigo = entry_codigo.get()
            titulo = entry_titulo.get()
            autor = entry_autor.get()
            editorial = entry_editorial.get()
            descripcion = entry_descripcion.get()
            categoria_nombre = combo_categoria.get()

            if not all([codigo, titulo, autor, categoria_nombre]):
                messagebox.showwarning("Campos incompletos", "Debes completar los campos obligatorios.")
                return

            id_categoria = categorias_dict.get(categoria_nombre)

            con = conectar()
            cur = con.cursor()
            try:
                cur.execute("""
                    INSERT INTO libro (codigo, titulo, autor, editorial, descripcion, id_categoria_fk)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (codigo, titulo, autor, editorial, descripcion, id_categoria))
                con.commit()
                messagebox.showinfo("Éxito", "Libro agregado correctamente")
                ventana_agregar.destroy()
                cargar_libros()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Ya existe un libro con ese código.")
            finally:
                con.close()

        btn_guardar = tk.Button(ventana_agregar, text="Guardar", command=guardar_libro)
        estilo_boton(btn_guardar)
        btn_guardar.pack(pady=10)


    # Función para eliminar libro seleccionado
    def eliminar_libro():
        seleccionado = tabla.selection()
        if not seleccionado:
            messagebox.showwarning("Advertencia", "Selecciona un libro para eliminar.")
            return
        id_libro = tabla.item(seleccionado[0])["values"][0]
        respuesta = messagebox.askyesno("Confirmar", "¿Seguro que deseas eliminar este libro?")
        if respuesta:
            con = conectar()
            cur = con.cursor()
            cur.execute("DELETE FROM libro WHERE id_libro = ?", (id_libro,))
            con.commit()
            con.close()
            cargar_libros()
            messagebox.showinfo("Éxito", "Libro eliminado correctamente.")
    
    def editar_libro():
        seleccionado = tabla.selection()
        if not seleccionado:
            messagebox.showwarning("Advertencia", "Selecciona un libro para editar.")
            return

        valores = tabla.item(seleccionado[0])["values"]
        id_libro, codigo_actual, titulo_actual, autor_actual, editorial_actual, descripcion_actual, categoria_actual, disponibilidad = valores

        ventana_editar = tk.Toplevel(ventana)
        ventana_editar.title("Editar Libro")
        ventana_editar.geometry("400x450")
        ventana_editar.configure(bg=tema_fondo)

        tk.Label(ventana_editar, text="Código", fg=tema_texto, bg=tema_fondo, font=("Arial", 12, "bold")).pack()
        entry_codigo = tk.Entry(ventana_editar)
        entry_codigo.insert(0, codigo_actual)
        entry_codigo.pack()

        tk.Label(ventana_editar, text="Título", fg=tema_texto, bg=tema_fondo, font=("Arial", 12, "bold")).pack()
        entry_titulo = tk.Entry(ventana_editar)
        entry_titulo.insert(0, titulo_actual)
        entry_titulo.pack()

        tk.Label(ventana_editar, text="Autor", fg=tema_texto, bg=tema_fondo, font=("Arial", 12, "bold")).pack()
        entry_autor = tk.Entry(ventana_editar)
        entry_autor.insert(0, autor_actual)
        entry_autor.pack()

        tk.Label(ventana_editar, text="Editorial", fg=tema_texto, bg=tema_fondo, font=("Arial", 12, "bold")).pack()
        entry_editorial = tk.Entry(ventana_editar)
        entry_editorial.insert(0, editorial_actual)
        entry_editorial.pack()

        tk.Label(ventana_editar, text="Descripción", fg=tema_texto, bg=tema_fondo, font=("Arial", 12, "bold")).pack()
        entry_descripcion = tk.Entry(ventana_editar)
        entry_descripcion.insert(0, descripcion_actual)
        entry_descripcion.pack()

        tk.Label(ventana_editar, text="Categoría", fg=tema_texto, bg=tema_fondo, font=("Arial", 12, "bold")).pack()
        combo_categoria = ttk.Combobox(ventana_editar, state="readonly")
        combo_categoria.pack()

        # Obtener categorías
        con = conectar()
        cur = con.cursor()
        cur.execute("SELECT id_categoria, nombre_categoria FROM categoria")
        categorias = cur.fetchall()
        con.close()

        categorias_dict = {nombre: id_ for id_, nombre in categorias}
        combo_categoria["values"] = list(categorias_dict.keys())
        combo_categoria.set(categoria_actual)  # Preselecciona categoría actual

        def guardar_cambios():
            nuevo_codigo = entry_codigo.get()
            nuevo_titulo = entry_titulo.get()
            nuevo_autor = entry_autor.get()
            nuevo_editorial = entry_editorial.get()
            nueva_descripcion = entry_descripcion.get()
            nueva_categoria = combo_categoria.get()

            if not all([nuevo_codigo, nuevo_titulo, nuevo_autor, nueva_categoria]):
                messagebox.showwarning("Campos incompletos", "Debes completar los campos obligatorios.")
                return

            id_categoria = categorias_dict.get(nueva_categoria)

            con = conectar()
            cur = con.cursor()
            try:
                cur.execute("""
                    UPDATE libro
                    SET codigo=?, titulo=?, autor=?, editorial=?, descripcion=?, id_categoria_fk=?
                    WHERE id_libro=?
                """, (nuevo_codigo, nuevo_titulo, nuevo_autor, nuevo_editorial, nueva_descripcion, id_categoria, id_libro))
                con.commit()
                messagebox.showinfo("Éxito", "Libro actualizado correctamente")
                ventana_editar.destroy()
                cargar_libros()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Ese código ya existe para otro libro.")
            finally:
                con.close()

        btn_guardar = tk.Button(ventana_editar, text="Guardar Cambios", command=guardar_cambios)
        estilo_boton(btn_guardar)
        btn_guardar.pack(pady=10)


    # Título
    tk.Label(ventana, text="Gestión de Libros", font=("Arial", 16, "bold"), fg=tema_texto, bg=tema_fondo).pack(pady=10)
    frame_busqueda = tk.Frame(ventana, bg=tema_fondo)
    frame_busqueda.pack(pady=5)

    tk.Label(frame_busqueda, text="Buscar por título o autor:", fg=tema_texto, bg=tema_fondo, font=("Arial", 11)).pack(side="left")
    entry_busqueda = tk.Entry(frame_busqueda, width=30)
    entry_busqueda.pack(side="left", padx=5)

    btn_buscar = tk.Button(frame_busqueda, text="Buscar", command=buscar_libros)
    estilo_boton(btn_buscar)
    btn_buscar.pack(side="left", padx=5)

    
    # Tabla
    columnas = ("ID", "Código", "Título", "Autor", "Editorial", "Descripción", "Categoría","Disponibilidad")
    tabla = ttk.Treeview(ventana, columns=columnas, show="headings")
    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, width=100)
    tabla.pack(fill="both", expand=True, padx=10, pady=10)

    # Botones
    frame_botones = tk.Frame(ventana, bg=tema_fondo)
    frame_botones.pack(pady=10)

    def add_btn(text, cmd, col):
        btn = tk.Button(frame_botones, text=text, command=cmd)
        estilo_boton(btn)
        btn.grid(row=0, column=col, padx=10)

    add_btn("Agregar Libro", agregar_libro, 0)
    add_btn("Eliminar Libro", eliminar_libro, 1)
    add_btn("Recargar", cargar_libros, 2)
    add_btn("Editar Libro", editar_libro, 3)

    btn_volver = tk.Button(ventana, text="Volver", command=volver_al_menu)
    estilo_boton(btn_volver)
    btn_volver.pack(pady=10)

    cargar_libros()