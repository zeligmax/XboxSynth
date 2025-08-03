# sonido.py
from pyo import Server, SawTable, SquareTable, HarmTable, Osc, Freeverb, Delay, Chorus, Phaser, Mix

# --- SINTETIZADOR CLÁSICO (botones)
class Sintetizador:
    def __init__(self):
        self.server = Server().boot()
        self.server.start()

        self.tables = [SawTable(), SquareTable(), HarmTable()]
        self.wave_index = 0
        self.wave_table = self.tables[self.wave_index]

        self.octave = 0
        self.base_freq = 220
        self.note_offset = None

        self.osc = Osc(table=self.wave_table, freq=0, mul=0.3)

        self.reverb = Freeverb(self.osc, size=0.8, damp=0.5, bal=0).out()
        self.delay = Delay(self.reverb, delay=0.3, feedback=0.4, mul=0)
        self.chorus = Chorus(self.delay, depth=1.5, feedback=0.25, mul=0)
        self.phaser = Phaser(self.chorus, freq=0.5, spread=0.6, q=2, feedback=0.5, mul=0)

        self.final_mix = Mix([self.reverb, self.delay, self.chorus, self.phaser], voices=2).out()
        self.effects_enabled = {
            "delay": False,
            "chorus": False,
            "phaser": False
        }

    def set_freq(self, note_offset):
        self.note_offset = note_offset
        freq = self.base_freq * (2 ** self.octave) * (2 ** (note_offset / 12))
        self.osc.freq = freq

    def silence(self):
        self.osc.freq = 0
        self.note_offset = None

    def change_waveform(self):
        self.wave_index = (self.wave_index + 1) % len(self.tables)
        self.wave_table = self.tables[self.wave_index]
        self.osc.setTable(self.wave_table)
        return self.wave_index

    def toggle_effect(self, effect_name):
        state = not self.effects_enabled[effect_name]
        self.effects_enabled[effect_name] = state
        getattr(self, effect_name).mul = 0.5 if state else 0
        return state

    def set_octave(self, change):
        self.octave = max(-3, min(3, self.octave + change))
        return self.octave

    def set_reverb_mix(self, value):  # value entre 0 y 1
        self.reverb.bal = value

    def set_phaser_freq(self, value):  # joystick derecho eje X
        self.phaser.freq = 0.1 + 5 * value

    def set_chorus_depth(self, value):  # joystick derecho eje Y
        self.chorus.depth = 0.1 + 1.9 * value

    def clear_note_offset(self):
        self.note_offset = None


# --- SINTETIZADOR DUAL (joysticks)
class SintetizadorDual:
    def __init__(self):
        self.left_table = SawTable()
        self.right_table = SquareTable()

        self.osc_left = Osc(table=self.left_table, freq=0, mul=0.3)
        self.osc_right = Osc(table=self.right_table, freq=0, mul=0.3)

        self.mix = Mix([self.osc_left, self.osc_right], voices=2).out()

        self.note_offset = None
        self.base_freq = 220
        self.octave = 0

    def set_left_joystick(self, x, y):
        freq = self.base_freq * (2 ** self.octave) + (x + 1) * 110
        vol = (1 - y) / 2
        self.osc_left.freq = freq
        self.osc_left.mul = vol

    def set_right_joystick(self, x, y):
        freq = self.base_freq * (2 ** self.octave) + (x + 1) * 220
        vol = (1 - y) / 2
        self.osc_right.freq = freq
        self.osc_right.mul = vol

    def set_octave(self, change):
        self.octave = max(-3, min(3, self.octave + change))
        return self.octave

    def silence(self):
        self.osc_left.freq = 0
        self.osc_right.freq = 0

    def clear_note_offset(self):
        self.note_offset = None


# --- SINTETIZADOR HÍBRIDO (combinación de ambos)
class SintetizadorHibrido:
    def __init__(self):
        self.sint = Sintetizador()
        self.dual = SintetizadorDual()
        self.left_joystick_enabled = True
        self.right_joystick_enabled = True

    def set_freq(self, note_offset):
        self.sint.set_freq(note_offset)

    def silence(self):
        self.sint.silence()
        self.dual.silence()

    def change_waveform(self):
        return self.sint.change_waveform()

    def toggle_effect(self, effect_name):
        return self.sint.toggle_effect(effect_name)

    def set_octave(self, change):
        octv1 = self.sint.set_octave(change)
        octv2 = self.dual.set_octave(change)
        return octv1

    def set_reverb_mix(self, value):
        self.sint.set_reverb_mix(value)

    def set_phaser_freq(self, value):
        self.sint.set_phaser_freq(value)

    def set_chorus_depth(self, value):
        self.sint.set_chorus_depth(value)

    def clear_note_offset(self):
        self.sint.clear_note_offset()

    def set_left_joystick(self, x, y):
        if self.left_joystick_enabled:
            self.dual.osc_left.freq = self.dual.base_freq * (2 ** self.dual.octave) + (x + 1) * 110
            self.dual.osc_left.mul = (1 - y) / 2
        else:
            self.dual.osc_left.freq = 0
            self.dual.osc_left.mul = 0

    def set_right_joystick(self, x, y):
        if self.right_joystick_enabled:
            self.dual.osc_right.freq = self.dual.base_freq * (2 ** self.dual.octave) + (x + 1) * 220
            self.dual.osc_right.mul = (1 - y) / 2
        else:
            self.dual.osc_right.freq = 0
            self.dual.osc_right.mul = 0

    def toggle_left_joystick(self):
        self.left_joystick_enabled = not self.left_joystick_enabled
        if not self.left_joystick_enabled:
            self.dual.osc_left.freq = 0
            self.dual.osc_left.mul = 0
        return self.left_joystick_enabled

    def toggle_right_joystick(self):
        self.right_joystick_enabled = not self.right_joystick_enabled
        if not self.right_joystick_enabled:
            self.dual.osc_right.freq = 0
            self.dual.osc_right.mul = 0
        return self.right_joystick_enabled
