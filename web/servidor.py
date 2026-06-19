from http.server import SimpleHTTPRequestHandler, HTTPServer
import json
import os
import time
import shutil
import math

# 📁 Carpeta de datos única
CARPETA_DATOS = "datos"
ARCHIVO_PROGRESO = os.path.join(CARPETA_DATOS, "progreso.json")
ARCHIVO_RESPALDO = os.path.join(CARPETA_DATOS, "respaldo_progreso.json")

def crear_estructura():
    os.makedirs(CARPETA_DATOS, exist_ok=True)

def estado_base():
    """Valores iniciales, usados para fusionar y reiniciar correctamente"""
    return {
        "dinero": 100.00,
        "multiplicador_global": 1.00,
        "nivel_cpu": 1,
        "ganancia_cpu": 0.50,
        "costo_cpu": 150.00,
        "renacimientos": 0,
        "bono_renacimiento": 1.00,
        "tiempo_ultima": time.time(),
        "estadisticas": {
            "dinero_total_ganado": 0.00,
            "mejoras_cpu": 0,
            "generadores_comprados": 0,
            "puertas_abiertas": 0,
            "tiempo_jugado": 0.00,
            "ganancia_maxima": 0.00
        },
        "logros": {
            "primeros_1k": {"desbloqueado": False, "bono": 1.10, "descripcion": "Alcanzar $1.000 → +10% ganancia"},
            "3_puertas": {"desbloqueado": False, "bono": 1.20, "descripcion": "Abrir 3 puertas → +20% ganancia"},
            "2_renacimientos": {"desbloqueado": False, "bono": 1.30, "descripcion": "Renacer 2 veces → +30% ganancia"},
            "primer_millon": {"desbloqueado": False, "bono": 1.50, "descripcion": "Alcanzar $1.000.000 → +50% ganancia"},
            "10_renacimientos": {"desbloqueado": False, "bono": 2.00, "descripcion": "Renacer 10 veces → Doble ganancia"}
        },
        "mejoras_pasivas": {
            "ahorro": {"nivel": 0, "efecto": 0.00, "costo": 1},
            "descuento": {"nivel": 0, "efecto": 0.00, "costo": 2},
            "inicio_mejorado": {"nivel": 0, "efecto": 100.00, "costo": 3}
        },
        "generadores": {
            "basico": {"cantidad": 0, "ganancia": 0.20, "costo": 200.00},
            "medio": {"cantidad": 0, "ganancia": 1.00, "costo": 1200.00},
            "avanzado": {"cantidad": 0, "ganancia": 5.00, "costo": 7500.00},
            "industrial": {"cantidad": 0, "ganancia": 25.00, "costo": 40000.00},
            "nuclear": {"cantidad": 0, "ganancia": 150.00, "costo": 250000.00},
            "cuantico": {"cantidad": 0, "ganancia": 1000.00, "costo": 2000000.00},
            "galactico": {"cantidad": 0, "ganancia": 8000.00, "costo": 15000000.00}
        },
        "puertas": {
            "p1": {"nombre": "Almacén Básico", "abierta": False, "costo": 200.00, "bono": 0.50},
            "p2": {"nombre": "Centro de Datos", "abierta": False, "costo": 1000.00, "bono": 1.50},
            "p3": {"nombre": "Sala de Procesos", "abierta": False, "costo": 5000.00, "bono": 4.00},
            "p4": {"nombre": "Servidor Principal", "abierta": False, "costo": 25000.00, "bono": 12.00},
            "p5": {"nombre": "Núcleo de Energía", "abierta": False, "costo": 130000.00, "bono": 45.00},
            "p6": {"nombre": "Red Global", "abierta": False, "costo": 700000.00, "bono": 180.00},
            "p7": {"nombre": "Centro Galáctico", "abierta": False, "costo": 4000000.00, "bono": 800.00},
            "p8": {"nombre": "Universo Digital", "abierta": False, "costo": 25000000.00, "bono": 3500.00}
        }
    }

def fusionar(datos_actuales, datos_defecto):
    """Agrega claves nuevas sin borrar lo que ya está guardado"""
    for clave, valor in datos_defecto.items():
        if clave not in datos_actuales:
            datos_actuales[clave] = valor
        elif isinstance(valor, dict) and isinstance(datos_actuales.get(clave), dict):
            fusionar(datos_actuales[clave], valor)
    return datos_actuales

def cargar_progreso():
    crear_estructura()
    estado = estado_base()
    if os.path.exists(ARCHIVO_PROGRESO):
        try:
            with open(ARCHIVO_PROGRESO, "r", encoding="utf-8") as f:
                guardado = json.load(f)
            estado = fusionar(guardado, estado)
        except Exception as e:
            print(f"⚠️ Archivo de progreso reiniciado por error: {e}")
    return estado

def redondear_recursivo(d):
    for k, v in d.items():
        if isinstance(v, float):
            d[k] = round(v, 2)
        elif isinstance(v, dict):
            redondear_recursivo(v)
    return d

def guardar_progreso(estado):
    estado = redondear_recursivo(estado.copy())
    with open(ARCHIVO_PROGRESO, "w", encoding="utf-8") as f:
        json.dump(estado, f, indent=2, ensure_ascii=False)
    shutil.copy2(ARCHIVO_PROGRESO, ARCHIVO_RESPALDO)

def calcular_bono_logros(estado):
    multiplicador = 1.0
    for logro in estado["logros"].values():
        if logro["desbloqueado"]:
            multiplicador *= logro["bono"]
    return round(multiplicador, 2)

def verificar_logros(estado):
    if not estado["logros"]["primeros_1k"]["desbloqueado"] and estado["dinero"] >= 1000:
        estado["logros"]["primeros_1k"]["desbloqueado"] = True
    if not estado["logros"]["3_puertas"]["desbloqueado"] and estado["estadisticas"]["puertas_abiertas"] >= 3:
        estado["logros"]["3_puertas"]["desbloqueado"] = True
    if not estado["logros"]["2_renacimientos"]["desbloqueado"] and estado["renacimientos"] >= 2:
        estado["logros"]["2_renacimientos"]["desbloqueado"] = True
    if not estado["logros"]["primer_millon"]["desbloqueado"] and estado["dinero"] >= 1000000:
        estado["logros"]["primer_millon"]["desbloqueado"] = True
    if not estado["logros"]["10_renacimientos"]["desbloqueado"] and estado["renacimientos"] >= 10:
        estado["logros"]["10_renacimientos"]["desbloqueado"] = True

class Manejador(SimpleHTTPRequestHandler):
    extensions_map = {
        ".html": "text/html; charset=utf-8",
        ".css": "text/css; charset=utf-8",
        ".js": "application/javascript; charset=utf-8",
        ".json": "application/json; charset=utf-8",
        "": "text/plain; charset=utf-8"
    }

    def do_GET(self):
        if self.path == "/api/estado":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            estado = cargar_progreso()
            ahora = time.time()
            segundos = ahora - estado["tiempo_ultima"]
            estado["estadisticas"]["tiempo_jugado"] += segundos

            base = estado["ganancia_cpu"]
            for gen in estado["generadores"].values():
                base += gen["cantidad"] * gen["ganancia"]

            bono_logros = calcular_bono_logros(estado)
            total_mult = estado["multiplicador_global"] * estado["bono_renacimiento"] * bono_logros
            ganancia = segundos * base * total_mult

            estado["dinero"] += ganancia
            estado["estadisticas"]["dinero_total_ganado"] += ganancia
            if (base * total_mult) > estado["estadisticas"]["ganancia_maxima"]:
                estado["estadisticas"]["ganancia_maxima"] = round(base * total_mult, 2)

            verificar_logros(estado)
            estado["tiempo_ultima"] = round(ahora, 3)
            guardar_progreso(estado)
            self.wfile.write(json.dumps(estado).encode("utf-8"))
            return
        return super().do_GET()

    def do_POST(self):
        if self.path.startswith("/api/"):
            largo = int(self.headers.get("Content-Length", 0))
            datos = json.loads(self.rfile.read(largo) or "{}")
            accion = self.path.replace("/api/", "")
            estado = cargar_progreso()
            descuento = 1 - estado["mejoras_pasivas"]["descuento"]["efecto"]

            if accion == "mejorar_cpu":
                costo = estado["costo_cpu"] * descuento
                if estado["dinero"] >= costo:
                    estado["dinero"] -= costo
                    estado["nivel_cpu"] += 1
                    estado["ganancia_cpu"] = round(estado["ganancia_cpu"] * 1.6, 2)
                    estado["costo_cpu"] = round(estado["costo_cpu"] * 2.0, 2)
                    estado["estadisticas"]["mejoras_cpu"] += 1

            elif accion == "comprar_multiplicador":
                costo = 100 * estado["multiplicador_global"] * 1.9 * descuento
                if estado["dinero"] >= costo:
                    estado["dinero"] -= round(costo, 2)
                    estado["multiplicador_global"] = round(estado["multiplicador_global"] * 1.3, 2)

            elif accion == "comprar_generador":
                tipo = datos.get("tipo")
                if tipo in estado["generadores"]:
                    gen = estado["generadores"][tipo]
                    costo = gen["costo"] * descuento
                    if estado["dinero"] >= costo:
                        estado["dinero"] -= round(costo, 2)
                        gen["cantidad"] += 1
                        gen["costo"] = round(gen["costo"] * 1.75, 2)
                        estado["estadisticas"]["generadores_comprados"] += 1

            elif accion == "comprar_max_generador":
                tipo = datos.get("tipo")
                if tipo in estado["generadores"]:
                    gen = estado["generadores"][tipo]
                    while estado["dinero"] >= (gen["costo"] * descuento):
                        costo = round(gen["costo"] * descuento, 2)
                        estado["dinero"] -= costo
                        gen["cantidad"] += 1
                        gen["costo"] = round(gen["costo"] * 1.75, 2)
                        estado["estadisticas"]["generadores_comprados"] += 1

            elif accion == "abrir_puerta":
                id_puerta = datos.get("id")
                if id_puerta in estado["puertas"]:
                    puerta = estado["puertas"][id_puerta]
                    costo = puerta["costo"] * descuento
                    if not puerta["abierta"] and estado["dinero"] >= costo:
                        estado["dinero"] -= round(costo, 2)
                        puerta["abierta"] = True
                        estado["multiplicador_global"] = round(estado["multiplicador_global"] + puerta["bono"], 2)
                        estado["estadisticas"]["puertas_abiertas"] += 1

            # ✅ RENACIMIENTO CORREGIDO
            elif accion == "hacer_renacimiento":
                if estado["nivel_cpu"] >= 5:
                    estado["renacimientos"] += 1
                    estado["bono_renacimiento"] = round(estado["bono_renacimiento"] * 1.5, 2)
                    # Reiniciar valores pero mantener mejoras pasivas, logros y estadísticas
                    estado["dinero"] = estado["mejoras_pasivas"]["inicio_mejorado"]["efecto"]
                    estado["multiplicador_global"] = 1.00
                    estado["nivel_cpu"] = 1
                    estado["ganancia_cpu"] = 0.50
                    estado["costo_cpu"] = 150.00
                    # Reiniciar generadores a su valor base
                    for tipo, gen in estado["generadores"].items():
                        gen["cantidad"] = 0
                        gen["costo"] = estado_base()["generadores"][tipo]["costo"]
                    # Reiniciar puertas
                    for puerta in estado["puertas"].values():
                        puerta["abierta"] = False
                    # Actualizar tiempo
                    estado["tiempo_ultima"] = time.time()

            elif accion == "mejorar_pasiva":
                tipo = datos.get("tipo")
                if tipo in estado["mejoras_pasivas"]:
                    mejora = estado["mejoras_pasivas"][tipo]
                    if estado["renacimientos"] >= mejora["costo"]:
                        estado["renacimientos"] -= mejora["costo"]
                        mejora["nivel"] += 1
                        if tipo == "ahorro":
                            mejora["efecto"] = round(mejora["nivel"] * 0.02, 2)
                        elif tipo == "descuento":
                            mejora["efecto"] = round(mejora["nivel"] * 0.015, 3)
                        elif tipo == "inicio_mejorado":
                            mejora["efecto"] = round(100 * (1.2 ** mejora["nivel"]), 2)

            guardar_progreso(estado)
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"ok": True}).encode("utf-8"))
            return

        self.send_response(404)
        self.end_headers()

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    servidor = HTTPServer(("0.0.0.0", 8080), Manejador)
    print("✅ Servidor corriendo en http://localhost:8080")
    print("📁 Datos guardados en:", ARCHIVO_PROGRESO)
    servidor.serve_forever()
