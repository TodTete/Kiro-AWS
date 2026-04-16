# Project Structure

```
main.py                  # Entry point: pygame init, GameApp instantiation
requirements.txt
hiscore.txt              # Persistent high score (plain int)

assets/
  extra/                 # Sprites: player ships, bullets, asteroids
  font/                  # Retronoid + RetroRace TTF/OTF fonts
  music/                 # MP3 audio files (SFX + music tracks)
  personajes/            # Boss sprites (jefe-1.png .. jefe-7.png, jefe.gif, malo.png)
                         # Player ship previews (personaje-*.png)
  scenes/                # Level backgrounds (fondo-1..8, animated GIFs)
    plants/              # Planet selector icons (1.png..8.png) + space backgrounds

game/
  app.py                 # GameApp class — main loop, state machine, event handling, draw
  constants.py           # All constants: screen size, FPS, colors, state names, difficulty presets
  state.py               # reset_juego() and activar_pantalla_nivel() — game state dict factory
  assets.py              # Global asset singletons; init_after_display(), set_player_skin()
  utils.py               # Helpers: load_font, dibujar_texto, cargar_sonido, reproducir, hiscore I/O
  audio.py               # Volumes class, play_music()
  background.py          # AnimatedBackground — dual-layer GIF background (main + boss)
  menu_bg.py             # MenuBG — animated menu background with zoom effect
  camera.py              # Camera — smooth lerp panning
  gif.py                 # load_gif_frames() — Pillow-based GIF/image loader
  character.py           # CharacterSelect — ship skin selection UI
  shooting.py            # shoot_pattern() — per-ship bullet patterns
  enemy_spawning.py      # Enemy spawn helpers
  level_select.py        # Level/planet selection logic
  ui_helpers.py          # draw_letterbox, draw_focus_ring, draw_slider
  entities/
    player.py            # Jugador class
    enemy.py             # Enemy class + crear_enemigos, respawnear_enemigo
    boss.py              # Boss class with attack patterns
    bullet.py            # Bala class
    powerups.py          # PowerUp, BombPickup, BombProjectile
    effects.py           # Visual effects
```

## Architecture Notes

- `GameApp` in `app.py` is the single orchestrator. It owns all game state and drives the loop.
- Game state is a plain `dict` returned by `reset_juego()` in `state.py`. No global mutable state outside of asset singletons in `assets.py`.
- State machine uses string constants from `constants.py` (e.g. `JUGANDO`, `MENU_MAIN`, `GAME_OVER`).
- Entities are plain classes with `update(dt, ...)` and `draw(surface, ...)` methods — no base class or ECS.
- All asset paths are relative to the project root. Never use absolute paths.
- New constants go in `constants.py`. New shared helpers go in `utils.py`.
- Adding a new entity: create a file in `game/entities/`, import it in `state.py` and `app.py` as needed.
