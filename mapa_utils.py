import subprocess
import os

def generar_mapa():
    subprocess.run(
        ["python", "mapa.py"],
        check=True
    )

    ruta = os.path.abspath(
        "mapa.html"
    )

    return ruta