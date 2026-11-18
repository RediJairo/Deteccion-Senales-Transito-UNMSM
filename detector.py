import cv2
import os
import time
import threading

from ultralytics import YOLO

from tkinter import messagebox

from database import guardar_deteccion
from voz import ejecutar_voz
from config import coordenadas,bloqueo_voz


def iniciar_deteccion():

    try:
        model=YOLO("best.pt")

    except Exception as e:

        messagebox.showerror(
            "Error",
            f"No se pudo cargar el modelo\n{e}"
        )

        return


    cap=cv2.VideoCapture(0)

    if not cap.isOpened():

        messagebox.showerror(
            "Error",
            "No se pudo abrir la cámara."
        )

        return


    ultima_senal_hablada=None
    tiempo_ultima_vision=0

    TIEMPO_OLVIDO=3


    while True:

        ret,frame=cap.read()

        if not ret:
            break

        resultados=model(frame)

        tiempo_actual=time.time()

        if tiempo_actual-tiempo_ultima_vision>TIEMPO_OLVIDO:
            ultima_senal_hablada=None


        for resultado in resultados:

            for caja in resultado.boxes:

                confianza=float(caja.conf[0])

                if confianza<0.65:
                    continue

                clase=int(caja.cls[0])

                nombre=resultado.names[clase]

                if nombre==ultima_senal_hablada:
                    tiempo_ultima_vision=tiempo_actual

                if nombre!=ultima_senal_hablada:

                    if bloqueo_voz.acquire(blocking=False):

                        ultima_senal_hablada=nombre
                        tiempo_ultima_vision=tiempo_actual

                        latitud,longitud=coordenadas.get(
                            nombre,
                            (-12.0555,-77.0835)
                        )

                        nombre_imagen=f"{nombre}_{int(time.time())}.jpg"

                        ruta=os.path.join(
                            "imagenes",
                            nombre_imagen
                        )

                        cv2.imwrite(ruta,frame)

                        guardar_deteccion(
                            nombre,
                            confianza,
                            latitud,
                            longitud,
                            ruta
                        )

                        threading.Thread(
                            target=ejecutar_voz,
                            args=(f"Señal detectada: {nombre}",bloqueo_voz),
                            daemon=True
                        ).start()

        imagen=resultados[0].plot()

        cv2.imshow(
            "Detección de Señales",
            imagen
        )

        if cv2.waitKey(1)==27:
            break


    cap.release()
    cv2.destroyAllWindows()