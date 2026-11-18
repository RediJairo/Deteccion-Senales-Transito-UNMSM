# Sistema Inteligente de Detección de Señales de Tránsito con YOLO, OpenCV, Python y SQLite

Sistema de detección y reconocimiento de señales de tránsito mediante técnicas de Inteligencia Artificial, Machine Learning y Visión Artificial.

El proyecto consiste en el desarrollo de un sistema capaz de identificar diferentes señales de tránsito mediante una cámara en tiempo real, utilizando un modelo YOLO entrenado para la detección de objetos.

## 🧠 Inteligencia Artificial y Machine Learning

Para el desarrollo del sistema se trabajó con técnicas de **Machine Learning supervisado**, específicamente **Deep Learning**, mediante un modelo YOLO (You Only Look Once) para la detección de objetos.

El entrenamiento del modelo se realizó utilizando imágenes etiquetadas de señales de tránsito, permitiendo que aprendiera a reconocer y localizar las diferentes clases.

Se aplicaron los siguientes conceptos:

- **Machine Learning supervisado:** aprendizaje a partir de imágenes previamente etiquetadas.
- **Deep Learning:** utilización de redes neuronales para el reconocimiento de patrones visuales.
- **Computer Vision:** procesamiento y análisis de imágenes y video mediante OpenCV.
- **Object Detection:** identificación, clasificación y localización de señales mediante cuadros delimitadores (*bounding boxes*).
- **Inferencia en tiempo real:** integración del modelo entrenado para realizar predicciones sobre fotogramas capturados por una cámara.

El modelo resultante se almacena en el archivo `best.pt`, que posteriormente se integra en la aplicación para realizar las detecciones.

## ⚙️ Funcionalidades

- Detección de señales mediante cámara en tiempo real.
- Reconocimiento utilizando un modelo YOLO entrenado.
- Visualización de resultados y niveles de confianza.
- Interfaz gráfica desarrollada con CustomTkinter.
- Almacenamiento de detecciones en SQLite.
- Notificaciones por voz de las señales detectadas.
- Registro de fecha, hora, confianza y ubicación de las detecciones.
- Visualización de ubicaciones registradas mediante un mapa interactivo.

## 🛠️ Tecnologías utilizadas

- **Python:** lenguaje principal de desarrollo.
- **YOLO (Ultralytics):** entrenamiento e inferencia del modelo de detección de objetos.
- **OpenCV:** captura y procesamiento de imágenes y video.
- **SQLite:** almacenamiento y gestión de registros.
- **Folium:** generación de mapas interactivos.
- **CustomTkinter:** desarrollo de la interfaz gráfica.
- **PyWebView:** visualización de contenido web dentro de la aplicación.
- **Pyttsx3:** generación de notificaciones por voz.
- **Pillow:** procesamiento y visualización de imágenes.

## 📦 Instalación

1. Clonar o descargar el repositorio.

2. Instalar las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

3. Inicializar la base de datos:

   ```bash
   python database.py
   ```

4. Ejecutar el sistema:

   ```bash
   python main.py
   ```

## 🤖 Modelo entrenado

El proyecto utiliza el archivo `best.pt`, que contiene los pesos del modelo YOLO obtenidos durante el proceso de entrenamiento.

Este modelo permite reconocer las clases de señales aprendidas y realizar predicciones sobre nuevos fotogramas capturados por la cámara.

## 🗄️ Base de datos

Las detecciones se almacenan localmente mediante SQLite. Se registran los siguientes datos:

- Nombre de la señal detectada.
- Fecha y hora.
- Nivel de confianza.
- Coordenadas geográficas.
- Referencia de la imagen capturada.

## 🗺️ Ubicación geográfica

El sistema integra Folium para representar las detecciones en un mapa interactivo.

Las coordenadas utilizadas actualmente son coordenadas de demostración predefinidas y no representan necesariamente la ubicación GPS real de cada detección.

## 🚀 Posibles mejoras futuras

- Integración de geolocalización GPS en tiempo real.
- Ampliación del conjunto de datos de entrenamiento.
- Evaluación del modelo mediante métricas como Precision, Recall y mAP.
- Optimización del rendimiento de detección.
- Implementación de reportes estadísticos de las detecciones.

---

**Desarrollado como proyecto académico en la Universidad Nacional Mayor de San Marcos (UNMSM).**
