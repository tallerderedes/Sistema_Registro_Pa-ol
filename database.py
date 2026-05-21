import sqlite3

DB_PATH = "paniol_cet22.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS herramientas (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre      TEXT NOT NULL,
            descripcion TEXT,
            cantidad    INTEGER DEFAULT 1,
            estado      TEXT DEFAULT 'Bueno'
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre    TEXT NOT NULL,
            curso     TEXT,
            division  TEXT,
            turno     TEXT NOT NULL,
            tipo      TEXT DEFAULT 'Alumno'
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS prestamos (
            id                INTEGER PRIMARY KEY AUTOINCREMENT,
            herramienta_id    INTEGER NOT NULL,
            usuario_id        INTEGER NOT NULL,
            sector            TEXT NOT NULL,
            observaciones     TEXT,
            fecha_prestamo    TEXT NOT NULL,
            fecha_devolucion  TEXT,
            FOREIGN KEY (herramienta_id) REFERENCES herramientas(id),
            FOREIGN KEY (usuario_id)     REFERENCES usuarios(id)
        )
    """)
    conn.commit()
    conn.close()
    print("Base de datos lista.")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
