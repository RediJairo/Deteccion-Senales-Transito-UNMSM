import customtkinter as ctk
from PIL import Image, ImageTk
import cv2
import threading
import webview

from camera_controller import CameraController
from detector_gui import DetectorGUI
from mapa_utils import generar_mapa

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        # ==========================
        # FUENTES
        # ==========================

        self.FONT_TITLE = ctk.CTkFont(
            family="Segoe UI",
            size=28,
            weight="bold"
        )

        self.FONT_HEADER = ctk.CTkFont(
            family="Segoe UI",
            size=20,
            weight="bold"
        )

        self.FONT_NORMAL = ctk.CTkFont(
            family="Segoe UI",
            size=15
        )

        self.FONT_SMALL = ctk.CTkFont(
            family="Segoe UI",
            size=12
        )

        self.title("Sistema Inteligente de Detección de Señales")
        self.geometry("1280x720")
        self.minsize(1100, 650)
        self.detector = DetectorGUI()
        self.camera = CameraController()
        self.camara_activa = False
        self.foto = None
        self.total_detecciones = 0
        self.ultima_senal_contada = None
        self.protocol(
            "WM_DELETE_WINDOW",
            self.cerrar_programa
        )
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.crear_barra_superior()
        self.crear_menu_lateral()
        self.crear_panel_principal()
        self.crear_barra_estado()
        self.mostrar_inicio()

    def crear_barra_superior(self):

        self.topbar = ctk.CTkFrame(
            self,
            height=75,
            corner_radius=0
        )

        self.topbar.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="nsew"
        )


        titulo = ctk.CTkLabel(
            self.topbar,
            text="🚦  VISION AI | Traffic Sign Detection",
            font=self.FONT_TITLE
        )

        titulo.pack(
            pady=(12,0)
        )


        subtitulo = ctk.CTkLabel(
            self.topbar,
            text="Sistema inteligente de detección mediante YOLO",
            font=self.FONT_SMALL
        )

        subtitulo.pack()

    def crear_menu_lateral(self):

        self.menu = ctk.CTkFrame(
            self,
            width=230,
            corner_radius=0
        )

        self.menu.grid(
            row=1,
            column=0,
            sticky="ns"
        )

        self.menu.grid_propagate(False)
        titulo = ctk.CTkLabel(

            self.menu,
            text="MENÚ",
            font=ctk.CTkFont(
                size=22,
                weight="bold"
            )

        )

        titulo.pack(
            pady=(25,20)
        )

        self.btnInicio = ctk.CTkButton(
            self.menu,
            text="⌂  Inicio",
            command=self.mostrar_inicio

        )

        self.btnInicio.pack(
            padx=20,
            pady=8,
            fill="x"
        )

        self.btnDeteccion = ctk.CTkButton(
            self.menu,
            text="◉  Detección",
            command=self.abrir_deteccion

        )

        self.btnDeteccion.pack(
            padx=20,
            pady=8,
            fill="x"
        )

        self.btnMapa = ctk.CTkButton(
            self.menu,
            text="◎  Mapa",
            command=self.abrir_mapa

        )

        self.btnMapa.pack(
            padx=20,
            pady=8,
            fill="x"
        )

        self.btnSalir = ctk.CTkButton(
            self.menu,
            text="⏻  Salir",
            fg_color="#c62828",
            hover_color="#b71c1c",
            command=self.cerrar_programa

        )

        self.btnSalir.pack(
            side="bottom",
            padx=20,
            pady=20,
            fill="x"
        )

    def crear_panel_principal(self):

        self.panel = ctk.CTkFrame(
            self
        )

        self.panel.grid(
            row=1,
            column=1,
            sticky="nsew",
            padx=20,
            pady=20
        )

    def crear_barra_estado(self):

        self.status = ctk.CTkFrame(
            self,
            height=35,
            corner_radius=0
        )

        self.status.grid(
            row=2,
            column=0,
            columnspan=2,
            sticky="ew"
        )

        self.lblEstado = ctk.CTkLabel(
            self.status,
            text="Estado: Sistema listo"

        )

        self.lblEstado.pack(
            side="left",
            padx=20
        )

        self.lblVersion = ctk.CTkLabel(
            self.status,
            text="UNMSM  |  v2.0"

        )

        self.lblVersion.pack(
            side="right",
            padx=20
        )
    
    def limpiar_panel(self):
        for widget in self.panel.winfo_children():
            widget.destroy()

    def mostrar_inicio(self):

        self.detener_camara()
        self.limpiar_panel()
        titulo = ctk.CTkLabel(
            self.panel,
            text="🚦 Vision AI",

            font=ctk.CTkFont(
                size=34,
                weight="bold"
            )
        )

        titulo.pack(
            pady=(80,20)
        )

        descripcion = ctk.CTkLabel(
            self.panel,
            text="Sistema inteligente de reconocimiento de señales de tránsito\nmediante visión artificial YOLO",
            font=ctk.CTkFont(
                size=18
            )

        )

        descripcion.pack()
        self.lblEstado.configure(
            text="Estado: Esperando una acción"
        )

    def abrir_deteccion(self):

        self.limpiar_panel()
        self.panel.grid_columnconfigure(0, weight=4)
        self.panel.grid_columnconfigure(1, weight=1)
        self.panel.grid_rowconfigure(0, weight=1)

        # ============================
        # PANEL DEL VIDEO
        # ============================

        panel_video = ctk.CTkFrame(
            self.panel
        )

        panel_video.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(10,5),
            pady=10
        )

        panel_video.grid_rowconfigure(
            0,
            weight=1
        )

        panel_video.grid_columnconfigure(
            0,
            weight=1
        )


        titulo_video = ctk.CTkLabel(

            panel_video,
            text="📷 Cámara en tiempo real",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )

        )

        titulo_video.pack(
            pady=10
        )


        self.video_label = ctk.CTkLabel(
            panel_video,
            text="Inicializando cámara..."

        )

        self.video_label.pack(
            expand=True,
            fill="both",
            padx=10,
            pady=10
        )

        # ============================
        # PANEL INFORMACIÓN
        # ============================

        panel_info = ctk.CTkFrame(
            self.panel
        )

        panel_info.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(5,10),
            pady=10
        )


        titulo_info = ctk.CTkLabel(

            panel_info,
            text="Información",
            font=ctk.CTkFont(
                size=22,
                weight="bold"
            )

        )

        titulo_info.pack(
            pady=20
        )


        self.lblSenal = self.crear_tarjeta(
            panel_info,
            "SEÑAL DETECTADA",
            "---"
        )


        self.lblConfianza = self.crear_tarjeta(
            panel_info,
            "CONFIANZA",
            "---"
        )


        self.lblHora = self.crear_tarjeta(
            panel_info,
            "HORA",
            "---"
        )


        self.lblTotal = self.crear_tarjeta(
            panel_info,
            "TOTAL DETECCIONES",
            "0"
        )


        self.lblEstadoDeteccion = self.crear_tarjeta(
            panel_info,
            "ESTADO",
            "Activo"
        )


        boton_atras = ctk.CTkButton(

            panel_info,
            text="⬅ Volver",
            height=40,
            command=self.mostrar_inicio

        )

        boton_atras.pack(
            side="bottom",
            pady=20,
            padx=20,
            fill="x"
        )


        # ============================
        # INICIAR CAMARA
        # ============================

        if self.camera.iniciar():
            self.camara_activa = True
            self.actualizar_video()

        else:

            self.lblEstado.configure(
                text="Error: No se pudo abrir la cámara"
            )
    
    def actualizar_video(self):

        if not self.camara_activa:
            return

        ret, frame = self.camera.leer()

        if not ret:
            self.after(
                10,
                self.actualizar_video
            )
            return

        datos = self.detector.procesar_frame(frame)
        frame = datos["frame"]

        if datos["deteccion"] is not None:
            deteccion = datos["deteccion"]

            self.lblSenal.configure(
                text=deteccion["senal"]
            )

            self.lblConfianza.configure(
                text=f"{deteccion['confianza']*100:.2f}%"
            )

            self.lblHora.configure(
                text=deteccion["hora"]
            )

            if deteccion["senal"] != self.ultima_senal_contada:
                self.total_detecciones += 1
                self.ultima_senal_contada = deteccion["senal"]

            self.lblTotal.configure(
                text=str(self.total_detecciones)
            )

        else:
            self.lblEstadoDeteccion.configure(
                text="Buscando..."
            )

        frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        imagen = Image.fromarray(frame)
        imagen = imagen.convert("RGB")

        ancho = self.video_label.winfo_width()
        alto = self.video_label.winfo_height()

        if ancho > 1 and alto > 1:
            imagen.thumbnail(
                (ancho, alto)
            )

        self.foto = ImageTk.PhotoImage(imagen)

        self.video_label.configure(
            image=self.foto,
            text=""
        )

        if datos["deteccion"] is not None:
            nombre = datos["deteccion"]["senal"]
            confianza = datos["deteccion"]["confianza"]

            self.lblEstado.configure(
                text=f"🟢 Detectado: {nombre} | Confianza: {confianza*100:.1f}%"
            )

        else:
            self.lblEstado.configure(
                text="🟡 Buscando señales..."
            )

        self.after(
            10,
            self.actualizar_video
        )

    def detener_camara(self):
        self.camara_activa = False
        self.camera.detener()

    def abrir_mapa(self):
        self.detener_camara()
        self.limpiar_panel()

        titulo = ctk.CTkLabel(
            self.panel,
            text="🗺 Mapa de detecciones",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        )

        titulo.pack(
            pady=20
        )

        try:
            ruta = generar_mapa()
            ruta_navegador = (
                "file:///"
                + ruta.replace("\\", "/")
            )

            frame_info = ctk.CTkLabel(
                self.panel,
                text="Cargando mapa..."
            )

            frame_info.pack(
                pady=20
            )


            webview.create_window(
                "Mapa de detecciones",
                ruta_navegador,
                width=1000,
                height=650

            )

            webview.start(
                gui="tkinter"
            )
        except Exception as e:
            error = ctk.CTkLabel(
                self.panel,
                text=f"Error cargando mapa:\n{e}"

            )
            error.pack(
                pady=50
            )

    def cerrar_programa(self):
        self.detener_camara()
        self.destroy()

    def crear_tarjeta(self, padre, titulo, texto):

        tarjeta = ctk.CTkFrame(
            padre,
            corner_radius=15
        )

        tarjeta.pack(
            padx=15,
            pady=8,
            fill="x"
        )


        lbl_titulo = ctk.CTkLabel(
            tarjeta,
            text=titulo,
            font=self.FONT_SMALL
        )

        lbl_titulo.pack(
            pady=(10,0)
        )

        lbl_valor = ctk.CTkLabel(
            tarjeta,
            text=texto,
            font=self.FONT_HEADER
        )

        lbl_valor.pack(
            pady=(0,10)
        )

        return lbl_valor