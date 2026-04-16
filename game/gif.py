import pygame
try:
    from PIL import Image
    PIL_OK = True
except Exception as e:
    print("[AVISO] Pillow no disponible, los GIF se verán estáticos:", e)
    PIL_OK = False

# Intervalo mínimo entre avances de frame: ~33 ms = 30 FPS
_GIF_MIN_FRAME_MS = 1000 / 30


class GifAnimator:
    """Gestiona el avance de frames de un GIF limitado a 30 FPS máximo."""

    def __init__(self, frames, durations):
        self.frames = frames
        self.durations = durations
        self.idx = 0
        self._accum = 0.0
        self._throttle_accum = 0.0

    def update(self, dt):
        """Avanza la animación con dt en milisegundos, limitado a 30 FPS."""
        self._throttle_accum += dt
        if self._throttle_accum < _GIF_MIN_FRAME_MS:
            return
        # Consumimos solo el tiempo acumulado hasta ahora
        effective_dt = self._throttle_accum
        self._throttle_accum = 0.0

        self._accum += effective_dt
        while self._accum >= self.durations[self.idx]:
            self._accum -= self.durations[self.idx]
            self.idx = (self.idx + 1) % len(self.frames)

    @property
    def current_frame(self):
        return self.frames[self.idx]

def load_gif_frames(path, size):
    frames, durations = [], []
    if not PIL_OK:
        try:
            img = pygame.image.load(path).convert_alpha()
            if size: img = pygame.transform.smoothscale(img, size)
            return [img], [120]
        except Exception as e:
            print(f"[AVISO] No se pudo cargar '{path}': {e}")
            surf = pygame.Surface(size, pygame.SRCALPHA)
            surf.fill((5,5,15,255))
            return [surf], [120]

    try:
        im = Image.open(path)
        frame_count = getattr(im, "n_frames", 1)
        canvas_size = im.size
        prev = Image.new("RGBA", canvas_size, (0,0,0,0))

        for i in range(frame_count):
            im.seek(i)
            dur = max(20, int(im.info.get("duration", 100)))
            curr = im.convert("RGBA")
            composed = prev.copy()
            composed.alpha_composite(curr, dest=(0,0))

            disposal = getattr(im, "disposal", im.info.get("disposal", 0))
            next_prev = Image.new("RGBA", canvas_size, (0,0,0,0)) if disposal == 2 else composed

            out_img = composed if not size or size==canvas_size else composed.resize(size, Image.LANCZOS)
            data = out_img.tobytes()
            py_img = pygame.image.fromstring(data, out_img.size, "RGBA").convert_alpha()
            frames.append(py_img); durations.append(dur)
            prev = next_prev

        if not frames:
            raise ValueError("GIF sin frames")
        return frames, durations
    except Exception as e:
        print(f"[AVISO] Error cargando GIF '{path}': {e}")
        surf = pygame.Surface(size, pygame.SRCALPHA)
        surf.fill((5,5,15,255))
        return [surf],[120]
