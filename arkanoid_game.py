"""Plantilla del juego Arkanoid para el hito M2.

Completa los métodos marcados con TODO respetando las anotaciones de tipo y la
estructura de la clase. El objetivo es construir un prototipo jugable usando
pygame que cargue bloques desde un fichero de nivel basado en caracteres.
"""
from arkanoid_core import *
# --------------------------------------------------------------------- #
# Métodos a completar por el alumnado
# --------------------------------------------------------------------- #


@arkanoid_method
def cargar_nivel(self) -> list[str]:
    if not self.level_path.is_file():
        raise FileNotFoundError(f"No se encontró el fichero de nivel: {self.level_path}")

    # Leemos, filtramos líneas vacías y comprobamos el ancho
    lineas = [
        linea.strip()
        for linea in self.level_path.read_text("utf-8").splitlines()
        if linea.strip()
    ]

    if not lineas:
        raise ValueError("El nivel está vacío.")

    ancho = len(lineas[0])
    if any(len(linea) != ancho for linea in lineas):
        raise ValueError("Todas las filas deben tener el mismo ancho.")

    self.layout = lineas
    return self.layout


@arkanoid_method
def preparar_entidades(self) -> None:
    self.paddle.width = self.PADDLE_SIZE[0]
    self.paddle.height = self.PADDLE_SIZE[1]
    self.paddle.centerx = self.SCREEN_WIDTH // 2
    self.paddle.bottom = self.SCREEN_HEIGHT - self.PADDLE_OFFSET

    self.score = 0
    self.lives = 3
    self.end_message = ""
    self.reiniciar_bola()


@arkanoid_method
def crear_bloques(self) -> None:
    self.blocks.clear()
    self.block_colors.clear()
    self.block_symbols.clear()

    for fila_idx, fila in enumerate(self.layout):
        for col_idx, simbolo in enumerate(fila):
            if simbolo != ".":
                rect = self.calcular_posicion_bloque(fila_idx, col_idx)
                self.blocks.append(rect)
                self.block_symbols.append(simbolo)
                self.block_colors.append(
                    self.BLOCK_COLORS.get(simbolo, (255, 255, 255))
                )


@arkanoid_method
def procesar_input(self) -> None:
    teclas = self.obtener_estado_teclas()

    # Movimiento a izquierda y derecha
    if teclas[self.KEY_LEFT] or teclas[self.KEY_A]:
        self.paddle.x -= self.PADDLE_SPEED
    if teclas[self.KEY_RIGHT] or teclas[self.KEY_D]:
        self.paddle.x += self.PADDLE_SPEED

    # Limitar para que no salga de la pantalla
    if self.paddle.left < 0:
        self.paddle.left = 0
    elif self.paddle.right > self.SCREEN_WIDTH:
        self.paddle.right = self.SCREEN_WIDTH


@arkanoid_method
def actualizar_bola(self) -> None:
    self.ball_pos += self.ball_velocity
    ball_rect = self.obtener_rect_bola()

    # Rebotes contra las paredes laterales y superior
    if self.ball_pos.x - self.BALL_RADIUS <= 0:
        self.ball_pos.x = self.BALL_RADIUS
        self.ball_velocity.x *= -1
    elif self.ball_pos.x + self.BALL_RADIUS >= self.SCREEN_WIDTH:
        self.ball_pos.x = self.SCREEN_WIDTH - self.BALL_RADIUS
        self.ball_velocity.x *= -1

    if self.ball_pos.y - self.BALL_RADIUS <= 0:
        self.ball_pos.y = self.BALL_RADIUS
        self.ball_velocity.y *= -1

    # Caída por la parte inferior
    elif self.ball_pos.y + self.BALL_RADIUS >= self.SCREEN_HEIGHT:
        self.lives -= 1
        if self.lives > 0:
            self.reiniciar_bola()
        else:
            self.end_message = "¡Has perdido!"
            self.running = False
        return

    # Rebote contra la paleta
    if ball_rect.colliderect(self.paddle) and self.ball_velocity.y > 0:
        self.ball_velocity.y *= -1
        # Efecto para que la bola cambie ligeramente el ángulo según dónde impacte en la pala
        impacto_relativo = (self.ball_pos.x - self.paddle.centerx) / (
            self.PADDLE_SIZE[0] / 2
        )
        self.ball_velocity.x = impacto_relativo * self.BALL_SPEED

    # Colisiones contra los bloques
    idx = ball_rect.collidelist(self.blocks)
    if idx != -1:
        bloque_hit = self.blocks[idx]

        # Determinar de dónde vino el golpe usando los centros para invertir eje X o Y
        if ball_rect.centerx < bloque_hit.left or ball_rect.centerx > bloque_hit.right:
            self.ball_velocity.x *= -1
        else:
            self.ball_velocity.y *= -1

        # Eliminar el bloque y actualizar puntos
        self.blocks.pop(idx)
        self.block_colors.pop(idx)
        simbolo = self.block_symbols.pop(idx)
        self.score += self.BLOCK_POINTS.get(simbolo, 10)

    # Condición de victoria
    if not self.blocks:
        self.end_message = "¡Has ganado!"
        self.running = False


@arkanoid_method
def dibujar_escena(self) -> None:
    if self.screen:
        self.screen.fill(self.BACKGROUND_COLOR)

    # Bloques
    for block, color in zip(self.blocks, self.block_colors):
        self.dibujar_rectangulo(block, color)

    # Paleta y Bola
    self.dibujar_rectangulo(self.paddle, self.PADDLE_COLOR)
    self.dibujar_circulo(
        (int(self.ball_pos.x), int(self.ball_pos.y)),
        self.BALL_RADIUS,
        self.BALL_COLOR,
    )

    # HUD (puntuación y vidas)
    self.dibujar_texto(f"Puntos: {self.score}", (20, 20))
    self.dibujar_texto(f"Vidas: {self.lives}", (self.SCREEN_WIDTH - 120, 20))

    # Mensaje de fin de partida
    if self.end_message:
        self.dibujar_texto(
            self.end_message,
            (self.SCREEN_WIDTH // 2 - 120, self.SCREEN_HEIGHT // 2),
            grande=True,
        )


@arkanoid_method
def run(self) -> None:
    self.inicializar_pygame()
    self.cargar_nivel()
    self.preparar_entidades()
    self.crear_bloques()

    self.running = True
    salir = False

    while not salir:
        # Procesar eventos generales de ventana
        for event in self.iterar_eventos():
            if event.type == self.EVENT_QUIT:
                salir = True
            elif event.type == self.EVENT_KEYDOWN and event.key == self.KEY_ESCAPE:
                salir = True

        # Lógica del juego
        if self.running:
            self.procesar_input()
            self.actualizar_bola()

        # Refrescar pantalla
        self.dibujar_escena()
        self.actualizar_pantalla()
        if self.clock:
            self.clock.tick(self.FPS)

    self.finalizar_pygame()



def main() -> None:
    """Permite ejecutar el juego desde la línea de comandos."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Plantilla del hito M2: Arkanoid con pygame.",
    )
    parser.add_argument(
        "level",
        nargs="?",
        default="niveles/demo.txt",
        type=str,
        help="Ruta al fichero de nivel (texto con # para bloques y . para huecos).",
    )
    args = parser.parse_args()

    game = ArkanoidGame(args.level)
    game.run()




if __name__ == "__main__":
    main()