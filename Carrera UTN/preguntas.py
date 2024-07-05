from datos import lista

def obtener_pregunta(indice_pregunta_actual):
    if indice_pregunta_actual < len(lista):
        return lista[indice_pregunta_actual]
    else:
        return None

def verificar_respuesta(pregunta, respuesta_seleccionada):
    return respuesta_seleccionada == pregunta['correcta']