import os
import threading

# Crear carpeta de imágenes
if not os.path.exists("imagenes"):
    os.makedirs("imagenes")

# Coordenadas de las señales
coordenadas = {
    "Pare": (-12.05670, -77.08450),
    "Zona de estacionamiento": (-12.05310, -77.08410),
    "Parada de bus": (-12.05420, -77.08180),
    "Limite maximo de velocidad": (-12.05630, -77.08150),
    "Altura maxima Serie de limites maximos": (-12.05500, -77.08480),
    "Ninos": (-12.05470, -77.08250),
    "Senal de advertencia anticipada de escuela": (-12.05400, -77.08100),
    "Punto de encuentro": (-12.05350, -77.08280)
}

# Candado para la voz
bloqueo_voz = threading.Lock()