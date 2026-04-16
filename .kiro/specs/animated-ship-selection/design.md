# Design Document

## Overview

La pantalla de selección de nave ya cuenta con la infraestructura de animación implementada en `game/character.py` (carga de frames, `AnimState`, `update(dt)`, `_current_frame`, llamada desde `app.py`). El único cambio necesario es eliminar la función local `_load_frames` duplicada y reemplazarla por `load_gif_frames` de `game/gif.py`, que es el cargador canónico del proyecto con mejor manejo de composición GIF y fallbacks.

## Architecture

No se introduce ninguna clase nueva ni se modifica la arquitectura existente. El cambio es una refactorización interna de `CharacterSelect`.

### Componentes involucrados

- **`game/character.py`** — único archivo a modificar:
  - Eliminar la función `_load_frames` local.
  - Importar `load_gif_frames` desde `game.gif`.
  - Reemplazar las 4 llamadas a `_load_frames(...)` en `__init__` por `load_gif_frames(...)`.
- **`game/gif.py`** — sin cambios; provee `load_gif_frames(path, size)`.
- **`game/app.py`** — sin cambios; ya llama `self.character.update(dt)` en `MENU_CHARACTER`.

## Data Models

### `CharacterSelect.previews`
```python
# dict[str, tuple[list[pygame.Surface], list[int]]]
previews = {
    "BRAYAN":   ([surf, ...], [dur_ms, ...]),  # GIF animado
    "FERNANDA": ([surf],      [150]),           # imagen estática
    "MARLIN":   ([surf, ...], [dur_ms, ...]),  # GIF animado
    "TETE":     ([surf, ...], [dur_ms, ...]),  # GIF animado
}
```

### `CharacterSelect._anim_state`
```python
# dict[str, dict] — sin cambios
_anim_state = {
    "BRAYAN":   {"i": 0, "t": 0},
    "FERNANDA": {"i": 0, "t": 0},
    "MARLIN":   {"i": 0, "t": 0},
    "TETE":     {"i": 0, "t": 0},
}
```

## Key Design Decisions

### ¿Por qué reemplazar `_load_frames` por `load_gif_frames`?

| Aspecto | `_load_frames` local | `load_gif_frames` (gif.py) |
|---|---|---|
| Composición GIF (disposal) | No | Sí |
| Fallback sin Pillow | Parcial | Completo |
| Fallback archivo faltante | Parcial | Superficie placeholder |
| Mantenimiento | Duplicado | Único punto de verdad |

### Comportamiento de fallback

`load_gif_frames` ya cumple todos los criterios del Req 5:
- Si el archivo no existe → superficie placeholder 100×100 oscura, sin excepción.
- Si Pillow no está disponible → carga con `pygame.image.load` como imagen estática.
- Si el GIF está vacío → superficie placeholder.

## Correctness Properties

1. **P1 — Unicidad de cargador**: Ninguna función de carga de GIF/imagen existe en `character.py` tras el cambio; toda carga pasa por `load_gif_frames`.
2. **P2 — Animación continua**: Para toda nave con `len(frames) > 1`, el índice de frame avanza correctamente con `dt` y hace loop sin saltar frames ni entrar en bucle infinito.
3. **P3 — Estático sin cómputo**: Para toda nave con `len(frames) == 1`, `update()` no modifica `_anim_state` y `_current_frame` retorna siempre `frames[0]`.
4. **P4 — Sin crash en assets faltantes**: La instanciación de `CharacterSelect` nunca lanza excepción, incluso si todos los archivos de asset están ausentes.
