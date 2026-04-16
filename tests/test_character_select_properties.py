"""
Property-based tests for CharacterSelect animation correctness.
Validates: Requirements 1.5, 2.2-2.5, 5.2-5.3

Requires: pytest, hypothesis, pygame
Run with: python -m pytest tests/test_character_select_properties.py -v
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame
import pytest
from unittest.mock import patch
from hypothesis import given, settings
from hypothesis import strategies as st


# ---------------------------------------------------------------------------
# Module-level pygame init — runs once for the whole test module
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module", autouse=True)
def init_pygame():
    pygame.init()
    pygame.display.set_mode((800, 600))
    yield
    pygame.quit()


# ---------------------------------------------------------------------------
# P1 — Unicidad de cargador
# Validates: Requirements 1.5
# ---------------------------------------------------------------------------

def test_p1_no_local_load_frames():
    """_load_frames no debe existir en character.py tras la refactorización."""
    import game.character as char_module

    # No debe existir como función de módulo
    assert not hasattr(char_module, '_load_frames'), \
        "_load_frames no debe existir como función de módulo en character.py"

    # No debe existir como atributo de instancia
    with patch('game.assets.set_player_skin'):
        cs = char_module.CharacterSelect()

    assert not hasattr(cs, '_load_frames'), \
        "_load_frames no debe existir como atributo de instancia"


# ---------------------------------------------------------------------------
# P2 — Animación continua (property-based)
# Validates: Requirements 2.2, 2.3, 2.5
# ---------------------------------------------------------------------------

@given(dt=st.integers(min_value=0, max_value=10000))
@settings(max_examples=200)
def test_p2_continuous_animation(dt):
    """Para cualquier dt >= 0, el índice de frame de una nave animada
    siempre permanece dentro de [0, len(frames))."""
    import game.character as char_module

    with patch('game.assets.set_player_skin'):
        cs = char_module.CharacterSelect()

    # Inyectar preview multi-frame controlado para "BRAYAN"
    fake_frames = [pygame.Surface((100, 100)) for _ in range(3)]
    fake_durations = [100, 100, 100]
    cs.previews["BRAYAN"] = (fake_frames, fake_durations)
    cs._anim_state["BRAYAN"] = {"i": 0, "t": 0}

    cs.update(dt)

    idx = cs._anim_state["BRAYAN"]["i"]
    assert 0 <= idx < 3, \
        f"Índice fuera de rango tras update({dt}): got {idx}"


@given(dts=st.lists(st.integers(min_value=0, max_value=500), min_size=5, max_size=20))
@settings(max_examples=200)
def test_p2_continuous_animation_sequential(dts):
    """Múltiples llamadas secuenciales a update() mantienen el índice en rango."""
    import game.character as char_module

    with patch('game.assets.set_player_skin'):
        cs = char_module.CharacterSelect()

    fake_frames = [pygame.Surface((100, 100)) for _ in range(3)]
    fake_durations = [100, 100, 100]
    cs.previews["BRAYAN"] = (fake_frames, fake_durations)
    cs._anim_state["BRAYAN"] = {"i": 0, "t": 0}

    for dt in dts:
        cs.update(dt)
        idx = cs._anim_state["BRAYAN"]["i"]
        assert 0 <= idx < 3, \
            f"Índice fuera de rango tras update({dt}): got {idx}"


# ---------------------------------------------------------------------------
# P3 — Estático sin cómputo (property-based)
# Validates: Requirements 2.4, 3.3
# ---------------------------------------------------------------------------

@given(dts=st.lists(st.integers(min_value=0, max_value=10000), min_size=1, max_size=20))
@settings(max_examples=200)
def test_p3_static_frame_unchanged(dts):
    """Para una nave con 1 frame, _anim_state["i"] siempre permanece en 0."""
    import game.character as char_module

    with patch('game.assets.set_player_skin'):
        cs = char_module.CharacterSelect()

    # Inyectar preview de un solo frame para "FERNANDA"
    fake_frame = pygame.Surface((100, 100))
    cs.previews["FERNANDA"] = ([fake_frame], [150])
    cs._anim_state["FERNANDA"] = {"i": 0, "t": 0}

    for dt in dts:
        cs.update(dt)
        assert cs._anim_state["FERNANDA"]["i"] == 0, \
            f"El índice de FERNANDA cambió tras update({dt})"


# ---------------------------------------------------------------------------
# P4 — Sin crash en assets faltantes
# Validates: Requirements 5.2
# ---------------------------------------------------------------------------

def test_p4_no_crash_missing_assets():
    """CharacterSelect se instancia sin excepción aunque los assets no existan."""
    import game.character as char_module

    # load_gif_frames ya maneja archivos faltantes con un placeholder —
    # simplemente instanciamos con los paths reales (que pueden o no existir)
    # y verificamos que no se lanza ninguna excepción.
    with patch('game.assets.set_player_skin'):
        cs = char_module.CharacterSelect()

    # Las 4 naves deben tener entradas en previews
    assert len(cs.previews) == 4, \
        f"Se esperaban 4 entradas en previews, se obtuvieron {len(cs.previews)}"

    # Cada entrada debe tener al menos 1 frame y 1 duración
    for key, (frames, durations) in cs.previews.items():
        assert len(frames) >= 1, \
            f"La nave '{key}' no tiene frames"
        assert len(durations) >= 1, \
            f"La nave '{key}' no tiene duraciones"
        assert len(frames) == len(durations), \
            f"La nave '{key}' tiene frames/duraciones desbalanceados"
