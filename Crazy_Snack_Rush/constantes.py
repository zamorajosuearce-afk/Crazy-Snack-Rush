# ==============================
# IMPORTS
# ==============================

import pygame

# ==============================
# CONSTANTES DE LA PANTALLA
# ==============================

# ANCHO DE LA VENTANA
ancho = 1200

# ALTO DE LA VENTANA
alto = 800

# FPS FIJOS A LOS QUE CORRERÁ EL PROGRAMA
fps = 60

# TÍTULO
titulo = "Crazy Snack Rush TEC" # Título que se usa para la ventana

# ==============================
# CONSTANTES DE CHEFS
# ==============================

# SPRITES DE PIGU
sprites_pigu = { # Usados para cargar las animaciones del chef Pigu
    "arriba": [pygame.image.load("sprites_pigu/back_quiet.png"),
               pygame.image.load("sprites_pigu/back_cam_1.png"),
               pygame.image.load("sprites_pigu/back_cam_2.png")],
    "abajo": [pygame.image.load("sprites_pigu/front_quiet.png"),
              pygame.image.load("sprites_pigu/front_cam_1.png"),
              pygame.image.load("sprites_pigu/front_cam_2.png")],
    "izquierda": [pygame.image.load("sprites_pigu/izq_quiet.png"),
                  pygame.image.load("sprites_pigu/izq_cam_1.png")],
    "derecha": [pygame.image.load("sprites_pigu/der_quiet.png"),
                pygame.image.load("sprites_pigu/der_cam_1.png")],
}

# SPRITES DE ROBO
sprites_robo = { # Usados para cargar las animaciones del chef Robo
    "arriba": [pygame.image.load("sprites_robo/back_quiet.png"),
               pygame.image.load("sprites_robo/back_cam_1.png"),
               pygame.image.load("sprites_robo/back_cam_2.png")],
    "abajo": [pygame.image.load("sprites_robo/front_quiet.png"),
              pygame.image.load("sprites_robo/front_cam_1.png"),
              pygame.image.load("sprites_robo/front_cam_2.png")],
    "izquierda": [pygame.image.load("sprites_robo/izq_quiet.png"),
                  pygame.image.load("sprites_robo/izq_cam_1.png")],
    "derecha": [pygame.image.load("sprites_robo/der_quiet.png"),
                pygame.image.load("sprites_robo/der_cam_1.png")],
}

# MÁRGENES DEL RECTÁNGULO DE COLISIÓN DE AMBOS CHEFS
margen_x_pigu = 5 # El movimiento en x para posicionar el rectángulo de colisión desde el inicio del sprite de Pigu
margen_x_robo = 10 # El movimiento en x para posicionar el rectángulo de colisión desde el inicio del sprite de Robo
margen_y = 50 # El movimiento en y para posicionar el rectángulo de colisión desde el inicio del sprite de ambos chefs
"""
Esto es por que si el rectángulo de colisión empieza desde el inicio del sprite, empezaría en la cabeza del personaje
y no empezaría en sus pies. Es decir, esto es para que el rectángulo de colisión esté en los pies del personaje.
"""

# TAMAÑOS DEL RECTÁNGULO DE COLISIÓN DE AMBOS CHEFS
largo_colision_pigu = 40 # El largo del rectángulo de colisión de Pigu
largo_colision_robo = 50 # El largo del rectángulo de colisión de Robo
alto_colision_chef = 30 # El alto del rectángulo de colisión de ambos chefs

# ==============================
# CONSTANTES DE OBJETO CARGADO
# ==============================

# MÁRGENES DEL OBJETO CARGADO DE AMBOS CHEFS
margenes_objeto_cargado = { # Donde se posiciona el objeto respecto al sprite del chef, según la dirección a la que este mire
    "arriba": (13, -10),
    "abajo": (13, 60),
    "izquierda": (-25, 30),
    "derecha": (50, 30),
}

# ==============================
# CONSTANTES DE INGREDIENTES
# ==============================

# SPRITES DEL PLÁTANO
sprites_platano = { # Los sprites según el estado en el que esté el plátano
    "crudo": pygame.image.load("sprites_ingredientes/platano_crudo.png"),
    "picado": pygame.image.load("sprites_ingredientes/platano_picado.png"),
    "frito": pygame.image.load("sprites_ingredientes/platano_frito.png"),
    "quemado": pygame.image.load("sprites_ingredientes/platano_quemado.png")
}

# SPRITES DEL HUEVO
sprites_huevo = {
    "crudo": pygame.image.load("sprites_ingredientes/huevo_crudo.png"),
    "frito": pygame.image.load("sprites_ingredientes/huevo_frito.png"),
    "quemado": pygame.image.load("sprites_ingredientes/huevo_quemado.png")
}

# SPRITES DEL ARROZ
sprites_arroz = {
    "crudo": pygame.image.load("sprites_ingredientes/arroz_crudo.png"),
    "cocinado": pygame.image.load("sprites_ingredientes/arroz_cocinado.png"),
    "quemado": pygame.image.load("sprites_ingredientes/arroz_quemado.png")
}

# SPRITES DE LOS FRIJOLES
sprites_frijoles = {
    "crudo": pygame.image.load("sprites_ingredientes/frijoles_crudo.png"),
    "cocinado": pygame.image.load("sprites_ingredientes/frijoles_cocinado.png"),
    "quemado": pygame.image.load("sprites_ingredientes/frijoles_quemado.png")
}

# SPRITES DEL POLLO
sprites_pollo = {
    "crudo": pygame.image.load("sprites_ingredientes/pollo_crudo.png"),
    "frito": pygame.image.load("sprites_ingredientes/pollo_frito.png"),
    "cocinado": pygame.image.load("sprites_ingredientes/pollo_cocinado.png"),
    "quemado": pygame.image.load("sprites_ingredientes/pollo_quemado.png"),
}

# SPRITES DE LAS PAPAS
sprites_papas = {
    "crudo": pygame.image.load("sprites_ingredientes/papa_crudo.png"),
    "picado": pygame.image.load("sprites_ingredientes/papa_picado.png"),
    "frito": pygame.image.load("sprites_ingredientes/papa_frito.png"),
    "quemado": pygame.image.load("sprites_ingredientes/papa_quemado.png"),
}

# SPRITES DE LAS VERDURAS
sprites_verduras = {
    "crudo": pygame.image.load("sprites_ingredientes/verdura_crudo.png"),
    "picado": pygame.image.load("sprites_ingredientes/verdura_picado.png"),
    "cocinado": pygame.image.load("sprites_ingredientes/verdura_cocinado.png"),
    "quemado": pygame.image.load("sprites_ingredientes/verdura_quemado.png"),
}

# SPRITES DE CARNE
sprites_carne = {
    "crudo": pygame.image.load("sprites_ingredientes/carne_crudo.png"),
    "cocinado": pygame.image.load("sprites_ingredientes/carne_cocinado.png"),
    "quemado": pygame.image.load("sprites_ingredientes/carne_quemado.png"),
}

# DICCIONARIO CON LOS SPRITES POR INGREDIENTE
sprites_ingredientes = { # Usado para un mejor manejo de los sprites según el ingrediente que se esté usando
    "platano": sprites_platano,
    "huevo": sprites_huevo,
    "arroz": sprites_arroz,
    "frijoles": sprites_frijoles,
    "pollo": sprites_pollo,
    "papas": sprites_papas,
    "verduras": sprites_verduras,
    "carne": sprites_carne,
}
"""
Nota: los ingredientes fusionados (arroz_frijoles, etc.) no tienen sprites propios, su visualización viene del sprite de plato correspondiente.
"""

# ==============================
# CONSTANTES DE PLATO
# ==============================

# SPRITES DEL PLATO
sprites_plato = { # Cada elemento cocinado o frito tiene su sprite con el plato, y las fusiones están en estos sprites; solo se hacen en el plato
    "vacio": pygame.image.load("sprites_ingredientes/plato_vacio.png"),
    "platano": pygame.image.load("sprites_ingredientes/plato_platano.png"),
    "huevo": pygame.image.load("sprites_ingredientes/plato_huevo.png"),
    "arroz": pygame.image.load("sprites_ingredientes/plato_arroz.png"),
    "frijoles": pygame.image.load("sprites_ingredientes/plato_frijoles.png"),
    "pollo_frito": pygame.image.load("sprites_ingredientes/plato_pollo_frito.png"),
    "pollo_cocinado": pygame.image.load("sprites_ingredientes/plato_pollo_cocinado.png"),
    "papas": pygame.image.load("sprites_ingredientes/plato_papa.png"),
    "verduras": pygame.image.load("sprites_ingredientes/plato_verdura.png"),
    "carne": pygame.image.load("sprites_ingredientes/plato_carne.png"),
    "arroz_frijoles": pygame.image.load("sprites_ingredientes/plato_arroz_frijoles.png"),
    "arroz_carne": pygame.image.load("sprites_ingredientes/plato_arroz_carne.png"),
    "frijoles_carne": pygame.image.load("sprites_ingredientes/plato_frijoles_carne.png"),
    "arroz_frijoles_carne": pygame.image.load("sprites_ingredientes/plato_arroz_frijoles_carne.png"),
    "pollo_papas": pygame.image.load("sprites_ingredientes/plato_pollo_papa.png"),
    "carne_verduras": pygame.image.load("sprites_ingredientes/plato_carne_verdura.png"),
    "carne_papas": pygame.image.load("sprites_ingredientes/plato_carne_papa.png"),
    "arroz_pollo": pygame.image.load("sprites_ingredientes/plato_arroz_pollo.png"),
}

# ESTADO REQUERIDO DE CADA INGREDIENTE PARA PODER PONERSE EN EL PLATO
estados_validos_para_plato = { # Los estados por cada ingrediente para ser agregados al plato
    "huevo": "frito",
    "platano": "frito",
    "arroz": "cocinado",
    "frijoles": "cocinado",
    "pollo": None,  # Acepta frito o cocinado, se verifica aparte en Plato.agregar_ingrediente. Se pone acá para que el lector del código sepa qe pollo tiene estados válidos.
    "papas": "frito",
    "verduras": "cocinado",
    "carne": "cocinado",
}

# FUSIONES POSIBLES DENTRO DEL PLATO
fusiones_plato = { # Todas las combinaciones se realizan aquí dentro. No hay fusiones fuera del plato.
    # Arroz con frijoles
    frozenset([("arroz", "cocinado"), ("frijoles", "cocinado")]): "arroz_frijoles",

    # Arroz, frijoles y carne
    frozenset([("arroz_frijoles", "cocinado"), ("carne", "cocinado")]): "arroz_frijoles_carne",
    frozenset([("arroz_carne", "cocinado"), ("frijoles", "cocinado")]): "arroz_frijoles_carne",
    frozenset([("frijoles_carne", "cocinado"), ("arroz", "cocinado")]): "arroz_frijoles_carne",

    # Pasos intermedios: arroz con carne y frijoles con carne
    frozenset([("arroz", "cocinado"), ("carne", "cocinado")]): "arroz_carne",
    frozenset([("frijoles", "cocinado"), ("carne", "cocinado")]): "frijoles_carne",

    # Pollo frito con papas
    frozenset([("pollo", "frito"), ("papas", "frito")]): "pollo_papas",

    # Sopa de carne con verduras
    frozenset([("carne", "cocinado"), ("verduras", "cocinado")]): "carne_verduras",

    # Carne con papas fritas
    frozenset([("carne", "cocinado"), ("papas", "frito")]): "carne_papas",

    # Arroz con pollo cocinado
    frozenset([("arroz", "cocinado"), ("pollo", "cocinado")]): "arroz_pollo",
}
"""
frozenset hace que dentro de lo que se le de no importe el orden, así no importa si se le da primero arroz o frijoles, devuelve arroz_frijoles por ejemplo.
frozenset([("arroz", "cocinado"), ("frijoles", "cocinado")]) es lo mismo que frozenset([("frijoles", "cocinado"), ("arroz", "cocinado")]) y devuelven lo mismo.
"""

# ==============================
# CONSTANTES DE ESTACIONES
# ==============================

# TABLA
#-Tiempo-#
duracion_tabla = 3  # Segundos manteniendo C para picar un ingrediente

#-Ingredientes-#
ingredientes_tabla = { # Los ingredientes que acepta la taba y en qué estado
    "platano": "crudo",
    "verduras": "crudo",
    "papas": "crudo"
}

# COCINA
#-Tiempo-#
duracion_cocina = 8 # Segundos para que se cocine un ingrediente
duracion_quemado_cocina = 6 # Segundos para que se queme un ingrediente

#-Ingredientes-#
ingredientes_cocina = { # Los ingredientes que acepta la cocina y en qué estado
    "arroz": "crudo",
    "frijoles": "crudo",
    "verduras": "picado",
    "carne": "crudo",
    "pollo": "crudo"
}

# FREIDORA
#-Tiempo-#
duracion_freidora = 7 # Segundos para que se fría un ingrediente
duracion_quemado_freidora = 5 # Segundos para que se queme un ingrediente

#-Ingredientes-#
ingredientes_freidora = { # Los ingredientes que acepta la freidora y en qué estado
    "platano": "picado",
    "huevo": "crudo",
    "pollo": "crudo",
    "papas": "picado",
}

# ==============================
# CONSTANTES DE RECETAS Y NIVEL
# ==============================

# TIEMPO
duracion_nivel = 360 # Cuanto dura el nivel, en este caso 5 minutos

duracion_receta = { # Cuanto dura en vencer una receta según los puntos que brinda
    2: 50,    # 50 segundos
    3: 60,    # 1 minuto
    4: 70,    # 1 minuto 10 segundos
    5: 80,    # 1 minuto 20 segundos
    6: 90,    # 1 minuto 30 segundos
}

espera_recetas_cocina1 = 30 # el tiempo que dura en aparecer una nueva receta según la cocina
espera_recetas_cocina2 = 35
espera_recetas_cocina3 = 45

max_recetas = 5 # la cantidad de recetas que pueden aparecer en pantalla

# PUNTOS
puntos_recetas = { # Los puntos que se ganan por receta según su díficultad de preparación

    # Cocina 1
    "huevo": 2,
    "platano": 2,
    "arroz_frijoles": 4,

    # Cocina 2
    "pollo_frito": 3,
    "arroz_pollo": 4,
    "pollo_papas": 4,
    "papas": 2,

    # Cocina 3
    "carne_verduras": 5,
    "carne_papas": 4,
    "arroz_frijoles_carne": 6,
}

puntos_receta_vencida = -3 # Los puntos que se restan si se vence una receta.
puntos_entrega_incorrecta = -1 # El punto que se resta si se entrega una receta que no está en la lista de recetas

# RECETAS POR COCINA
# Las recetas que se trabajan en cada cocina
recetas_posibles_cocina1 = ["huevo", "platano", "arroz_frijoles"]
recetas_posibles_cocina2 = ["pollo_frito", "arroz_pollo", "pollo_papas", "papas"]
recetas_posibles_cocina3 = ["carne_verduras", "carne_papas", "arroz_frijoles_carne"]

# SPRITES DE LOS RECETAS EN LA INTERFAZ
sprites_plato_interfaz = {

    # Cocina 1
    "huevo": pygame.image.load("sprites_ingredientes/plato_huevo_interfaz.png"),
    "platano": pygame.image.load("sprites_ingredientes/plato_platano_interfaz.png"),
    "arroz_frijoles": pygame.image.load("sprites_ingredientes/plato_arroz_frijoles_interfaz.png"),

    # Cocina 2
    "pollo_frito": pygame.image.load("sprites_ingredientes/plato_pollo_frito_interfaz.png"),
    "arroz_pollo": pygame.image.load("sprites_ingredientes/plato_arroz_pollo_interfaz.png"),
    "pollo_papas": pygame.image.load("sprites_ingredientes/plato_pollo_papa_interfaz.png"),
    "papas": pygame.image.load("sprites_ingredientes/plato_papa_interfaz.png"),

    # Cocina 3
    "carne_verduras": pygame.image.load("sprites_ingredientes/plato_carne_verdura_interfaz.png"),
    "carne_papas": pygame.image.load("sprites_ingredientes/plato_carne_papa_interfaz.png"),
    "arroz_frijoles_carne": pygame.image.load("sprites_ingredientes/plato_arroz_frijoles_carne_interfaz.png"),
}


