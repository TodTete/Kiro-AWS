"""
enemy_spawning.py — Ajuste dinámico de dificultad basado en puntaje histórico.
"""

HISCORE_PATH = "hiscore.txt"
HISCORE_THRESHOLD = 5000
SPEED_BOOST_FACTOR = 1.20  # +20%


def leer_hiscore() -> int:
    try:
        with open(HISCORE_PATH, "r") as f:
            return int(f.read().strip())
    except (FileNotFoundError, ValueError):
        return 0


def velocidad_enemigo_adaptativa(vel_base: float) -> float:
    """
    Si el hiscore supera el umbral, aumenta la velocidad base un 20%.
    Imprime un aviso en consola cuando se activa el ajuste.
    """
    hiscore = leer_hiscore()
    if hiscore > HISCORE_THRESHOLD:
        print("Dificultad ajustada por IA")
        return vel_base * SPEED_BOOST_FACTOR
    return vel_base
