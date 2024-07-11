import pygame
import json
from puntajes import *
def mostrar_mensaje_ganador(pantalla, fuente, ANCHO, ALTO, puntaje, puntuaciones_guardadas):
    pantalla.fill((0, 0, 255))  # Fondo azul
    mensaje_ganador = fuente.render("¡Has ganado!", True, (255, 255, 255))  # Texto blanco
    pantalla.blit(mensaje_ganador, (ANCHO // 2 - mensaje_ganador.get_width() // 2, ALTO // 2 - mensaje_ganador.get_height() // 2))
    pygame.display.flip()
    nombre = input("Ingresa tu nombre: ")
    datos_jugador = {"nombre": nombre, "puntaje": puntaje}
    guardar_puntuacion(datos_jugador)
    puntuaciones_guardadas.append(datos_jugador)
    pygame.time.delay(3000)  # Espera 3 segundos

def mostrar_mensaje_perdedor(pantalla, fuente, ANCHO, ALTO):
    pantalla.fill((0, 0, 255))  # Fondo azul
    mensaje_perdedor = fuente.render("¡Has perdido!", True, (255, 255, 255))  # Texto blanco
    pantalla.blit(mensaje_perdedor, (ANCHO // 2 - mensaje_perdedor.get_width() // 2, ALTO // 2 - mensaje_perdedor.get_height() // 2))
    pygame.display.flip()
    pygame.time.delay(3000)  # Espera 3 segundos