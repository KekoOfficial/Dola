from http.server import SimpleHTTPRequestHandler, HTTPServer
import json
import os
from urllib.parse import parse_qs, urlparse

ARCHIVO_DATOS = "datos/progreso.json"

def estado_inicial():
    return {
        "dinero": 100.0,
        "multiplicador_global": 1.0,
        "nivel_cpu": 1,
        "ganancia_cpu": 0.5,
        "costo_cpu": 150.0,
        "generadores": {
            "basico": {"cantidad": 0, "ganancia": 0.2, "costo": 200.0},
            "medio": {"cantidad": 0, "ganancia": 1.0, "costo": 1200.0},
            "avanzado": {"cantidad": 0, "ganancia": 5.0, "costo": 7500.0}
        },
        "puertas_abiertas": [],
        "tiempo_ultima": 0
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
    with open(ARCHIVO_DATOS, "w", encoding="utf-8") as f:
        json.dump(estado, f, indent=2)

class Manejador(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/estado":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            estado = cargar_estado()
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
                    estado["dinero"] -= estado["costo_cpu"]
                    estado["nivel_cpu"] += 1
                    estado["ganancia_cpu"] *= 1.6
                    estado["costo_cpu"] = round(estado["costo_cpu"] * 2, 2)

            elif accion == "comprar_multiplicador":
                costo = round(80 * estado["multiplicador_global"] * 1.8, 2)
                if estado["dinero"] >= costo:
                    estado["dinero"] -= costo
                    estado["multiplicador_global"] = round(estado["multiplicador_global"] * 1.25, 2)

            elif accion == "comprar_generador":
                tipo = json.loads(datos)["tipo"]
                gen = estado["generadores"][tipo]
                if estado["dinero"] >= gen["costo"]:
                    estado["dinero"] -= gen["costo"]
                    gen["cantidad"] += 1
                    gen["costo"] = round(gen["costo"] * 1.7, 2)

            elif accion == "abrir_puerta":
                codigo = json.loads(datos)["codigo"]
                puertas = {
                    "1024": {"costo": 150, "bono": 0.3},
                    "2048": {"costo": 800, "bono": 1.2},
                    "4096": {"costo": 4500, "bono": 3.5},
                    "8192": {"costo": 22000, "bono": 10},
                    "16384": {"costo": 120000, "bono": 40}
                }
                if codigo in puertas and codigo not in estado["puertas_abiertas"]:
                    if estado["dinero"] >= puertas[codigo]["costo"]:
                        estado["dinero"] -= puertas[codigo]["costo"]
                        estado["puertas_abiertas"].append(codigo)
                        estado["multiplicador_global"] += puertas[codigo]["bono"]

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
    print("🌐 Servidor activo en: http://localhost:8080")
    print("💡 Para verlo en Termux: abre esa dirección en el navegador")
    servidor.serve_forever()
