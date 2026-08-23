import sqlite3
from pathlib import Path

# Definimos la ruta donde se guardará nuestra base de datos
DB_PATH = Path.home() / "mis_proyectos.db"

def inicializar_bd():
    # Conectamos a la base de datos (si no existe, SQLite la crea automáticamente)
    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()
    
    # Creamos una tabla llamada 'proyectos'
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS proyectos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            estado TEXT NOT NULL,
            prioridad INTEGER
        )
    """)
    
    conexion.commit()
    conexion.close()
    print(f"Base de datos inicializada en: {DB_PATH}")

def agregar_proyecto(nombre, estado, prioridad):
    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()
    
    # Insertamos un nuevo registro de forma segura usando parámetros (?)
    cursor.execute("""
        INSERT INTO proyectos (nombre, estado, prioridad)
        VALUES (?, ?, ?)
    """, (nombre, estado, prioridad))
    
    conexion.commit()
    conexion.close()
    print(f"[Éxito] Proyecto '{nombre}' agregado a la base de datos.")

def consultar_proyectos():
    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()
    
    # Consultamos todos los registros almacenados
    cursor.execute("SELECT * FROM proyectos")
    filas = cursor.fetchall()
    
    print("\n=== LISTA DE PROYECTOS EN LA BASE DE DATOS ===")
    for fila in filas:
        print(f"ID: {fila[0]} | Proyecto: {fila[1]} | Estado: {fila[2]} | Prioridad: {fila[3]}")
        
    conexion.close()

if __name__ == "__main__":
    inicializar_bd()
    # Agregamos un par de proyectos de ejemplo
    agregar_proyecto("El Rincón de las Esquinas", "En desarrollo", 1)
    agregar_proyecto("Automatización con Python", "Completado", 2)
    # Consultamos la información guardada
    consultar_proyectos()

