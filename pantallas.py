# ==============================
# IMPORTS
# ==============================

from pygame.constants import *
from chef import *
from estaciones import *
from ingrediente_plato import *
import random
from recetas import *

# ==============================
# MENÚ
# ==============================

class Menu:
    """
    Clase Menu que representa la pantalla Menu.
    Muestra la interfaz del menú y si se presiona enter se avanza al juego.
    """

    # INICIADOR
    def __init__(self):
        self.fondo = pygame.image.load("imagenes_interfaz/fondo.png")  # Imagen del fondo
        self.logo = pygame.image.load("imagenes_interfaz/logo.png")  # Imagen del logo
        self.enter = pygame.image.load("imagenes_interfaz/enter.png")  # Imagen de la señal de enter
        self.controles = pygame.image.load("imagenes_interfaz/controles.png")  # Imagen de los controles

    # MANEJAR EVENTOS
    def manejar_eventos(self, eventos):
        """
        Metodo para manejar los eventos de pygame.
        :param eventos: eventos de pygame.
        :return: la Cocina1 si se presiona enter.
        """

        # Si se presiona enter se avanza al juego
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if evento.key == K_RETURN:
                    return Cocina1()
        return self  # Si no se devuelve a si mismo para seguir con el bucle

    def actualizar(self, cambio_tiempo):
        """
        Metodo para actualizar.
        En este caso no hace nada.
        """
        pass  # Evita que se rompa al intentar actualizar el menú

    def dibujar(self, pantalla):
        """
        Metodo para dibujar en pantalla.
        :param pantalla: Donde se dibujarán los elementos.
        """
        pantalla.blit(self.fondo, (0, 0))
        pantalla.blit(self.logo, (10, -50))
        pantalla.blit(self.enter, (165, 600))
        pantalla.blit(self.controles, (125, 350))


# ==============================
# CLASE BASE DE COCINA
# ==============================

class CocinaBase:
    """
    Clase base que representa una cocina.
    Maneja toda la lógica que comparten las tres cocinas: chefs, recoger y dejar objetos,
    entrega de recetas, generación de recetas, puntaje y dibujo. Cada cocina concreta
    solo define su propio diseño en configurar() y a dónde avanzar en siguiente_pantalla().
    """

    # INICIADOR
    def __init__(self, puntaje_inicial=0):
        # FONDO
        self.fondo = None  # Las cocinas lo cambian en configurar

        # CHEFS
        self.pos_pigu = (600, 200)  # Posición por defecto, las cocinas la pueden cambiar en configurar
        self.pos_robo = (600, 490)  # Posición por defecto, las cocinas la pueden cambiar en configurar

        # SE VA A LLENAR EN configurar()
        self.despensas = []  # Lista de despensas de la cocina
        self.tablas = []  # Lista de tablas de picar de la cocina
        self.cocina = None  # La estación de cocina
        self.freidora = None  # La estación de freidora
        self.mesas = []  # Lista de mesas de la cocina
        self.paredes = []  # Lista de paredes (obstáculos invisibles)
        self.entrega = None  # La estación de entrega de recetas
        self.basurero = None  # El basurero
        self.dispensa_platos = None  # La dispensa de platos
        self.recetas_posibles = []  # Las recetas que puede pedir esta cocina

        # NIVEL
        self.tiempo_nivel = duracion_nivel  # Lo que dura una cocina
        self.puntaje = puntaje_inicial  # Empieza con el puntaje que traiga de la cocina anterior, o 0 si es la primera
        self.recetas_activas = []  # Las recetas que están en pantalla esperando ser entregadas
        self.tiempo_espera_receta = 0  # Cuenta el tiempo que falta para que aparezca la siguiente receta

        # CADA COCINA LLENA LOS ATRIBUTOS ANTERIORES
        self.configurar()  # Cada subclase implementa esto con su propio diseño

        # CHEFS
        self.pigu = Chef(self.pos_pigu[0], self.pos_pigu[1], sprites_pigu, margen_x_pigu, margen_y, largo_colision_pigu,
                         alto_colision_chef)  # Configura los chefs según la posición que se le asigne en cada cocina
        self.robo = Chef(self.pos_robo[0], self.pos_robo[1], sprites_robo, margen_x_robo, margen_y, largo_colision_robo,
                         alto_colision_chef)
        self.chef_activo = self.pigu  # Se empieza jugando con pigu

        # OBSTÁCULOS
        self.obstaculos = self.paredes + [  # Las paredes ya son rectángulos
            self.entrega.rectangulo_estacion,
            self.cocina.rectangulo_estacion,
            self.freidora.rectangulo_estacion,
            self.basurero.rectangulo_estacion,
            self.dispensa_platos.rectangulo_estacion,
        ] + [despensa.rectangulo_estacion for despensa in
             self.despensas]  # Se agregan los rectángulos de colisión de las despensas con una comprensión de lista

    # ====================================
    # METODOS QUE IMPLEMENTAN LAS COCINAS
    # ====================================

    def configurar(self):
        """
        Metodo para configurar las cocinas.
        Cada cocina concreta lo sobreescribe para definir su fondo, posiciones de chefs,
        despensas, estaciones, mesas, paredes y recetas posibles.
        """
        raise NotImplementedError  # Lanza error si no se implementa

    def siguiente_pantalla(self):
        """
        Metodo que devuelve la siguiente pantalla al finalizar el nivel.
        Cada cocina concreta lo sobreescribe para encadenar el avance entre niveles.
        """
        raise NotImplementedError  # Lanza error si no se implementa

    # ====================================
    # METODOS PARA COLISIÓN
    # ====================================

    def rect_chef(self, chef):
        """
        Metodo para calcular el rectángulo de colisión del chef (zona de los pies).
        :param chef: el chef del que se quiere calcular el rectángulo.
        """
        return pygame.Rect(
            chef.x + chef.margen_x,
            chef.y + chef.margen_y,
            chef.largo_colision_chef,
            chef.alto_colision_chef
        )

    # ====================================
    # METODOS PARA EJECUTAR ACCIÓN
    # ====================================

    # VERIFICAR SI SE PUEDE RECOGER
    def puede_recoger(self, chef, ingrediente):
        """
        Metodo para verificar si el chef puede recoger un ingrediente, sin sacarlo todavía de su lugar.
        Solo se permite recoger si el chef no carga nada, o si carga un plato y lo que va a
        recoger es un ingrediente (la validación final la hace Plato.agregar_ingrediente).
        :param chef: el chef que intenta recoger.
        :param ingrediente: el ingrediente que se está evaluando.
        :return: True si se puede intentar recoger, False si no.
        """

        if ingrediente is None:  # Si no hay nada que recoger
            return False
        if chef.objeto_cargado is None:  # Si el chef no carga nada puede recoger lo que sea
            return True
        # Chef carga un plato: dejar que Plato.agregar_ingrediente decida si entra
        if isinstance(chef.objeto_cargado, Plato) and isinstance(ingrediente, Ingrediente):
            return True
        return False  # En cualquier otro caso no se puede recoger

    # INTENTAR RECOGER
    def intentar_recoger(self, chef, ingrediente):
        """
        Metodo para que el chef recoja un ingrediente.
        Si el chef carga un plato intenta agregarlo (puede fusionarse o no, según corresponda).
        Si el chef no carga nada simplemente lo recoge.
        :param chef: el chef que recoge.
        :param ingrediente: el ingrediente a recoger.
        :return: True si se pudo recoger, False si no.
        """

        if ingrediente is None:  # Si no hay nada que recoger no hace nada
            return False
        if isinstance(chef.objeto_cargado, Plato) and isinstance(ingrediente, Ingrediente):
            return chef.objeto_cargado.agregar_ingrediente(ingrediente)  # El plato decide si se agrega o se fusiona
        if chef.objeto_cargado is None:  # Si el chef no carga nada
            chef.objeto_cargado = ingrediente  # El chef pasa a cargar el ingrediente
            return True
        return False  # En cualquier otro caso no se puede recoger

    # ====================================
    # MANEJAR EVENTOS
    # ====================================

    def manejar_eventos(self, eventos):
        """
        Metodo para manejar los eventos de pygame: cambio de chef, recoger y dejar objetos.
        :param eventos: eventos de pygame.
        :return: la pantalla actual (this), ya que las cocinas no cambian de pantalla aquí.
        """

        for evento in eventos:
            if evento.type == pygame.KEYDOWN:

                # CAMBIAR CHEF (R)
                if evento.key == pygame.K_r:
                    # Si el chef activo es pigu pasa a ser robo, y viceversa
                    self.chef_activo = (
                        self.robo if self.chef_activo == self.pigu else self.pigu
                    )

                # RECOGER (E)
                if evento.key == pygame.K_e:
                    chef = self.chef_activo
                    rect = self.rect_chef(chef)  # El rectángulo de colisión del chef activo

                    if rect.colliderect(self.dispensa_platos.rectangulo_area_uso):  # Si está en la dispensa de platos
                        if chef.objeto_cargado is None:  # Si no carga nada
                            chef.objeto_cargado = Plato()  # Pasa a cargar un plato vacío

                    elif rect.colliderect(self.basurero.rectangulo_area_uso):  # Si está en el basurero
                        chef.objeto_cargado = None  # Se descarta lo que cargaba

                    elif rect.colliderect(self.entrega.rectangulo_area_uso):  # Si está en la entrega
                        self.intentar_entregar(chef)  # Intenta entregar el plato

                    else:
                        # Despensas
                        for despensa in self.despensas:  # Por cada despensa evalúa si el chef está cerca
                            if rect.colliderect(despensa.rectangulo_area_uso):
                                preview = despensa.dar_ingrediente()  # Crea un ingrediente nuevo sin afectar nada
                                if self.puede_recoger(chef, preview):  # Si se puede recoger
                                    self.intentar_recoger(chef, preview)  # Lo recoge
                                break  # Ya encontró la estación, no sigue revisando las demás

                        # Estaciones de trabajo y mesas
                        for estacion in self.tablas + [self.cocina, self.freidora] + self.mesas:
                            if rect.colliderect(estacion.rectangulo_area_uso):  # Si el chef está en el área de uso
                                preview = estacion.ver_ingrediente()  # Mira el ingrediente sin sacarlo todavía
                                if self.puede_recoger(chef, preview):  # Si sí se puede recoger
                                    ingrediente = estacion.recoger_ingrediente()  # Ahora sí lo saca de la estación
                                    self.intentar_recoger(chef, ingrediente)  # Intenta que el chef lo cargue
                                break

                # DEJAR (F)
                if evento.key == pygame.K_f:
                    chef = self.chef_activo
                    rect = self.rect_chef(chef)

                    # Estaciones de trabajo
                    for estacion in self.tablas + [self.cocina, self.freidora]:
                        if rect.colliderect(estacion.rectangulo_area_uso):  # Si el chef está en el área
                            if estacion.dejar_ingrediente(chef.objeto_cargado):  # Si se pudo dejar
                                chef.objeto_cargado = None  # El chef ya no carga nada
                            break

                    # Mesas
                    for mesa in self.mesas:
                        if rect.colliderect(mesa.rectangulo_area_uso):  # Si el chef está en el área
                            if mesa.dejar_ingrediente(chef.objeto_cargado):  # Si se pudo dejar en la mesa
                                chef.objeto_cargado = None  # El chef ya no carga nada
                            break

        return self  # Las cocinas no cambian de pantalla en manejar_eventos, eso ocurre en actualizar()

    # ====================================
    # ENTREGAR
    # ====================================

    def intentar_entregar(self, chef):
        """
        Metodo para entregar el plato del chef en la estación de entrega.
        Si coincide con alguna receta activa suma puntos y la elimina.
        Si no coincide con ninguna resta puntos por entrega incorrecta.
        :param chef: el chef que está entregando.
        """

        if not isinstance(chef.objeto_cargado, Plato):  # Si no carga un plato no se puede entregar
            return
        if len(chef.objeto_cargado.ingredientes) == 0:  # Si el plato está vacío no se puede entregar
            return

        ingrediente = chef.objeto_cargado.ingredientes[0]  # El único ingrediente que tiene el plato

        # Nombre de receta para pollo: depende del estado, ya que puede ser frito o cocinado
        nombre_receta = ingrediente.nombre
        if ingrediente.nombre == "pollo":
            nombre_receta = f"pollo_{ingrediente.estado}"  # "pollo_frito" o "pollo_cocinado"

        for receta in self.recetas_activas:  # Busca si hay una receta activa que coincida
            if receta.nombre == nombre_receta:
                self.puntaje += puntos_recetas.get(receta.nombre, 0)  # Suma los puntos de esa receta
                self.recetas_activas.remove(receta)  # La receta ya se entregó, se elimina de la lista
                chef.objeto_cargado = None  # El chef ya no carga el plato
                return

        # No coincidió con ninguna receta activa
        self.puntaje = max(0, self.puntaje + puntos_entrega_incorrecta)  # Resta puntos, sin bajar de 0
        chef.objeto_cargado = None  # El chef ya no carga el plato, se entregó igual aunque estaba mal

    # ====================================
    # ACTUALIZAR
    # ====================================

    def actualizar(self, cambio_tiempo):
        """
        Metodo para actualizar la cocina: movimiento del chef, estaciones, temporizador del nivel y recetas.
        :param cambio_tiempo: Tiempo desde el último frame.
        :return: la siguiente pantalla si el tiempo del nivel llega a 0, None en cualquier otro caso.
        """

        self.chef_activo.actualizar(cambio_tiempo, self.obstaculos)  # Solo se actualiza el chef que está en uso

        chef = self.chef_activo
        teclas = pygame.key.get_pressed()
        rect = self.rect_chef(chef)

        # Tablas (se actualizan según si el chef está encima y si mantiene C)
        for tabla in self.tablas:
            tabla.actualizar(
                cambio_tiempo,
                rect.colliderect(tabla.rectangulo_area_uso),
                teclas[pygame.K_c]
            )

        # Cocina y freidora (se actualizan solas, no necesitan al chef)
        self.cocina.actualizar(cambio_tiempo, None, None)
        self.freidora.actualizar(cambio_tiempo, None, None)

        # Temporizador del nivel
        self.tiempo_nivel -= cambio_tiempo  # Baja el tiempo del nivel sin importar los FPS
        if self.tiempo_nivel <= 0:  # Si se acabó el tiempo de esta cocina
            return self.siguiente_pantalla()  # Devuelve la siguiente pantalla para que el bucle principal cambie a ella

        # Generar recetas
        if len(self.recetas_activas) < max_recetas:  # Solo genera una nueva si no se llegó al máximo
            self.tiempo_espera_receta -= cambio_tiempo
            if self.tiempo_espera_receta <= 0:  # Si ya pasó el tiempo de espera
                nombre = random.choice(
                    self.recetas_posibles)  # Elige una receta al azar entre las posibles de esta cocina
                self.recetas_activas.append(Receta(nombre))  # La agrega a la lista de recetas activas
                self.tiempo_espera_receta = self.espera_entre_recetas  # Reinicia la espera para la siguiente receta

        # Actualizar recetas y eliminar vencidas
        for receta in self.recetas_activas[:]:  # Se recorre una copia para poder eliminar mientras se itera
            receta.actualizar(cambio_tiempo)
            if receta.vencida:  # Si el tiempo de la receta llegó a 0
                self.puntaje = max(0, self.puntaje + puntos_receta_vencida)  # Resta puntos, sin bajar de 0
                self.recetas_activas.remove(receta)  # Se elimina de la lista de recetas activas

    # ====================================
    # DIBUJAR
    # ====================================

    def dibujar(self, pantalla):
        """
        Metodo para dibujar la cocina completa: fondo, estaciones, mesas, recetas, puntaje, tiempo y chefs.
        :param pantalla: La pantalla sobre la que se dibujará todo.
        """

        pantalla.blit(self.fondo, (0, 0))  # Fondo de la cocina

        # Estaciones de trabajo
        for tabla in self.tablas:
            tabla.dibujar(pantalla)
        self.cocina.dibujar(pantalla)
        self.freidora.dibujar(pantalla)

        # Mesas
        for mesa in self.mesas:
            mesa.dibujar(pantalla)

        # Recetas (UI arriba a la izquierda)
        for pos, receta in enumerate(self.recetas_activas):  # pos sirve para ir corriendo cada receta hacia la derecha
            receta.dibujar(pantalla, 10 + pos * 75, 10)

        # Puntaje
        fuente = pygame.font.Font(None, 48)
        texto_puntaje = fuente.render(f"Puntaje: {self.puntaje}", True, (255, 255, 255))
        pantalla.blit(texto_puntaje, (10, 730))

        # Tiempo
        minutos = int(self.tiempo_nivel) // 60
        segundos = int(self.tiempo_nivel) % 60
        texto_tiempo = fuente.render(f"{minutos}:{segundos:02d}", True, (255, 255, 255))
        pantalla.blit(texto_tiempo, (1100, 730))

        # Chefs (se dibujan los dos, aunque solo uno se controle a la vez)
        self.pigu.dibujar(pantalla)
        self.robo.dibujar(pantalla)


# ==============================
# COCINA 1
# Ingredientes: arroz, frijoles, huevo, plátano
# Recetas: huevo, platano, arroz_frijoles
# ==============================

class Cocina1(CocinaBase):
    """
    Clase que representa la primera cocina del juego.
    Solo define su propio diseño y a dónde avanzar; toda la lógica de juego la hereda de CocinaBase.
    """

    # CONFIGURAR
    def configurar(self):
        self.fondo = pygame.image.load("imagenes_interfaz/cocina_1.png")

        self.despensas = [
            EstacionDespensa(90, 160, 70, 70, "arroz"),
            EstacionDespensa(75, 275, 70, 70, "frijoles"),
            EstacionDespensa(25, 625, 70, 70, "huevo"),
            EstacionDespensa(1040, 165, 70, 70, "platano"),
        ]

        self.entrega = EstacionEntrega(530, 15, 150, 70)
        self.tablas = [
            EstacionTrabajo(400, 370, 50, 30, "tabla"),
            EstacionTrabajo(750, 370, 50, 30, "tabla"),
        ]
        self.cocina = EstacionTrabajo(1050, 275, 75, 55, "cocina", (-35, -35, 70, 50))
        self.freidora = EstacionTrabajo(50, 510, 60, 90, "freidora")
        self.basurero = Basurero(1080, 520, 70, 70)
        self.dispensa_platos = DispensaPlatos(1070, 430, 70, 70)

        self.mesas = [
            Mesa(70, 380, 50, 30),
            Mesa(150, 380, 50, 30),
            Mesa(230, 380, 50, 30),
            Mesa(310, 380, 50, 30),
            Mesa(490, 380, 50, 30),
            Mesa(570, 380, 50, 30),
            Mesa(650, 380, 50, 30),
            Mesa(850, 380, 50, 30),
            Mesa(930, 380, 50, 30),
            Mesa(1010, 380, 50, 30),
        ]

        self.paredes = [
            pygame.Rect(0, 80, 1200, 40),  # pared arriba
            pygame.Rect(0, 680, 1200, 40),  # pared abajo
            pygame.Rect(80, 100, 20, 300),  # pared izquierda
            pygame.Rect(1100, 100, 20, 300),  # pared derecha
            pygame.Rect(30, 400, 20, 300),  # pared izquierda2
            pygame.Rect(1170, 400, 20, 300),  # pared derecha2
            pygame.Rect(0, 360, 1200, 70),  # mesa larga
        ]

        self.recetas_posibles = recetas_posibles_cocina1  # Las recetas que puede pedir esta cocina
        self.espera_entre_recetas = espera_recetas_cocina1  # Cuanto tarda en aparecer una nueva receta

    # SIGUIENTE PANTALLA
    def siguiente_pantalla(self):
        """
        Metodo que devuelve la siguiente pantalla, en este caso la Cocina2, pasándole el puntaje acumulado.
        """
        return Cocina2(self.puntaje)


# ==============================
# COCINA 2
# Ingredientes: pollo, arroz, papas
# Recetas: pollo_frito, arroz_pollo, pollo_papas, papas
# ==============================

class Cocina2(CocinaBase):
    """
    Clase que representa la segunda cocina del juego.
    """

    # CONFIGURAR
    def configurar(self):
        self.pos_pigu = (300, 200)  # Posición inicial de pigu en esta cocina
        self.pos_robo = (800, 400)  # Posición inicial de robo en esta cocina

        self.fondo = pygame.image.load("imagenes_interfaz/cocina_2.png")

        self.despensas = [
            EstacionDespensa(125, 145, 90, 90, "pollo"),
            EstacionDespensa(95, 340, 90, 90, "arroz"),
            EstacionDespensa(1005, 280, 90, 90, "papas", (-20, 0, 40, 0)),
        ]

        self.entrega = EstacionEntrega(530, 30, 150, 70)
        self.tablas = [
            EstacionTrabajo(805, 220, 50, 30, "tabla", (-25, -60, 50, 120)),
            EstacionTrabajo(645, 370, 50, 30, "tabla", (-60, -25, 120, 50)),
        ]
        self.cocina = EstacionTrabajo(80, 500, 85, 100, "cocina")
        self.freidora = EstacionTrabajo(1015, 370, 60, 90, "freidora", (-35, -10, 70, 2))
        self.basurero = Basurero(735, 560, 70, 70, (0, -10, 40, 20))
        self.dispensa_platos = DispensaPlatos(1025, 470, 90, 90, (-20, 0, 40, 40))

        self.mesas = [
            Mesa(890, 220, 50, 30, (-7, -30, 15, 90)),
            Mesa(970, 220, 50, 30),
            Mesa(1050, 220, 50, 30),
            Mesa(620, 230, 50, 30, (-20, -30, 70, 40)),
            Mesa(620, 300, 50, 30, (-25, -25, 70, 40)),
            Mesa(630, 450, 50, 30, (-25, -25, 70, 40)),
            Mesa(630, 520, 50, 30, (-25, -25, 70, 40)),
            Mesa(630, 600, 50, 30, (-25, -25, 70, 40)),
        ]

        self.paredes = [
            pygame.Rect(0, 100, 1200, 40),  # arriba
            pygame.Rect(0, 630, 1200, 80),  # abajo
            pygame.Rect(100, 120, 20, 300),  # pared izquierda 1
            pygame.Rect(70, 420, 20, 300),  # pared izquierda 2
            pygame.Rect(1100, 100, 20, 300),  # pared derecha 1
            pygame.Rect(1150, 400, 20, 300),  # pared derecha 2
            pygame.Rect(620, 215, 90, 800),  # mesa 1
            pygame.Rect(620, 210, 1200, 80),  # mesa 2
        ]

        self.recetas_posibles = recetas_posibles_cocina2
        self.espera_entre_recetas = espera_recetas_cocina2

    # SIGUIENTE PANTALLA
    def siguiente_pantalla(self):
        """
        Metodo que devuelve la siguiente pantalla, en este caso la Cocina3, pasándole el puntaje acumulado.
        """
        return Cocina3(self.puntaje)


# ==============================
# COCINA 3
# Ingredientes: verduras, carne, papas, arroz, frijoles
# Recetas: carne_verduras, carne_papas, arroz_frijoles_carne
# ==============================

class Cocina3(CocinaBase):
    """
    Clase que representa la tercera y última cocina del juego.
    """

    # CONFIGURAR
    def configurar(self):
        self.pos_pigu = (300, 200)
        self.pos_robo = (600, 400)

        self.fondo = pygame.image.load("imagenes_interfaz/cocina_3.png")

        self.despensas = [
            EstacionDespensa(285, 80, 95, 95, "verduras"),
            EstacionDespensa(790, 75, 95, 95, "carne"),
            EstacionDespensa(140, 300, 95, 95, "papas"),
            EstacionDespensa(125, 565, 95, 95, "arroz"),
            EstacionDespensa(850, 315, 100, 95, "frijoles", (0, -10, 30, 20)),
        ]

        self.entrega = EstacionEntrega(1040, 240, 70, 150)
        self.tablas = [
            EstacionTrabajo(570, 215, 50, 30, "tabla"),
            EstacionTrabajo(570, 515, 50, 30, "tabla", (-35, -35, 70, 90)),
        ]
        self.cocina = EstacionTrabajo(530, 325, 60, 90, "cocina")
        self.freidora = EstacionTrabajo(615, 325, 60, 90, "freidora")
        self.basurero = Basurero(850, 630, 70, 70, (-40, -10, 40, 20))
        self.dispensa_platos = DispensaPlatos(945, 625, 70, 70)

        self.mesas = [
            Mesa(455, 225, 50, 30, (-35, -40, 70, 60)),
            Mesa(675, 225, 50, 30, (-20, -40, 60, 60)),
            Mesa(455, 515, 50, 30),
            Mesa(675, 515, 50, 30),
            Mesa(765, 295, 50, 30, (-30, -20, 70, 40)),
            Mesa(765, 440, 50, 30, (-30, -20, 70, 40)),
            Mesa(380, 440, 50, 30, (-30, -20, 70, 40)),
            Mesa(380, 295, 50, 30, (-30, -20, 70, 40)),
            Mesa(380, 365, 50, 30, (-30, -20, 70, 40)),
        ]

        self.paredes = [
            pygame.Rect(0, 80, 1200, 40),  # arriba
            pygame.Rect(0, 690, 1200, 40),  # abajo
            pygame.Rect(120, 90, 60, 300),  # izquierda 1
            pygame.Rect(1050, 100, 60, 440),  # derecha 1
            pygame.Rect(120, 300, 20, 400),  # izquierda 2
            pygame.Rect(1090, 400, 20, 300),  # derecha 2
            pygame.Rect(380, 215, 60, 360),  # mesa 1
            pygame.Rect(380, 207, 440, 60),  # mesa 2
            pygame.Rect(380, 500, 440, 80),  # mesa 3
            pygame.Rect(370, 420, 70, 210),  # mesa 3 borde
            pygame.Rect(760, 220, 60, 345),  # mesa 4
            pygame.Rect(760, 420, 60, 210),  # mesa 4 borde
            pygame.Rect(170, 100, 60, 60),  # maseta 1
            pygame.Rect(950, 125, 60, 60),  # maseta 2
            pygame.Rect(1045, 650, 60, 60),  # maseta 3
            pygame.Rect(500, 65, 180, 100),  # estante
        ]

        self.recetas_posibles = recetas_posibles_cocina3
        self.espera_entre_recetas = espera_recetas_cocina3

    # SIGUIENTE PANTALLA
    def siguiente_pantalla(self):
        """
        Metodo que devuelve la siguiente pantalla. Al terminar la última cocina se vuelve al Menu.
        """
        return Menu()
