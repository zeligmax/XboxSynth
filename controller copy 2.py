import pygame
from pyo import Server, SawTable, SquareTable, HarmTable, Osc, Freeverb

# Inicialización
pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("No joystick conectado")
    exit()

joystick = pygame.joystick.Joystick(0)
joystick.init()
print(f"Mando detectado: {joystick.get_name()}")

# Setup pyo
s = Server().boot()
s.start()

# Tablas de ondas
tables = [SawTable(), SquareTable(), HarmTable()]
wave_names = ['Saw', 'Square', 'Harm']
wave_index = 0
wave_table = tables[wave_index]

# Nota base
base_freq = 220

# Oscilador
osc = Osc(table=wave_table, freq=base_freq, mul=0.3)

# Efecto reverb (Freeverb) controlado por el gatillo izquierdo
reverb = Freeverb(osc, size=0.8, damp=0.5, bal=0.0).out()

print("Sintetizador listo. Usa botones A,B,X,Y para notas, RB para cambiar onda, gatillo izquierdo para reverb, D-Pad para octava.")

octave = 0

def freq_for_note(note_base):
    return base_freq * (2 ** octave) * (2 ** (note_base / 12))

# Nota asignación botones (A,B,X,Y)
note_map = {
    0: 0,   # A - nota base
    1: 2,   # B - Re
    2: 4,   # X - Mi
    3: 5,   # Y - Fa
}

# Loop principal
running = True
while running:
    pygame.event.pump()

    # Leer gatillos
    gatillo_izq_val = (joystick.get_axis(4) + 1) / 2  # de 0 a 1

    # Controlar reverb: balance (0 = seco, 1 = húmedo)
    reverb.bal = gatillo_izq_val

    # Leer botón RB para cambiar onda
    rb_pressed = joystick.get_button(5)
    if rb_pressed:
        wave_index = (wave_index + 1) % len(tables)
        wave_table = tables[wave_index]
        osc.setTable(wave_table)
        print(f"Cambio onda a: {wave_names[wave_index]}")
        pygame.time.wait(200)

    # Leer botones A,B,X,Y para notas
    nota = None
    for btn, note_offset in note_map.items():
        if joystick.get_button(btn):
            nota = note_offset
            break

    if nota is not None:
        osc.freq = freq_for_note(nota)
    else:
        osc.freq = 0  # silencio

    # Leer D-Pad para octava
    hat = joystick.get_hat(0)
    if hat[1] == 1:
        octave = min(octave + 1, 3)
        print(f"Octava arriba: {octave}")
        pygame.time.wait(200)
    elif hat[1] == -1:
        octave = max(octave - 1, -3)
        print(f"Octava abajo: {octave}")
        pygame.time.wait(200)

    print(f"Reverb level (gatillo izquierdo): {gatillo_izq_val:.2f}")

pygame.quit()
