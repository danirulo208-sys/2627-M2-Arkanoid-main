"""Utilidades comunes para el hito M2 de Arkanoid.

Este módulo proporciona la clase `ArkanoidGame` con toda la infraestructura del
minijuego (constantes, estado compartido y utilidades) y un decorador
`arkanoid_method` que permite registrar funciones definidas en los ficheros de la
plantilla como métodos de la clase. De esta forma, el alumnado solo tiene que
rellenar los `TODO` en `arkanoid_game.py` sin preocuparse por detalles de
herencia o subclases.
"""

from __future__ import annotations

from pathlib import Path
from typing import Callable, Iterable, Iterator, TypeVar

import os

os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

import pygame
from pygame import Vector2

__all__ = ["ArkanoidGame", "arkanoid_method", "pygame", "Vector2"]

F = TypeVar("F", bound=Callable[..., object])


class ArkanoidGame:
    """Contenedor con la lógica común del Arkanoid simplificado."""

    # Configuración visual y de juego
    SCREEN_WIDTH: int = 800
    SCREEN_HEIGHT: int = 600
    FPS: int = 60

    BACKGROUND_COLOR = (12, 20, 32)
    PADDLE_COLOR = (230, 230, 240)
    BALL_COLOR = (255, 245, 235)

    # Paleta
    PADDLE_SIZE = (120, 18)
    PADDLE_OFFSET = 48
    PADDLE_SPEED = 8.0

    # Bola
    BALL_RADIUS = 10
    BALL_SPEED = 6.0

    # Bloques
    BLOCK_WIDTH = 60
    BLOCK_HEIGHT = 24
    BLOCK_GAP_X = 8
    BLOCK_GAP_Y = 6
    BLOCK_OFFSET_TOP = 80

    BLOCK_COLORS = {
        "#": (214, 103, 103),
        "@": (102, 170, 214),
        "%": (234, 190, 104),
    }
    BLOCK_POINTS = {
        "#": 50,
        "@": 75,
        "%": 120,
    }

    # Entradas y eventos (para minimizar el uso directo de pygame en la plantilla)
    KEY_LEFT = pygame.K_LEFT
    KEY_RIGHT = pygame.K_RIGHT
    KEY_A = pygame.K_a
    KEY_D = pygame.K_d
    KEY_ESCAPE = pygame.K_ESCAPE

    EVENT_QUIT = pygame.QUIT
    EVENT_KEYDOWN = pygame.KEYDOWN

    def __init__(self, level_path: str | os.PathLike[str]) -> None:
        self.level_path = Path(level_path)
        self.layout: list[str] = []

        # Entidades
        self.paddle = self.crear_rect(0, 0, *self.PADDLE_SIZE)
        self.blocks: list[pygame.Rect] = []
        self.block_colors: list[tuple[int, int, int]] = []
        self.block_symbols: list[str] = []
        self.ball_pos = Vector2(0, 0)
        self.ball_velocity = Vector2(0, 0)

        # Estado del juego
        self.score: int = 0
        self.lives: int = 3
        self.running: bool = False
        self.end_message: str = ""

        # Recursos de pygame
        self.screen: pygame.Surface | None = None
        self.clock: pygame.time.Clock | None = None
        self._font_small: pygame.font.Font | None = None
        self._font_big: pygame.font.Font | None = None

    # ------------------------------------------------------------------ #
    # Métodos auxiliares ya implementados para el hito
    # ------------------------------------------------------------------ #
    def reiniciar_bola(self, direction: Vector2 | Iterable[float] = (0, -1)) -> None:
        """Coloca la bola justo encima de la paleta y reinicia su velocidad."""
        if isinstance(direction, Vector2):
            direccion = direction
        else:
            direccion = Vector2(direction)

        if direccion.length_squared() == 0:
            direccion = Vector2(0, -1)

        self.ball_pos.update(self.paddle.centerx, self.paddle.top - self.BALL_RADIUS - 1)
        self.ball_velocity = direccion.normalize() * self.BALL_SPEED

    def calcular_posicion_bloque(self, fila: int, columna: int) -> pygame.Rect:
        """Convierte coordenadas de cuadrícula en un rectángulo de pygame."""
        if not self.layout:
            raise RuntimeError("No se ha cargado ningún nivel todavía.")

        columnas = len(self.layout[0])
        if columnas <= 0:
            raise ValueError("El nivel debe tener al menos una columna.")

        total_ancho = columnas * self.BLOCK_WIDTH + (columnas - 1) * self.BLOCK_GAP_X
        margen_x = max(0, (self.SCREEN_WIDTH - total_ancho) // 2)

        x = margen_x + columna * (self.BLOCK_WIDTH + self.BLOCK_GAP_X)
        y = self.BLOCK_OFFSET_TOP + fila * (self.BLOCK_HEIGHT + self.BLOCK_GAP_Y)
        return self.crear_rect(x, y, self.BLOCK_WIDTH, self.BLOCK_HEIGHT)

    def inicializar_pygame(self) -> None:
        """Inicializa pygame, la ventana y los recursos principales."""
        if self.screen is not None:
            return

        # No forzamos un driver "dummy" para permitir abrir la ventana en un
        # entorno gráfico normal (PC con escritorio).
        pygame.init()
        pygame.display.set_caption("Arkanoid M2")
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

    def iterar_eventos(self) -> Iterator[pygame.event.Event]:
        """Itera sobre la cola de eventos de pygame."""
        return iter(pygame.event.get())

    def _obtener_fuente(self, grande: bool) -> pygame.font.Font | None:
        if not pygame.font:
            return None

        if grande:
            if not self._font_big:
                self._font_big = pygame.font.Font(None, 48)
            return self._font_big

        if not self._font_small:
            self._font_small = pygame.font.Font(None, 26)
        return self._font_small

    def dibujar_texto(self, texto: str, posicion: tuple[int, int], grande: bool = False) -> None:
        """Dibuja texto en pantalla usando las fuentes configuradas."""
        if not self.screen:
            return

        fuente = self._obtener_fuente(grande)
        if not fuente:
            return

        superficie = fuente.render(texto, True, (240, 240, 245))
        self.screen.blit(superficie, posicion)

    # ------------------------------------------------------------------ #
    # Utilidades que encapsulan operaciones habituales de pygame
    # ------------------------------------------------------------------ #
    def crear_rect(self, x: int, y: int, width: int, height: int) -> pygame.Rect:
        """Crea un rectángulo de pygame."""
        return pygame.Rect(x, y, width, height)

    def obtener_rect_bola(self) -> pygame.Rect:
        """Devuelve un rectángulo posicionado sobre la bola actual."""
        return self.crear_rect(
            int(self.ball_pos.x - self.BALL_RADIUS),
            int(self.ball_pos.y - self.BALL_RADIUS),
            self.BALL_RADIUS * 2,
            self.BALL_RADIUS * 2,
        )

    def obtener_estado_teclas(self) -> pygame.key.ScancodeWrapper:
        """Devuelve el estado actual del teclado."""
        return pygame.key.get_pressed()

    def dibujar_rectangulo(self, rect: pygame.Rect, color: tuple[int, int, int], borde: int = 0) -> None:
        """Dibuja un rectángulo en pantalla."""
        if not self.screen:
            return
        pygame.draw.rect(self.screen, color, rect, borde)

    def dibujar_circulo(self, centro: tuple[int, int], radio: int, color: tuple[int, int, int]) -> None:
        """Dibuja un círculo en pantalla."""
        if not self.screen:
            return
        pygame.draw.circle(self.screen, color, centro, radio)

    def actualizar_pantalla(self) -> None:
        """Refresca el contenido de la ventana principal."""
        if not self.screen:
            return
        pygame.display.flip()

    def esperar(self, milisegundos: int) -> None:
        """Pausa la ejecución el tiempo indicado (en ms)."""
        pygame.time.wait(milisegundos)

    def finalizar_pygame(self) -> None:
        """Cierra pygame y libera la ventana."""
        pygame.quit()
        self.screen = None
        self.clock = None

    # ------------------------------------------------------------------ #
    # Métodos a completar por el alumnado (se sobreescriben en la plantilla)
    # ------------------------------------------------------------------ #
    def cargar_nivel(self) -> list[str]:
        raise NotImplementedError

    def preparar_entidades(self) -> None:
        raise NotImplementedError

    def crear_bloques(self) -> None:
        raise NotImplementedError

    def procesar_input(self) -> None:
        raise NotImplementedError

    def actualizar_bola(self) -> None:
        raise NotImplementedError

    def dibujar_escena(self) -> None:
        raise NotImplementedError

    def run(self) -> None:
        raise NotImplementedError


def arkanoid_method(func: F) -> F:
    """Registra `func` como método de `ArkanoidGame`.

    Permite mantener los `TODO` como funciones en `arkanoid_game.py` y que,
    tras importar este módulo, queden enlazadas automáticamente con la clase.
    """
    nombre = func.__name__
    if not hasattr(ArkanoidGame, nombre):
        raise AttributeError(
            f"ArkanoidGame no tiene ningún método llamado {nombre!r} para sobrescribir."
        )

    setattr(ArkanoidGame, nombre, func)
    return func
