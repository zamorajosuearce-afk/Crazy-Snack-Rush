# ==============================
# IMPORTS
# ==============================

from constantes import *
from ingrediente_plato import Ingrediente


# ==============================
# CLASES DE ESTACIONES
# ==============================

# ESTACIÓN BASE
class Estacion:
    """
    Clase base que representa una estación.
    Maneja los atributos que heredaran el resto de estaciones.
    """

    # INICIADOR
    def __init__(self, x, y, tamano_x, tamano_y, margen_uso):
        self.x = x # Posición en x
        self.y = y # Posición en y
        self.tamano_x = tamano_x # Largo de la estación
        self.tamano_y = tamano_y # Alto de la estación

        margen_x_estacion, margen_y_estacion, margen_largo, margen_alto = margen_uso # Tupla con los márgenes que tendrá el rectángulo del área de uso de la estación
        self.rectangulo_estacion = pygame.Rect(self.x, self.y, self.tamano_x, self.tamano_y) # El rectángulo de la colisión
        self.rectangulo_area_uso = pygame.Rect(self.x + margen_x_estacion, self.y + margen_y_estacion, self.tamano_x + margen_largo, self.tamano_y + margen_alto) # El rectángulo del área de uso


# DISPENSA PLATOS
class DispensaPlatos(Estacion):
    """
    Clase que representa una estación de dispensa de platos.
    Únicamente rectángulos de referencia para colisión y que el chef pase a tener un plato al estar su rectángulo de colisión sobre el área de uso.
    """

    # INICIADOR
    def __init__(self, x, y, tamano_x, tamano_y,margen_uso=None):
        if margen_uso is None: margen_uso = (-20, -20, 40, 40)  # Margen por defecto actual. Esto sirve para acomodar el área de una estación, pero ya tiene una por defecto
        super().__init__(x, y, tamano_x, tamano_y, margen_uso) # Llama al __init__ de la clase padre Estacion para que se ejecute su inicialización

# BASURERO
class Basurero(Estacion):
    """
    Clase que representa una estación basurero.
    Únicamente rectángulos de referencia para colisión y que el chef pasea no tener objeto al estar su rectángulo de colisión sobre el área de uso.
    """
    def __init__(self, x, y, tamano_x, tamano_y, margen_uso = None):
        if margen_uso is None: margen_uso = (-20, 0, 40, 20)  # margen por defecto actual
        super().__init__(x, y, tamano_x, tamano_y, margen_uso)

# ENTREGA
class EstacionEntrega(Estacion):
    """
    Clase que representa una estación de entrega de recetas.
    Únicamente rectángulos de referencia para colisión y que el chef entregue el plato que tiene en manos al estar su rectángulo de colisión sobre el área de uso.
    """

    # INICIADOR
    def __init__(self, x, y, tamano_x, tamano_y):
        super().__init__(x, y, tamano_x, tamano_y, (-50, -50, 100, 100))  # Llama al __init__ de la clase padre Estacion para que se ejecute su inicialización

# DESPENSA
class EstacionDespensa(Estacion):
    """
    Clase que representa una estación de despensa de ingredientes.
    Maneja la lógica para darle el ingrediente al chef según el ingrediente que represente la despensa.
    """

    # INICIADOR
    def __init__(self, x, y, tamano_x, tamano_y, ingrediente_nombre,margen_uso=None):
        if margen_uso is None: margen_uso = (-20, -20, 40, 40)  # Margen por defecto actual. Esto sirve para acomodar el área de una estación, pero ya tiene una por defecto
        super().__init__(x, y, tamano_x, tamano_y, margen_uso) # Llama al __init__ de la clase padre Estacion para que se ejecute su inicialización
        self.ingrediente_nombre = ingrediente_nombre

    # DAR INGREDIENTE
    def dar_ingrediente(self):
        """
        Metodo para darle un ingrediente al chef.
        :return: Devuelve un objeto ingrediente con el nombre del ingrediente que debe dar la estación.
        """

        sprites = sprites_ingredientes[self.ingrediente_nombre] # Carga los sprites del ingrediente
        return Ingrediente(self.ingrediente_nombre, "crudo", sprites) # Devuelve el ingrediente

# MESA
class Mesa(Estacion):
    """
    Clase que representa una estación mesa.
    Únicamente rectángulos de referencia para colisión y que el chef entregue el plato que tiene en manos al estar su rectángulo de colisión sobre el área de uso.
    """

    # INICIADOR
    def __init__(self, x, y, tamano_x, tamano_y, margen_uso=None):
        if margen_uso is None: margen_uso = (-20, -30, 40, 90)  # Margen por defecto actual. Esto sirve para acomodar el área de una estación, pero ya tiene una por defecto
        super().__init__(x, y, tamano_x, tamano_y, margen_uso) # Llama al __init__ de la clase padre Estacion para que se ejecute su inicialización

        self.objeto_mesa = None # El ingrediente que está en la mesa

    # DEJAR OBJETO (En este caso puede ser cualquier objeto, ingrediente es para que funcione el programa)
    def dejar_ingrediente(self, objeto):
        """
        Metodo para dejar un objeto en la mesa.
        :param objeto: El objeto que deja el chef.
        :return: Devuelve True si se pudo poner el objeto sobre la mesa, False si no se pudo.
        """

        if self.objeto_mesa is None and objeto is not None: # Si la mesa no tiene un objeto y si el chef sí tiene un objeto
            self.objeto_mesa = objeto # El objeto de la mesa pasa a ser el que deja el chef
            return True # Se pudo poner sobre la mesa

        return False # No se pudo poner (la mesa ya tiene un objeto o el chef no tiene objeto)

    # RECOGER OBJETO (En este caso puede ser cualquier objeto, ingrediente es para que funcione el programa)
    def recoger_ingrediente(self):
        """
        Metodo para recoger un objeto de la mesa.
        :return: Devuelve None si no hay nada en la mesa, y el objeto si sí hay un objeto en la mesa.
        """

        if self.objeto_mesa is not None: # Si el objeto no es None
            objeto = self.objeto_mesa # El objeto a entregar es el que está en la mesa
            self.objeto_mesa = None # Se vacía la mesa
            return objeto # Se devuelve el objeto
        return None # Si no hay objeto no se devuelve nada

    # VER OBJETO (En este caso puede ser cualquier objeto, ingrediente es para que funcione el programa)
    def ver_ingrediente(self):
        """
        Metodo para ver el objeto que está en la mesa, sin quitarlo.
        """

        return self.objeto_mesa

    def dibujar(self, pantalla):
        """
        Metodo para dibujar lo que hay en la mesa.
        :param pantalla: La pantalla sobre la que se dibujará el objeto que está en la mesa.
        """

        if self.objeto_mesa is not None: # Si hay un objeto sobre la mesa
            sprite = self.objeto_mesa.obtener_sprite() # Se obtiene el sprite del objeto
            pantalla.blit(sprite, (self.x + self.tamano_x // 2 - 10, self.y )) # Se dibuja el sprite del objeto

# TRABAJO (tabla, cocina, freidora)
class EstacionTrabajo(Estacion):
    """
    Clase que representa una estación de trabajo (tabla, cocina, freidora).
    Maneja la lógica de freír, cocinar y picar alimentos, así como barras de quemado y de cocinado-freído.
    """

    # INICIADOR
    def __init__(self, x, y, tamano_x, tamano_y, tipo, margen_uso=None):
        if margen_uso is None: margen_uso = (-35, -35, 70, 70)  # Margen por defecto actual. Esto sirve para acomodar el área de una estación, pero ya tiene una por defecto
        super().__init__(x, y, tamano_x, tamano_y, margen_uso) # Llama al __init__ de la clase padre Estacion para que se ejecute su inicialización

        self.tipo = tipo # El tipo de estación de trabajo (cocina, freidora, tabla)

        self.progreso = 0 # Progreso en cocinado, freido o picado
        self.procesando = False # Para ver si se progresa antes de llegar a cocinado, freido o picado
        self.progreso_quemado = 0 # Para ver si se progresa antes de llegar a quemado

        self.ingrediente_estacion = None # El ingrediente que hay en la estación, ninguno al inicio

    # ACTUALIZAR
    def actualizar(self, cambio_tiempo, chef_en_area, c_presionado):
        """
        Metodo para actualizar la estación de trabajo: lo que se muestra, el estado del alimento que procesa.
        :param cambio_tiempo: Tiempo desde el último frame.
        :param chef_en_area: True o False dependiendo si el chef está en el área de trabajo de la estación.
        :param c_presionado: True o False dependiendo de si C se está presionando.
        """

        if self.tipo == "tabla": # Si el tipo de estación de trabajo es tabla
            # La tabla solo avanza mientras el chef mantiene C sobre ella con ingrediente
            if (
                    self.ingrediente_estacion is not None and # Si hay un ingrediente en la tabla
                    self.ingrediente_estacion.estado not in "picado" and # Si el ingrediente todavía no está picado
                    chef_en_area and # Si el chef está en el área de uso
                    c_presionado # Si se presiona la C
            ):

                self.procesando = True # Pasa a procesar
                self.progreso += cambio_tiempo / duracion_tabla # Lo que avanza cada frame en relación con el tiempo de duracion

                # Si llega a 1 significa que pasaron los segundos de la duración de la tabla
                if self.progreso >= 1: # Si el progreso es mayor a 1 o igual a 1
                    self.progreso = 1 # Se queda el progreso en 1
                    self.ingrediente_estacion.estado = "picado" # El estado del ingrediente que está en la estacion pasa a ser picado
            else:
                self.procesando = False # Si no se cumple alguna de las condiciones no se pica el ingrediente

        elif self.tipo == "cocina": # Si el tipo de estación de trabajo es cocina
            if self.ingrediente_estacion is not None: # Si hay un ingrediente en la estación de trabajo
                ingrediente_actual = self.ingrediente_estacion # El ingrediente actual en la estación
                estado_entrada = ingredientes_cocina[ingrediente_actual.nombre] # El estado que debería tener el ingrediente para poder cocinarse

                if ingrediente_actual.estado == estado_entrada:  # Si el ingrediente está en el estado de entrada a la cocina
                    self.progreso += cambio_tiempo / duracion_cocina # Lo que avanza cada frame en relación con el tiempo de duracion

                    # Si llega a 1 significa que pasaron los segundos de la duración de la cocina
                    if self.progreso >= 1:  # Si el progreso es mayor a 1 o igual a 1
                        self.progreso = 1 # Se queda el progreso en 1
                        ingrediente_actual.estado = "cocinado" # El estado del ingrediente que está en la estacion pasa a ser cocinado

                elif ingrediente_actual.estado == "cocinado":  # Si el ingrediente ya se cocinó
                    self.progreso_quemado += cambio_tiempo / duracion_quemado_cocina # Lo que avanza cada frame en relación con el tiempo de duracion de quemado

                    # Si llega a 1 significa que pasaron los segundos de la duración de quemado de la cocina
                    if self.progreso_quemado >= 1:  # Si el progreso de quemado es mayor a 1 o igual a 1
                        self.progreso_quemado = 1 # Se queda el progreso en 1
                        ingrediente_actual.estado = "quemado" # El estado del ingrediente que está en la estacion pasa a ser quemado

        elif self.tipo == "freidora": # Si el tipo de estación de trabajo es freidora
            if self.ingrediente_estacion is not None: # Si hay un ingrediente en la estación de trabajo
                ingrediente_actual = self.ingrediente_estacion # El ingrediente actual en la estación
                estado_entrada = ingredientes_freidora[ingrediente_actual.nombre] # El estado que debería tener el ingrediente para poder freírse

                if estado_entrada is not None and ingrediente_actual.estado == estado_entrada:  # Si el ingrediente está en el estado de entrada a la freidora
                    self.progreso += cambio_tiempo / duracion_freidora # Lo que avanza cada frame en relación con el tiempo de duracion

                    # Si llega a 1 significa que pasaron los segundos de la duración de la freidora
                    if self.progreso >= 1: # Si el progreso es mayor a 1 o igual a 1
                        self.progreso = 1 # Se queda el progreso en 1
                        ingrediente_actual.estado = "frito" # El estado del ingrediente que está en la estacion pasa a ser frito

                elif ingrediente_actual.estado == "frito":  # Si el ingrediente ya se frío
                    self.progreso_quemado += cambio_tiempo / duracion_quemado_freidora # Lo que avanza cada frame en relación con el tiempo de duracion de quemado
                    if self.progreso_quemado >= 1: # Si el progreso de quemado es mayor a 1 o igual a 1
                        self.progreso_quemado = 1 # Se queda el progreso en 1
                        ingrediente_actual.estado = "quemado" # El estado del ingrediente que está en la estacion pasa a ser quemado

    # DEJAR
    def dejar_ingrediente(self, ingrediente):
        """
        Metodo para dejar un ingrediente en la estación según el tipo de estación de trabajo.
        :param ingrediente: El ingrediente que se evaluará para ser dejado en la estación de trabajo.
        :return: True si sí se pudo dejar, False si no.
        """

        # Carga los ingredientes válidos según el tipo de estación de trabajo
        if self.tipo == "tabla":
            ingredientes_validos = ingredientes_tabla
        elif self.tipo == "cocina":
            ingredientes_validos = ingredientes_cocina
        elif self.tipo == "freidora":
            ingredientes_validos = ingredientes_freidora
        else:
            return False # Evitar error por no crear la variable de ingredientes válidos


        if (
                self.ingrediente_estacion is None and # Si no hay ingredientes en la estación
                isinstance(ingrediente, Ingrediente) and # Si es un ingrediente y no un plato o None
                ingrediente.nombre in ingredientes_validos and # Si el ingrediente está en los ingredientes válidos para el tipo de estación de trabajo
                ingrediente.estado == ingredientes_validos[ingrediente.nombre] # Si está en el estado válido
        ):
            self.ingrediente_estacion = ingrediente # El ingrediente de la estación pasa a ser el ingrediente dado
            return True # Devuelve True, pues sí se pudo dejar
        return False # Devuelve False si no se pudo dejar

    # RECOGER
    def recoger_ingrediente(self):
        """
        Metodo para dejar un ingrediente en la estación según el tipo de estación de trabajo.
        :return: Devuelve el ingrediente si sí se puede agarrar, y None si no.
        """

        if self.ingrediente_estacion is not None: # Si hay un ingrediente en la estación
            ingrediente = self.ingrediente_estacion # Se carga el ingrediente
            self.ingrediente_estacion = None # Se quita el ingrediente
            self.progreso = 0 # Se reinicia el progreso para que el siguiente ingrediente empiece con 0
            self.progreso_quemado = 0 # Se reinicia el progreso de quemado para que el siguiente ingrediente empiece con 0
            return ingrediente # Se devuelve el ingrediente si sí se puede agarrar
        return None # Se devuelve None si no se puede agarrar

    # VER
    def ver_ingrediente(self):
        """
        Metodo para ver el objeto que está en la estación de trabajo, sin quitarlo.
        """

        return self.ingrediente_estacion

    # DIBUJAR
    def dibujar(self, pantalla):
        """
        Metodo para dibujar lo que hay en la estación de trabajo.
        :param pantalla: La pantalla sobre la que se dibujará el objeto que está en la estación de trabajo.
        """

        # Dibujar el ingrediente
        if self.ingrediente_estacion is not None: # Si hay un ingrediente en la estación de trabajo
            sprite = self.ingrediente_estacion.obtener_sprite() # Se carga el sprite del ingrediente
            pantalla.blit(sprite, (self.x + self.tamano_x // 2 - 10, self.y )) # Se dibuja en medio -10

        # Barra de progreso (tabla)
        if self.progreso > 0 and self.tipo == "tabla": # Si la estación es una tabla
            pygame.draw.rect(pantalla, (200, 200, 200), (self.x, self.y - 12, self.tamano_x, 6)) # Rectángulo gris. -12 para estar arriba de la tabla
            pygame.draw.rect(pantalla, (0, 200, 0), (self.x, self.y - 12, int(self.tamano_x * self.progreso), 6)) # Rectángulo verde. int(self.tamano_x * self.progreso) avanzando según el progreso

        # Barra de cocción verde (cocina-freidora)
        if 0 < self.progreso < 1 and self.tipo in ("cocina", "freidora"): # Si el progreso está entre 0 y 1 se va dibujando la barra de cocinado
            pygame.draw.rect(pantalla, (200, 200, 200), (self.x, self.y - 20, self.tamano_x, 6)) # Rectángulo gris. -20 para estar arriba de la cocina o freidora
            pygame.draw.rect(pantalla, (0, 200, 0), (self.x, self.y - 20, int(self.tamano_x * self.progreso), 6)) # Rectángulo verde. int(self.tamano_x * self.progreso) avanzando según el progreso

        # Barra de quemado naranja (cocina / freidora)
        if self.progreso_quemado > 0 and self.tipo in ("cocina", "freidora"): # Si el progreso de quemado es mayor a 0
            pygame.draw.rect(pantalla, (200, 200, 200),(self.x, self.y - 20, self.tamano_x, 6)) # Rectángulo gris. -20 para estar arriba de la cocina o freidora
            pygame.draw.rect(pantalla, (255, 140, 0), (self.x, self.y - 20, int(self.tamano_x * self.progreso_quemado), 6)) # Rectángulo naranja. int(self.tamano_x * self.progreso) avanzando según el progreso de quemado
