import pygame
from .gif import load_gif_frames, GifAnimator
from .constants import ANCHO, ALTO

class MenuBG:
    def __init__(self, gif_path):
        frames, durations = load_gif_frames(gif_path, size=(ANCHO, ALTO))
        self._anim = GifAnimator(frames, durations)
        self.zoom_factor = 1.0  # Inicializamos el factor de zoom
        self.offset_x = 0  # Para mover el fondo horizontalmente
        self.offset_y = 0  # Para mover el fondo verticalmente
        self.zoom_speed = 0.001  # Velocidad de incremento del zoom
        self.offset_speed = 0.05  # Velocidad de desplazamiento del fondo

    def update(self, dt_ms):
        """Actualiza la animación del fondo y el zoom"""
        self._anim.update(dt_ms)

        # Aplicamos zoom progresivo (se puede ajustar la velocidad)
        self.zoom_factor += self.zoom_speed  # Aumenta el zoom poco a poco
        if self.zoom_factor > 1.5:  # Limitamos el zoom máximo
            self.zoom_factor = 1.5

        # Movemos el fondo (desplazamiento)
        self.offset_x += self.offset_speed
        if self.offset_x > ANCHO * 0.1 or self.offset_x < -ANCHO * 0.1:  # Si el fondo se desplaza mucho, revertimos
            self.offset_speed *= -1

    def draw(self, surface):
        """Dibuja el fondo escalado sobre la superficie con desplazamiento"""
        frame = self._anim.current_frame
        
        # Escalamos el fotograma actual del gif
        scaled_frame = pygame.transform.smoothscale(frame, 
                                                     (int(ANCHO * self.zoom_factor), int(ALTO * self.zoom_factor)))
        
        # Calculamos la posición para centrar la imagen escalada, desplazándola también
        offset_x = (scaled_frame.get_width() - ANCHO) // 2 + int(self.offset_x)
        offset_y = (scaled_frame.get_height() - ALTO) // 2 + int(self.offset_y)

        # Dibujamos el fondo escalado y desplazado
        surface.blit(scaled_frame, (-offset_x, -offset_y))