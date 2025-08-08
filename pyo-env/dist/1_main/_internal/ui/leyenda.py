# ui/leyenda.py
from PyQt6.QtWidgets import QTextEdit

def crear_leyenda():
    leyenda = QTextEdit()
    leyenda.setReadOnly(True)
    leyenda.setHtml("""
    <h2>Controles</h2>
    <ul>
    <li><b>A, B, X, Y:</b> Notas musicales</li>
    <li><b>RB:</b> Cambia la forma de onda</li>
    <li><b>LT:</b> Controla la reverb</li>
    <li><b>Stick Izquierdo:</b> Oscilador 1 (freq / vol)</li>
    <li><b>Stick Derecho:</b> Oscilador 2 (freq / vol)</li>
    <li><b>D-Pad:</b> Octava ↑↓</li>
    <li><b>L3 / R3:</b> Encender/Apagar joystick synth</li>
    <li><b>Back / Start / LB:</b> Efectos: delay, chorus, phaser</li>
    <li><b>D-Pad ↓:</b> Silenciar notas</li>
    </ul>
    """)
    return leyenda
