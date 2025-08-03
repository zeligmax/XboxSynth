# config.py
tables = ['Saw', 'Square', 'Harm']

note_map = {
    0: 6,  # A → SI
    1: 9,  # B → LA
    2: 5,  # X → FA
    3: 7,  # Y → SOL
}

hat_map = {
    (-1, 0): 0,  # izquierda → DO
    (0, 1): 2,   # arriba → RE
    (1, 0): 4,   # derecha → MI
}

base_freq = 220
