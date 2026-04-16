# Implementation Tasks

## Tasks

- [x] 1. Refactorizar carga de assets en CharacterSelect
  - [x] 1.1 Agregar `from .gif import load_gif_frames` al inicio de `game/character.py`
  - [x] 1.2 Eliminar la función `_load_frames` local de `game/character.py`
  - [x] 1.3 Reemplazar las 4 llamadas a `_load_frames(...)` en `CharacterSelect.__init__` por `load_gif_frames(path, size=(100, 100))`
  - [x] 1.4 Verificar que el fallback de `load_gif_frames` produce una superficie 100×100 cuando el archivo no existe (sin excepción)

- [x] 2. Verificar animación en el carrusel
  - [x] 2.1 Confirmar que `CharacterSelect.update(dt)` avanza correctamente los frames de las naves animadas (BRAYAN, MARLIN, TETE)
  - [x] 2.2 Confirmar que FERNANDA (imagen estática, 1 frame) no ejecuta lógica de animación en `update()`
  - [x] 2.3 Confirmar que `app.py` ya llama `self.character.update(dt)` en el estado `MENU_CHARACTER` (sin cambios necesarios)

- [x] 3. Pruebas de propiedades de corrección
  - [x] 3.1 Escribir test de propiedad P1: instanciar `CharacterSelect` y verificar que no existe `_load_frames` como atributo ni función local accesible
  - [x] 3.2 Escribir test de propiedad P2: dado `dt` arbitrario ≥ 0, verificar que el índice de frame de una nave animada avanza correctamente y hace loop sin exceder `len(frames)`
  - [x] 3.3 Escribir test de propiedad P3: para una nave con 1 frame, verificar que `_anim_state["i"]` permanece en 0 tras múltiples llamadas a `update(dt)`
  - [x] 3.4 Escribir test de propiedad P4: instanciar `CharacterSelect` con paths de assets inexistentes y verificar que no se lanza ninguna excepción
