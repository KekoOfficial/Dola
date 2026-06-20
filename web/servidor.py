from http.server import SimpleHTTPRequestHandler, HTTPServer
import json
import os
import time
import shutil

# Configuración
CARPETA_DATOS = "datos"
ARCHIVO_PROGRESO = os.path.join(CARPETA_DATOS, "progreso.json")
ARCHIVO_RESPALDO = os.path.join(CARPETA_DATOS, "respaldo_progreso.json")
CONTRASEÑA_ADMIN = "111"
MAX_SEGUNDOS_CALCULO = 60  # Evita saltos enormes si estás mucho tiempo sin entrar

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
    # ✅ SIEMPRE ACTUALIZAMOS EL TIEMPO AL CARGAR
    estado["tiempo_ultima"] = time.time()
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

def calcular_bono_total(estado):
    logros = 1.0
    for l in estado["logros"].values():
        if l["desbloqueado"]:
            logros *= l["bono"]
    return round(estado["multiplicador_global"] * estado["bono_renacimiento"] * logros, 4)

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
            segundos = min(ahora - estado["tiempo_ultima"], MAX_SEGUNDOS_CALCULO)

            if segundos > 0:
                estado["estadisticas"]["tiempo_jugado"] += segundos

                # Cálculo de ganancia base
                ganancia_base = estado["ganancia_cpu"]
                for gen in estado["generadores"].values():
                    ganancia_base += gen["cantidad"] * gen["ganancia"]

                ganancia_total = ganancia_base * calcular_bono_total(estado)
                estado["dinero"] = round(estado["dinero"] + ganancia_total * segundos, 4)
                estado["estadisticas"]["dinero_total_ganado"] = round(estado["estadisticas"]["dinero_total_ganado"] + ganancia_total * segundos, 4)

                if ganancia_total > estado["estadisticas"]["ganancia_maxima"]:
                    estado["estadisticas"]["ganancia_maxima"] = round(ganancia_total, 4)

                verificar_logros(estado)
                estado["tiempo_ultima"] = round(ahora, 3)
                guardar_progreso(estado)

            self.wfile.write(json.dumps(estado).encode("utf-8"))
            return

        if self.path == "/perfil":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write("""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Perfil - Administrador</title>
    <style>
        *{margin:0;padding:0;box-sizing:border-box;font-family:Arial,sans-serif;}
        body{background:#12121f;color:#fff;padding:20px;max-width:450px;margin:0 auto;}
        h2{text-align:center;margin-bottom:25px;color:#4facfe;}
        .panel{background:#1e1e2f;padding:25px;border-radius:12px;margin:15px 0;box-shadow:0 4px 12px rgba(0,0,0,0.3);}
        input{width:100%;padding:12px;margin:12px 0;border-radius:8px;border:none;background:#2d2d44;color:#fff;font-size:16px;}
        button{width:100%;padding:12px;border:none;border-radius:8px;font-size:16px;font-weight:bold;cursor:pointer;margin:8px 0;}
        .btn-admin{background:#e63946;color:white;}
        .btn-volver{background:#457b9d;color:white;}
        .btn-admin:hover{background:#d62828;}
        .btn-volver:hover{background:#1d3557;}
    </style>
</head>
<body>
    <h2>👤 Perfil y Administración</h2>
    <div class="panel" id="login">
        <h3>Acceso Administrador</h3>
        <input type="password" id="clave" placeholder="Ingrese contraseña">
        <button class="btn-admin" onclick="entrar()">Ingresar</button>
        <button class="btn-volver" onclick="volver()">Volver al juego</button>
    </div>

    <div class="panel" id="panelAdmin" style="display:none;">
        <h3>⚙️ Control Total</h3>
        <p>Dinero actual: <strong id="dineroActual">$0.00</strong></p>
        <input type="number" step="0.01" min="0" id="nuevoDinero" placeholder="Nueva cantidad de dinero">
        <button class="btn-admin" onclick="guardarCambios()">💾 Guardar cambios</button>
        <button class="btn-volver" onclick="cerrarAdmin()">Cerrar</button>
    </div>

    <script>
        async function cargarEstado(){
            const res = await fetch('/api/estado');
            const datos = await res.json();
            document.getElementById('dineroActual').textContent = `$${datos.dinero.toFixed(2)}`;
        }
        async function entrar(){
            const clave = document.getElementById('clave').value.trim();
            const res = await fetch('/api/verificar-admin', {
                method: 'POST',
                headers: {'Content-Type':'application/json'},
                body: JSON.stringify({clave})
            });
            const r = await res.json();
            if(r.ok){
                document.getElementById('login').style.display = 'none';
                document.getElementById('panelAdmin').style.display = 'block';
                cargarEstado();
            }else alert('❌ Contraseña incorrecta');
        }
        async function guardarCambios(){
            const valor = parseFloat(document.getElementById('nuevoDinero').value) || 0;
            await fetch('/api/admin-cambiar-dinero', {
                method: 'POST',
                headers: {'Content-Type':'application/json'},
                body: JSON.stringify({nuevo_valor: valor})
            });
            alert('✅ Dinero actualizado. Ahora sigue generando automáticamente.');
            cargarEstado();
        }
        function cerrarAdmin(){
            document.getElementById('panelAdmin').style.display = 'none';
            document.getElementById('login').style.display = 'block';
        }
        function volver(){window.location.href='/';}
    </script>
</body>
            """.encode("utf-8"))
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
        estado = cargar_progreso()
        descuento = 1 - estado["mejoras_pasivas"]["descuento"]["efecto"]

        # --- ADMIN ---
        if accion == "verificar-admin":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"ok": datos.get("clave") == CONTRASEÑA_ADMIN}).encode("utf-8"))
            return

        if accion == "admin-cambiar-dinero":
            estado["dinero"] = max(0, round(float(datos.get("nuevo_valor", 0)), 4))
            estado["tiempo_ultima"] = time.time()  # ✅ REINICIAMOS CONTADOR AL CAMBIAR DINERO
            guardar_progreso(estado)
            self.send_response(200)
            self.end_headers()
            return

        # --- CPU ---
        if accion == "mejorar_cpu":
            costo = round(estado["costo_cpu"] * descuento, 4)
            if estado["dinero"] >= costo:
                estado["dinero"] -= costo
                estado["nivel_cpu"] += 1
                estado["ganancia_cpu"] = round(estado["ganancia_cpu"] * 1.6, 4)
                estado["costo_cpu"] = round(estado["costo_cpu"] * 2.0, 4)
                estado["estadisticas"]["mejoras_cpu"] += 1
                estado["tiempo_ultima"] = time.time()
                guardar_progreso(estado)
            self.send_response(200)
            self.end_headers()
            return

        if accion == "comprar_max_cpu":
            cantidad = max(1, int(datos.get("cantidad", 1)))
            costo_actual = estado["costo_cpu"]
            for _ in range(cantidad):
                costo = round(costo_actual * descuento, 4)
                if estado["dinero"] < costo: break
                estado["dinero"] -= costo
                estado["nivel_cpu"] += 1
                estado["ganancia_cpu"] = round(estado["ganancia_cpu"] * 1.6, 4)
                costo_actual = round(costo_actual * 2.0, 4)
                estado["estadisticas"]["mejoras_cpu"] += 1
            estado["costo_cpu"] = costo_actual
            estado["tiempo_ultima"] = time.time()
            guardar_progreso(estado)
            self.send_response(200)
            self.end_headers()
            return

        # --- MULTIPLICADORES ---
        if accion == "comprar_multiplicador":
            costo = round(100 * estado["multiplicador_global"] * 1.9 * descuento, 4)
            if estado["dinero"] >= costo:
                estado["dinero"] -= costo
                estado["multiplicador_global"] = round(estado["multiplicador_global"] * 1.3, 4)
                estado["tiempo_ultima"] = time.time()
                guardar_progreso(estado)
            self.send_response(200)
            self.end_headers()
            return

        if accion == "comprar_max_multiplicador":
            for _ in range(max(1, int(datos.get("cantidad", 1)))):
                costo = round(100 * estado["multiplicador_global"] * 1.9 * descuento, 4)
                if estado["dinero"] < costo: break
                estado["dinero"] -= costo
                estado["multiplicador_global"] = round(estado["multiplicador_global"] * 1.3, 4)
            estado["tiempo_ultima"] = time.time()
            guardar_progreso(estado)
            self.send_response(200)
            self.end_headers()
            return

        # --- GENERADORES ---
        if accion == "comprar_generador":
            tipo = datos.get("tipo")
            if tipo in estado["generadores"]:
                g = estado["generadores"][tipo]
                costo = round(g["costo"] * descuento, 4)
                if estado["dinero"] >= costo:
                    estado["dinero"] -= costo
                    g["cantidad"] += 1
                    g["costo"] = round(g["costo"] * 1.75, 4)
                    estado["estadisticas"]["generadores_comprados"] += 1
                    estado["tiempo_ultima"] = time.time()
                    guardar_progreso(estado)
            self.send_response(200)
            self.end_headers()
            return

        if accion == "comprar_max_generador":
            tipo = datos.get("tipo")
            if tipo in estado["generadores"]:
                g = estado["generadores"][tipo]
                while True:
                    costo = round(g["costo"] * descuento, 4)
                    if estado["dinero"] < costo: break
                    estado["dinero"] -= costo
                    g["cantidad"] += 1
                    g["costo"] = round(g["costo"] * 1.75, 4)
                    estado["estadisticas"]["generadores_comprados"] += 1
                estado["tiempo_ultima"] = time.time()
                guardar_progreso(estado)
            self.send_response(200)
            self.end_headers()
            return

        # --- PUERTAS ---
        if accion == "abrir_puerta":
            id_p = datos.get("id")
            if id_p in estado["puertas"]:
                p = estado["puertas"][id_p]
                costo = round(p["costo"] * descuento, 4)
                if not p["abierta"] and estado["dinero"] >= costo:
                    estado["dinero"] -= costo
                    p["abierta"] = True
                    estado["multiplicador_global"] = round(estado["multiplicador_global"] + p["bono"], 4)
                    estado["estadisticas"]["puertas_abiertas"] += 1
                    estado["tiempo_ultima"] = time.time()
                    guardar_progreso(estado)
            self.send_response(200)
            self.end_headers()
            return

        # --- RENACIMIENTO ---
        if accion == "hacer_renacimiento":
            for _ in range(max(1, int(datos.get("cantidad", 1)))):
                if estado["nivel_cpu"] < 5: break
                estado["renacimientos"] += 1
                estado["bono_renacimiento"] = round(estado["bono_renacimiento"] * 1.5, 4)
                estado["dinero"] = round(estado["mejoras_pasivas"]["inicio_mejorado"]["efecto"], 4)
                estado["multiplicador_global"] = 1.00
                estado["nivel_cpu"] = 1
                estado["ganancia_cpu"] = 0.50
                estado["costo_cpu"] = 150.00
                for g in estado["generadores"].values(): g["cantidad"] = 0; g["costo"] = estado_base()["generadores"][g["tipo"]]["costo"]
                for p in estado["puertas"].values(): p["abierta"] = False
                estado["tiempo_ultima"] = time.time()
            guardar_progreso(estado)
            self.send_response(200)
            self.end_headers()
            return

        # --- MEJORAS PASIVAS ---
        if accion == "mejorar_pasiva":
            tipo = datos.get("tipo")
            if tipo in estado["mejoras_pasivas"]:
                m = estado["mejoras_pasivas"][tipo]
                if estado["renacimientos"] >= m["costo"]:
                    estado["renacimientos"] -= m["costo"]
                    m["nivel"] += 1
                    if tipo == "ahorro": m["efecto"] = round(m["nivel"] * 0.02, 3)
                    elif tipo == "descuento": m["efecto"] = round(m["nivel"] * 0.015, 3)
                    elif tipo == "inicio_mejorado": m["efecto"] = round(100 * (1.2 ** m["nivel"]), 2)
                    estado["tiempo_ultima"] = time.time()
                    guardar_progreso(estado)
            self.send_response(200)
            self.end_headers()
            return

        self.send_response(400)
        self.end_headers()

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print("✅ Servidor corriendo en http://localhost:8080")
    print("🔑 Contraseña Admin: 111")
    servidor = HTTPServer(("0.0.0.0", 8080), Manejador)
    servidor.serve_forever()
