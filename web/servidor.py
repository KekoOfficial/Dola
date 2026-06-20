from http.server import SimpleHTTPRequestHandler, HTTPServer
import json
import os
import time
import shutil

CARPETA_DATOS = "datos"
ARCHIVO_PROGRESO = os.path.join(CARPETA_DATOS, "progreso.json")
ARCHIVO_RESPALDO = os.path.join(CARPETA_DATOS, "respaldo_progreso.json")
CONTRASEÑA_ADMIN = "111"

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
            "2_renacimientos": {"desbloqueado": False, "bono": 1.30, "descripcion": "Tener 2 renacimientos → +30% ganancia"},
            "primer_millon": {"desbloqueado": False, "bono": 1.50, "descripcion": "Alcanzar $1.000.000 → +50% ganancia"},
            "10_renacimientos": {"desbloqueado": False, "bono": 2.00, "descripcion": "Tener 10 renacimientos → Doble ganancia"}
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
            print(f"⚠️ Archivo reiniciado por error: {e}")
    return estado

def redondear_recursivo(d):
    for k, v in d.items():
        if isinstance(v, float):
            d[k] = round(v, 4)
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
    return round(multiplicador, 4)

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

            estado["dinero"] = round(estado["dinero"] + ganancia, 4)
            estado["estadisticas"]["dinero_total_ganado"] = round(estado["estadisticas"]["dinero_total_ganado"] + ganancia, 4)

            ganancia_actual = round(base * total_mult, 4)
            if ganancia_actual > estado["estadisticas"]["ganancia_maxima"]:
                estado["estadisticas"]["ganancia_maxima"] = ganancia_actual

            verificar_logros(estado)
            estado["tiempo_ultima"] = round(ahora, 3)
            guardar_progreso(estado)
            self.wfile.write(json.dumps(estado).encode("utf-8"))
            return

        if self.path == "/perfil":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            html = """
            <!DOCTYPE html>
            <html lang="es">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Perfil</title>
                <style>
                    body { font-family: Arial; background: #1a1a2e; color: white; text-align: center; padding: 20px; }
                    .btn { padding: 12px 25px; margin: 10px; border: none; border-radius: 6px; font-size: 16px; cursor: pointer; }
                    .btn-admin { background: #e94560; color: white; }
                    .btn-volver { background: #0f3460; color: white; }
                    .panel { background: #16213e; padding: 25px; border-radius: 10px; max-width: 420px; margin: 20px auto; display: none; }
                    input { padding: 10px; width: 85%; margin: 10px 0; border-radius: 5px; border: none; font-size: 16px; }
                </style>
            </head>
            <body>
                <h2>👤 Perfil</h2>
                <button class="btn btn-admin" onclick="mostrarLogin()">🔑 Acceso Administrador</button>
                <br><br>
                <button class="btn btn-volver" onclick="window.location.href='/'">⬅️ Volver al Menú Principal</button>

                <div id="loginAdmin" class="panel">
                    <h3>Ingresar Contraseña</h3>
                    <input type="password" id="clave" placeholder="Escribir contraseña">
                    <br>
                    <button class="btn btn-admin" onclick="verificar()">Entrar</button>
                    <button class="btn btn-volver" onclick="cerrarLogin()">Cancelar</button>
                </div>

                <div id="panelAdmin" class="panel">
                    <h3>⚙️ Panel de Administrador</h3>
                    <p>Dinero actual: <strong>$<span id="dineroActual">0.00</span></strong></p>
                    <input type="number" step="0.01" id="nuevoDinero" placeholder="Cantidad nueva">
                    <br>
                    <button class="btn btn-admin" onclick="guardarDinero()">💾 Guardar</button>
                    <br><br>
                    <button class="btn btn-volver" onclick="salir()">🚪 Volver</button>
                </div>

                <script>
                    async function cargarDatos() {
                        const res = await fetch('/api/estado');
                        const datos = await res.json();
                        document.getElementById('dineroActual').textContent = datos.dinero.toFixed(2);
                    }
                    function mostrarLogin() { document.getElementById('loginAdmin').style.display = 'block'; }
                    function cerrarLogin() { document.getElementById('loginAdmin').style.display = 'none'; }
                    async function verificar() {
                        const clave = document.getElementById('clave').value.trim();
                        const res = await fetch('/api/verificar-admin', {
                            method: 'POST',
                            headers: {'Content-Type':'application/json'},
                            body: JSON.stringify({clave: clave})
                        });
                        const respuesta = await res.json();
                        if(respuesta.ok) {
                            cerrarLogin();
                            document.getElementById('panelAdmin').style.display = 'block';
                            cargarDatos();
                        } else alert('❌ Contraseña incorrecta');
                    }
                    async function guardarDinero() {
                        const monto = parseFloat(document.getElementById('nuevoDinero').value);
                        if(isNaN(monto) || monto < 0) return alert('⚠️ Número inválido');
                        await fetch('/api/admin-cambiar-dinero', {
                            method: 'POST',
                            headers: {'Content-Type':'application/json'},
                            body: JSON.stringify({nuevo_valor: monto})
                        });
                        alert('✅ Dinero actualizado');
                        cargarDatos();
                    }
                    function salir() { window.location.href = '/'; }
                </script>
            </body>
            </html>
            """
            self.wfile.write(html.encode("utf-8"))
            return

        return super().do_GET()

    def do_POST(self):
        if self.path.startswith("/api/"):
            largo = int(self.headers.get("Content-Length", 0))
            datos = json.loads(self.rfile.read(largo) or "{}")
            accion = self.path.replace("/api/", "")
            estado = cargar_progreso()
            descuento = 1 - estado["mejoras_pasivas"]["descuento"]["efecto"]

            if accion == "verificar-admin":
                ok = (datos.get("clave") == CONTRASEÑA_ADMIN)
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"ok": ok}).encode("utf-8"))
                return

            if accion == "admin-cambiar-dinero":
                estado["dinero"] = max(0, round(float(datos.get("nuevo_valor", 0)), 4))
                guardar_progreso(estado)
                self.send_response(200)
                self.end_headers()
                return

            # 🖥️ CPU
            if accion == "mejorar_cpu":
                costo = round(estado["costo_cpu"] * descuento, 4)
                if estado["dinero"] >= costo:
                    estado["dinero"] -= costo
                    estado["nivel_cpu"] += 1
                    estado["ganancia_cpu"] = round(estado["ganancia_cpu"] * 1.6, 4)
                    estado["costo_cpu"] = round(estado["costo_cpu"] * 2.0, 4)
                    estado["estadisticas"]["mejoras_cpu"] += 1

            elif accion == "comprar_max_cpu":
                cantidad = max(1, int(datos.get("cantidad", 1)))
                costo_actual = estado["costo_cpu"]
                for _ in range(cantidad):
                    costo = round(costo_actual * descuento, 4)
                    if estado["dinero"] < costo:
                        break
                    estado["dinero"] -= costo
                    estado["nivel_cpu"] += 1
                    estado["ganancia_cpu"] = round(estado["ganancia_cpu"] * 1.6, 4)
                    costo_actual = round(costo_actual * 2.0, 4)
                    estado["estadisticas"]["mejoras_cpu"] += 1
                estado["costo_cpu"] = costo_actual

            # ⚡ Multiplicadores
            elif accion == "comprar_multiplicador":
                costo = round(100 * estado["multiplicador_global"] * 1.9 * descuento, 4)
                if estado["dinero"] >= costo:
                    estado["dinero"] -= costo
                    estado["multiplicador_global"] = round(estado["multiplicador_global"] * 1.3, 4)

            elif accion == "comprar_max_multiplicador":
                cantidad = max(1, int(datos.get("cantidad", 1)))
                for _ in range(cantidad):
                    costo = round(100 * estado["multiplicador_global"] * 1.9 * descuento, 4)
                    if estado["dinero"] < costo:
                        break
                    estado["dinero"] -= costo
                    estado["multiplicador_global"] = round(estado["multiplicador_global"] * 1.3, 4)

            # 🏭 Generadores
            elif accion == "comprar_generador":
                tipo = datos.get("tipo")
                if tipo in estado["generadores"]:
                    gen = estado["generadores"][tipo]
                    costo = round(gen["costo"] * descuento, 4)
                    if estado["dinero"] >= costo:
                        estado["dinero"] -= costo
                        gen["cantidad"] += 1
                        gen["costo"] = round(gen["costo"] * 1.75, 4)
                        estado["estadisticas"]["generadores_comprados"] += 1

            elif accion == "comprar_max_generador":
                tipo = datos.get("tipo")
                if tipo in estado["generadores"]:
                    gen = estado["generadores"][tipo]
                    while True:
                        costo = round(gen["costo"] * descuento, 4)
                        if estado["dinero"] < costo:
                            break
                        estado["dinero"] -= costo
                        gen["cantidad"] += 1
                        gen["costo"] = round(gen["costo"] * 1.75, 4)
                        estado["estadisticas"]["generadores_comprados"] += 1

            # 🚪 Puertas
            elif accion == "abrir_puerta":
                id_puerta = datos.get("id")
                if id_puerta in estado["puertas"]:
                    p = estado["puertas"][id_puerta]
                    costo = round(p["costo"] * descuento, 4)
                    if not p["abierta"] and estado["dinero"] >= costo:
                        estado["dinero"] -= costo
                        p["abierta"] = True
                        estado["multiplicador_global"] = round(estado["multiplicador_global"] + p["bono"], 4)
                        estado["estadisticas"]["puertas_abiertas"] += 1

            # 🔄 Renacimiento
            elif accion == "hacer_renacimiento":
                cantidad = max(1, int(datos.get("cantidad", 1)))
                for _ in range(cantidad):
                    estado["renacimientos"] += 1
                    estado["bono_renacimiento"] = round(estado["bono_renacimiento"] * 1.5, 4)

                estado["dinero"] = round(estado["mejoras_pasivas"]["inicio_mejorado"]["efecto"], 4)
                estado["multiplicador_global"] = 1.00
                estado["nivel_cpu"] = 1
                estado["ganancia_cpu"] = 0.50
                estado["costo_cpu"] = 150.00

                for g in estado["generadores"].values():
                    g["cantidad"] = 0
                    g["costo"] = estado_base()["generadores"][g["tipo"]]["costo"] if "tipo" in g else estado_base()["generadores"][list(estado["generadores"].keys())[0]]["costo"]

                for p in estado["puertas"].values():
                    p["abierta"] = False

                estado["tiempo_ultima"] = time.time()

            # ⭐ Mejoras pasivas
            elif accion == "mejorar_pasiva":
                tipo = datos.get("tipo")
                if tipo in estado["mejoras_pasivas"]:
                    m = estado["mejoras_pasivas"][tipo]
                    if estado["renacimientos"] >= m["costo"]:
                        estado["renacimientos"] -= m["costo"]
                        m["nivel"] += 1
                        if tipo == "ahorro":
                            m["efecto"] = round(m["nivel"] * 0.02, 3)
                        elif tipo == "descuento":
                            m["efecto"] = round(m["nivel"] * 0.015, 3)
                        elif tipo == "inicio_mejorado":
                            m["efecto"] = round(100 * (1.2 ** m["nivel"]), 2)

            guardar_progreso(estado)
            self.send_response(200)
            self.end_headers()
            return

        self.send_response(404)
        self.end_headers()

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    servidor = HTTPServer(("0.0.0.0", 8080), Manejador)
    print("✅ Servidor corriendo en http://localhost:8080")
    print("🔑 Contraseña Admin: 111")
    servidor.serve_forever()
