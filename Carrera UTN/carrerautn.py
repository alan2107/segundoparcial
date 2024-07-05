import pygame
import json
import os
from datos import lista
from constantes import *
from puntajes import *
from preguntas import *
from movimientos import *

# Inicializar pygame
pygame.init()

# Configuración de pantalla
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("CARRERA UTN")

# Cargar imágenes
imagen_principal = pygame.image.load("utn.png")
imagen_principal = pygame.transform.scale(imagen_principal, (150, 150))
imagen_participante = pygame.image.load("hombre.jpg")
imagen_participante = pygame.transform.scale(imagen_participante, (50, 80))
imagen_llegada = pygame.image.load('utn.png')
imagen_llegada = pygame.transform.scale(imagen_llegada, (80, 80))

# Variables del juego
puntaje = 0
tiempo = 5
indice_pregunta_actual = 0
casilla_actual = 0
juego_comenzado = False
mostrar_puntuaciones = False
pregunta_actual = lista[indice_pregunta_actual]
mostrar_mensaje_ganador = False
mostrar_mensaje_perdedor = False

# Puntuaciones hardcodeadas
puntuaciones_hardcodeadas = [
    {"nombre": "Ana", "puntaje": 150},
    {"nombre": "Luis", "puntaje": 120},
    {"nombre": "Marta", "puntaje": 100},
    {"nombre": "Carlos", "puntaje": 80},
    {"nombre": "Elena", "puntaje": 60},
]

# Leer puntuaciones guardadas
puntuaciones_guardadas = leer_puntuaciones()

# Fuentes
fuente = pygame.font.SysFont("Arial", 24)
fuente_pequena = pygame.font.SysFont("Arial", 10)

# Posiciones de los botones de opciones (dinámicas)
posiciones_opciones = [(195, 101), (369, 101), (539, 101)]

# Bucle principal del juego
corriendo = True
reloj = pygame.time.Clock()

# Posiciones de las casillas (dinámicas)
casillas = [
    (120, 270), (200, 270), (280, 270), (360, 270), (440, 270), (520, 270), (600, 270), (680, 270),
    (120, 370), (200, 370), (280, 370), (360, 370), (440, 370), (520, 370), (600, 370), (680 , 370)
]

# Colores de las casillas
colores_casillas = [
    VERDE, NARANJA, ROJO, AMARILLO, CELESTE, MORADO, VERDE, NARANJA,
    ROJO, AMARILLO, CELESTE, VERDE, NARANJA, VERDE, MORADO, CELESTE 
]

# Textos especiales en las casillas (avanza 1, retrocede 1)
texto_casillas = [
    None, None, None, None, None, None, "avanza 1", None,
    None, None, None, "retrocede 1", None, None, None, None
]

# Rectángulo del participante (inicialmente antes de la primera casilla)
rect_participante = pygame.Rect(40, 250, 50, 80)

# Crear rectángulos para las casillas
rect_casillas = [pygame.Rect(x, y, 60, 60) for x, y in casillas]

# Rectángulo de la casilla de llegada
rect_llegada = pygame.Rect(680, 370, 60, 60)  # Ajustar según sea necesario

while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False
        if evento.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = evento.pos
            if mostrar_puntuaciones:
                if ANCHO // 2 - 75 <= mouse_pos[0] <= ANCHO // 2 + 75 and ALTO - 100 <= mouse_pos[1] <= ALTO - 50:
                    mostrar_puntuaciones = False
            else:
                if 195 <= mouse_pos[0] <= 345 and 478 <= mouse_pos[1] <= 558:  # Botón Comenzar
                    juego_comenzado = True
                    tiempo = 5
                if 408 <= mouse_pos[0] <= 558 and 478 <= mouse_pos[1] <= 558:  # Botón Terminar
                    nombre = input("Ingresa tu nombre: ")
                    datos_jugador = {"nombre": nombre, "puntaje": puntaje}
                    guardar_puntuacion(datos_jugador)
                    puntuaciones_guardadas.append(datos_jugador)
                    mostrar_puntuaciones = True  # Mostrar la pantalla de puntuaciones al terminar
                if juego_comenzado:
                    for i, (x, y) in enumerate(posiciones_opciones):
                        if x <= mouse_pos[0] <= x + 150 and y <= mouse_pos[1] <= y + 50:
                            respuesta_correcta = verificar_respuesta(pregunta_actual, ['a', 'b', 'c'][i])
                            if respuesta_correcta:
                                puntaje += 10
                                
                                if casilla_actual < len(rect_casillas) - 1:  # Solo avanzar si no está en la última casilla
                                    casilla_actual += 2  # Avanza 2 casillas
                                if casilla_actual >= len(rect_casillas):  # Si llega al final del tablero
                                    casilla_actual = len(rect_casillas) - 1
                            else:
                                casilla_actual -= 1
                                if casilla_actual < 0:
                                    casilla_actual = 0
                            rect_participante.topleft = rect_casillas[casilla_actual].topleft
                            indice_pregunta_actual += 1
                            if indice_pregunta_actual < len(lista):
                                pregunta_actual = lista[indice_pregunta_actual]
                            tiempo = 5
                
                if 640 <= mouse_pos[0] <= 790 and 10 <= mouse_pos[1] <= 60:  # Botón para mostrar puntuaciones
                    mostrar_puntuaciones = True

    if mostrar_puntuaciones:
        mostrar_puntuaciones(pantalla, fuente, puntuaciones_hardcodeadas, puntuaciones_guardadas, ANCHO, ALTO)
    else:
        pantalla.fill(AZUL)

        # Dibujar casillas
        for i, (x, y) in enumerate(casillas):
            pygame.draw.rect(pantalla, colores_casillas[i], (x, y, 60, 60))
            if texto_casillas[i] is not None:
                texto_especial = fuente_pequena.render(texto_casillas[i], True, BLANCO)
                pantalla.blit(texto_especial, (x + 5, y + 20))

        # Dibuja el participante
        pantalla.blit(imagen_participante, (rect_participante.x, rect_participante.y))

        # Dibujar imagen principal arriba de la casilla
        pantalla.blit(imagen_principal, (5, 10))

        # Dibujar la casilla de llegada
        pantalla.blit(imagen_llegada, (660, 370))

        # Dibuja botones de comenzar y terminar
        pygame.draw.rect(pantalla, CELESTE, (408, 478, 150, 80))
        pygame.draw.rect(pantalla, CELESTE, (195, 478, 150, 80))
        texto_comenzar = fuente.render("Comenzar", True, NEGRO)
        texto_terminar = fuente.render("Terminar", True, NEGRO)
        pantalla.blit(texto_comenzar, (200, 500))
        pantalla.blit(texto_terminar, (420, 500))

        # Mostrar puntaje y tiempo
        texto_puntaje = fuente.render(f"Puntaje: {puntaje}", True, BLANCO)
        texto_tiempo = fuente.render(f"Tiempo: {tiempo:.0f}", True, BLANCO)
        pantalla.blit(texto_puntaje, (640, 46))
        pantalla.blit(texto_tiempo, (640, 10))

        if juego_comenzado:
            if indice_pregunta_actual < len(lista):
                texto_pregunta = fuente.render(pregunta_actual["pregunta"], True, BLANCO)
                pantalla.blit(texto_pregunta, (195, 10))
                for i, (x, y) in enumerate(posiciones_opciones):
                    pygame.draw.rect(pantalla, CELESTE, (x, y, 150, 50))
                    texto_opcion = fuente.render(pregunta_actual[["a", "b", "c"][i]], True, NEGRO)
                    pantalla.blit(texto_opcion, (x + 5, y + 5))
            else:
                juego_comenzado = False
                mostrar_puntuaciones = True

    # Control del tiempo
    if juego_comenzado:
        tiempo -= reloj.get_time() / 1000
        if tiempo <= 0:
            indice_pregunta_actual += 1
            if indice_pregunta_actual < len(lista):
                pregunta_actual = lista[indice_pregunta_actual]
            tiempo = 5
            casilla_actual -= 1  # Retroceder una casilla si no se responde a tiempo
            if casilla_actual < 0:
                casilla_actual = 0
            rect_participante.topleft = rect_casillas[casilla_actual].topleft

    # Comprobar colisiones con casillas especiales
    mover_participante(casilla_actual, texto_casillas, rect_casillas, rect_participante)

    # Comprobar si el participante ha llegado a la casilla de llegada
    if rect_participante.colliderect(rect_llegada) and indice_pregunta_actual < len(lista):
        mostrar_mensaje_ganador = True

    # Mostrar mensaje "Has ganado"
    if mostrar_mensaje_ganador:
        pantalla.fill(AZUL)
        mensaje_ganador = fuente.render("¡Has ganado!", True, BLANCO)
        pantalla.blit(mensaje_ganador, (ANCHO // 2 - mensaje_ganador.get_width() // 2, ALTO // 2 - mensaje_ganador.get_height() // 2))
        pygame.display.flip()
        nombre = input("Ingresa tu nombre: ")
        datos_jugador = {"nombre": nombre, "puntaje": puntaje}
        guardar_puntuacion(datos_jugador)
        puntuaciones_guardadas.append(datos_jugador)
        pygame.time.delay(3000)  # Espera 3 segundos
        mostrar_mensaje_ganador = False
        corriendo = False

    # Mostrar mensaje "Has perdido"
    if indice_pregunta_actual >= len(lista) and not rect_participante.colliderect(rect_llegada):
        mostrar_mensaje_perdedor = True

    if mostrar_mensaje_perdedor:
        pantalla.fill(AZUL)
        mensaje_perdedor = fuente.render("¡Has perdido!", True, BLANCO)
        pantalla.blit(mensaje_perdedor, (ANCHO // 2 - mensaje_perdedor.get_width() // 2, ALTO // 2 - mensaje_perdedor.get_height() // 2))
        pygame.display.flip()
        pygame.time.delay(3000)  # Espera 3 segundos
        mostrar_mensaje_perdedor = False
        corriendo = False

    pygame.display.flip()
    reloj.tick(60)

pygame.quit()