import cv2
import os
import time
import threading
from datetime import datetime

from ultralytics import YOLO

from database import guardar_deteccion
from voz import ejecutar_voz
from config import coordenadas, bloqueo_voz


class DetectorGUI:

    def __init__(self):

        print("Cargando modelo YOLO...")

        self.model = YOLO("best.pt")

        print("Modelo cargado correctamente.")

        self.ultima_senal_hablada = None
        self.tiempo_ultima_vision = 0
        self.TIEMPO_OLVIDO = 3

    def procesar_frame(self, frame):
        resultados = self.model(frame)
        tiempo_actual = time.time()

        if (
            tiempo_actual - self.tiempo_ultima_vision
        ) > self.TIEMPO_OLVIDO:

            self.ultima_senal_hablada = None

        ultima_deteccion = None

        for resultado in resultados:
            for caja in resultado.boxes:
                confianza = float(caja.conf[0])

                if confianza < 0.65:
                    continue

                clase = int(caja.cls[0])
                nombre = resultado.names[clase]
                ultima_deteccion = {
                    "senal": nombre,
                    "confianza": confianza,
                    "hora": datetime.now().strftime("%H:%M:%S")
                }

                if nombre == self.ultima_senal_hablada:

                    self.tiempo_ultima_vision = tiempo_actual

                if nombre != self.ultima_senal_hablada:

                    if bloqueo_voz.acquire(blocking=False):

                        self.ultima_senal_hablada = nombre
                        self.tiempo_ultima_vision = tiempo_actual
                        self.guardar_evento(
                            nombre,
                            confianza,
                            frame
                        )

                        threading.Thread(
                            target=ejecutar_voz,
                            args=(
                                f"Señal detectada: {nombre}",
                                bloqueo_voz
                            ),
                            daemon=True
                        ).start()

        frame = resultados[0].plot()

        return {
            "frame": frame,
            "deteccion": ultima_deteccion

        }
    
    def guardar_evento(
        self,
        nombre,
        confianza,
        frame
    ):

        latitud, longitud = coordenadas.get(
            nombre,
            (
                -12.0555,
                -77.0835
            )

        )

        nombre_imagen = f"{nombre}_{int(time.time())}.jpg"

        ruta_imagen = os.path.join(
            "imagenes",
            nombre_imagen

        )

        cv2.imwrite(
            ruta_imagen,
            frame
        )

        guardar_deteccion(
            nombre,
            confianza,
            latitud,
            longitud,
            ruta_imagen

        )