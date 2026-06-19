from http.server import SimpleHTTPRequestHandler, HTTPServer
import json
import os
import time
import shutil

# 📁 RUTA FIJA DE GUARDADO - NO CAMBIAR
CARPETA_DATOS = "datos"
ARCHIVO_PROGRESO = os.path.join(CARPETA_DATOS, "progreso.json")
ARCHIVO_RESPALDO = os.path.join(CARPETA_DATOS, "respaldo_progreso.json")

def crear_estructura():
    """Crea la carpeta y archivos si no existen"""
    os.makedirs(CARPETA_DATOS, exist_ok=True)

def estado_base():
    """Devuelve la estructura completa por defecto - se actualiza al agregar funciones"""
    return {
        "dinero": 100.00,
        "multiplicador_global": 1.00,
        "nivel_cpu": 1,
        "ganancia_cpu": 0.50,
        "costo_cpu": 150.00,
        "renacimientos": 0,
        "bono_renacimiento": 1.00,
        "tiempo_ultima": time.time(),
        # Estadísticas
        "estadisticas": {
            "dinero_total_ganado": 0.00,
            "mejoras_cpu": 0,
            "generadores_comprados": 0,
            "puertas_abiertas": 0,
            "tiempo_jugado": 0.00,
            "ganancia_maxima": 0.00
        },
        # Logros
        "logros": {
            "primeros_1k": {"desbloqueado": False, "bono": 1.10, "descripcion": "Alcanzar $1.000 → +10% ganancia"},
            "3_puertas": {"desbloqueado": False, "bono": 1.20, "descripcion": "Abrir 3 puertas → +20% ganancia"},
            "2_renacimientos": {"desbloqueado": False, "bono": 1.30, "descripcion": "Renacer 2 veces → +30% ganancia"},
            "primer_millon": {"desbloqueado": False, "bono": 1.50, "descripcion": "Alcanzar $1.000.000 → +50% ganancia"},
            "10_renacimientos": {"desbloqueado": False, "bono": 2.00, "descripcion": "Renacer 10 veces → Doble ganancia"}
        },
        # Mejoras pasivas / Prestigio
        "mejoras_pasivas": {
            "ahorro": {"nivel": 0, "efecto": 0.00, "costo": 1},
            "descuento": {"nivel": 0, "efecto": 0.00, "costo": 2},
            "inicio_mejorado": {"nivel": 0, "efecto": 100.00, "costo": 3}
        },
        # Generadores
        "generadores": {
            "basico": {"cantidad": 0, "ganancia": 0.20, "costo": 200.00},
            "medio": {"cantidad": 0, "ganancia": 1.00, "costo": 1200.00},
            "avanzado": {"cantidad": 0, "ganancia": 5.00, "costo": 7500.00},
            "industrial": {"cantidad": 0, "ganancia": 25.00, "costo": 40000.00},
            "nuclear": {"cantidad": 0, "ganancia": 150.00, "costo": 250000.00},
            "cuantico": {"cantidad": 0, "ganancia": 1000.00, "costo": 2000000.00},
            "galactico": {"cantidad": 0, "ganancia": 8000.00, "costo": 15000000.00}
        },
        # Puertas
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

def cargar_progreso():
    """Carga el progreso y agrega automáticamente datos nuevos si faltan"""
    crear_estructura()
    estado = estado_base()

    if os.path.exists(ARCHIVO_PROGRESO):
        try:
            with open(ARCHIVO_PROGRESO, "r", encoding="utf-8") as f:
                datos_guardados = json.load(f)

            # ✅ FUSIÓN SEGURA: mantiene lo guardado, agrega lo nuevo
            def fusionar(datos_actuales, datos_defecto):
                for clave, valor in datos_defecto.items():
                    if clave not in datos_actuales:
                        datos_actuales[clave] = valor
                    elif isinstance(valor, dict):
                        if not isinstance(datos_actuales[clave], dict):
                            datos_actuales[clave] = valor
                        else:
                            fusionar(datos_actuales[clave], valor)
                return datos_actuales

            estado = fusionar(datos_guardados, estado)

        except Exception as e:
            print(f"⚠️ Archivo de progreso dañado: {e} → se usa estado inicial")

    return estado

def guardar_progreso(estado):
    """Guarda el progreso y hace respaldo automático"""
    # Redondear valores para evitar decimales largos
    def redondear_recursivo(datos):
        for k, v in datos.items():
            if isinstance(v, float):
                datos[k] = round(v, 2)
            elif isinstance(v, dict):
                redondear_recursivo(v)
        return datos

    estado = redondear_recursivo(estado.copy())

    # Guardar principal
    with open(ARCHIVO_PROGRESO, "w", encoding="utf-8") as f:
        json.dump(estado, f, indent=2, ensure_ascii=False)

    # Hacer respaldo cada vez que guarda
    shutil.copy2(ARCHIVO_PROGRESO, ARCHIVO_RESPALDO)

def respaldo_manual():
    """Genera una copia con fecha para tener control total"""
    fecha = time.strftime("%Y%m%d-%H%M%S")
    ruta = os.path.join(CARPETA_DATOS, f"respaldo_{fecha}.json")
    shutil.copy2(ARCHIVO_PROGRESO, ruta)
    return ruta

# -------------------
# RESTO DEL SERVIDOR
# -------------------
def calcular_bono_logros(estado):
    total = 1.00
    for logro in estado["logros"].values():
        if logro["desbloqueado"]:
            total *= logro["bono"]
    return round(total, 2)

def verificar_logros(estado):
    s = estado["estadisticas"]
    if not estado["logros"]["primeros_1k"]["desbloqueado"] and estado["dinero"] >= 1000:
        estado["logros"]["primeros_1k"]["desbloqueado"] = True
    if not estado["logros"]["3_puertas"]["desbloqueado"] and s["puertas_abiertas"] >= 3:
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
                estado["estadisticas"]["ganancia_maxima"] = base * total_mult

            verificar_logros(estado)
            estado["tiempo_ultima"] = round(ahora, 3)
            guardar_progreso(estado)
            self.wfile.write(json.dumps(estado).encode("utf-8"))
            return

        if self.path == "/api/respaldo":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            ruta = respaldo_manual()
            self.wfile.write(json.dumps({"mensaje": f"Respaldo guardado en: {ruta}"}).encode("utf-8"))
            return

        return super().do_GET()

    def do_POST(self):
        if self.path.startswith("/api/"):
            longitud = int(self.headers.get("Content-Length", 0))
            datos = self.rfile.read(longitud)
            accion = self.path.replace("/api/", "")
            estado = cargar_progreso()
            s = estado["estadisticas"]

            if accion == "mejorar_cpu":
                descuento = 1 - estado["mejoras_pasivas"]["descuento"]["efecto"]
                costo = estado["costo_cpu"] * descuento
                if estado["dinero"] >= costo:
                    estado["dinero"] -= costo
                    estado["nivel_cpu"] += 1
                    estado["ganancia_cpu"] *= 1.6
                    estado["costo_cpu"] *= 2.0
                    s["mejoras_cpu"] += 1

            elif accion == "comprar_multiplicador":
                descuento = 1 - estado["mejoras_pasivas"]["descuento"]["efecto"]
                costo = 100 * estado["multiplicador_global"] * 1.9 * descuento
                if estado["dinero"] >= costo:
                    estado["dinero"] -= costo
                    estado["multiplicador_global"] *= 1.3

            elif accion == "comprar_generador":
                tipo = json.loads(datos)["tipo"]
                gen = estado["generadores"][tipo]
                descuento = 1 - estado["mejoras_pasivas"]["descuento"]["efecto"]
                costo = gen["costo"] * descuento
                if estado["dinero"] >= costo:
                    estado["dinero"] -= costo
                    gen["cantidad"] += 1
                    gen["costo"] *= 1.75
                    s["generadores_comprados"] += 1

            elif accion == "comprar_max_generador":
                tipo = json.loads(datos)["tipo"]
                gen = estado["generadores"][tipo]
                descuento = 1 - estado["mejoras_pasivas"]["descuento"]["efecto"]
                while True:
                    costo = gen["costo"] * descuento
                    if estado["dinero"] >= costo:
                        estado["dinero"] -= costo
                        gen["cantidad"] += 1
                        gen["costo"] *= 1.75
                        s["generadores_comprados"] += 1
                    else:
                        break

            elif accion == "abrir_puerta":
                id_puerta = json.loads(datos)["id"]
                p = estado["puertas"][id_puerta]
                descuento = 1 - estado["mejoras_pasivas"]["descuento"]["efecto"]
                costo = p["costo"] * descuento
                if not p["abierta"] and estado["dinero"] >= costo:
                    estado["dinero"] -= costo
                    p["abierta"] = True
                    estado["multiplicador_global"] += p["bono"]
                    s["puertas_abiertas"] += 1

            elif accion == "hacer_renacimiento":
                if estado["nivel_cpu"] >= 5:
                    estado["renacimientos"] += 1
                    estado["bono_renacimiento"] *= 1.5
                    estado["dinero"] = estado["mejoras_pasivas"]["inicio_mejorado"]["efecto"]
                    estado["multiplicador_global"] = 1.00
                    estado["nivel_cpu"] = 1
                    estado["ganancia_cpu"] = 0.50
                    estado["costo_cpu"] = 150.00
                    for gen in estado["generadores"].values():
                        gen["cantidad"] = 0
                        gen["costo"] = estado_base()["generadores"][gen]["costo"] if gen in estado_base()["generadores"] else gen["costo"]
                    for p in estado["puertas"].values():
                        p["abierta"] = False
                    estado["tiempo_ultima"] = time.time()

            elif accion == "mejorar_pasiva":
                tipo = json.loads(datos)["tipo"]
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
    print("✅ Servidor con guardado seguro corriendo en http://localhost:8080")
    print("📁 Archivo de progreso:", ARCHIVO_PROGRESO)
    servidor.serve_forever()
