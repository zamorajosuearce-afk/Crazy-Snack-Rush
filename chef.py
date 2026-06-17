# ==============================
# IMPORTS
# ==============================

from constantes import margenes_objeto_cargado
import pygame

# ==============================
# CLASE DE CHEF
# ==============================

class Chef:
    """
    Clase que representa un chef.
    Guarda la lógica detrás de los chefs, los objetos que sostienen, su movimiento y de dibujar sus sprites y el de los objetos que sostienen.
    """

    # INICIADOR
    def __init__(self, x, y, sprites, margen_x, margen_y, largo_colision_chef, alto_colision_chef):
        # POSICIÓN Y MOVIMIENTO
        self.x = x # Posición en x
        self.y = y # Posición en y
        self.velocidad = 400 # Velocidad de movimiento del chef

        # COLISIÓN
        self.margen_x = margen_x # El movimiento en x para posicionar el rectángulo de colisión, desde el inicio del sprite del chef
        self.margen_y = margen_y # El movimiento en y para posicionar el rectángulo de colisión, desde el inicio del sprite del chef
        self.largo_colision_chef = largo_colision_chef # El largo del rectángulo de colisión del chef
        self.alto_colision_chef = alto_colision_chef # El alto del rectángulo de colisión del chef

        # SPRITES
        self.sprites = sprites # Se agarra de constantes después, es un diccionario con movimientos y las imágenes de los sprites de los movimientos

        # ANIMACIÓN
        self.direccion = "abajo" # Empieza mirando hacia abajo con el sprite hacia abajo quedito
        self.frame_actual = 0 # El frame actual indica si el sprite está quedito o en movimiento, 0 es quedito
        self.temporizador_animacion = 0 # Define cada cuántos segundos cambia el frame del sprite
        self.velocidad_animacion = 0.15 # Va sumando el cambio_tiempo de cada frame hasta llegar a 0.15, cuando llega cambia el frame y se reinicia a 0

        # OBJETOS O INGREDIENTES
        self.objeto_cargado = None

    # ACTUALIZADOR (actualiza movimiento y animación).
    def actualizar(self, cambio_tiempo, obstaculos):
        """
        Metodo para actualizar al chef: su movimiento, colisión, posición.
        :param cambio_tiempo: Tiempo desde el último frame.
        :param obstaculos: la lista de rectángulos invisibles con los que puede colisionar el chef. (estaciones y paredes)
        """

        teclas = pygame.key.get_pressed() # Se obtienen las teclas que se presionen
        movimiento_x, movimiento_y = 0, 0 # El movimiento empieza en 0 y 0, pues no se está moviendo

        # MOVIMIENTO GENERAL
        if teclas[pygame.K_w]: movimiento_y = -1 # Solo la direccion (arriba) si se presiona W
        if teclas[pygame.K_s]: movimiento_y = 1 # Solo la direccion (abajo) si se presiona S
        if teclas[pygame.K_a]: movimiento_x = -1 # Solo la direccion (izquierda) si se presiona A
        if teclas[pygame.K_d]: movimiento_x = 1 # Solo la direccion (derecha) si se presiona D

        # MOVIMIENTO Y COLISIÓN EN X
        self.x += movimiento_x * self.velocidad * cambio_tiempo
        """
        Cuántos píxeles le toca avanzar en este frame específico para mantener una velocidad constante sin importar los FPS.
        La velocidad = 200 y cambio_tiempo = 1/60 ≈ 0.0167, entonces en ese frame se mueve 200 * 0.0167 ≈ 3.33 pixeles.
        En un segundo (60 frames), se moverá 200 pixeles en total, sin importar los FPS.
        Se suma a self.x y self.y para el movimiento del chef.
        """

        # COLISIÓN X (área y obstáculos)
        rectangulo_chef = pygame.Rect(self.x + self.margen_x, self.y + self.margen_y, self.largo_colision_chef, self.alto_colision_chef) # El rectángulo de colisión del chef

        for estacion in obstaculos:
            if rectangulo_chef.colliderect(estacion): #.colliderect detecta si dos rectángulos se superponen, en este caso el del chef y la estación
                if movimiento_x > 0: # Detecta si se movía a la derecha
                    self.x = estacion.left - self.largo_colision_chef - self.margen_x # Devuelve al chef al borde izquierdo de la estación, resta a la posicion derecha de la estación el largo del chef, para actualizar la posición x
                elif movimiento_x < 0: # Detecta se movía a la izquierda
                    self.x = estacion.right - self.margen_x # Devuelve al chef al borde derecho de la estación
                """
                En un caso el rectángulo de los pies entra por la derecha al de la estación, por lo que se ajusta self.x para que el borde
                derecho del rectángulo de los pies concuerde con el borde izquierdo de la estación (restando largo_colision_chef y
                margen_x para volver a la posición del sprite). En el otro caso simplemente se hace que concuerde el borde izquierdo
                del rectángulo de los pies con el borde derecho de la estación (restando solo margen_x).
                """

        # MOVIMIENTO Y COLISIÓN EN Y
        self.y += movimiento_y * self.velocidad * cambio_tiempo

        # COLISIÓN Y (area y obstáculos)
        rectangulo_chef = pygame.Rect(self.x + self.margen_x, self.y + self.margen_y, self.largo_colision_chef, self.alto_colision_chef) # El rectangulo de colisión del chef (se actualiza)
        for estacion in obstaculos:
            if rectangulo_chef.colliderect(estacion):
                if movimiento_y > 0:  # Detecta si se movía hacia abajo
                    self.y = estacion.top - self.alto_colision_chef - self.margen_y # Devuelve al chef al borde superior de la estación, resta a la posicion superior de la estación el alto del chef, para actualizar la posición y
                elif movimiento_y < 0:  # Detecta se movía hacia arriba
                    self.y = estacion.bottom - self.margen_y # Devuelve al chef al borde inferior de la estación
                """
                En un caso el rectángulo de los pies entra por arriba de la estación, por lo que se ajusta self.y para que el borde
                inferior del rectángulo de los pies concuerde con el borde superior de la estación (restando alto_colision_chef y
                margen_y para volver a la posición del sprite). En el otro caso simplemente se hace que concuerde el borde superior
                del rectángulo de los pies con el borde inferior de la estación (restando solo margen_y).
                """

        # DIRECCIÓN
        direccion_anterior = self.direccion # Empieza mirando hacia abajo. Pero se actualiza a medida que se mueve. Sirve para reiniciar frames

        if movimiento_y < 0:
            self.direccion = "arriba" # Únicamente para las animaciones, según hacia donde se mueva esa será la dirección.
        elif movimiento_y > 0:
            self.direccion = "abajo"
        elif movimiento_x < 0:
            self.direccion = "izquierda"
        elif movimiento_x > 0:
            self.direccion = "derecha"

        if self.direccion != direccion_anterior: # Si cambia se cambia de dirección se reinicia el frame y el temporizador para la animación.
            self.frame_actual = 0
            self.temporizador_animacion = 0

        # ANIMACIÓN
        if movimiento_x == 0 and movimiento_y == 0: #Si no hay movimiento el frame que se muestra es el 0 (quedito)
            self.frame_actual = 0
        else:
            self.temporizador_animacion += cambio_tiempo # cada 0.15 segundos se avanza un frame de animación, sin importar los FPS del juego, se suma el cambio de tiempo sin importar los FPS
            if self.temporizador_animacion >= self.velocidad_animacion: # si se supera la velocidad de animacion se reinicia el temporizador de la animación y se cambia de frame, según el actual
                self.temporizador_animacion = 0
                if self.direccion in ("izquierda", "derecha"): # si la dirección es derecha o izquierda cambia solo entre los dos frames que tienen estas direcciones
                    if self.frame_actual == 0: # si el frame actual es 0 cambia a 1
                        self.frame_actual = 1
                    else:                      # si el frame actual es 1 cambia a 0
                        self.frame_actual = 0
                else:                                          # si la dirección es arriba o abajo se cambia el frame entre los 3 que hay.
                    if self.frame_actual == 0 or self.frame_actual == 2: # 0 es quedito, así que pasa de quedito (0) a moverse (1) y luego alterna entre (1) y (2)
                        self.frame_actual = 1
                    else:
                        self.frame_actual = 2

    # DIBUJAR
    def dibujar(self, pantalla):
        """
        Metodo para dibujar al chef y el objeto que sostiene.
        :param pantalla: La pantalla sobre la que se dibujará el chef y el objeto que sostiene.
        """

        imagen = self.sprites[self.direccion][self.frame_actual] # Se carga la imagen actual del chef

        # SUPERPOSICIÓN CHEF-OBJETO O OBJETO-CHEF
        if self.objeto_cargado is not None: # Para que no intente cargar la imagen de un None
            margen_x, margen_y = margenes_objeto_cargado[self.direccion]  # Carga los margenes según la direccióna
            pos_objeto = (self.x + margen_x, self.y + margen_y) # Una tupla con la que dará la posición del objeto
            sprite_objeto = self.objeto_cargado.obtener_sprite() # Funciona para Plato e Ingrediente

            if self.direccion == "arriba": # Si la dirección es arriba
                pantalla.blit(sprite_objeto, pos_objeto)  # Primero el objeto (detrás)
                pantalla.blit(imagen, (self.x, self.y))  # Luego el chef (encima)
            else:
                pantalla.blit(imagen, (self.x, self.y))  # Primero el chef
                pantalla.blit(sprite_objeto, pos_objeto)  # Luego el objeto (encima)
        else:
            pantalla.blit(imagen, (self.x, self.y)) #  Por si objeto es None igual se carga el chef
