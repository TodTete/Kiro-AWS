import pygame
from .gif import load_gif_frames, GifAnimator
from .constants import ANCHO, ALTO

def _load_any_frames(path, size):
    """Carga frames desde GIF si aplica; si es PNG/JPG devuelve un frame."""
    frames, durs = [], []
    # Intento 1: como GIF
    try:
        frames, durs = load_gif_frames(path, size=size)
        if frames:
            return frames, durs
    except Exception:
        pass
    # Intento 2: imagen estática
    try:
        img = pygame.image.load(path).convert_alpha()
        img = pygame.transform.smoothscale(img, size)
        return [img], [120]
    except Exception as e:
        print(f"[AVISO] No se pudo cargar fondo '{path}': {e}")
        surf = pygame.Surface(size, pygame.SRCALPHA)
        surf.fill((0,0,0,255))
        return [surf], [120]

class AnimatedBackground:
    def __init__(self, path_main="assets/scenes/fondo.gif", path_boss="assets/scenes/fondo-gf.gif"):
        self._anim_a = GifAnimator(*_load_any_frames(path_main, size=(ANCHO, ALTO)))
        self._anim_b = GifAnimator(*_load_any_frames(path_boss, size=(ANCHO, ALTO)))
        self.use_b = False
        self.transition = False
        self.transition_time = 0.0
        self.transition_duration = 1200
        self.alpha = 0

    def set_main_path(self, path_main):
        """Cambia el fondo principal (del nivel actual)."""
        self._anim_a = GifAnimator(*_load_any_frames(path_main, size=(ANCHO, ALTO)))

    def switch_to_boss(self):
        if not self.transition and not self.use_b:
            self.transition = True; self.transition_time = 0.0; self.alpha = 0

    def switch_to_main(self):
        if not self.transition and self.use_b:
            self.transition = True; self.transition_time = 0.0; self.alpha = 0

    def update(self, dt):
        self._anim_a.update(dt)
        self._anim_b.update(dt)

        if self.transition:
            self.transition_time += dt
            self.alpha = int(255 * min(1.0, self.transition_time / self.transition_duration))
            if self.transition_time >= self.transition_duration:
                self.transition = False
                self.use_b = not self.use_b
                self.alpha = 255

    def draw(self, surface):
        frame_a = self._anim_a.current_frame
        frame_b = self._anim_b.current_frame
        if not self.transition:
            surface.blit(frame_b if self.use_b else frame_a, (0, 0))
        else:
            if not self.use_b:
                img_b = frame_b.copy(); img_b.set_alpha(self.alpha)
                surface.blit(frame_a, (0, 0)); surface.blit(img_b, (0, 0))
            else:
                img_a = frame_a.copy(); img_a.set_alpha(self.alpha)
                surface.blit(frame_b, (0, 0)); surface.blit(img_a, (0, 0))
