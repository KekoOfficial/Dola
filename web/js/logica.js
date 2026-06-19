let estado = {};

async function cargarEstado() {
    try {
        const res = await fetch("/api/estado");
        estado = await res.json();
        mostrarDatos();
    } catch (e) {
        console.log("Cargando datos...");
    }
}

function mostrarDatos() {
    if (document.getElementById("dinero"))
        document.getElementById("dinero").textContent = `$${estado.dinero.toFixed(2)}`;
    if (document.getElementById("multiplicador"))
        document.getElementById("multiplicador").textContent = (estado.multiplicador_global * estado.bono_renacimiento).toFixed(2);
    if (document.getElementById("nivel_cpu"))
        document.getElementById("nivel_cpu").textContent = estado.nivel_cpu;
    if (document.getElementById("renacimientos"))
        document.getElementById("renacimientos").textContent = estado.renacimientos;
    if (document.getElementById("bono_renacimiento"))
        document.getElementById("bono_renacimiento").textContent = estado.bono_renacimiento.toFixed(2);
    if (document.getElementById("ganancia_seg")) {
        let base = estado.ganancia_cpu;
        for (const g of Object.values(estado.generadores)) base += g.cantidad * g.ganancia;
        const total = base * estado.multiplicador_global * estado.bono_renacimiento;
        document.getElementById("ganancia_seg").textContent = total.toFixed(2);
    }
    if (document.getElementById("costo_cpu"))
        document.getElementById("costo_cpu").textContent = estado.costo_cpu.toFixed(2);
    if (document.getElementById("costo_mult"))
        document.getElementById("costo_mult").textContent = (100 * estado.multiplicador_global * 1.9).toFixed(2);
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
    if (document.getElementById("costo_industrial"))
        document.getElementById("costo_industrial").textContent = estado.generadores.industrial.costo.toFixed(2);
    if (document.getElementById("cant_industrial"))
        document.getElementById("cant_industrial").textContent = estado.generadores.industrial.cantidad;
    if (document.getElementById("lista_puertas")) {
        let html = "";
        for (const [id, p] of Object.entries(estado.puertas)) {
            if (p.abierta) {
                html += `<div class="panel-mejora"><h3>${p.nombre}</h3><p>✅ ABIERTA | Bono: +x${p.bono}</p></div>`;
            } else {
                html += `<div class="panel-mejora"><h3>${p.nombre}</h3><p>Costo: $${p.costo.toFixed(2)} | Bono: +x${p.bono}</p><button onclick="abrirPuerta('${id}')" class="btn btn-accion">Abrir</button></div>`;
            }
        }
        document.getElementById("lista_puertas").innerHTML = html;
    }
}

async function accion(tipo) {
    await fetch(`/api/${tipo}`, { method: "POST" });
    cargarEstado();
}

async function comprarGenerador(tipo) {
    await fetch("/api/comprar_generador", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({tipo})
    });
    cargarEstado();
}

async function abrirPuerta(id) {
    await fetch("/api/abrir_puerta", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({id})
    });
    cargarEstado();
}

setInterval(cargarEstado, 1000);
window.onload = cargarEstado;
