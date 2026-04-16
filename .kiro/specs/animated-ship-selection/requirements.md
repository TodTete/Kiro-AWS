# Requirements Document

## Introduction

Esta feature agrega soporte de animación GIF a la pantalla de selección de nave ("SELECCIONA PERSONAJE") del juego Spaces Astro. Actualmente, la pantalla muestra imágenes estáticas para todas las naves. El objetivo es que las naves que tengan un GIF animado disponible (Brayan: `nave.gif`, Marlin: `nave-m.gif`, Tete: `nave-t.gif`) se muestren en movimiento, mientras que las que solo tienen imagen estática (Fernanda: `nave-f.jpg`) continúen mostrándose como imagen fija. La animación debe ser fluida, sincronizada con el delta-time del game loop, y no debe afectar el rendimiento ni la lógica de selección existente.

## Glossary

- **CharacterSelect**: Módulo y clase en `game/character.py` que gestiona la UI de selección de nave.
- **GifLoader**: Función `load_gif_frames()` en `game/gif.py` que extrae frames y duraciones de GIFs usando Pillow.
- **Preview**: Representación visual de una nave en el carrusel de selección, compuesta por una lista de frames y sus duraciones.
- **AnimState**: Estado de animación por nave: índice de frame actual y acumulador de tiempo en milisegundos.
- **Frame**: Superficie pygame (`pygame.Surface`) que representa un fotograma de la animación.
- **Carrusel**: Componente visual en `CharacterSelect` que muestra las 4 naves desplazables horizontalmente.
- **dt**: Delta-time en milisegundos devuelto por `clock.tick(FPS)` en el game loop.
- **SHIP_ORDER**: Lista ordenada de claves de naves: `["BRAYAN", "FERNANDA", "MARLIN", "TETE"]`.
- **Skin**: Identificador de nave seleccionada que determina el sprite usado durante el juego.

---

## Requirements

### Requirement 1: Carga de assets animados para el carrusel

**User Story:** Como jugador, quiero ver las naves animadas en el menú de selección, para poder apreciar el aspecto real de cada nave antes de elegirla.

#### Acceptance Criteria

1. WHEN `CharacterSelect` es instanciado, THE `CharacterSelect` SHALL cargar los frames y duraciones de cada nave usando `GifLoader` con un tamaño de preview de 100×100 píxeles.
2. WHEN el asset de una nave es un GIF animado válido, THE `CharacterSelect` SHALL almacenar todos sus frames y duraciones en el diccionario `previews`.
3. WHEN el asset de una nave es una imagen estática (JPG, PNG) o el GIF no puede cargarse, THE `CharacterSelect` SHALL almacenar un único frame con duración de 150ms como fallback.
4. IF Pillow no está disponible, THEN THE `CharacterSelect` SHALL cargar el primer frame del GIF como imagen estática sin lanzar excepción.
5. THE `CharacterSelect` SHALL usar `GifLoader` (`load_gif_frames` de `game/gif.py`) como mecanismo único de carga, eliminando la función `_load_frames` local duplicada.

---

### Requirement 2: Animación sincronizada con el game loop

**User Story:** Como jugador, quiero que las animaciones de las naves sean fluidas y no dependan de la velocidad del hardware, para tener una experiencia visual consistente.

#### Acceptance Criteria

1. THE `CharacterSelect` SHALL mantener un `AnimState` independiente por cada nave en el carrusel.
2. WHEN `CharacterSelect.update(dt)` es llamado con el delta-time en milisegundos, THE `CharacterSelect` SHALL avanzar el acumulador de tiempo de cada `AnimState` en `dt` milisegundos.
3. WHEN el acumulador de tiempo de un `AnimState` supera la duración del frame actual, THE `CharacterSelect` SHALL avanzar al siguiente frame y restar la duración consumida del acumulador.
4. WHEN una nave tiene un único frame (imagen estática), THE `CharacterSelect` SHALL omitir el cálculo de animación para esa nave.
5. WHEN el índice de frame alcanza el último frame de la secuencia, THE `CharacterSelect` SHALL reiniciar el índice al primer frame (loop continuo).
6. WHILE el estado del juego es `MENU_CHARACTER`, THE `GameApp` SHALL llamar a `CharacterSelect.update(dt)` en cada iteración del game loop.

---

### Requirement 3: Renderizado del frame correcto en el carrusel

**User Story:** Como jugador, quiero ver el frame animado correcto de cada nave en su posición del carrusel, para que la animación se vea coherente independientemente de qué nave esté seleccionada.

#### Acceptance Criteria

1. WHEN `CharacterSelect.draw(surface, fuente_titulo, fuente)` es llamado, THE `CharacterSelect` SHALL renderizar el frame correspondiente al `AnimState` actual de cada nave en su posición del carrusel.
2. THE `CharacterSelect` SHALL renderizar todas las naves visibles en el carrusel con su frame animado actual, no solo la nave seleccionada.
3. WHEN una nave tiene un único frame, THE `CharacterSelect` SHALL renderizar siempre ese frame sin consultar el `AnimState`.

---

### Requirement 4: Compatibilidad con la selección y aplicación de skin

**User Story:** Como jugador, quiero que al confirmar mi selección de nave animada, el juego use esa nave correctamente durante la partida, para que la elección visual tenga efecto real en el gameplay.

#### Acceptance Criteria

1. WHEN el jugador presiona ENTER o SPACE en `MENU_CHARACTER`, THE `CharacterSelect` SHALL registrar la nave actualmente resaltada como `selected_ship`.
2. WHEN `CharacterSelect.apply_selected_skin()` es llamado, THE `CharacterSelect` SHALL invocar `Assets.set_player_skin(selected_ship)` para cargar los frames de juego de la nave elegida.
3. THE `CharacterSelect` SHALL mantener el `AnimState` de todas las naves activo e independiente de cuál esté seleccionada, de modo que al volver al menú las animaciones continúen desde donde se detuvieron.

---

### Requirement 5: Rendimiento y estabilidad

**User Story:** Como desarrollador, quiero que la carga y animación de GIFs en el menú no cause caídas de FPS ni crashes, para mantener la estabilidad del juego a 60 FPS.

#### Acceptance Criteria

1. THE `CharacterSelect` SHALL cargar todos los assets de preview una única vez durante la instanciación, no en cada frame del game loop.
2. IF un archivo de asset no existe o no puede leerse, THEN THE `CharacterSelect` SHALL generar una superficie placeholder de 100×100 píxeles y continuar sin lanzar excepción.
3. WHEN `CharacterSelect.update(dt)` es llamado con `dt` mayor a la duración total de la animación, THE `CharacterSelect` SHALL avanzar correctamente múltiples frames en una sola llamada sin entrar en un bucle infinito.
