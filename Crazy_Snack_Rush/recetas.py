# ==============================
# IMPORTS
# ==============================

from constantes import *

# ==============================
# CLASE RECETA
# ==============================

class Receta:
    """
    Clase que representa una receta.
    Es la encargada de generar las recetas de manera aleatoria y mostrar el plato que se debe entregar en la estación de entrega.
    """

    # INICIADOR
    def __init__(self, nombre):
        self.nombre = nombre # Nombre de la receta
        puntos = puntos_recetas[nombre] # Los puntos de esa receta
        self.tiempo_total = duracion_receta[puntos] # Lo que dura en vencer la receta según los puntos que brinda
        self.tiempo_restante = self.tiempo_total # El tiempo que queda para que la receta venza, empieza con el tiempo total que tiene para vencer.
        self.vencida = False # Si la receta se venció, empieza en False, pues no se ha vencido

    # ACTUALIZADOR (actualiza el tiempo que queda para que venza y el estado de vencida o no)
    def actualizar(self, cambio_tiempo):
        """
        Metodo para actualizar la receta.
        :param cambio_tiempo: Tiempo desde el último frame.
        """

        if not self.vencida: # Si no se ha vencido
            self.tiempo_restante -= cambio_tiempo # Se baja un segundo real sin importar los FPS al tiempo restante
            if self.tiempo_restante <= 0: # Si el tiempo baja de 0 o es igual a 0
                self.tiempo_restante = 0 # El tiempo que resta para dicha receta vuelve a 0
                self.vencida = True # Está vencida, ahora el self.vencida es True

    # DIBUJAR
    def dibujar(self, pantalla, x, y):
        """
        Metodo para dibujar la receta y la barra que representa el tiempo que queda antes de que la receta venza.
        :param pantalla: La pantalla sobre la receta y la barra de tiempo.
        :param x: La x de la receta y la barra de tiempo.
        :param y: La y de la receta y la barra de tiempo. (se suma 65 a la barra de tiempo para que esta aparezca debajo de la receta).
        """

        sprite = sprites_plato_interfaz[self.nombre] # Carga el sprite del plato de la lista de los sprites del plato para la interfaz
        pantalla.blit(sprite, (x, y)) # Dibujar el sprite en pantalla

        # BARRA DE TIEMPO
        pygame.draw.rect(pantalla, (200, 200, 200), (x, y + 65, 60, 8)) # La barra gris de abajo. Se suma 65 a "y" para que la barra quede debajo del sprite

        progreso = self.tiempo_restante / self.tiempo_total # El progreso es el porcentaje que queda del tiempo de la receta respecto al tiempo total
        if progreso > 0.5: # Si el progreso es mayor a la mitad la barra es de color verde
            color = (0, 200, 0)
        elif progreso > 0.25: # Si el progreso está entre 25% y 50% la barra es amarilla
            color = (255, 165, 0)
        else: # Si el progreso es menor a 25% el color de la barra es rojo
            color = (255, 0, 0)

        # Dibuja el rectángulo de color, según el tiempo que queda antes de que se venza
        pygame.draw.rect(pantalla, color, (x, y + 65, int(60 * progreso), 8))
        """
        int(60 * progreso) hace que la barra vaya disminuyendo según el porcentaje que queda antes de que la receta venza. 
        int() por que progreso es un float, y pygame.draw.rect acepta integers.
        """
