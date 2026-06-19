from time import time

def calcular_ganancia_total(estado):
    base = round(estado["ganancia_cpu"], 2)
    for gen in estado["generadores"].values():
        base += gen["cantidad"] * round(gen["ganancia"], 2)
    return round(base * round(estado["multiplicador_global"], 2), 4)

def actualizar_ganancias(estado):
    ahora = time()
    segundos = ahora - estado["tiempo_ultima"]
    ganancia = round(segundos * calcular_ganancia_total(estado), 2)
    nuevo_dinero = round(estado["dinero"] + ganancia, 2)
    
    # Solo actualizar si es mayor o igual
    if nuevo_dinero >= estado["dinero"]:
        estado["dinero"] = nuevo_dinero
    
    estado["tiempo_ultima"] = round(ahora, 3)
