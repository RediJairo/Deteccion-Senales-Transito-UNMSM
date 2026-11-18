import sqlite3
import folium

# Conectar a la base de datos
conexion = sqlite3.connect("database.db")
cursor = conexion.cursor()

cursor.execute("""
SELECT senal, fecha, hora, confianza, latitud, longitud
FROM detecciones
""")

datos = cursor.fetchall()
conexion.close()

# Crear mapa
mapa = folium.Map(location=[-12.0555, -77.0835], zoom_start=16)

for senal, fecha, hora, confianza, latitud, longitud in datos:

    confianza *= 100
    color = "blue"

    if senal == "Pare":
        color = "red"

    elif senal == "Ninos":
        color = "orange"

    elif senal == "Limite maximo de velocidad":
        color = "green"

    elif senal == "Parada de bus":
        color = "purple"

    elif senal == "Gasolinera":
        color = "darkblue"

    folium.Marker(
        location=[latitud, longitud],
        popup=f"""
        <b>Señal:</b> {senal}<br>
        <b>Fecha:</b> {fecha}<br>
        <b>Hora:</b> {hora}<br>
        <b>Confianza:</b> {confianza:.2f}%
        """,
        tooltip=senal,
        icon=folium.Icon(color=color, icon="info-sign")
    ).add_to(mapa)

mapa.save("mapa.html")

print("Mapa generado correctamente.")