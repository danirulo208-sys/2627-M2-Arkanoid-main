# Arkanoid-M2
En este segundo hito construiremos una versión básica de Arkanoid empleando `pygame`. El objetivo es que el alumnado practique el manejo de bucles del juego reutilizando una clase preparada a modo de plantilla.

Para no empezar desde cero, se entrega un fichero `arkanoid_game.py` con la estructura del juego el cual importa un fichero core con todo lo que se necesita. Cada método incluye instrucciones `TODO` que debes resolver.

> **Cómo entregar (curso 26/27).** En el repositorio `2627-M2-Arkanoid` pulsad
> **«Use this template» → Create a new repository** para crear el repositorio del grupo
> (ya no se usa *fork*). Cuando lo tengáis resuelto, comprimid el proyecto en
> `arkanoid-<nombre del grupo>.zip` y subidlo al formulario de ev.us.es.
> **Fecha límite: jueves 12 de noviembre.** Basta con que lo suba una persona del grupo.

## Cómo se evalúa este hito

Este hito **no puntúa por sí solo**. Cumple dos funciones:

- **Derecho a asiento en el Control 1** (martes 24 nov): tienes que haberlo **entregado en
  plazo** y el proyecto tiene que **ejecutarse sin errores**. Se comprueba entrega por entrega:
  si no arranca, no cuenta como entregada y no hay asiento.
- **Bonus**: el conjunto de los tres hitos puede aportar hasta **+0,5** sobre la nota de
  teoría por calidad y extras, según la rúbrica común.

La nota de teoría sale de los **dos controles individuales de laboratorio**
(martes 24 nov y martes 15 dic), de 110 minutos cada uno y con el mismo formato que el
examen práctico de enero. Los controles se plantean **sobre el dominio de
este hito**: cuanto mejor entiendas el código que has escrito aquí, menos te costará el
control.

> **Lo que pone la nota son los controles.** Este hito no da nota por sí solo: es la llave para
> poder presentarte a ellos.

> Trabajad el proyecto vosotros. Lo que no sepáis escribir sin ayuda no lo sabréis escribir
> en el laboratorio, que es donde se pone la nota.

### Uso de inteligencia artificial

Se **desaconseja** usar IA generativa para resolver los TODO. Antes de recurrir a ella,
utiliza los apuntes, la documentación, las pruebas propias y las tutorías. Si la usas de
forma puntual, decláralo en el README y comprueba que puedes explicar, probar y modificar
todo el código generado. La IA no está permitida en simulacros, controles ni exámenes.

## Requisitos previos
1. Asegúrate de tener Python 3.10 o superior.
2. Instala `pygame` en tu entorno si aún no lo tienes:
   ```bash
   python -m pip install pygame
   ```
3. Ejecuta la plantilla con:
   ```bash
   python arkanoid_game.py niveles/demo.txt
   ```
   Sustituye `niveles/demo.txt` por el fichero de nivel que quieras usar durante el desarrollo.

## Contexto
La nueva entrega de Arkanoid necesita un prototipo jugable que recoja los fundamentos del juego clásico: una paleta, una bola y filas de bloques que deben desaparecer con los rebotes. Para facilitar el desarrollo, el fichero arkanoid_core se encarga de gestionar el ciclo principal del juego, la carga de niveles, la detección de colisiones y el pintado en pantalla. Cada funcionalidad está separada en métodos que debes completar.

Los ficheros de niveles definen una cuadrícula rectangular utilizando caracteres. Cada línea representa una fila de bloques y cada símbolo define el tipo de bloque:

- `#`: bloque sólido clásico que debe destruirse.
- `@`: bloque reforzado que otorga más puntos (cambia el color de la fila superior).
- `%`: bloque bonus (puntuación más alta; aparece en filas intermedias del ejemplo).
- `.`: celda vacía (no se dibuja nada en esa posición).

Puedes ampliar esta codificación si lo deseas, pero la versión básica solo necesita interpretar estos símbolos.

### Utilidades disponibles

Para evitar que tengáis que recurrir directamente a `pygame`, la clase `ArkanoidGame`
incluye varios métodos y constantes auxiliares:

- `self.crear_rect(x, y, ancho, alto)` y `self.obtener_rect_bola()` para obtener `Rect`.
- `self.obtener_estado_teclas()` junto con las constantes `self.KEY_LEFT`, `self.KEY_RIGHT`, `self.KEY_A`, `self.KEY_D`, `self.KEY_ESCAPE`.
- `self.dibujar_rectangulo(rect, color, borde=0)` y `self.dibujar_circulo(centro, radio, color)` para renderizar formas.
- `self.actualizar_pantalla()` y `self.esperar(ms)` para gestionar el refresco y pequeñas pausas.
- Constantes de eventos (`self.EVENT_QUIT`, `self.EVENT_KEYDOWN`) y el método `self.finalizar_pygame()` para cerrar el juego con seguridad.

## Ejercicios
Completa los métodos marcados con `TODO` siguiendo el orden propuesto y respetando las anotaciones de tipo. Se recomienda leer los docstrings de cada método en `arkanoid_game.py` para entender mejor los requisitos.

1. **`cargar_nivel`**  
   Lee el fichero indicado en `level_path` y devuelve la cuadrícula como una lista de cadenas. Debes validar que el fichero existe y que todas las filas tienen la misma longitud.  
   *Pistas:* `Path.read_text` (lee el fichero completo como texto), `splitlines()` (separa en filas), control de excepciones y comprobación de anchura con `len`.

2. **`preparar_entidades`**  
   Inicializa la paleta, la bola y las variables de puntuación/vidas. La paleta debe aparecer centrada en la parte inferior y la bola justo encima, lista para salir disparada.  
   *Pistas:* usa `self.crear_rect` para configurar la paleta, `Vector2` para la bola y llama a `self.reiniciar_bola()` para dejarla lista sobre la paleta.

3. **`crear_bloques`**  
   A partir de la cuadrícula generada en el paso 1, crea los rectángulos de `pygame` que representarán los bloques. Almacénalos en `self.blocks` junto con la información necesaria para dibujarlos (color, puntuación, etc.).  
   *Pistas:* apóyate en `self.calcular_posicion_bloque` para obtener cada `Rect` y rellena las listas `self.blocks`, `self.block_colors` y `self.block_symbols`.

4. **`procesar_input`**  
   Gestiona la entrada del usuario moviendo la paleta. Debes contemplar las teclas de dirección izquierda/derecha (o `A/D`) y mantener la paleta dentro de los límites de la pantalla.  
   *Pistas:* obtén el estado de teclado con `self.obtener_estado_teclas()` y utiliza las constantes `self.KEY_LEFT`, `self.KEY_RIGHT`, `self.KEY_A`, `self.KEY_D`. Ajusta `self.paddle.x` respetando los límites de la pantalla.

5. **`actualizar_bola`**  
   Calcula el movimiento de la bola en cada fotograma, aplicando una velocidad inicial y rebotes con paredes, paleta y bloques. Cuando impacte contra un bloque, elimínalo y suma la puntuación correspondiente.  
   *Pistas:* tras mover `self.ball_pos`, obtén el rectángulo de colisión con `self.obtener_rect_bola()`. Usa `Rect.colliderect` contra paleta y bloques, invirtiendo las componentes de `self.ball_velocity` según corresponda y actualiza puntuación/vidas.

6. **`dibujar_escena`**  
   Dibuja fondo, bloques, paleta, bola y marcadores (puntuación y vidas). Aprovecha este método para centralizar todo el renderizado y mantener legible el bucle principal.  
   *Pistas:* rellena el fondo con `self.screen.fill(...)` y utiliza `self.dibujar_rectangulo`, `self.dibujar_circulo` y `self.dibujar_texto` para renderizar cada elemento.

7. **`run`**  
   Implementa el bucle de juego principal: inicializa `pygame`, llama a los métodos anteriores en el orden correcto, controla los FPS con `Clock.tick` y detecta las condiciones de victoria o derrota.  
   *Pistas:* recorre `self.iterar_eventos()` vigilando `self.EVENT_QUIT` y `self.EVENT_KEYDOWN`. Tras cada actualización llama a `self.actualizar_pantalla()` y limita la velocidad con `self.clock.tick(self.FPS)`. Usa `self.finalizar_pygame()` al cerrar.

> Consejo: ve probando tu juego tras completar cada método para evitar acumular errores. Utiliza el bloque `if __name__ == "__main__":` que se incluye al final de la plantilla.

## Recursos
- [Documentación oficial de pygame](https://www.pygame.org/docs/)
- [Tutorial básico de Arkanoid en pygame](https://realpython.com/pygame-a-primer/) (inspírate en la estructura, pero escribe tu propia solución)
- [`PRUEBAS.md`](PRUEBAS.md), con los casos mínimos que deben funcionar antes de entregar.

## Criterios de calidad (bonus)
- Código funcional que respete las anotaciones de tipo y el estilo de la plantilla.
- Control del flujo de juego (inicialización, loop principal y cierre limpio).
- Gestión de colisiones y actualización de puntuación/vidas.
- Apartado opcional: se valorará positivamente añadir niveles extra, mejoras visuales o efectos de sonido siempre que no rompan la estructura base.
