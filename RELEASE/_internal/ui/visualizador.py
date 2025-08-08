# ui/visualizador.py
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import numpy as np
from PyQt6.QtCore import QTimer

class VisualizadorOnda(PlotWidget):
    def __init__(self, get_audio_callback, parent=None):
        super().__init__(parent)
        self.get_audio = get_audio_callback

        self.setYRange(-1, 1)
        self.setBackground('w')
        self.wave = self.plot(pen=pg.mkPen(color=(0, 0, 255), width=2))

        self.timer = QTimer()
        self.timer.timeout.connect(self.actualizar)
        self.timer.start(30)

    def actualizar(self):
        data = self.get_audio()
        if data is not None:
            self.wave.setData(data)
