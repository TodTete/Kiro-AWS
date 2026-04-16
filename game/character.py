import pygame
from . import assets as Assets
from .constants import ANCHO, ALTO, SHIP_ORDER, SHIP_DISPLAY, MENU_CHARACTER, BLANCO, AMARILLO, AZUL, MORADO
from .gif import load_gif_frames, GifAnimator


class CharacterSelect:
    def __init__(self):
        self.selected_ship = "BRAYAN"
        self.ship_index = 0
        self.spacing = 180

        # Cargar animadores (GIFs animados incluidos)
        self._animators = {
            key: GifAnimator(*load_gif_frames(path, size=(100, 100)))
            for key, path in [
                ("BRAYAN",   "assets/extra/nave.gif"),
                ("FERNANDA", "assets/extra/nave-f.jpg"),
                ("MARLIN",   "assets/extra/nave-m.gif"),
                ("TETE",     "assets/extra/nave-t.gif"),
            ]
        }

        # aplicar por defecto
        self.apply_selected_skin()

    def apply_selected_skin(self):
        Assets.set_player_skin(self.selected_ship)

    def handle_input(self, evento):
        if evento.key in (pygame.K_LEFT, pygame.K_a):
            self.ship_index = (self.ship_index - 1) % len(SHIP_ORDER)
        if evento.key in (pygame.K_RIGHT, pygame.K_d):
            self.ship_index = (self.ship_index + 1) % len(SHIP_ORDER)
        if evento.key in (pygame.K_RETURN, pygame.K_SPACE):
            self.selected_ship = SHIP_ORDER[self.ship_index]
            return "APPLY"
        return None

    def update(self, dt_ms: int):
        """
        Avanza la animación de todos los GIFs limitado a 30 FPS.
        Ej: character_select.update(clock.get_time())
        """
        for anim in self._animators.values():
            anim.update(dt_ms)

    def draw(self, surface, fuente_titulo, fuente):
        from .utils import dibujar_texto

        # Título
        dibujar_texto(surface, "SELECCIONA PERSONAJE", fuente_titulo, MORADO, ANCHO//2, 80, centrado=True)

        # Carrusel (SIN cuadros grises)
        cx = ANCHO//2; cy = ALTO//2 + 10
        spacing = self.spacing

        for idx, key in enumerate(SHIP_ORDER):
            px = cx + (idx - self.ship_index) * spacing

            # Dibujar solo el sprite animado centrado (sin rectángulos de fondo/borde)
            frame = self._animators[key].current_frame
            fr = frame.get_rect(center=(px, cy - 10))
            surface.blit(frame, fr)

            # Etiqueta
            label = SHIP_DISPLAY[key]
            dibujar_texto(surface, label, fuente,
                          AMARILLO if idx == self.ship_index else BLANCO,
                          px, cy + 90, centrado=True)

            # Opcional: un pequeño indicador bajo la nave seleccionada (no un cuadro)
            if idx == self.ship_index:
                pygame.draw.circle(surface, AMARILLO, (px, cy + 70), 4)

        # Instrucciones
        dibujar_texto(surface, "←/→ para cambiar  |  ENTER para seleccionar  |  ESC volver",
                      fuente, AZUL, ANCHO//2, ALTO - 60, centrado=True)
