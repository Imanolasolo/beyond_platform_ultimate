import sqlite3
from passlib.context import CryptContext
import os

# Nombre de la base de datos
DB_NAME = "db/beyond_platform.db"

def create_tables():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Tabla de usuarios internos (solo admin por ahora)
    c.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        rol TEXT NOT NULL CHECK(rol IN ('admin'))
    )
    """)

    # Tabla de videos
    c.execute("""
    CREATE TABLE IF NOT EXISTS videos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        url TEXT NOT NULL,
        descripcion TEXT,
        likes INTEGER DEFAULT 0
    )
    """)

    # Tabla de podcasts
    c.execute("""
    CREATE TABLE IF NOT EXISTS podcasts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        url TEXT NOT NULL,
        descripcion TEXT
    )
    """)

    # Tabla de Beyond Summit
    c.execute("""
    CREATE TABLE IF NOT EXISTS beyond_summit (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        descripcion TEXT NOT NULL,
        fecha DATE NOT NULL,
        hora TIME NOT NULL
    )
    """)

    conn.commit()
    conn.close()

def create_admin_user():
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Datos del admin
    admin_username = "admin"
    admin_password = "admin123"
    admin_rol = "admin"
    # Verifica si ya existe
    c.execute("SELECT * FROM usuarios WHERE username = ?", (admin_username,))
    if not c.fetchone():
        hashed = pwd_context.hash(admin_password)
        c.execute(
            "INSERT INTO usuarios (username, password, rol) VALUES (?, ?, ?)",
            (admin_username, hashed, admin_rol)
        )
        print("✅ Usuario admin creado.")
    else:
        print("ℹ️ Usuario admin ya existe.")
    conn.commit()
    conn.close()

def update_existing_tables():
    """Add likes column to existing videos table if it doesn't exist."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Check if likes column exists, if not add it
    c.execute("PRAGMA table_info(videos)")
    columns = [column[1] for column in c.fetchall()]
    if 'likes' not in columns:
        c.execute("ALTER TABLE videos ADD COLUMN likes INTEGER DEFAULT 0")
        print("✅ Columna 'likes' agregada a la tabla videos.")
    
    conn.commit()
    conn.close()

def initialize_database():
    """Ensure the database and tables are created."""
    # Ensure the directory for the database exists
    db_dir = os.path.dirname(DB_NAME)
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
        print(f"📂 Directorio '{db_dir}' creado.")

    # Always create tables to ensure they exist
    print(f"📂 Verificando tablas en la base de datos {DB_NAME}...")
    create_tables()
    update_existing_tables()
    create_admin_user()
    print("✅ Base de datos inicializada correctamente.")

if __name__ == "__main__":
    initialize_database()
    print(f"📂 Base de datos inicializada en {DB_NAME}")
    initialize_database()
    print(f"📂 Base de datos inicializada en {DB_NAME}")
