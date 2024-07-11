import pygame
import json
import os
from datos import lista
from constantes import *
from puntajes import *
from preguntas import *
from movimientos import *
from mensaje import *

# Inicializar pygame
pygame.init()

# Configuración de pantalla
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
mostrar_puntuaciones_bool = False
pregunta_actual = lista[indice_pregunta_actual]
mostrar_mensaje_ganador_bool = False
mostrar_mensaje_perdedor_bool = False

#tiempo maximo del juego (2 minutos)
tiempo_maximo = 120
tiempo_transcurrido = 0

# Puntuaciones hardcodeadas
puntuaciones_hardcodeadas = [
    {"nombre": "Ana", "puntaje": 150},
    {"nombre": "Luis", "puntaje": 120},
    {"nombre": "Marta", "puntaje": 100},
    {"nombre": "Carlos", "puntaje": 80},
    {"nombre": "Elena", "puntaje": 60},
    {"nombre": "Emanuel", "puntaje": 120},
    {"nombre": "Juan", "puntaje": 90},
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
    (120, 370), (200, 370), (280, 370), (360, 370), (440, 370), (520, 370), (600, 370)
]

# Colores de las casillas
colores_casillas = [
    VERDE, NARANJA, ROJO, AMARILLO, CELESTE, MORADO, VERDE, NARANJA,
    ROJO, ROJO, CELESTE, VERDE, NARANJA, VERDE, MORADO
]

# Textos especiales en las casillas (avanza 1, retrocede 1, volver al inicio)
texto_casillas = [
    None, None, None, None, None, None, "avanza 1", None,
    None, "volver al inicio", None, "retrocede 1", None, None, None
]

# Rectángulo del participante (inicialmente antes de la primera casilla)
rect_participante = pygame.Rect(40, 250, 50, 80)

# Crear rectángulos para las casillas
rect_casillas = [pygame.Rect(x, y, 60, 60) for x, y in casillas]

# Rectángulo de la casilla de llegada
rect_llegada = pygame.Rect(480, 370, 60, 60)  

while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False
        if evento.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = evento.pos
            if mostrar_puntuaciones_bool:
                if ANCHO // 2 - 75 <= mouse_pos[0] <= ANCHO // 2 + 75 and ALTO - 100 <= mouse_pos[1] <= ALTO - 50:
                    mostrar_puntuaciones_bool = False
            else:
                if 195 <= mouse_pos[0] <= 345 and 478 <= mouse_pos[1] <= 558:  # Botón Comenzar
                    juego_comenzado = True
                    tiempo = 5
                    tiempo_transcurrido = 0
                if 408 <= mouse_pos[0] <= 558 and 478 <= mouse_pos[1] <= 558:  # Botón Terminar
                    nombre_ingresado = ingresar_nombre(pantalla, fuente)
                    mostrar_puntuaciones_bool = manejar_puntajes(nombre_ingresado, puntaje, puntuaciones_guardadas)
                    tiempo = 5  # Reiniciar el tiempo
                    tiempo_transcurrido = 0
                    juego_comenzado = False  # Marcar que el juego ha terminado
                    
                if juego_comenzado:
                    for i, (x, y) in enumerate(posiciones_opciones):
                        if x <= mouse_pos[0] <= x + 150 and y <= mouse_pos[1] <= y + 50:
                            respuesta_correcta = verificar_respuesta(pregunta_actual, ['a', 'b', 'c'][i])
                            if respuesta_correcta:
                                puntaje += 10
                                if casilla_actual == 7:
                                    casilla_actual = 8  # Avanza 2 casillas
                                else:
                                    casilla_actual += 2
                                if casilla_actual > 14:
                                    mostrar_mensaje_ganador(pantalla, fuente, ANCHO, ALTO, puntaje, puntuaciones_guardadas)
                                    mostrar_mensaje_ganador_bool = False
                                    corriendo = False

                                if casilla_actual >= len(rect_casillas):  # Si llega al final del tablero
                                    casilla_actual = len(rect_casillas) - 1
                            else:
                                casilla_actual -= 1
                                if casilla_actual < 0:
                                    casilla_actual = 0

                            rect_participante.midbottom = rect_casillas[casilla_actual].midtop
                            indice_pregunta_actual += 1
                            if indice_pregunta_actual < len(lista):
                                pregunta_actual = lista[indice_pregunta_actual]
                            tiempo = 5
                        
                if 640 <= mouse_pos[0] <= 790 and 10 <= mouse_pos[1] <= 60:  # Botón para mostrar puntuaciones
                    mostrar_puntuaciones_bool = True


    if mostrar_puntuaciones_bool:
        mostrar_puntuaciones(pantalla, fuente, puntuaciones_hardcodeadas, puntuaciones_guardadas, ANCHO, ALTO)
    else:
        pantalla.fill(AZUL)

        # Dibujar casillas
        for i, (x, y) in enumerate(casillas):
            pygame.draw.rect(pantalla, colores_casillas[i], (x, y, 68, 60))
            if texto_casillas[i] is not None:
                texto_especial = fuente_pequena.render(texto_casillas[i], True, BLANCO)
                pantalla.blit(texto_especial, (x + 2, y + 20))

        # Dibuja el participante
        pantalla.blit(imagen_participante, (rect_participante.x, rect_participante.y))

        # Dibujar imagen principal arriba de la casilla
        pantalla.blit(imagen_principal, (5, 10))

        # Dibujar la casilla de llegada
        pantalla.blit(imagen_llegada, (680, 360))

        # Dibuja botones de comenzar y terminar
        pygame.draw.rect(pantalla, CELESTE, (408, 478, 150, 80))
        pygame.draw.rect(pantalla, CELESTE, (195, 478, 150, 80))
        texto_comenzar = fuente.render("Comenzar", True, NEGRO)
        texto_terminar = fuente.render("Terminar", True, NEGRO)
        pantalla.blit(texto_comenzar, (210, 500))
        pantalla.blit(texto_terminar, (430, 500))

        # Mostrar puntaje y tiempo
        texto_puntaje = fuente.render(f"Puntaje: {puntaje}", True, BLANCO)
        texto_tiempo = fuente.render(f"Tiempo: {tiempo:.0f}", True, BLANCO)
        pantalla.blit(texto_puntaje, (640, 70))
        pantalla.blit(texto_tiempo, (640, 40))

        #mostrar reloj global
        tiempo_restante = tiempo_maximo - tiempo_transcurrido
        minutos = int(tiempo_restante) // 60
        segundos = int(tiempo_restante) % 60
        texto_reloj= fuente.render(f"RELOJ: {minutos:02}:{segundos:02}", True, BLANCO)
        pantalla.blit(texto_reloj, (10, 180))

        if juego_comenzado:
            if indice_pregunta_actual < len(lista):
                texto_pregunta = fuente.render(pregunta_actual["pregunta"], True, BLANCO)
                pantalla.blit(texto_pregunta, (170, 10))
                for i, (x, y) in enumerate(posiciones_opciones):
                    pygame.draw.rect(pantalla, CELESTE, (x, y, 150, 50))
                    texto_opcion = fuente.render(pregunta_actual[["a", "b", "c"][i]], True, NEGRO)
                    pantalla.blit(texto_opcion, (x + 5, y + 5))
            else:
                juego_comenzado = False
                mostrar_puntuaciones_bool = True

    # Control del tiempo
    if juego_comenzado:
        tiempo -= reloj.get_time() / 1000
        tiempo_transcurrido += reloj.get_time() / 1000
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
    casilla_actual = mover_participante(casilla_actual, texto_casillas, rect_casillas, rect_participante)

    # Comprobar si el participante ha llegado a la casilla de llegada
    if rect_participante.colliderect(rect_llegada) and indice_pregunta_actual < len(lista):
        mostrar_mensaje_ganador_bool = True

    # Mostrar mensaje "Has ganado"
    if mostrar_mensaje_ganador_bool:
        mostrar_mensaje_ganador(pantalla, fuente, ANCHO, ALTO, puntaje, puntuaciones_guardadas)
        mostrar_mensaje_ganador_bool = False
        corriendo = False

    # Mostrar mensaje "Has perdido"
    if tiempo_restante <= 0:
        mostrar_mensaje_perdedor = True

    if indice_pregunta_actual >= len(lista) and not rect_participante.colliderect(rect_llegada):
        mostrar_mensaje_perdedor_bool = True

    if mostrar_mensaje_perdedor_bool:
        mostrar_mensaje_perdedor(pantalla, fuente, ANCHO, ALTO)
        mostrar_mensaje_perdedor_bool = False
        corriendo = False

    pygame.display.flip()
    reloj.tick(60)

pygame.quit()