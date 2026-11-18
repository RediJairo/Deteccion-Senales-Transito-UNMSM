import sqlite3

conexion = sqlite3.connect("database.db")
cursor = conexion.cursor()

cursor.execute("SELECT * FROM detecciones")

datos = cursor.fetchall()

if len(datos) == 0:
    print("La tabla está vacía.")
else:
    for fila in datos:
        print(fila)

conexion.close()