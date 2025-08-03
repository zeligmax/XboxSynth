import pygame
from pyo import Server, SawTable, SquareTable, HarmTable, Osc, Freeverb, Delay, Chorus, Phaser, Mix

# Inicialización pygame y joystick
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
octave = 0

def freq_for_note(note_base):
    return base_freq * (2 ** octave) * (2 ** (note_base / 12))

# Oscilador principal
osc = Osc(table=wave_table, freq=0, mul=0.3)

# Efectos sin mezcla directa
reverb = Freeverb(osc, size=0.8, damp=0.5, bal=0).out()

delay = Delay(reverb, delay=0.3, feedback=0.4, mul=0)
chorus = Chorus(delay, depth=1.5, feedback=0.25, mul=0)
phaser = Phaser(chorus, freq=0.5, spread=0.6, q=2, feedback=0.5, mul=0)

# Mezcla final de efectos
final_mix = Mix([reverb, delay, chorus, phaser], voices=2).out()

# Flags para activar/desactivar efectos
effects_enabled = {
    "delay": False,
    "chorus": False,
    "phaser": False
}

print("Controles:")
print("- Botones A, B, X, Y → Tocar notas")
print("- RB → Cambiar forma de onda")
print("- Gatillo izquierdo → Controla reverb (mezcla)")
print("- D-Pad → Cambiar octava")
print("- Back → Toggle Delay | Start → Toggle Chorus | LB → Toggle Phaser")

# Mapa de notas a botones
note_map = {
    0: 0,  # A
    1: 2,  # B
    2: 4,  # X
    3: 5,  # Y
}

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Leer botones de notas
    nota = None
    for btn, note_offset in note_map.items():
        if joystick.get_button(btn):
            nota = note_offset
            break

    if nota is not None:
        freq = freq_for_note(nota)
        osc.freq = freq
        print(f"Tocando nota botón {btn}: freq {freq:.2f} Hz")
    else:
        osc.freq = 0  # silencio

    # Cambiar onda con RB (botón 5)
    if joystick.get_button(5):
        wave_index = (wave_index + 1) % len(tables)
        wave_table = tables[wave_index]
        osc.setTable(wave_table)
        print(f"Cambio onda a: {wave_names[wave_index]}")
        pygame.time.wait(300)  # anti-rebote

    # Gatillo izquierdo controla mezcla de reverb
    gatillo_izq_val = (joystick.get_axis(4) + 1) / 2  # 0 a 1
    reverb.bal = gatillo_izq_val

    # Cambiar octava con D-Pad (hat)
    hat = joystick.get_hat(0)
    if hat[1] == 1:
        octave = min(octave + 1, 3)
        print(f"Octava arriba: {octave}")
        pygame.time.wait(200)
    elif hat[1] == -1:
        octave = max(octave - 1, -3)
        print(f"Octava abajo: {octave}")
        pygame.time.wait(200)

    # Toggle efectos con botones Back (6), Start (7), LB (4)
    if joystick.get_button(6):  # Back toggle Delay
        effects_enabled["delay"] = not effects_enabled["delay"]
        delay.mul = 0.5 if effects_enabled["delay"] else 0
        print(f"Delay {'activado' if effects_enabled['delay'] else 'desactivado'}")
        pygame.time.wait(300)

    if joystick.get_button(7):  # Start toggle Chorus
        effects_enabled["chorus"] = not effects_enabled["chorus"]
        chorus.mul = 0.5 if effects_enabled["chorus"] else 0
        print(f"Chorus {'activado' if effects_enabled['chorus'] else 'desactivado'}")
        pygame.time.wait(300)

    if joystick.get_button(4):  # LB toggle Phaser
        effects_enabled["phaser"] = not effects_enabled["phaser"]
        phaser.mul = 0.5 if effects_enabled["phaser"] else 0
        print(f"Phaser {'activado' if effects_enabled['phaser'] else 'desactivado'}")
        pygame.time.wait(300)

    pygame.time.wait(50)

pygame.quit()
s.stop()
