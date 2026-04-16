
---

# 🌌 Spaces Astro

Arcade 2D desarrollado en **Python + Pygame**, con fondos animados, jefes progresivos, sistema de niveles, power-ups, cámara dinámica, transiciones y manejo de audio. El proyecto incluye una organización modular, assets clasificados por tipo y un flujo general optimizado.

---

## 🎮 Descripción general

* Juego estilo arcade orientado a esquivar y destruir asteroides.
* Sistema de **jefe por nivel** con patrones avanzados.
* Fondos GIF animados tanto en juego como en menús.
* Power-ups temporales (velocidad, disparo rápido, ralentización).
* Bomba automática durante la fase de jefe.
* **Dificultad adaptativa**: si el hiscore supera 5 000 puntos, la velocidad de los enemigos aumenta un 20% automáticamente.
* **Historial de partidas**: al terminar cada partida se guarda una entrada en `hiscore.json` con fecha, puntaje, nivel alcanzado y nave seleccionada. El archivo se ordena automáticamente de mayor a menor puntaje.
* Navegación mediante menús con opciones, dificultad y créditos.
* Cámara con paneo suave y transiciones visuales.

---

## ⌨️ Controles

* **Flechas**: movimiento
* **SPACE**: disparo
* **F**: ralentización (cuando esté disponible)
* **ENTER**: pausar o reanudar
* **F11**: pantalla completa
* **M**: silenciar
* **ESC**: retroceder en menús o salir

---

## 🎧 Recursos utilizados

* Música en formato **.mp3** para juego, jefe y efectos.
* Tipografías **Retronoid** y **RetroRace** en variantes TTF/OTF.
* GIFs animados para fondos y sprites específicos.
* Diversos personajes, jefes, proyectiles y elementos extra en “assets”.

---

## 📦 Instalación

```bash
git clone https://github.com/TodTete/VideoGame-Nave.git
cd VideoGame-Nave

python -m venv .venv
.venv\Scripts\activate   # Windows
# o
source .venv/bin/activate  # macOS / Linux

pip install -r requirements.txt
```

---

## ▶️ Ejecución

```bash
python main.py
```

Asegúrese de mantener la estructura original de archivos para evitar fallos en la carga de sprites, audio o fondos.

---

## 🗂️ Estructura actual del proyecto

```
C:.
│   .gitignore
│   hiscore.txt
│   hiscore.json
│   LICENSE
│   main.py
│   README.md
│   requirements.txt
│
├───assets
│   ├───extra
│   │       asteroides.gif
│   │       bala-2.png
│   │       bala.png
│   │       nave-f.jpg
│   │       nave-m.gif
│   │       nave-t.gif
│   │       nave.gif
│   │
│   ├───font
│   │       Retronoid Italic.otf
│   │       Retronoid Italic.ttf
│   │       Retronoid.otf
│   │       Retronoid.ttf
│   │       RetroRaceDemoItalic.ttf
│   │       RetroRaceDemoRegular.ttf
│   │       SPACEBAR.ttf
│   │
│   ├───music
│   │       boss.mp3
│   │       break.mp3
│   │       game-over.mp3
│   │       game-start-317318.mp3
│   │       game.mp3
│   │       laser-shot-ingame-230500.mp3
│   │       powerup.mp3
│   │       wood-crate-destory-2-97263.mp3
│   │
│   ├───personajes
│   │       jefe-1.png
│   │       jefe-2.png
│   │       jefe-3.png
│   │       jefe-4.png
│   │       jefe-5.png
│   │       jefe-6.png
│   │       jefe-7.png
│   │       jefe.gif
│   │       malo.png
│   │       personaje-b.png
│   │       personaje-f.png
│   │       personaje-m.png
│   │       personaje-t.png
│   │
│   └───scenes
│       │   fondo-1.png
│       │   fondo-2.gif
│       │   fondo-3.gif
│       │   fondo-4.gif
│       │   fondo-5.gif
│       │   fondo-6.png
│       │   fondo-7.gif
│       │   fondo-8.gif
│       │   fondo-gf.gif
│       │   fondo.gif
│       │   space.gif
│       │
│       └───plants
│               1.png
│               2.png
│               3.png
│               4.png
│               5.png
│               6.png
│               7.png
│               8.png
│               espacio.gif
│               espacio.png
│               space.gif
│
├───game
│   │   app.py
│   │   assets.py
│   │   audio.py
│   │   background.py
│   │   camera.py
│   │   character.py
│   │   constants.py
│   │   enemy_spawning.py
│   │   gif.py
│   │   level_select.py
│   │   menu_bg.py
│   │   shooting.py
│   │   state.py
│   │   ui_helpers.py
│   │   utils.py
│   │   __init__.py
│   │
│   ├───entities
│   │   │   boss.py
│   │   │   bullet.py
│   │   │   effects.py
│   │   │   enemy.py
│   │   │   player.py
│   │   │   powerups.py
│   │   │   __init__.py
│   │   │
│   │   └───__pycache__
│   │           boss.cpython-311.pyc
│   │           bullet.cpython-311.pyc
│   │           enemy.cpython-311.pyc
│   │           player.cpython-311.pyc
│   │           powerups.cpython-311.pyc
│   │           __init__.cpython-311.pyc
│   │
│   └───__pycache__
│           app.cpython-311.pyc
│           assets.cpython-311.pyc
│           audio.cpython-311.pyc
│           background.cpython-311.pyc
│           camera.cpython-311.pyc
│           character.cpython-311.pyc
│           constants.cpython-311.pyc
│           gif.cpython-311.pyc
│           menu_bg.cpython-311.pyc
│           shooting.cpython-311.pyc
│           state.cpython-311.pyc
│           ui_helpers.cpython-311.pyc
│           utils.cpython-311.pyc
│           __init__.cpython-311.pyc
│
└───__pycache__
        naves.cpython-311.pyc
```

---

## 🧪 Problemas comunes

* Si los GIF no cargan, el juego mostrará sprites estáticos.
* Si el audio falla, el título continúa ejecutándose sin sonido.
* Optimice los GIF grandes para mejorar el rendimiento.

---

## 👤 Autor

Desarrollado por **@TodTete** / **Ricardo Vallejo Sanchez.*
Créditos visibles dentro del juego.

---
