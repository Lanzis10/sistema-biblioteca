import sqlite3

def conectar():
    con = sqlite3.connect("Sistema_De_Biblioteca.db")
    con.execute("PRAGMA foreign_keys = ON") # esto sirve para que las llaves foraneas funcionen y las tablas se relacionen correctamente
    return con

def crear_tablas():  # con esta linea de codigo se crean las tablas correctamente, haciendo un tipo de automatizacion
    con = conectar()
    cur = con.cursor()

     # Tabla usuario (bibliotecario)
    cur.execute(""" 
        CREATE TABLE IF NOT EXISTS usuario (
            id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            contraseña TEXT NOT NULL
        )
    """)

    # Tabla solicitante (profesor o estudiante)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS solicitante (
            id_solicitante INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            rut TEXT NOT NULL UNIQUE,
            tipo TEXT NOT NULL,  -- 'estudiante' o 'profesor'
            correo TEXT UNIQUE
        )
    """)

    # Tabla categoría
    cur.execute("""
        CREATE TABLE IF NOT EXISTS categoria (
            id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_categoria TEXT NOT NULL
        )
    """)

    # Tabla libro
    cur.execute("""
        CREATE TABLE IF NOT EXISTS libro (
            id_libro INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT UNIQUE NOT NULL,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            editorial TEXT,
            descripcion TEXT,
            id_categoria_fk INTEGER,
            FOREIGN KEY (id_categoria_fk) REFERENCES categoria(id_categoria)
        )
    """)

    # Tabla prestamo 
    cur.execute("""
        CREATE TABLE IF NOT EXISTS prestamo (
            id_prestamo INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha_prestamo TEXT NOT NULL,
            fecha_devolucion_estimada TEXT NOT NULL,
            estado TEXT NOT NULL,
            id_libro_fk INTEGER NOT NULL,
            id_solicitante_fk INTEGER NOT NULL,
            id_usuario_fk INTEGER NOT NULL,
            FOREIGN KEY (id_libro_fk) REFERENCES libro(id_libro),
            FOREIGN KEY (id_solicitante_fk) REFERENCES solicitante(id_solicitante),
            FOREIGN KEY (id_usuario_fk) REFERENCES usuario(id_usuario)
        )
    """)

    # Tabla multa (ahora la FK a prestamo funcionará correctamente)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS multa (
            id_multa INTEGER PRIMARY KEY AUTOINCREMENT,
            monto REAL NOT NULL,
            pagado INTEGER NOT NULL DEFAULT 0, -- 0 = No, 1 = Sí,
            fecha_pago TEXT,
            id_prestamo_fk INTEGER,
            FOREIGN KEY (id_prestamo_fk) REFERENCES prestamo(id_prestamo)
        )
    """)

    # Tabla devolucion
    cur.execute("""
        CREATE TABLE IF NOT EXISTS devolucion (
            id_devolucion INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha_devolucion_real TEXT NOT NULL,
            id_prestamo_fk INTEGER NOT NULL,
            FOREIGN KEY (id_prestamo_fk) REFERENCES prestamo(id_prestamo)
        )
    """)

    # Tabla renovación
    cur.execute("""
        CREATE TABLE IF NOT EXISTS renovacion (
            id_renovacion INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha_renovacion TEXT NOT NULL,
            nueva_fecha_devolucion TEXT NOT NULL,
            id_prestamo_fk INTEGER NOT NULL,
            FOREIGN KEY (id_prestamo_fk) REFERENCES prestamo(id_prestamo)
        )
    """)

    cur.execute("SELECT COUNT (*) FROM categoria")
    if cur.fetchone()[0] == 0:
        categorias_iniciales = [
            ("Ciencia Ficción",),
            ("Matemáticas",),
            ("Historia",),
            ("Literatura",),
            ("Tecnología",),
            ("Filosofía",),
            ("Psicología",),
            ("Educación",),
            ("Economía",),
            ("Programación",),
        ]
        cur.executemany("INSERT INTO categoria (nombre_categoria) VALUES (?)", categorias_iniciales)
        
    con.commit()
    con.close()

if __name__ == "__main__":
    crear_tablas()
    print("Tablas creadas correctamente")