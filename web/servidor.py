from http.server import SimpleHTTPRequestHandler, HTTPServer
import json
import os
import time
import shutil

CARPETA_DATOS = "datos"
ARCHIVO_PROGRESO = os.path.join(CARPETA_DATOS, "progreso.json")
ARCHIVO_RESPALDO = os.path.join(CARPETA_DATOS, "respaldo_progreso.json")
CONTRASEÑA_ADMIN = "111"
MAX_SEGUNDOS = 60

def crear_estructura():
    os.makedirs(CARPETA_DATOS, exist_ok=True)

def estado_base():
    return {
        "dinero": 100.00,
        "multiplicador_global": 1.00,
        "nivel_cpu": 1,
        "ganancia_cpu": 0.50,
        "costo_cpu": 150.00,
        "renacimientos": 0,
        "bono_renacimiento": 1.00,
        "tiempo_ultima": time.time(),
        "estadisticas": {"dinero_total":0, "mejoras_cpu":0, "generadores":0, "puertas":0, "tiempo_jugado":0, "ganancia_max":0},
        "logros": {
            "1k": {"desbloqueado":False, "bono":1.1},
            "3puertas": {"desbloqueado":False, "bono":1.2},
            "2renac": {"desbloqueado":False, "bono":1.3}
        },
        "generadores": {
            "basico": {"cantidad":0, "ganancia":0.2, "costo":200},
            "medio": {"cantidad":0, "ganancia":1, "costo":1200},
            "avanzado": {"cantidad":0, "ganancia":5, "costo":7500}
        },
        "puertas": {
            "p1": {"nombre":"Almacén", "abierta":False, "costo":200, "bono":0.5},
            "p2": {"nombre":"Centro Datos", "abierta":False, "costo":1000, "bono":1.5},
            "p3": {"nombre":"Sala Procesos", "abierta":False, "costo":5000, "bono":4}
        }
    }

def fusionar(actual, base):
    for k, v in base.items():
        if k not in actual: actual[k] = v
        elif isinstance(v, dict) and isinstance(actual.get(k), dict): fusionar(actual[k], v)
    return actual

def cargar():
    crear_estructura()
    estado = estado_base()
    if os.path.exists(ARCHIVO_PROGRESO):
        try:
            with open(ARCHIVO_PROGRESO, "r", encoding="utf-8") as f:
                estado = fusionar(json.load(f), estado)
        except: pass
    estado["tiempo_ultima"] = time.time()
    return estado

def guardar(estado):
    with open(ARCHIVO_PROGRESO, "w", encoding="utf-8") as f:
        json.dump(estado, f, indent=2)
    shutil.copy2(ARCHIVO_PROGRESO, ARCHIVO_RESPALDO)

def calcular_ganancia(estado, segundos):
    base = estado["ganancia_cpu"]
    for g in estado["generadores"].values():
        base += g["cantidad"] * g["ganancia"]
    bono = estado["multiplicador_global"] * estado["bono_renacimiento"]
    for l in estado["logros"].values():
        if l["desbloqueado"]: bono *= l["bono"]
    return round(base * bono * segundos, 4)

class Manejador(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/estado":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            estado = cargar()
            ahora = time.time()
            segundos = min(ahora - estado["tiempo_ultima"], MAX_SEGUNDOS)
            if segundos > 0:
                ganancia = calcular_ganancia(estado, segundos)
                estado["dinero"] = round(estado["dinero"] + ganancia, 4)
                estado["tiempo_ultima"] = round(ahora, 3)
                guardar(estado)
            self.wfile.write(json.dumps(estado).encode("utf-8"))
            return
        return super().do_GET()

    def do_POST(self):
        if not self.path.startswith("/api/"):
            self.send_response(404)
            self.end_headers()
            return
        largo = int(self.headers.get("Content-Length", 0))
        datos = json.loads(self.rfile.read(largo) or "{}")
        accion = self.path.replace("/api/", "").strip()
        estado = cargar()

        if accion == "admin":
            if datos.get("clave") == CONTRASEÑA_ADMIN:
                estado["dinero"] = max(0, round(float(datos.get("valor", 0)), 4))
                estado["tiempo_ultima"] = time.time()
                guardar(estado)
                self.wfile.write(json.dumps({"ok":True}).encode("utf-8"))
            else:
                self.wfile.write(json.dumps({"ok":False}).encode("utf-8"))
            return

        if accion == "mejorar_cpu":
            costo = round(estado["costo_cpu"], 2)
            if estado["dinero"] >= costo:
                estado["dinero"] -= costo
                estado["nivel_cpu"] += 1
                estado["ganancia_cpu"] = round(estado["ganancia_cpu"] * 1.6, 4)
                estado["costo_cpu"] = round(estado["costo_cpu"] * 2, 2)
                estado["tiempo_ultima"] = time.time()
                guardar(estado)
            self.wfile.write(json.dumps({"ok":True}).encode("utf-8"))
            return

        self.send_response(200)
        self.end_headers()

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print("✅ Servidor en http://localhost:8080")
    print("🔑 Admin: 111")
    HTTPServer(("0.0.0.0", 8080), Manejador).serve_forever()
