# Tech Stack

## Language & Runtime
- Python 3.11+
- Virtual environment via `.venv`

## Dependencies
- `pygame >= 2.5.0` — game loop, rendering, input, audio
- `Pillow >= 10.0.0` — GIF frame extraction

## Common Commands

```bash
# Setup
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # macOS/Linux
pip install -r requirements.txt

# Run
python main.py
```

## Key Technical Patterns

### Pygame Initialization
`pygame.init()` and `pygame.mixer.init()` are called in `main.py`. Audio failure is non-fatal — the game continues without sound. `pygame.display.set_mode()` must be called before loading any image/GIF assets; `init_after_display()` in `game/assets.py` handles this.

### Game Loop
Fixed at 60 FPS (`FPS = 60` in `constants.py`). `clock.tick(FPS)` returns `dt` in milliseconds, passed to all `update(dt, ...)` calls.

### Audio
`pygame.mixer` with per-channel volume. `Volumes` class in `game/audio.py` manages master, SFX, and music levels. `play_music()` wraps `pygame.mixer.music` with fade support. Audio errors are caught and printed as `[AVISO]`.

### GIF Handling
`game/gif.py` uses Pillow to extract frames and durations from animated GIFs. Returns `(frames: list[Surface], durations: list[int])`. Static images return a single-frame list. All sprite animation uses this pattern.

### Asset Loading
Assets are loaded lazily after display init. Missing files print `[AVISO]` warnings and fall back to colored placeholder surfaces — the game never crashes on missing assets.

### Fonts
Primary font: `Retronoid.ttf` / `Retronoid.otf` from `assets/font/`. `load_font(size)` in `utils.py` falls back to Arial if not found.
