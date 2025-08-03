# controlador.py
import pygame

class MandoXbox:
    def __init__(self):
        pygame.init()
        pygame.joystick.init()
        if pygame.joystick.get_count() == 0:
            raise Exception("No hay joystick conectado")
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()
        print(f"Mando detectado: {self.joystick.get_name()}")

    def get_eventos(self):
        return pygame.event.get()

    def boton_presionado(self, index):
        return self.joystick.get_button(index)

    def get_hat(self):
        return self.joystick.get_hat(0)

    def get_axis(self, axis_index):
        return self.joystick.get_axis(axis_index)

    def close(self):
        pygame.quit()
