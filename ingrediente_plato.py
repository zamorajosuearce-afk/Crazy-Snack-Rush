# ==============================
# IMPORTS
# ==============================

from constantes import *

# ==============================
# CLASE DE INGREDIENTES
# ==============================

class Ingrediente:
    """
    Clase que representa un ingrediente.
    Es la encargada de la lógica detrás de los ingredientes.
    """

    # INICIADOR
    def __init__(self, nombre, estado, sprites):
        self.nombre = nombre  # Nombre del ingrediente
        self.estado = estado  # Estado actual
        self.sprites = sprites  # Diccionario con sprites según estado

    # OBTENER ESTADO
    def obtener_sprite(self):
        """
        Metodo que devuelve el sprite del estado actual del ingrediente.
        """

        return self.sprites[self.estado]  # Se usa al dibujar el ingrediente que sostiene el chef o al dibujarlo en alguna estación

# ==============================
# CLASE PLATO
# ==============================

class Plato:
    """
    Clase que representa un plato.
    Es la encargada de la lógica detrás de los platos.
    """

    # INICIADOR
    def __init__(self):
        self.ingredientes = []  # Lista de ingredientes dentro del plato (solo 1)
        self.sprite = sprites_plato["vacio"] # El sprite actual del plato, empieza vacío

    # AGREGAR UN INGREDIENTE AL PLATO
    def agregar_ingrediente(self, ingrediente):
        """
        Metodo que agrega un ingrediente al plato.
        :param ingrediente: Ingrediente que se va a intentar agregar.
        :return: False si no se puede agregar el ingrediente al plato y True si sí se puede.
        """

        # VERIFICAR SI EL ESTADO ES VALIDO
        if not self.estado_valido(ingrediente): # Lo envía al metodo que evalúa si su estado es válido
            return False # Si no es válido devuelve False

        # VERIFICA SI EL PLATO YA TIENE UNA FUSIÓN
        if len(self.ingredientes) == 1: # Si el plato ya tiene un ingrediente
            fusion = self.intentar_fusion(ingrediente) # Intenta hacer una fusión
            if fusion is not None: # Si se hizo una fusión
                self.ingredientes = [fusion] # Se actualiza el ingrediente al objeto ingrediente que devuelve la fusion
                self.actualizar_sprite() # Y se actualiza el sprite para que concuerde con ls fusión
                return True # Devuelve True, pues si se pudo hacer una fusión y agregarla al plato
            return False  # No se puede fusionar, devuelve False, pues no se agregó nada al plato

        # SI EL PLATO ESTÁ VACÍO SE AGREGA DIRECTAMENTE
        self.ingredientes.append(ingrediente) # Se agrega el ingrediente a la lista de ingredientes del plato
        self.actualizar_sprite() # Se actualiza el sprite para que concuerde con lo que hay en el plato
        return True # Devuelve True, pues el ingrediente se agregó al plato.

    # ==============================
    # LÓGIA INTERNA
    # ==============================

    # VERIFICAR SI EL ESTADO DE UN INGREDIENTE ES VALIDO PARA EL PLATO
    def estado_valido(self,ingrediente):
        """
        Metodo que verifica que el estado de un ingrediente sea válido para ponerlo en el plato.
        :return: Devuelve True si el estado es válido para el plato, False si no lo es.
        """

        # VERIFICAR SI EL INGREDIENTE ES POLLO Y ESTÁ DENTRO DE LOS ESTADOS VALIDOS
        if ingrediente.nombre == "pollo": # Caso especial del pollo. Evalúa primero si el ingrediente es pollo porque es un caso especial
            return ingrediente.estado in ("frito", "cocinado") # Si el estado del pollo es frito o cocinado se agrega al plato, devuelve True, si no False

        # VERIFICAR SI EL ESTADO ACTUAL DEL INGREDIENTE ES IGUAL ESTADO VALIDO DEL INGREDIENTE
        estado_requerido = estados_validos_para_plato[ingrediente.nombre] # Carga el estado requerido del ingrediente para ser agregado al plato
        return ingrediente.estado == estado_requerido # Devuelve True o False según si el estado actual del ingrediente es igual al estado requerido

    # INTENTAR FUSIONAR INGREDIENTES
    def intentar_fusion(self, ingrediente_nuevo):
        """
        Metodo que se puedan fusionar dos ingredientes dentro del plato.
        :return: Un Objeto ingrediente que representa la fusión, o None si no se logra obtener el nombre de alguna fusión.
        """

        ingrediente_actual = self.ingredientes[0] # Cargamos el ingrediente actual aca para más legibilidad
        clave = frozenset([(ingrediente_actual.nombre, ingrediente_actual.estado),(ingrediente_nuevo.nombre, ingrediente_nuevo.estado)])
        """
        Formamos la clave para buscar en el diccionario de fusiones que se pueden tener dentro del plato.
        """

        nombre_fusion = fusiones_plato.get(clave) # Obtiene el nombre de la fusión si existe, si no existe devuelve None.
        if nombre_fusion is not None: # Si sí se logró obtener un nombre
            """
            Se devuelve un objeto ingrediente nuevo que representa a la fusión que va a estar en el plato.
            Esto es importante porque las fusiones solo se realizan en el plato. Por lo que el ingrediente de esa fusión anteriormente no existía.
            """
            return Ingrediente(nombre_fusion, "cocinado", {}) # Ingrediente con el nombre de la fusión y con estado cocinado, sin sprites porque los sprites dependen del plato.

        return None # Si no se logra obtener el nombre de alguna fusion se devuelve None

    # ==============================
    # SPRITES
    # ==============================

    # OBTENER SPRITE
    def obtener_sprite(self):
        """
        Metodo que devuelve el sprite actual del plato.
        """

        return self.sprite # Se usa al dibujar el plato que sostiene el chef o al dibujarlo en alguna mesa

    # ACTUALIZAR SPRITE SPRITE
    def actualizar_sprite(self):
        """
        Metodo que actualiza el sprite del plato según lo que haya en él.
        """

        ingrediente = self.ingredientes[0] # El único ingrediente del plato

        if ingrediente.nombre == "pollo": # Caso especial del pollo, ya que puede ser frito o cocinado
            clave = f"pollo_{ingrediente.estado}" # Forma la clave según el estado del pollo
            self.sprite = sprites_plato[clave] # Se actualiza el sprite a la imagen del plato con el pollo cocinado o frito
        else:
            self.sprite = sprites_plato[ingrediente.nombre] # Se actualiza el sprite a la imagen del plato con el ingrediente