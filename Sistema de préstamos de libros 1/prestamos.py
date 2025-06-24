import tkinter as tk
from tkinter import messagebox, ttk
from db import conectar
import datetime

def ver_prestamos(ventana_anterior, id_usuario, nombre_usuario):
    ventana_anterior.destroy()
    ventana = tk.Toplevel()
    ventana.title("Gestionar Préstamos")
    ventana.geometry("800x500")

    tk.Label(ventana, text="Gestión de Préstamos", font=("Arial", 16)).pack(pady=10)

    frame_botones = tk.Frame(ventana)
    frame_botones.pack(pady=10)

    def volver_menu():
        ventana.destroy()
        from home import mostrar_home
        mostrar_home(id_usuario, nombre_usuario)

    def registrar_prestamo():
        ventana_prestamo = tk.Toplevel(ventana)
        ventana_prestamo.title("Registrar Préstamo")
        ventana_prestamo.geometry("450x550")

        tk.Label(ventana_prestamo, text="Tipo de solicitante:").pack()
        combo_tipo = ttk.Combobox(ventana_prestamo, values=["estudiante", "profesor"], state="readonly")
        combo_tipo.pack()

        tk.Label(ventana_prestamo, text="Nombre completo:").pack()
        entry_nombre = tk.Entry(ventana_prestamo)
        entry_nombre.pack()

        tk.Label(ventana_prestamo, text="RUT:").pack()
        entry_rut = tk.Entry(ventana_prestamo)
        entry_rut.pack()

        tk.Label(ventana_prestamo, text="Correo (@inacapmail.cl):").pack()
        entry_correo = tk.Entry(ventana_prestamo)
        entry_correo.pack()

        tk.Label(ventana_prestamo, text="Libro a prestar:").pack()
        combo_libros = ttk.Combobox(ventana_prestamo, state="readonly")
        combo_libros.pack()

        con = conectar()
        cur = con.cursor()
        cur.execute("""
            SELECT id_libro, titulo, autor FROM libro
            WHERE id_libro NOT IN (
                SELECT id_libro_fk FROM prestamo WHERE estado = 'en préstamo'
            )
        """)
        libros = cur.fetchall()
        con.close()

        libro_dict = {f"{titulo} - {autor}": id_ for id_, titulo, autor in libros}
        combo_libros["values"] = list(libro_dict.keys())

        fecha_hoy = datetime.date.today()
        tk.Label(ventana_prestamo, text=f"Fecha de préstamo: {fecha_hoy}").pack(pady=5)

        tk.Label(ventana_prestamo, text="Fecha estimada de devolución (YYYY-MM-DD):").pack()
        entry_devolucion = tk.Entry(ventana_prestamo)
        entry_devolucion.pack()

        def guardar_prestamo():
            tipo = combo_tipo.get()
            nombre = entry_nombre.get()
            rut = entry_rut.get()
            correo = entry_correo.get()
            libro_titulo = combo_libros.get()
            fecha_devolucion = entry_devolucion.get()

            if not (tipo and nombre and rut and correo and libro_titulo and fecha_devolucion):
                messagebox.showwarning("Campos incompletos", "Completa todos los campos.")
                return

            if not correo.endswith("@inacapmail.cl"):
                messagebox.showerror("Correo inválido", "El correo debe terminar en @inacapmail.cl")
                return

            try:
                datetime.datetime.strptime(fecha_devolucion, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Error de fecha", "La fecha debe tener el formato YYYY-MM-DD")
                return

            id_libro = libro_dict[libro_titulo]

            con = conectar()
            cur = con.cursor()

            cur.execute("SELECT id_solicitante FROM solicitante WHERE rut = ?", (rut,))
            resultado = cur.fetchone()
            if resultado:
                id_solicitante = resultado[0]
            else:
                cur.execute("""
                    INSERT INTO solicitante (nombre, rut, tipo, correo) VALUES (?, ?, ?, ?)
                """, (nombre, rut, tipo, correo))
                id_solicitante = cur.lastrowid

            try:
                cur.execute("""
                    INSERT INTO prestamo (fecha_prestamo, fecha_devolucion_estimada, estado, id_libro_fk, id_solicitante_fk, id_usuario_fk)
                    VALUES (?, ?, 'en préstamo', ?, ?, ?)
                """, (str(fecha_hoy), fecha_devolucion, id_libro, id_solicitante, id_usuario))
                con.commit()
                messagebox.showinfo("Éxito", "Préstamo registrado correctamente.")
                ventana_prestamo.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo registrar: {e}")
            finally:
                con.close()

        frame_botones = tk.Frame(ventana_prestamo)
        frame_botones.pack(pady=20)

        tk.Button(frame_botones, text="Registrar Préstamo", command=guardar_prestamo).grid(row=0, column=0, padx=10)
        tk.Button(frame_botones, text="Volver", command=ventana_prestamo.destroy).grid(row=0, column=1, padx=10)

    def renovar_prestamo():
        ventana_renovar = tk.Toplevel(ventana)
        ventana_renovar.title("Renovar Préstamo")
        ventana_renovar.geometry("400x300")

        tk.Label(ventana_renovar, text="RUT del solicitante:").pack()
        entry_rut = tk.Entry(ventana_renovar)
        entry_rut.pack()

        tk.Label(ventana_renovar, text="Nueva fecha de devolución (YYYY-MM-DD):").pack()
        entry_nueva_fecha = tk.Entry(ventana_renovar)
        entry_nueva_fecha.pack()

        def guardar_renovacion():
            rut = entry_rut.get()
            nueva_fecha = entry_nueva_fecha.get()
            try:
                datetime.datetime.strptime(nueva_fecha, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Error", "Formato de fecha inválido")
                return

            con = conectar()
            cur = con.cursor()
            cur.execute("""
                SELECT p.id_prestamo FROM prestamo p
                JOIN solicitante s ON p.id_solicitante_fk = s.id_solicitante
                WHERE s.rut = ? AND p.estado = 'en préstamo'
            """, (rut,))
            resultado = cur.fetchone()

            if resultado:
                id_prestamo = resultado[0]
                cur.execute("""
                    INSERT INTO renovacion (fecha_renovacion, nueva_fecha_devolucion, id_prestamo_fk)
                    VALUES (?, ?, ?)
                """, (datetime.date.today(), nueva_fecha, id_prestamo))

                cur.execute("""
                    UPDATE prestamo SET fecha_devolucion_estimada = ? WHERE id_prestamo = ?
                """, (nueva_fecha, id_prestamo))

                con.commit()
                messagebox.showinfo("Éxito", "Préstamo renovado correctamente.")
                ventana_renovar.destroy()
            else:
                messagebox.showerror("Error", "No se encontró préstamo activo para este RUT")

            con.close()

        tk.Button(ventana_renovar, text="Renovar", command=guardar_renovacion).pack(pady=10)
        tk.Button(ventana_renovar, text="Volver", command=ventana_renovar.destroy).pack()

    tk.Button(frame_botones, text="Registrar Préstamo", command=registrar_prestamo).grid(row=0, column=0, padx=10)
    tk.Button(frame_botones, text="Renovar Préstamo", command=renovar_prestamo).grid(row=0, column=1, padx=10)
    tk.Button(frame_botones, text="Volver", command=volver_menu).grid(row=0, column=2, padx=10)