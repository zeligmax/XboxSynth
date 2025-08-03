# ui/interfaz.py
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QLabel, QHBoxLayout, QVBoxLayout
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

from ui.leyenda import crear_leyenda
from ui.visualizador import VisualizadorOnda
from ui.hilo_mando import HiloMando

from controlador import MandoXbox
from sonido import SintetizadorHibrido


class InterfazSintetizador(QMainWindow):
    def __init__(self, get_audio_callback):
        super().__init__()
        self.setWindowTitle("Sintetizador Xbox")
        self.setMinimumSize(1200, 600)

        # 🎛 Inicializa sintetizador y mando
        self.sint = SintetizadorHibrido()
        self.mando = MandoXbox()

        # 🧵 Inicia hilo para leer el mando
        self.hilo_mando = HiloMando(self.mando, self.sint)
        self.hilo_mando.actualizacion_estado.connect(self.actualizar_estado_ui)
        self.hilo_mando.start()

        # 🖼️ Configuración de UI
        widget_central = QWidget()
        self.setCentralWidget(widget_central)

        layout = QHBoxLayout()
        widget_central.setLayout(layout)

        # 🎮 Imagen del mando
        mando = QLabel()
        mando.setPixmap(QPixmap("ui/mando_xbox.png").scaledToWidth(350, Qt.TransformationMode.SmoothTransformation))
        layout.addWidget(mando)

        # 📄 Leyenda
        leyenda = crear_leyenda()
        leyenda.setMaximumWidth(400)
        layout.addWidget(leyenda)

        # 📈 Visualizador de onda
        visual = VisualizadorOnda(get_audio_callback)
        layout.addWidget(visual)

    def actualizar_estado_ui(self, estado):
        # Aquí podrías usar `estado` para actualizar elementos de la UI
        # Por ejemplo, mostrar si L3/R3 están activos
        # print("Estado recibido:", estado)
        pass

    def closeEvent(self, event):
        self.hilo_mando.detener()
        self.hilo_mando.wait()
        self.sint.sint.server.stop()
        event.accept()
