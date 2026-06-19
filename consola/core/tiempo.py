from time import time

def calcular_bono_total(estado):
    """Calcula todos los multiplicadores acumulados"""
    # Multiplicador base
    multiplicador = estado.get("multiplicador_global", 1.0)
    # Bono por renacimientos
    multiplicador *= estado.get("bono_renacimiento", 1.0)
    # Bono por logros desbloqueados
    logros = estado.get("logros", {})
    for logro in logros.values():
        if logro.get("desbloqueado", False):
            multiplicador *= logro.get("bono", 1.0)
    return round(multiplicador, 4)

def calcular_ganancia_total(estado):
    """Calcula la ganancia base por segundo"""
    # Ganancia de CPU
    base = round(estado.get("ganancia_cpu", 0.5), 2)
    # Ganancia de todos los generadores
    generadores = estado.get("generadores", {})
    for gen in generadores.values():
        cantidad = gen.get("cantidad", 0)
        ganancia = gen.get("ganancia", 0.0)
        base += cantidad * round(ganancia, 2)
    # Aplicar todos los bonos
    total = base * calcular_bono_total(estado)
    return round(total, 4)

def actualizar_ganancias(estado):
    """Actualiza el dinero según el tiempo transcurrido"""
    ahora = time()
    tiempo_anterior = estado.get("tiempo_ultima", ahora)
    segundos = max(0.0, round(ahora - tiempo_anterior, 3))  # Evita valores negativos

    if segundos <= 0:
        estado["tiempo_ultima"] = round(ahora, 3)
        return

    ganancia_por_segundo = calcular_ganancia_total(estado)
    ganancia_total = round(segundos * ganancia_por_segundo, 2)

    # Actualizar dinero
    dinero_actual = estado.get("dinero", 0.0)
    nuevo_dinero = round(dinero_actual + ganancia_total, 2)

    # Solo actualizar si no es negativo
    if nuevo_dinero >= dinero_actual:
        estado["dinero"] = nuevo_dinero

    # Actualizar estadísticas
    estadisticas = estado.setdefault("estadisticas", {})
    estadisticas["dinero_total_ganado"] = round(estadisticas.get("dinero_total_ganado", 0.0) + ganancia_total, 2)
    if ganancia_por_segundo > estadisticas.get("ganancia_maxima", 0.0):
        estadisticas["ganancia_maxima"] = ganancia_por_segundo
    estadisticas["tiempo_jugado"] = round(estadisticas.get("tiempo_jugado", 0.0) + segundos, 2)

    # Guardar marca de tiempo
    estado["tiempo_ultima"] = round(ahora, 3)
