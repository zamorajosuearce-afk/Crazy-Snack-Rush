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
        self.fondo = pygame.image.load("imagenes_interfaz/fondo.png") # Imagen del fondo
        self.logo = pygame.image.load("imagenes_interfaz/logo.png") # Imagen del logo
        self.enter = pygame.image.load("imagenes_interfaz/enter.png") # Imagen de la señal de enter
        self.controles = pygame.image.load("imagenes_interfaz/controles.png") # Imagen de los controles

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
        return self # Si no se devuelve a si mismo para seguir con el bucle

    def actualizar(self, cambio_tiempo):
        """
        Metodo para actualizar.
        En este caso noo hace nada
        """
        pass #Evita que se rompa al intentar actualizar el menú

    def dibujar(self, pantalla):
        """
        Metodo para dibujar en pantalla.
        :param pantalla: Donde se dibujarán los elementos.
        """
        pantalla.blit(self.fondo, (0,0 ))
        pantalla.blit(self.logo, (10, -50))
        pantalla.blit(self.enter, (165, 600))
        pantalla.blit(self.controles, (125, 350))


# ==============================
# CLASE BASE DE COCINA
# ==============================

class CocinaBase:

    def __init__(self, puntaje_inicial = 0):
        # FONDO
        self.fondo = None # Las cocinas lo cambian en configurar

        # CHEFS
        self.pos_pigu = (600, 200)  # Posición por defecto
        self.pos_robo = (600, 490)  # Posición por defecto

        # SE VA A LLENAR EN configurar()
        self.despensas = []
        self.tablas = []
        self.cocina = None
        self.freidora = None
        self.mesas = []
        self.paredes = []
        self.entrega = None
        self.basurero = None
        self.dispensa_platos = None
        self.recetas_posibles = []

        # NIVEL
        self.tiempo_nivel = duracion_nivel # Lo que dura una cocina
        self.puntaje = puntaje_inicial # Empieza en 0
        self.recetas_activas = [] # Se configura después
        self.tiempo_espera_receta = 0 # Se configura después, depende de cada cocina

        # CADA COCINA LLENA LOS ATRIBUTOS ANTERIORES
        self.configurar()

        # CHEFS
        self.pigu = Chef(self.pos_pigu[0], self.pos_pigu[1], sprites_pigu, margen_x_pigu, margen_y, largo_colision_pigu, alto_colision_chef) # Configura los chefs según la posición que se le asigne en cada cocina
        self.robo = Chef(self.pos_robo[0], self.pos_robo[1], sprites_robo, margen_x_robo, margen_y, largo_colision_robo, alto_colision_chef)
        self.chef_activo = self.pigu # Se empieza jugando con pigu

        # OBSTÁCULOS
        self.obstaculos = self.paredes + [ # Paredes
            self.entrega.rectangulo_estacion,
            self.cocina.rectangulo_estacion,
            self.freidora.rectangulo_estacion,
            self.basurero.rectangulo_estacion,
            self.dispensa_platos.rectangulo_estacion,
        ] + [despensa.rectangulo_estacion for despensa in self.despensas] # Estaciones y despensas

    # ====================================
    # METODOS QUE IMPLEMENTAN LAS COCINAS
    # ====================================
    def configurar(self):
        """Llena fondo, despensas, estaciones, mesas, paredes y recetas_posibles."""
        raise NotImplementedError # Lanza error si no se implementa

    def siguiente_pantalla(self):
        """Devuelve la instancia de la siguiente pantalla al terminar el nivel."""
        raise NotImplementedError # Lanza error si no se implementa

    # ------------------------------------------------------------------
    # Helpers de colisión
    # ------------------------------------------------------------------

    def _rect_chef(self, chef):
        return pygame.Rect(
            chef.x + chef.margen_x,
            chef.y + chef.margen_y,
            chef.largo_colision_chef,
            chef.alto_colision_chef
        )

    # ------------------------------------------------------------------
    # PUEDE RECOGER
    # No hay fusiones fuera del plato, así que solo se permite recoger si:
    #   a) el chef no carga nada, o
    #   b) el chef carga un plato y el ingrediente es válido para entrar al plato.
    # ------------------------------------------------------------------

    def _puede_recoger(self, chef, ingrediente):
        if ingrediente is None:
            return False
        if chef.objeto_cargado is None:
            return True
        # Chef carga un plato: dejar que Plato.agregar_ingrediente decida
        if isinstance(chef.objeto_cargado, Plato) and isinstance(ingrediente, Ingrediente):
            return True
        return False

    def _intentar_recoger(self, chef, ingrediente):
        if ingrediente is None:
            return False
        if isinstance(chef.objeto_cargado, Plato) and isinstance(ingrediente, Ingrediente):
            return chef.objeto_cargado.agregar_ingrediente(ingrediente)
        if chef.objeto_cargado is None:
            chef.objeto_cargado = ingrediente
            return True
        return False

    # ------------------------------------------------------------------
    # MANEJAR EVENTOS
    # ------------------------------------------------------------------

    def manejar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:

                # CAMBIAR CHEF (R)
                if evento.key == pygame.K_r:
                    self.chef_activo = (
                        self.robo if self.chef_activo == self.pigu else self.pigu
                    )

                # RECOGER (E)
                if evento.key == pygame.K_e:
                    chef = self.chef_activo
                    rect = self._rect_chef(chef)

                    if rect.colliderect(self.dispensa_platos.rectangulo_area_uso):
                        if chef.objeto_cargado is None:
                            chef.objeto_cargado = Plato()

                    elif rect.colliderect(self.basurero.rectangulo_area_uso):
                        chef.objeto_cargado = None

                    elif rect.colliderect(self.entrega.rectangulo_area_uso):
                        self._intentar_entregar(chef)

                    else:
                        # Despensas
                        for despensa in self.despensas:
                            if rect.colliderect(despensa.rectangulo_area_uso):
                                preview = despensa.dar_ingrediente()
                                if self._puede_recoger(chef, preview):
                                    self._intentar_recoger(chef, preview)
                                break

                        # Estaciones de trabajo y mesas
                        for estacion in self.tablas + [self.cocina, self.freidora] + self.mesas:
                            if rect.colliderect(estacion.rectangulo_area_uso):
                                preview = estacion.ver_objeto()
                                if self._puede_recoger(chef, preview):
                                    ingrediente = estacion.recoger_ingrediente()
                                    if not self._intentar_recoger(chef, ingrediente):
                                        estacion.dejar_objeto(ingrediente)  # devolver si falló
                                break

                # DEJAR (F)
                if evento.key == pygame.K_f:
                    chef = self.chef_activo
                    rect = self._rect_chef(chef)

                    # Estaciones de trabajo
                    for estacion in self.tablas + [self.cocina, self.freidora]:
                        if rect.colliderect(estacion.rectangulo_area_uso):
                            # Si el chef lleva plato con ingrediente, intentar dejar el ingrediente
                            objeto = chef.objeto_cargado
                            if isinstance(objeto, Plato) and len(objeto.ingredientes) == 1:
                                ing = objeto.ingredientes[0]
                                if estacion.dejar_objeto(ing):
                                    objeto.ingredientes = []
                                    objeto.actualizar_sprite()
                            elif isinstance(objeto, Ingrediente):
                                if estacion.dejar_objeto(objeto):
                                    chef.objeto_cargado = None
                            break

                    # Mesas
                    for mesa in self.mesas:
                        if rect.colliderect(mesa.rectangulo_area_uso):
                            objeto = chef.objeto_cargado
                            if mesa.dejar_objeto(objeto):
                                chef.objeto_cargado = None
                            break

        return self

    # ------------------------------------------------------------------
    # ENTREGAR
    # ------------------------------------------------------------------

    def _intentar_entregar(self, chef):
        if not isinstance(chef.objeto_cargado, Plato):
            return
        if len(chef.objeto_cargado.ingredientes) == 0:
            return

        ingrediente = chef.objeto_cargado.ingredientes[0]

        # Nombre de receta para pollo solo: depende del estado
        nombre_receta = ingrediente.nombre
        if ingrediente.nombre == "pollo":
            nombre_receta = f"pollo_{ingrediente.estado}"  # "pollo_frito" o "pollo_cocinado"

        for receta in self.recetas_activas:
            if receta.nombre == nombre_receta:
                self.puntaje += puntos_recetas.get(receta.nombre, 0)
                self.recetas_activas.remove(receta)
                chef.objeto_cargado = None
                return

        # No coincidió con ninguna receta activa
        self.puntaje = max(0, self.puntaje + puntos_entrega_incorrecta)
        chef.objeto_cargado = None

    # ------------------------------------------------------------------
    # ACTUALIZAR
    # ------------------------------------------------------------------

    def actualizar(self, cambio_tiempo):
        self.chef_activo.actualizar(cambio_tiempo, self.obstaculos)

        chef = self.chef_activo
        teclas = pygame.key.get_pressed()
        rect = self._rect_chef(chef)

        # Tablas
        for tabla in self.tablas:
            tabla.actualizar(
                cambio_tiempo,
                rect.colliderect(tabla.rectangulo_area_uso),
                teclas[pygame.K_c]
            )

        # Cocina y freidora (se actualizan solas)
        self.cocina.actualizar(cambio_tiempo, None, None)
        self.freidora.actualizar(cambio_tiempo, None, None)

        # Temporizador del nivel
        self.tiempo_nivel -= cambio_tiempo
        if self.tiempo_nivel <= 0:
            return self.siguiente_pantalla()

        # Generar recetas
        if len(self.recetas_activas) < max_recetas:
            self.tiempo_espera_receta -= cambio_tiempo
            if self.tiempo_espera_receta <= 0:
                nombre = random.choice(self.recetas_posibles)
                self.recetas_activas.append(Receta(nombre))
                self.tiempo_espera_receta = self.espera_entre_recetas

        # Actualizar recetas y eliminar vencidas
        for receta in self.recetas_activas[:]:
            receta.actualizar(cambio_tiempo)
            if receta.vencida:
                self.puntaje = max(0, self.puntaje + puntos_receta_vencida)
                self.recetas_activas.remove(receta)

    # ------------------------------------------------------------------
    # DIBUJAR
    # ------------------------------------------------------------------

    def dibujar(self, pantalla):
        pantalla.blit(self.fondo, (0, 0))

        # Estaciones de trabajo
        for tabla in self.tablas:
            tabla.dibujar(pantalla)
        self.cocina.dibujar(pantalla)
        self.freidora.dibujar(pantalla)

        # Mesas
        for mesa in self.mesas:
            mesa.dibujar(pantalla)

        # Recetas (UI arriba a la izquierda)
        for pos, receta in enumerate(self.recetas_activas):
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

        # Chefs
        self.pigu.dibujar(pantalla)
        self.robo.dibujar(pantalla)


# ==============================
# COCINA 1
# Ingredientes: arroz, frijoles, huevo, plátano
# Recetas: huevo, platano, arroz_frijoles
# ==============================

class Cocina1(CocinaBase):

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
        self.cocina = EstacionTrabajo(1050, 275, 75, 55, "cocina",(-35, -35, 70, 50))
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
            pygame.Rect(0, 80, 1200, 40),
            pygame.Rect(0, 680, 1200, 40),
            pygame.Rect(80, 100, 20, 300),
            pygame.Rect(1100, 100, 20, 300),
            pygame.Rect(30, 400, 20, 300),
            pygame.Rect(1170, 400, 20, 300),
            pygame.Rect(0, 360, 1200, 70),
        ]

        self.recetas_posibles = recetas_posibles_cocina1
        self.espera_entre_recetas = espera_recetas_cocina1

    def siguiente_pantalla(self):
        return Cocina2(self.puntaje)


# ==============================
# COCINA 2
# Ingredientes: pollo, arroz, papas
# Recetas: pollo_frito, arroz_pollo, pollo_papas, papas
# ==============================

class Cocina2(CocinaBase):

    def configurar(self):
        self.pos_pigu = (300, 200)
        self.pos_robo = (800, 400)

        self.fondo = pygame.image.load("imagenes_interfaz/cocina_2.png")  # cambia cuando tengas el asset

        self.despensas = [
            EstacionDespensa(125, 145, 90, 90, "pollo" ),
            EstacionDespensa(95, 340, 90, 90, "arroz"),
            EstacionDespensa(1005, 280, 90, 90, "papas",(-20, 0, 40, 0)),
        ]

        self.entrega = EstacionEntrega(530, 30, 150, 70)
        self.tablas = [
            EstacionTrabajo(805, 220, 50, 30, "tabla", (-25, -60, 50, 120) ),
            EstacionTrabajo(645, 370, 50, 30, "tabla",(-60, -25, 120, 50)),
        ]
        self.cocina = EstacionTrabajo(80, 500, 85, 100, "cocina")
        self.freidora = EstacionTrabajo(1015, 370, 60, 90, "freidora",(-35, -10, 70, 2))
        self.basurero = Basurero(735, 560, 70, 70, (0, -10, 40, 20))
        self.dispensa_platos = DispensaPlatos(1025, 470, 90, 90,(-20, 0, 40, 40))

        self.mesas = [

            Mesa(890, 220, 50, 30,(-7, -30, 15, 90)),
            Mesa(970, 220, 50, 30),
            Mesa(1050, 220, 50, 30),
            Mesa(620, 230, 50, 30,(-20, -30, 70, 40) ),
            Mesa(620, 300, 50, 30,(-25,-25 , 70, 40)),
            Mesa(630, 450, 50, 30,(-25,-25 , 70, 40)),
            Mesa(630, 520, 50, 30,(-25,-25 , 70, 40)),
            Mesa(630, 600, 50, 30,(-25,-25 , 70, 40)),
        ]

        self.paredes = [
            pygame.Rect(0, 100, 1200, 40), # arriba
            pygame.Rect(0, 630, 1200, 80), # abajo
            pygame.Rect(100, 120, 20, 300), # pared izquierda 1
            pygame.Rect(70, 420, 20, 300),  # pared izquierda 2
            pygame.Rect(1100, 100, 20, 300), # pared derecha 1
            pygame.Rect(1150, 400, 20, 300), # pared derecha 2
            pygame.Rect(620, 215, 90, 800), # mesa 1
            pygame.Rect(620, 210, 1200, 80), # mesa 2
        ]

        self.recetas_posibles = recetas_posibles_cocina2
        self.espera_entre_recetas = espera_recetas_cocina2

    def siguiente_pantalla(self):
        return Cocina3(self.puntaje)


# ==============================
# COCINA 3
# Ingredientes: verduras, carne, papas, arroz, frijoles
# Recetas: carne_verduras, carne_papas, arroz_frijoles_carne
# ==============================

class Cocina3(CocinaBase):

    def configurar(self):
        self.pos_pigu = (300, 200)
        self.pos_robo = (600, 400)

        self.fondo = pygame.image.load("imagenes_interfaz/cocina_3.png")  # cambia cuando tengas el asset

        self.despensas = [
            EstacionDespensa(285, 80, 95, 95, "verduras"),
            EstacionDespensa(790, 75, 95, 95, "carne"),
            EstacionDespensa(140, 300, 95, 95, "papas"),
            EstacionDespensa(125, 565, 95, 95, "arroz"),
            EstacionDespensa(850, 315, 100, 95, "frijoles",(0, -10, 30, 20)),
        ]

        self.entrega = EstacionEntrega(1040, 240, 70, 150)
        self.tablas = [
            EstacionTrabajo(570, 215, 50, 30, "tabla"),
            EstacionTrabajo(570, 515, 50, 30, "tabla",(-35, -35, 70, 90)),
        ]
        self.cocina = EstacionTrabajo(530, 325, 60, 90, "cocina")
        self.freidora = EstacionTrabajo(615, 325, 60, 90, "freidora")
        self.basurero = Basurero(850, 630, 70, 70,(-40, -10, 40, 20))
        self.dispensa_platos = DispensaPlatos(945, 625, 70, 70)

        self.mesas = [
            Mesa(455, 225, 50, 30,(-35, -40, 70, 60)),
            Mesa(675, 225, 50, 30,(-20, -40, 60, 60)),
            Mesa(455, 515, 50, 30),
            Mesa(675, 515, 50, 30),
            Mesa(765, 295, 50, 30, (-30, -20, 70, 40)),
            Mesa(765, 440, 50, 30, (-30, -20, 70, 40)),
            Mesa(380, 440, 50, 30,(-30, -20, 70, 40)),
            Mesa(380, 295, 50, 30,(-30, -20, 70, 40)),
            Mesa(380, 365, 50, 30,(-30, -20, 70, 40)),
        ]

        self.paredes = [
            pygame.Rect(0, 80, 1200, 40), # arriba
            pygame.Rect(0, 690, 1200, 40), # abajo
            pygame.Rect(120, 90, 60, 300), # izquierda 1
            pygame.Rect(1050, 100, 60, 440), # derecha 1
            pygame.Rect(120, 300, 20, 400), # izquierda 2
            pygame.Rect(1090, 400, 20, 300), # derecha 2
            pygame.Rect(380, 215, 60, 360),  # mesa 1
            pygame.Rect(380, 207, 440, 60),  # mesa 2
            pygame.Rect(380, 500, 440, 80),  # mesa 3
            pygame.Rect(370, 420, 70, 210),  # mesa 3 borde
            pygame.Rect(760, 220, 60, 345),  # mesa 4
            pygame.Rect(760, 420, 60, 210),  # mesa 4 borde
            pygame.Rect(170, 100, 60, 60),  # maseta 1
            pygame.Rect(950, 125, 60, 60),  # maseta 2
            pygame.Rect(1045, 650, 60, 60),  # maseta 2
            pygame.Rect(500, 65, 180, 100),  # estante
        ]

        self.recetas_posibles = recetas_posibles_cocina3
        self.espera_entre_recetas = espera_recetas_cocina3

    def siguiente_pantalla(self):
        return Menu()  # o una pantalla de victoria — ajusta según necesites