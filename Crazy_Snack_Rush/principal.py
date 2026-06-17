# ==============================
# IMPORTS
# ==============================

from pantallas import *
from constantes import *

# ==============================
# PANTALLA DEL JUEGO
# ==============================

# INICIALIZACIÓN DE JUEGO

pygame.init() # Inicia pygame

pantalla = pygame.display.set_mode((ancho, alto)) # Muestra la pantalla

pygame.display.set_caption(titulo) # Cambia el título

clock = pygame.time.Clock() # Objeto reloj que sirve para controlar el ritmo del juego (los FPS)

# ==============================
# BUCLE PRINCIPAL
# ==============================

ejecutando = True # Mientras se ejecute se mostrará el juego
pantalla_actual = Cocina2() # La pantalla que se muestra al inicio es el Menú

while ejecutando:
    cambio_tiempo = clock.tick(fps) / 1000.0
    """
    clock.tick(fps) devuelve el tiempo transcurrido desde el último frame en milisegundos, y límita la velocidad del bucle para que no supere los 60 FPS.
    Se divide por 1000.0 para convertirlo a segundos.
    Entonces cambio_tiempo el tiempo que transcurrió desde el último frame en segundos.
    """

    eventos = pygame.event.get() # Se obtienen los eventos

    for evento in eventos:
        if evento.type == pygame.QUIT:
            ejecutando = False # Si se quita, deja de ejecutarse el juego

    # MANEJAR EVENTOS DE LA VENTANA
    pantalla_actual = pantalla_actual.manejar_eventos(eventos) # Cada pantalla devuelve una pantalla según los eventos

    # MANEJAR SI SE ACABA EL TIEMPO
    resultado = pantalla_actual.actualizar(cambio_tiempo) # Normalmente se devuelve None, pero cuando finaliza el tiempo se devuelve la siguiente pantalla

    if resultado is not None: # Si el resultado es la siguiente pantalla
        pantalla_actual = resultado # Se actualiza la pantalla actual

    # DIBUJAR LA PANTALLA ACTUAL
    pantalla_actual.dibujar(pantalla) # Se dibuja lo que hay en cada pantalla
    pygame.display.flip() # Actualiza la pantalla mostrando lo que se dibujó en este frame


pygame.quit() # Finaliza pygame
