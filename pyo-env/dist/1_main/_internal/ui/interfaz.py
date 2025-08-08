from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QProgressBar, QPushButton
from PyQt6.QtCore import pyqtSignal, Qt, QTimer
import numpy as np

class InterfazSintetizador(QWidget):
    update_reverb = pyqtSignal(float)
    update_delay = pyqtSignal(float)
    update_chorus_depth = pyqtSignal(float)
    update_note = pyqtSignal(str)
    toggle_recording = pyqtSignal(bool)  # ✅ Señal necesaria

    def __init__(self, get_audio_snapshot_callback):
        super().__init__()
        self.setWindowTitle("XboxSynth - Controlador en tiempo real")
        self.resize(400, 300)

        self.get_audio_snapshot = get_audio_snapshot_callback

        layout = QVBoxLayout()

        # Nota actual
        self.label_nota = QLabel("Nota: --")
        self.label_nota.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_nota.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(self.label_nota)

        # Barras de efectos
        self.progress_reverb = QProgressBar()
        self.progress_reverb.setRange(0, 100)
        self.progress_reverb.setFormat("Reverb Mix: %p%")
        layout.addWidget(self.progress_reverb)

        self.progress_delay = QProgressBar()
        self.progress_delay.setRange(0, 100)
        self.progress_delay.setFormat("Delay Feedback: %p%")
        layout.addWidget(self.progress_delay)

        self.progress_chorus = QProgressBar()
        self.progress_chorus.setRange(0, 100)
        self.progress_chorus.setFormat("Chorus Depth: %p%")
        layout.addWidget(self.progress_chorus)

        # Visualizador de audio
        self.label_audio_snapshot = QLabel("Audio Snapshot: --")
        self.label_audio_snapshot.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label_audio_snapshot)

        # ✅ Botón de grabación
        self.boton_grabar = QPushButton("Start Recording")
        self.boton_grabar.setCheckable(True)
        self.boton_grabar.clicked.connect(self.on_toggle_recording)
        layout.addWidget(self.boton_grabar)

        self.setLayout(layout)

        # Conexiones
        self.update_reverb.connect(self.on_update_reverb)
        self.update_delay.connect(self.on_update_delay)
        self.update_chorus_depth.connect(self.on_update_chorus)
        self.update_note.connect(self.on_update_note)

        # Timer visualización de audio
        self.timer = QTimer()
        self.timer.timeout.connect(self.refrescar_audio_snapshot)
        self.timer.start(200)

    def on_update_reverb(self, valor):
        self.progress_reverb.setValue(int(valor * 100))

    def on_update_delay(self, valor):
        self.progress_delay.setValue(int(valor * 100))

    def on_update_chorus(self, valor):
        self.progress_chorus.setValue(int(valor * 100))

    def on_update_note(self, texto):
        self.label_nota.setText(f"Nota: {texto}")

    def refrescar_audio_snapshot(self):
        snapshot = self.get_audio_snapshot()
        if snapshot is not None and len(snapshot) > 0:
            nivel = int(np.abs(snapshot).mean() * 1000)
            self.label_audio_snapshot.setText(f"Audio Snapshot (nivel): {nivel}")
        else:
            self.label_audio_snapshot.setText("Audio Snapshot: --")

    def on_toggle_recording(self, checked):
        if checked:
            self.boton_grabar.setText("Stop Recording")
            self.toggle_recording.emit(True)
        else:
            self.boton_grabar.setText("Start Recording")
            self.toggle_recording.emit(False)
