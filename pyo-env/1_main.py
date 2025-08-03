# main.py
from controlador import MandoXbox
from sonido import SintetizadorHibrido as Sintetizador
from config import note_map, tables
from ui.interfaz import InterfazSintetizador
from PyQt6.QtWidgets import QApplication
import pygame
import time
import numpy as np
import sys

sint = Sintetizador()
mando = MandoXbox()

print("Controles:")
print("- Botones A, B, X, Y → Tocar notas")
print("- RB → Cambiar forma de onda")
print("- Gatillo izquierdo → Controla reverb")
print("- Stick izquierdo → Oscilador 1 (freq/vol)")
print("- Stick derecho → Oscilador 2 (freq/vol)")
print("- D-Pad → Octava")
print("- Back / Start / LB → Toggle efectos")
print("- L3 / R3 → Activar/Desactivar joystick synth izquierdo/derecho")
print("- Cruceta abajo → Apagar notas de botones")

try:
    while True:
        for event in mando.get_eventos():
            if event.type == pygame.QUIT:
                raise KeyboardInterrupt

        # Cruceta abajo apaga las notas de botones
        hat = mando.get_hat()
        if hat[1] == -1:
            sint.silence()
            print("Notas de botones apagadas")
            time.sleep(0.3)

        # Leer botones para notas
        nota = None
        for btn, offset in note_map.items():
            if mando.boton_presionado(btn):
                nota = offset
                break

        if nota is not None:
            sint.set_freq(nota)
        else:
            sint.clear_note_offset()

        # Cambio de onda (RB)
        if mando.boton_presionado(5):
            nueva = sint.change_waveform()
            print(f"Onda cambiada a: {tables[nueva]}")
            time.sleep(0.3)

        # Gatillo izquierdo → mezcla de reverb
        reverb_val = (mando.get_axis(4) + 1) / 2
        sint.set_reverb_mix(reverb_val)

        # Toggle joystick synth con L3 (botón 8)
        if mando.boton_presionado(8):
            estado = sint.toggle_left_joystick()
            print(f"Joystick izquierdo {'activado' if estado else 'desactivado'}")
            time.sleep(0.3)

        # Toggle joystick synth con R3 (botón 9)
        if mando.boton_presionado(9):
            estado = sint.toggle_right_joystick()
            print(f"Joystick derecho {'activado' if estado else 'desactivado'}")
            time.sleep(0.3)

        # Controlar joysticks solo si están activados
        if sint.left_joystick_enabled:
            lx = mando.get_axis(0)
            ly = mando.get_axis(1)
            sint.set_left_joystick(lx, ly)
        else:
            sint.set_left_joystick(0, 0)  # Silenciar por si acaso

        if sint.right_joystick_enabled:
            rx = mando.get_axis(2)
            ry = mando.get_axis(3)
            sint.set_right_joystick(rx, ry)
        else:
            sint.set_right_joystick(0, 0)  # Silenciar por si acaso

        # D-Pad (hat) → octava (arriba/abajo)
        if hat[1] == 1:
            octv = sint.set_octave(1)
            print(f"Octava arriba: {octv}")
            time.sleep(0.2)
        # Nota: la opción de abajo ya se usa para apagar notas, por eso no hacemos octava abajo aquí.

        # Efectos toggle
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

# Función para obtener una instantánea del audio
# (para el visualizador)
def get_audio_snapshot():
    return sint.sint.osc.getTable().getTable() if sint.sint.osc is not None else np.zeros(512)

if __name__ == "__main__":
    # Lanzar interfaz gráfica
    app = QApplication(sys.argv)
    ventana = InterfazSintetizador(get_audio_snapshot)
    ventana.show()

    # Arranca el bucle de UI
    sys.exit(app.exec())
