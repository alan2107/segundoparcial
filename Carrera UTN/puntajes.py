import json
import os
import pygame
from constantes import *

def leer_puntuaciones():
    if os.path.exists("puntajes.json"):
        with open("puntajes.json", "r") as archivo:
            return [json.loads(linea) for linea in archivo]
    else:
        return []

def guardar_puntuacion(datos_jugador):
    with open("puntajes.json", "a") as archivo:
        json.dump(datos_jugador, archivo)
        archivo.write("\n")

def mostrar_puntuaciones(pantalla, fuente, puntuaciones_hardcodeadas, puntuaciones_guardadas, ANCHO, ALTO):
    pantalla.fill(AZUL)
    titulo = fuente.render("Puntuaciones", True, BLANCO)
    pantalla.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 20))

    puntuaciones_totales = puntuaciones_hardcodeadas + puntuaciones_guardadas
    puntuaciones_totales = sorted(puntuaciones_totales, key=lambda x: x['puntaje'], reverse=True)[:10]

    for i, puntuacion in enumerate(puntuaciones_totales):
        texto_puntuacion = fuente.render(f"{puntuacion['nombre']}: {puntuacion['puntaje']}", True, BLANCO)
        pantalla.blit(texto_puntuacion, (ANCHO // 2 - texto_puntuacion.get_width() // 2, 80 + i * 40))

    texto_volver = fuente.render("Salir", True, NEGRO)
    pygame.draw.rect(pantalla, CELESTE, (ANCHO // 2 - 75, ALTO - 100, 150, 50))
    pantalla.blit(texto_volver, (ANCHO // 2 - texto_volver.get_width() // 2, ALTO - 90))