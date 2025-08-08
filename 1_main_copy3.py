import sys
import time
import numpy as np
import pygame
import os
import csv
from datetime import datetime
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

from controlador import MandoXbox
from sonido import SintetizadorHibrido as Sintetizador
from config import note_map, hat_map, tables
from ui.interfaz import InterfazSintetizador

from pyo import Record, Sine, Noise, ButLP, Fader, SfPlayer, Linseg

def potencia_ajustada(val, potencia=2.5):
    return min(1.0, max(0.0, val ** potencia))

class Controlador:
    def __init__(self):
        self.sint = Sintetizador()
        self.mando = MandoXbox()

        self.app = QApplication(sys.argv)
        self.ventana = InterfazSintetizador(self.get_audio_snapshot)
        self.ventana.toggle_recording.connect(self.toggle_grabacion)
        self.ventana.show()

        self.octava_offset = 0
        self.nota_actual = "--"
        self.grabando = False
        self.recorder = None

        self.setup_logger()
        self.timer = QTimer()
        self.timer.timeout.connect(self.loop)
        self.timer.start(50)

    def setup_logger(self):
        os.makedirs("logs", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_path = f"logs/control_log_{timestamp}.csv"
        self.log_file = open(self.log_path, mode="w", newline="")
        self.logger = csv.writer(self.log_file)
        self.logger.writerow([
            "timestamp", "nota", "lx", "ly", "rx", "ry", "lt", "rt",
            "delay_feedback", "chorus_depth", "reverb_mix"
        ])

    def toggle_grabacion(self):
        self.grabando = not self.grabando
        if self.grabando:
            os.makedirs("logs/audio", exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre = f"logs/audio/grabacion_{timestamp}.wav"
            self.recorder = Record(self.sint.salida, filename=nombre, fileformat=0, sampletype=1)
            self.recorder.play()
            print(f"[GRABACIÓN INICIADA]: {nombre}")
        else:
            if self.recorder is not None:
                self.recorder.stop()
                self.recorder = None
                print("[GRABACIÓN FINALIZADA]")

    def escribir_log(self, nota, lx, ly, rx, ry, lt, rt, delay, chorus, reverb):
        timestamp = time.time()
        self.logger.writerow([
            timestamp, nota, lx, ly, rx, ry, lt, rt,
            delay, chorus, reverb
        ])
        self.log_file.flush()

    def get_audio_snapshot(self):
        return np.zeros(512)

    def sonido_laser(self):
        print("[FX] Piu-piu (láser)")

        freq_inicial = np.random.uniform(800, 1200)
        freq_final = np.random.uniform(200, 400)
        duracion = 0.3

        env = Fader(fadein=0.01, fadeout=duracion - 0.01, dur=duracion, mul=1).play()

        curva_freq = Linseg(
            list=[(0, freq_inicial), (duracion, freq_final)]
        ).play()

        self.laser_sine = Sine(freq=curva_freq, mul=env).out()

    def sonido_szoom(self):
        print("[FX] Szoom (láser grave y largo)")

        freq_inicial = np.random.uniform(250, 450)
        freq_final = np.random.uniform(70, 140)
        duracion = 5

        env = Fader(fadein=0.01, fadeout=duracion - 0.01, dur=duracion, mul=2).play()

        curva_freq = Linseg(
            list=[(0, freq_inicial), (duracion, freq_final)]
        ).play()

        self.laser_sine = Sine(freq=curva_freq, mul=env).out()

    def loop(self):
        for event in self.mando.get_eventos():
            if event.type == pygame.QUIT:
                self.salir()

        hat = self.mando.get_hat()
        if hat == (0, -1):
            self.sint.silence()
            time.sleep(0.3)

        nota = None
        for btn, offset in note_map.items():
            if self.mando.boton_presionado(btn):
                nota = offset
                break

        if nota is None and hat in hat_map:
            nota = hat_map[hat]

        if nota is not None:
            self.sint.set_freq(nota + self.octava_offset)
            self.nota_actual = f"{nota + self.octava_offset}"
        else:
            self.sint.clear_note_offset()
            self.nota_actual = "--"

        self.ventana.update_note.emit(self.nota_actual)

        if self.mando.boton_presionado(5):
            nueva = self.sint.change_waveform()
            print(f"Onda cambiada a: {tables[nueva]}")
            time.sleep(0.3)

        lx = self.mando.get_axis(0)
        ly = self.mando.get_axis(1)
        rx = self.mando.get_axis(2)
        ry = self.mando.get_axis(3)
        lt_val = (self.mando.get_axis(4) + 1) / 2
        rt_val = (self.mando.get_axis(5) + 1) / 2

        # LT -> szoom grave
        if lt_val > 0.8:
            self.sonido_szoom()

        # RT -> piu-piu agudo
        if rt_val > 0.8:
            self.sonido_laser()

        if abs(lx) > 0.2 or abs(ly) > 0.2:
            angle = (np.arctan2(-ly, lx) + np.pi) % (2 * np.pi)
            sector = int((angle / (2 * np.pi)) * 5)
            pentatonica = [0, 2, 4, 7, 9]
            nota_penta = pentatonica[sector % 5]
            self.sint.set_freq(nota_penta + self.octava_offset)
            self.ventana.update_note.emit(f"{nota_penta + self.octava_offset}")
            self.nota_actual = f"{nota_penta + self.octava_offset}"

        reverb_val = (rx + 1) / 2
        delay_val = potencia_ajustada((ry + 1) / 2)
        chorus_depth = 0.1 + potencia_ajustada(rt_val) * 1.9

        self.sint.set_reverb_mix(reverb_val)
        self.sint.sint.delay.feedback = delay_val
        self.sint.sint.chorus.depth = chorus_depth

        self.ventana.update_reverb.emit(reverb_val)
        self.ventana.update_delay.emit(delay_val)
        self.ventana.update_chorus_depth.emit(potencia_ajustada(rt_val))

        if self.mando.boton_presionado(0) and rt_val > 0.5:
            bend = (rt_val - 0.5) * 2
            self.sint.pitch_bend(bend)
        else:
            self.sint.pitch_bend(0)

        if self.mando.boton_presionado(8):
            self.octava_offset = self.sint.set_octave(-1)
            print(f"Octava abajo: {self.octava_offset}")
            time.sleep(0.3)

        if self.mando.boton_presionado(9):
            self.octava_offset = self.sint.set_octave(1)
            print(f"Octava arriba: {self.octava_offset}")
            time.sleep(0.3)

        if self.mando.boton_presionado(4):
            estado = self.sint.toggle_effect("phaser")
            print(f"Phaser {'activado' if estado else 'desactivado'}")
            time.sleep(0.3)

        self.escribir_log(
            self.nota_actual,
            round(lx, 3), round(ly, 3),
            round(rx, 3), round(ry, 3),
            round(lt_val, 3), round(rt_val, 3),
            round(delay_val, 3),
            round(chorus_depth, 3),
            round(reverb_val, 3)
        )

    def salir(self):
        print("Cerrando...")
        if self.recorder:
            self.recorder.stop()
        self.log_file.close()
        self.mando.close()
        self.sint.sint.server.stop()
        self.app.quit()

if __name__ == "__main__":
    controlador = Controlador()
    sys.exit(controlador.app.exec())

