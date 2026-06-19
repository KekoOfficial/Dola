let estado = {};
let tiempoUltima = 0;

async function cargarEstado() {
    const res = await fetch("/api/estado");
    const nuevoEstado = await res.json();
    
    // Evitar que el dinero baje
    if (!estado.dinero || nuevoEstado.dinero >= estado.dinero) {
        estado = nuevoEstado;
    }
    
    if (tiempoUltima === 0) tiempoUltima = Date.now() / 1000;
    actualizarGanancias();
    mostrarDatos();
}

function actualizarGanancias() {
    const ahora = Date.now() / 1000;
    const segundos = ahora - tiempoUltima;
    let base = estado.ganancia_cpu;
    
    for (const gen of Object.values(estado.generadores)) {
        base += gen.cantidad * gen.ganancia;
    }
    
    const ganancia = segundos * base * estado.multiplicador_global;
    const nuevoDinero = Math.round((estado.dinero + ganancia) * 100) / 100;
    
    // Solo actualizar si es mayor o igual
    if (nuevoDinero >= estado.dinero) {
        estado.dinero = nuevoDinero;
    }
    
    tiempoUltima = ahora;
}

function mostrarDatos() {
    if (document.getElementById("dinero"))
        document.getElementById("dinero").textContent = `$${estado.dinero.toFixed(2)}`;
    
    if (document.getElementById("multiplicador"))
        document.getElementById("multiplicador").textContent = estado.multiplicador_global.toFixed(2);
    
    if (document.getElementById("nivel_cpu"))
        document.getElementById("nivel_cpu").textContent = estado.nivel_cpu;
    
    if (document.getElementById("ganancia_seg")) {
        let base = estado.ganancia_cpu;
        for (const gen of Object.values(estado.generadores)) base += gen.cantidad * gen.ganancia;
        document.getElementById("ganancia_seg").textContent = (base * estado.multiplicador_global).toFixed(2);
    }
    
    if (document.getElementById("costo_cpu"))
        document.getElementById("costo_cpu").textContent = estado.costo_cpu.toFixed(2);
    
    if (document.getElementById("costo_mult"))
        document.getElementById("costo_mult").textContent = (80 * estado.multiplicador_global * 1.8).toFixed(2);
    
    if (document.getElementById("costo_basico"))
        document.getElementById("costo_basico").textContent = estado.generadores.basico.costo.toFixed(2);
    if (document.getElementById("cant_basico"))
        document.getElementById("cant_basico").textContent = estado.generadores.basico.cantidad;
    
    if (document.getElementById("costo_medio"))
        document.getElementById("costo_medio").textContent = estado.generadores.medio.costo.toFixed(2);
    if (document.getElementById("cant_medio"))
        document.getElementById("cant_medio").textContent = estado.generadores.medio.cantidad;
    
    if (document.getElementById("costo_avanzado"))
        document.getElementById("costo_avanzado").textContent = estado.generadores.avanzado.costo.toFixed(2);
    if (document.getElementById("cant_avanzado"))
        document.getElementById("cant_avanzado").textContent = estado.generadores.avanzado.cantidad;
    
    if (document.getElementById("lista_puertas")) {
        const puertas = [
            {cod:"1024", nom:"Almacén Básico", costo:150},
            {cod:"2048", nom:"Centro de Procesos", costo:800},
            {cod:"4096", nom:"Sala Multiplicación", costo:4500},
            {cod:"8192", nom:"Servidor Principal", costo:22000},
            {cod:"16384", nom:"Núcleo Energía", costo:120000}
        ];
        let html = "<h3>Puertas disponibles:</h3>";
        puertas.forEach(p => {
            const abierta = estado.puertas_abiertas.includes(p.cod) ? "✅ ABIERTA" : `❌ Cerrada - $${p.costo.toFixed(2)}`;
            html += `<p>Código ${p.cod}: ${p.nom} → ${abierta}</p>`;
        });
        document.getElementById("lista_puertas").innerHTML = html;
    }
}

async function accion(tipo) {
    await fetch(`/api/${tipo}`, {method: "POST"});
    cargarEstado();
}

async function comprarGenerador(tipo) {
    await fetch("/api/comprar_generador", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({tipo: tipo})
    });
    cargarEstado();
}

async function abrirPuerta() {
    const cod = document.getElementById("codigo_puerta").value.trim();
    if (!cod) return;
    await fetch("/api/abrir_puerta", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({codigo: cod})
    });
    document.getElementById("codigo_puerta").value = "";
    cargarEstado();
}

setInterval(cargarEstado, 1000);
window.onload = cargarEstado;
