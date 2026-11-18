import sqlite3
from datetime import datetime

def crear_base_datos():
    conexion = sqlite3.connect("database.db")
    cursor = conexion.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS detecciones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT,
        hora TEXT,
        senal TEXT,
        confianza REAL,
        latitud REAL,
        longitud REAL,
        imagen TEXT
    )
    """)

    conexion.commit()
    conexion.close()

    print("Base de datos creada correctamente.")

if __name__ == "__main__":
    crear_base_datos()

def guardar_deteccion(senal, confianza, latitud, longitud, imagen):
    conexion = sqlite3.connect("database.db")
    cursor = conexion.cursor()

    ahora = datetime.now()

    fecha = ahora.strftime("%d/%m/%Y")
    hora = ahora.strftime("%H:%M:%S")

    cursor.execute("""
    INSERT INTO detecciones (fecha, hora, senal, confianza, latitud, longitud, imagen)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (fecha, hora, senal, confianza, latitud, longitud, imagen))

    conexion.commit()
    conexion.close()

    print(f"Guardado: {senal} ({confianza:.2f})")