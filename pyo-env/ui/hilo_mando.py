# ui/hilo_mando.py
from PyQt6.QtCore import QThread, pyqtSignal
import pygame
import time

class HiloMando(QThread):
    actualizacion_estado = pyqtSignal(dict)

    def __init__(self, mando, sintetizador):
        super().__init__()
        self.mando = mando
        self.sint = sintetizador
        self.running = True
        self.joy_left = False
        self.joy_right = False
        self.sonido_boton_activo = True

    def run(self):
        while self.running:
            for event in self.mando.get_eventos():
                if event.type == pygame.QUIT:
                    self.running = False
                    return

            # Notas (solo si están activas)
            if self.sonido_boton_activo:
                from config import note_map
                nota = None
                for btn, offset in note_map.items():
                    if self.mando.boton_presionado(btn):
                        nota = offset
                        break

                if nota is not None:
                    self.sint.set_freq(nota)
                else:
                    self.sint.clear_note_offset()

            # Efectos toggle
            for boton, efecto in [(6, "delay"), (7, "chorus"), (4, "phaser")]:
                if self.mando.boton_presionado(boton):
                    estado = self.sint.toggle_effect(efecto)
                    print(f"{efecto.title()} {'activado' if estado else 'desactivado'}")
                    time.sleep(0.3)

            # Cambio de onda
            if self.mando.boton_presionado(5):
                nueva = self.sint.change_waveform()
                print(f"Onda cambiada")
                time.sleep(0.3)

            # Reverb
            val = (self.mando.get_axis(4) + 1) / 2
            self.sint.set_reverb_mix(val)

            # Octava
            hat = self.mando.get_hat()
            if hat[1] == 1:
                self.sint.set_octave(1)
                time.sleep(0.2)
            elif hat[1] == -1:
                self.sint.set_octave(-1)
                time.sleep(0.2)
            elif hat[1] == 0 and hat[0] == 0:
                pass

            # 🔇 Cruceta ↓ silencia notas
            if hat[1] == -1:
                self.sonido_boton_activo = False
                self.sint.clear_note_offset()
            else:
                self.sonido_boton_activo = True

            # L3
            if self.mando.boton_presionado(8):
                self.joy_left = not self.joy_left
                print(f"Joystick izquierdo {'activado' if self.joy_left else 'desactivado'}")
                time.sleep(0.3)

            # R3
            if self.mando.boton_presionado(9):
                self.joy_right = not self.joy_right
                print(f"Joystick derecho {'activado' if self.joy_right else 'desactivado'}")
                time.sleep(0.3)

            # Joysticks → control dual
            if self.joy_left:
                lx = self.mando.get_axis(0)
                ly = self.mando.get_axis(1)
                self.sint.set_left_joystick(lx, ly)
            if self.joy_right:
                rx = self.mando.get_axis(2)
                ry = self.mando.get_axis(3)
                self.sint.set_right_joystick(rx, ry)

            # Emitir estado para futura UI reactiva
            self.actualizacion_estado.emit({
                "joy_left": self.joy_left,
                "joy_right": self.joy_right,
                "reverb": val
            })

            time.sleep(0.05)

    def detener(self):
        self.running = False
 