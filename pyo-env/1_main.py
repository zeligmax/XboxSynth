# 1_main.py modificado
from controlador import MandoXbox
from sonido import SintetizadorHibrido as Sintetizador
from config import note_map, hat_map, tables
from ui.interfaz import InterfazSintetizador
from PyQt6.QtWidgets import QApplication
import pygame
import time
import numpy as np
import sys

sint = Sintetizador()
mando = MandoXbox()

print("Controles:")
print("- Botones A, B, X, Y → SI, LA, FA, SOL")
print("- Cruceta izquierda/arriba/derecha → DO, RE, MI")
print("- RB → Cambiar forma de onda")
print("- Gatillo izquierdo → Reverb (mezcla)")
print("- Stick izquierdo X → Phaser freq / Y → Chorus depth")
print("- Stick derecho X → Reverb mix / Y → Delay feedback")
print("- L3 → Octava abajo")
print("- R3 → Octava arriba")
print("- Cruceta abajo → Apagar sonido")

try:
    while True:
        for event in mando.get_eventos():
            if event.type == pygame.QUIT:
                raise KeyboardInterrupt

        # Leer D-Pad (cruceta)
        hat = mando.get_hat()

        # Apagar sonido con cruceta abajo
        if hat == (0, -1):
            sint.silence()
            print("Notas de botones apagadas")
            time.sleep(0.3)

        # Detectar nota desde botones o D-Pad
        nota = None

        # Desde botones (A, B, X, Y)
        for btn, offset in note_map.items():
            if mando.boton_presionado(btn):
                nota = offset
                break

        # Desde D-Pad (izquierda, arriba, derecha)
        if nota is None and hat in hat_map:
            nota = hat_map[hat]

        # Activar nota si se detectó
        if nota is not None:
            sint.set_freq(nota)
        else:
            sint.clear_note_offset()

        # Cambio de onda con RB (botón 5)
        if mando.boton_presionado(5):
            nueva = sint.change_waveform()
            print(f"Onda cambiada a: {tables[nueva]}")
            time.sleep(0.3)

        # Reverb mezcla con gatillo izquierdo (eje 4)
        reverb_val = (mando.get_axis(4) + 1) / 2
        sint.set_reverb_mix(reverb_val)

        # Octava ↓ (L3 - botón 8)
        if mando.boton_presionado(8):
            octv = sint.set_octave(-1)
            print(f"Octava abajo: {octv}")
            time.sleep(0.3)

        # Octava ↑ (R3 - botón 9)
        if mando.boton_presionado(9):
            octv = sint.set_octave(1)
            print(f"Octava arriba: {octv}")
            time.sleep(0.3)

        # Joysticks → efectos dinámicos SOLO si hay nota activa
        if sint.sint.note_offset is not None:
            lx = mando.get_axis(0)
            ly = mando.get_axis(1)
            rx = mando.get_axis(2)
            ry = mando.get_axis(3)

            sint.set_phaser_freq((lx + 1) / 2)         # joystick izq X
            sint.set_chorus_depth((ly + 1) / 2)        # joystick izq Y
            sint.set_reverb_mix((rx + 1) / 2)          # joystick der X
            sint.sint.delay.feedback = (ry + 1) / 2    # joystick der Y

        # Toggle efectos (opcional, siguen activos)
        if mando.boton_presionado(6):
            estado = sint.toggle_effect("delay")
            print(f"Delay {'activado' if estado else 'desactivado'}")
            time.sleep(0.3)

        if mando.boton_presionado(7):
            estado = sint.toggle_effect("chorus")
            print(f"Chorus {'activado' if estado else 'desactivado'}")
            time.sleep(0.3)

        if mando.boton_presionado(4):
            estado = sint.toggle_effect("phaser")
            print(f"Phaser {'activado' if estado else 'desactivado'}")
            time.sleep(0.3)

        pygame.time.wait(50)

except KeyboardInterrupt:
    print("Cerrando...")
    mando.close()
    sint.sint.server.stop()

# Visualizador (audio snapshot)
def get_audio_snapshot():
    return sint.sint.osc.getTable().getTable() if sint.sint.osc is not None else np.zeros(512)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = InterfazSintetizador(get_audio_snapshot)
    ventana.show()
    sys.exit(app.exec())

