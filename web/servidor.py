from http.server import SimpleHTTPRequestHandler, HTTPServer
import json
import os
import time

ARCHIVO_DATOS = "datos/progreso.json"

def estado_inicial():
    return {
        "dinero": 100.00,
        "multiplicador_global": 1.00,
        "nivel_cpu": 1,
        "ganancia_cpu": 0.50,
        "costo_cpu": 150.00,
        "renacimientos": 0,
        "bono_renacimiento": 1.00,
        "generadores": {
            "basico": {"cantidad": 0, "ganancia": 0.20, "costo": 200.00},
            "medio": {"cantidad": 0, "ganancia": 1.00, "costo": 1200.00},
            "avanzado": {"cantidad": 0, "ganancia": 5.00, "costo": 7500.00},
            "industrial": {"cantidad": 0, "ganancia": 25.00, "costo": 40000.00}
        },
        "puertas": {
            "p1": {"nombre": "Almacén Básico", "abierta": False, "costo": 200, "bono": 0.5},
            "p2": {"nombre": "Centro de Datos", "abierta": False, "costo": 1000, "bono": 1.5},
            "p3": {"nombre": "Sala de Procesos", "abierta": False, "costo": 5000, "bono": 4},
            "p4": {"nombre": "Servidor Principal", "abierta": False, "costo": 25000, "bono": 12},
            "p5": {"nombre": "Núcleo de Energía", "abierta": False, "costo": 130000, "bono": 45},
            "p6": {"nombre": "Red Global", "abierta": False, "costo": 700000, "bono": 180},
            "p7": {"nombre": "Centro Galáctico", "abierta": False, "costo": 4000000, "bono": 800}
        },
        "tiempo_ultima": time.time()
    }

def cargar_estado():
    os.makedirs("datos", exist_ok=True)
    if os.path.exists(ARCHIVO_DATOS):
        try:
            with open(ARCHIVO_DATOS, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return estado_inicial()

def guardar_estado(estado):
    estado["dinero"] = round(estado["dinero"], 2)
    estado["multiplicador_global"] = round(estado["multiplicador_global"], 2)
    estado["ganancia_cpu"] = round(estado["ganancia_cpu"], 2)
    estado["costo_cpu"] = round(estado["costo_cpu"], 2)
    estado["bono_renacimiento"] = round(estado["bono_renacimiento"], 2)
    for gen in estado["generadores"].values():
        gen["costo"] = round(gen["costo"], 2)
    with open(ARCHIVO_DATOS, "w", encoding="utf-8") as f:
        json.dump(estado, f, indent=2, ensure_ascii=False)

class Manejador(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/estado":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            estado = cargar_estado()
            # Actualizar ganancia antes de enviar
            ahora = time.time()
            segundos = ahora - estado["tiempo_ultima"]
            base = estado["ganancia_cpu"]
            for gen in estado["generadores"].values():
                base += gen["cantidad"] * gen["ganancia"]
            total_mult = estado["multiplicador_global"] * estado["bono_renacimiento"]
            ganancia = segundos * base * total_mult
            estado["dinero"] = round(estado["dinero"] + ganancia, 2)
            estado["tiempo_ultima"] = round(ahora, 3)
            guardar_estado(estado)
            self.wfile.write(json.dumps(estado).encode("utf-8"))
            return
        return super().do_GET()

    def do_POST(self):
        if self.path.startswith("/api/"):
            longitud = int(self.headers.get("Content-Length", 0))
            datos = self.rfile.read(longitud)
            accion = self.path.replace("/api/", "")
            estado = cargar_estado()

            if accion == "mejorar_cpu":
                if estado["dinero"] >= estado["costo_cpu"]:
                    estado["dinero"] = round(estado["dinero"] - estado["costo_cpu"], 2)
                    estado["nivel_cpu"] += 1
                    estado["ganancia_cpu"] = round(estado["ganancia_cpu"] * 1.6, 2)
                    estado["costo_cpu"] = round(estado["costo_cpu"] * 2.0, 2)

            elif accion == "comprar_multiplicador":
                costo = round(100 * estado["multiplicador_global"] * 1.9, 2)
                if estado["dinero"] >= costo:
                    estado["dinero"] = round(estado["dinero"] - costo, 2)
                    estado["multiplicador_global"] = round(estado["multiplicador_global"] * 1.3, 2)

            elif accion == "comprar_generador":
                tipo = json.loads(datos)["tipo"]
                gen = estado["generadores"][tipo]
                if estado["dinero"] >= gen["costo"]:
                    estado["dinero"] = round(estado["dinero"] - gen["costo"], 2)
                    gen["cantidad"] += 1
                    gen["costo"] = round(gen["costo"] * 1.75, 2)

            elif accion == "abrir_puerta":
                id_puerta = json.loads(datos)["id"]
                p = estado["puertas"][id_puerta]
                if not p["abierta"] and estado["dinero"] >= p["costo"]:
                    estado["dinero"] = round(estado["dinero"] - p["costo"], 2)
                    p["abierta"] = True
                    estado["multiplicador_global"] = round(estado["multiplicador_global"] + p["bono"], 2)

            elif accion == "hacer_renacimiento":
                if estado["nivel_cpu"] >= 5:
                    estado["renacimientos"] += 1
                    estado["bono_renacimiento"] = round(estado["bono_renacimiento"] * 1.5, 2)
                    estado["dinero"] = 100.00
                    estado["multiplicador_global"] = 1.00
                    estado["nivel_cpu"] = 1
                    estado["ganancia_cpu"] = 0.50
                    estado["costo_cpu"] = 150.00
                    for gen in estado["generadores"].values():
                        gen["cantidad"] = 0
                        gen["costo"] = 200.00 if gen == estado["generadores"]["basico"] else gen["costo"]
                    for p in estado["puertas"].values():
                        p["abierta"] = False
                    estado["tiempo_ultima"] = time.time()

            guardar_estado(estado)
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"ok": True}).encode("utf-8"))
            return
        self.send_response(404)
        self.end_headers()

if __name__ == "__main__":
    servidor = HTTPServer(("0.0.0.0", 8080), Manejador)
    print("🌐 Servidor en http://localhost:8080")
    print("✅ Progreso se mantiene al cambiar de página")
    servidor.serve_forever()
