import tkinter as tk
from tkinter import ttk, messagebox
from db import conectar
import datetime

def estilo_ventana(ventana):
    tema_fondo = "#ffffff"
    ventana.configure(bg=tema_fondo)

def estilo_label(label):
    tema_fondo = "#ffffff"
    tema_texto = "#c0392b"
    label.configure(bg=tema_fondo, fg=tema_texto, font=("Arial", 12))

def estilo_tabla(tabla):
    style = ttk.Style()
    style.theme_use('default')
    style.configure("Treeview",
                    background="#fff",
                    foreground="#c0392b",
                    rowheight=25,
                    fieldbackground="#fff",
                    font=("Arial", 11))
    style.configure("Treeview.Heading",
                    background="#c0392b",
                    foreground="#fff",
                    font=("Arial", 12, "bold"))
    style.map('Treeview', background=[('selected', '#e74c3c')], foreground=[('selected', '#fff')])

def estilo_boton(boton):
    tema_fondo = "#c0392b"
    tema_texto = "#ffffff"
    boton.configure(bg=tema_fondo, fg=tema_texto, font=("Arial", 12, "bold"))

def registrar_devolucion(ventana_anterior, id_usuario, nombre_usuario):
    ventana_anterior.destroy()
    ventana = tk.Toplevel()
    ventana.title("Registrar Devolución")
    ventana.geometry("800x500")
    estilo_ventana(ventana)

    label_prestamos = tk.Label(ventana, text="Préstamos Activos", font=("Arial", 16, "bold"))
    estilo_label(label_prestamos)
    label_prestamos.config(font=("Arial", 16, "bold"))
    label_prestamos.pack(pady=10)

    tabla = ttk.Treeview(ventana, columns=("ID", "Solicitante", "Libro", "Fecha préstamo", "Fecha estimada devolución"), show="headings")
    estilo_tabla(tabla)
    tabla.column("ID", width=60)
    tabla.column("Solicitante", width=140)
    tabla.column("Libro", width=180)
    tabla.column("Fecha préstamo", width=120)
    tabla.column("Fecha estimada devolución", width=160)
    for col in tabla["columns"]:
        tabla.heading(col, text=col)
    tabla.pack(padx=10, pady=10, fill="both", expand=True)

    # Cargar préstamos activos
    def cargar_prestamos():
        for row in tabla.get_children():
            tabla.delete(row)

        con = conectar()
        cur = con.cursor()
        cur.execute("""
            SELECT 
                p.id_prestamo,
                s.nombre,
                l.titulo,
                p.fecha_prestamo,
                p.fecha_devolucion_estimada
            FROM prestamo p
            JOIN solicitante s ON s.id_solicitante = p.id_solicitante_fk
            JOIN libro l ON l.id_libro = p.id_libro_fk
            WHERE p.estado = 'en préstamo'
        """)
        for fila in cur.fetchall():
            tabla.insert("", "end", values=fila)

        con.close()

    cargar_prestamos()

    # Función para registrar devolución
    def registrar():
        seleccionado = tabla.selection()
        if not seleccionado:
            messagebox.showwarning("Advertencia", "Selecciona un préstamo para registrar la devolución.")
            return

        fila = tabla.item(seleccionado[0])["values"]
        id_prestamo = fila[0]
        fecha_devolucion_real = datetime.date.today()

        con = conectar()
        cur = con.cursor()

        try:
            # Cambiar estado a devuelto
            cur.execute("UPDATE prestamo SET estado = 'devuelto' WHERE id_prestamo = ?", (id_prestamo,))

            # Registrar devolución
            cur.execute("""
                INSERT INTO devolucion (fecha_devolucion_real, id_prestamo_fk)
                VALUES (?, ?)
            """, (fecha_devolucion_real, id_prestamo))

            # Obtener fecha estimada para calcular multa
            cur.execute("SELECT fecha_devolucion_estimada FROM prestamo WHERE id_prestamo = ?", (id_prestamo,))
            fecha_estimada = cur.fetchone()[0]

            fecha_estimada_dt = datetime.datetime.strptime(fecha_estimada, "%Y-%m-%d").date()
            dias_atraso = (fecha_devolucion_real - fecha_estimada_dt).days

            if dias_atraso > 0:
                monto = dias_atraso * 500
                cur.execute("""
                    INSERT INTO multa (monto, pagado, id_prestamo_fk)
                    VALUES (?, 0, ?)
                """, (monto, id_prestamo))
                messagebox.showwarning("Multa Generada", f"El libro se devolvió con {dias_atraso} días de atraso.\nSe generó una multa de ${monto} CLP.")

            con.commit()
            messagebox.showinfo("Éxito", "Devolución registrada correctamente.")
            cargar_prestamos()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar la devolución: {e}")
        finally:
            con.close()


    # Botones
    frame_botones = tk.Frame(ventana, bg="#ffffff")
    frame_botones.pack(pady=15)

    btn_registrar = tk.Button(frame_botones, text="Registrar Devolución", command=registrar)
    estilo_boton(btn_registrar)
    btn_registrar.grid(row=0, column=0, padx=10)

    def volver():
        ventana.destroy()
        from home import mostrar_home
        mostrar_home(id_usuario, nombre_usuario)

    btn_volver = tk.Button(frame_botones, text="Volver", command=volver)
    estilo_boton(btn_volver)
    btn_volver.grid(row=0, column=1, padx=10)
