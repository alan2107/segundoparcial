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

def ingresar_nombre(pantalla, fuente):
    nombre = ""
    ingresando_nombre = True

    while ingresando_nombre:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    ingresando_nombre = False
                elif evento.key == pygame.K_BACKSPACE:
                    nombre = nombre[:-1]
                else:
                    nombre += evento.unicode

        pantalla.fill(AZUL)
        texto_ingresar_nombre = fuente.render("Ingrese su nombre:", True, BLANCO)
        texto_rect = texto_ingresar_nombre.get_rect(center=(ANCHO // 2, ALTO // 2 - 50))
        pantalla.blit(texto_ingresar_nombre, texto_rect)

        pygame.draw.rect(pantalla, BLANCO, (ANCHO // 2 - 100, ALTO // 2, 200, 50), 2)
        texto_nombre = fuente.render(nombre, True, BLANCO)
        pantalla.blit(texto_nombre, (ANCHO // 2 - 90, ALTO // 2 + 10))

        pygame.display.flip()

    return nombre

def manejar_puntajes(nombre_ingresado, puntaje, puntuaciones_guardadas):
    if nombre_ingresado:
        datos_jugador = {"nombre": nombre_ingresado, "puntaje": puntaje}
        guardar_puntuacion(datos_jugador)
        puntuaciones_guardadas.append(datos_jugador)
        return True  # Indicar que se deben mostrar las puntuaciones al terminar
    return False  # No se mostraran las puntuaciones al terminar