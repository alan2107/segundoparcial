import pygame

def mover_participante(casilla_actual, texto_casillas, rect_casillas, rect_participante):
    if texto_casillas[casilla_actual] == "avanza 1":
        casilla_actual += 1
        if casilla_actual >= len(rect_casillas):
            casilla_actual = len(rect_casillas) - 1
        rect_participante.topleft = rect_casillas[casilla_actual].topleft
    elif texto_casillas[casilla_actual] == "retrocede 1":
        casilla_actual -= 1
        if casilla_actual < 0:
            casilla_actual = 0
        rect_participante.topleft = rect_casillas[casilla_actual].topleft

def verificar_colision(rect_participante, rect_llegada, indice_pregunta_actual, lista):
    return rect_participante.colliderect(rect_llegada) and indice_pregunta_actual < len(lista)