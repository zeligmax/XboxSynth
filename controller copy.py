import pygame
import time

# Inicialización
pygame.init()
pygame.joystick.init()

# Conectar al primer joystick detectado
if pygame.joystick.get_count() == 0:
    print("No se detectó ningún mando.")
    exit()

joystick = pygame.joystick.Joystick(0)
joystick.init()
print(f"Mando detectado: {joystick.get_name()}")

# Bucle principal
try:
    while True:
        pygame.event.pump()  # Actualiza el estado de los controles

        # Botones digitales
        for i in range(joystick.get_numbuttons()):
            if joystick.get_button(i):
                print(f"Botón {i} PRESIONADO")

        # Joystick Izquierdo y Derecho
        eje_x_izq = joystick.get_axis(0)
        eje_y_izq = joystick.get_axis(1)
        eje_x_der = joystick.get_axis(3)
        eje_y_der = joystick.get_axis(4)

        # Triggers (algunos mandos usan ejes separados)
        gatillo_izq = joystick.get_axis(2)
        gatillo_der = joystick.get_axis(5)

        print(f"Joystick Izq: ({eje_x_izq:.2f}, {eje_y_izq:.2f}) | Joystick Der: ({eje_x_der:.2f}, {eje_y_der:.2f})")
        print(f"Trigger Izq: {gatillo_izq:.2f} | Trigger Der: {gatillo_der:.2f}")
        print("-" * 50)

        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nCerrando...")
    pygame.quit()
