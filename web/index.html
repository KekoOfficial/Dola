<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Multiplicadores de Dinero</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: Arial, sans-serif; }
        body { background: #0f172a; color: #f8fafc; padding: 20px; max-width: 1000px; margin: 0 auto; }
        h1, h2, h3 { text-align: center; margin: 20px 0; color: #38bdf8; }
        .panel { background: #1e293b; border-radius: 12px; padding: 20px; margin: 15px 0; box-shadow: 0 4px 8px rgba(0,0,0,0.2); }
        .valor { font-size: 1.2em; font-weight: bold; color: #4ade80; }
        button { padding: 10px 18px; border: none; border-radius: 6px; background: #2563eb; color: white; cursor: pointer; font-size: 1em; margin: 5px; }
        button:hover { background: #1d4ed8; }
        button:disabled { background: #475569; cursor: not-allowed; }
        .btn-max { background: #9333ea; }
        .btn-max:hover { background: #7e22ce; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 15px; }
        .logro { padding: 10px; border-radius: 6px; margin: 5px 0; }
        .desbloqueado { background: #064e3b; border-left: 4px solid #4ade80; }
        .bloqueado { background: #332a22; border-left: 4px solid #fbbf24; opacity: 0.7; }
        .fila-cpu { display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px; }
    </style>
</head>
<body>

    <!-- 📊 Panel Principal -->
    <div class="panel">
        <h2>💰 Dinero: <span id="dinero" class="valor">$0.00</span></h2>
        <p>Ganancia por segundo: <span id="ganancia_seg" class="valor">$0.00/seg</span></p>
        <p>Multiplicador total: <span id="multiplicador" class="valor">x1.00</span></p>
        <p>Nivel de CPU: <span id="nivel_cpu" class="valor">1</span></p>
        <p>Renacimientos: <span id="renacimientos" class="valor">0</span></p>
    </div>

    <!-- 🛠️ Mejoras de CPU con opción de compra máxima -->
    <div class="panel">
        <h2>🖥️ Mejoras de CPU</h2>
        <div class="fila-cpu">
            <div>
                <p>Costo por 1 nivel: <span id="costo_cpu" class="valor">$0.00</span></p>
                <p>Podés comprar hasta: <span id="cant_max_cpu" class="valor">0</span> niveles</p>
                <p>Costo total máximo: <span id="costo_total_cpu" class="valor">$0.00</span></p>
            </div>
            <div>
                <button onclick="comprar1CPU()">🔹 Comprar 1 CPU</button>
                <button class="btn-max" onclick="comprarMaxCPU()">🔺 Comprar MÁXIMO</button>
            </div>
        </div>
    </div>

    <!-- 🛠️ Multiplicadores -->
    <div class="panel">
        <h2>⚡ Multiplicadores</h2>
        <p>Costo: <span id="costo_mult" class="valor">$0.00</span></p>
        <button onclick="comprarMultiplicador()">Comprar</button>
    </div>

    <!-- 🛠️ Generadores -->
    <div class="panel">
        <h2>🏭 Generadores</h2>
        <div class="grid">
            <div>
                <p>Básico | Cantidad: <span id="cant_basico">0</span></p>
                <p>Costo: <span id="costo_basico">$0.00</span></p>
                <button onclick="comprarGenerador('basico')">1 Unidad</button>
                <button class="btn-max" onclick="comprarMaxGenerador('basico')">Máximo</button>
            </div>
            <div>
                <p>Medio | Cantidad: <span id="cant_medio">0</span></p>
                <p>Costo: <span id="costo_medio">$0.00</span></p>
                <button onclick="comprarGenerador('medio')">1 Unidad</button>
                <button class="btn-max" onclick="comprarMaxGenerador('medio')">Máximo</button>
            </div>
            <div>
                <p>Avanzado | Cantidad: <span id="cant_avanzado">0</span></p>
                <p>Costo: <span id="costo_avanzado">$0.00</span></p>
                <button onclick="comprarGenerador('avanzado')">1 Unidad</button>
                <button class="btn-max" onclick="comprarMaxGenerador('avanzado')">Máximo</button>
            </div>
            <div>
                <p>Industrial | Cantidad: <span id="cant_industrial">0</span></p>
                <p>Costo: <span id="costo_industrial">$0.00</span></p>
                <button onclick="comprarGenerador('industrial')">1 Unidad</button>
                <button class="btn-max" onclick="comprarMaxGenerador('industrial')">Máximo</button>
            </div>
            <div>
                <p>Nuclear | Cantidad: <span id="cant_nuclear">0</span></p>
                <p>Costo: <span id="costo_nuclear">$0.00</span></p>
                <button onclick="comprarGenerador('nuclear')">1 Unidad</button>
                <button class="btn-max" onclick="comprarMaxGenerador('nuclear')">Máximo</button>
            </div>
            <div>
                <p>Cuántico | Cantidad: <span id="cant_cuantico">0</span></p>
                <p>Costo: <span id="costo_cuantico">$0.00</span></p>
                <button onclick="comprarGenerador('cuantico')">1 Unidad</button>
                <button class="btn-max" onclick="comprarMaxGenerador('cuantico')">Máximo</button>
            </div>
            <div>
                <p>Galáctico | Cantidad: <span id="cant_galactico">0</span></p>
                <p>Costo: <span id="costo_galactico">$0.00</span></p>
                <button onclick="comprarGenerador('galactico')">1 Unidad</button>
                <button class="btn-max" onclick="comprarMaxGenerador('galactico')">Máximo</button>
            </div>
        </div>
    </div>

    <!-- 🚪 Puertas -->
    <div class="panel">
        <h2>🚪 Puertas</h2>
        <div id="lista_puertas"></div>
    </div>

    <!-- 🔄 Renacimiento -->
    <div class="panel">
        <h2>🔄 Renacimiento</h2>
        <p>Bono acumulado: <span id="bono_renacimiento" class="valor">x1.00</span></p>
        <p id="info_renacer">Requisito: Nivel de CPU ≥ 5</p>
        <button id="btn_renacer" onclick="hacerRenacimiento()">Renacer ahora</button>
    </div>

    <!-- ⭐ Mejoras Pasivas / Prestigio -->
    <div class="panel">
        <h2>⭐ Mejoras Pasivas</h2>
        <p>Ahorro | Nivel: <span id="nivel_ahorro">0</span>
        <button onclick="mejorarPasiva('ahorro')">Mejorar</button></p>
        <p>Descuento | Nivel: <span id="nivel_descuento">0</span>
        <button onclick="mejorarPasiva('descuento')">Mejorar</button></p>
        <p>Inicio Mejorado | Nivel: <span id="nivel_inicio">0</span>
        <button onclick="mejorarPasiva('inicio_mejorado')">Mejorar</button></p>
    </div>

    <!-- 🏆 Logros -->
    <div class="panel">
        <h2>🏆 Logros</h2>
        <div id="lista_logros"></div>
    </div>

    <!-- 📊 Estadísticas -->
    <div class="panel">
        <h2>📊 Estadísticas</h2>
        <p>Dinero total ganado: <span id="total_ganado" class="valor">$0.00</span></p>
        <p>Mejoras de CPU realizadas: <span id="mejoras_cpu">0</span></p>
        <p>Generadores comprados: <span id="generadores_totales">0</span></p>
        <p>Puertas abiertas: <span id="puertas_totales">0</span></p>
        <p>Tiempo total jugado: <span id="tiempo_jugado">0h 0m</span></p>
        <p>Ganancia máxima por segundo: <span id="ganancia_max" class="valor">$0.00</span></p>
    </div>

    <!-- 👤 Perfil y Administrador -->
    <div class="panel">
        <h2>👤 Perfil</h2>
        <button onclick="irAPerfil()">Ir a Perfil y Panel de Administrador</button>
    </div>

    <!-- 🔗 Enlace al JS -->
    <script type="module" src="js/servidor.js"></script>

    <script>
        function irAPerfil() {
            window.location.href = "/perfil";
        }
    </script>

</body>
</html>
