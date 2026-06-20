import { estado, aplicarDescuento, formatearMonto, cargarEstado } from "./utilidades.js";

export function mostrarPuertas() {
    const cont = document.getElementById("lista_puertas");
    if (!estado || !cont) return;
    let html = "";
    for (const [id, p] of Object.entries(estado.puertas || {})) {
        const costo = aplicarDescuento(p.costo || 0);
        if (p.abierta) {
            html += `<div class="panel" style="margin:5px 0; padding:10px; background:#064e3b;">
                <h4>${p.nombre}</h4>
                <p>✅ ABIERTA | Bono: +x${p.bono.toFixed(2)}</p>
            </div>`;
        } else {
            html += `<div class="panel" style="margin:5px 0; padding:10px; background:#332a22;">
                <h4>${p.nombre}</h4>
                <p>Costo: ${formatearMonto(costo)} | Bono: +x${p.bono.toFixed(2)}</p>
                <button onclick="abrirPuerta('${id}')" ${estado.dinero < costo ? "disabled" : ""}>Abrir</button>
            </div>`;
        }
    }
    cont.innerHTML = html;
}

export async function abrirPuerta(id) {
    await fetch("/api/abrir_puerta", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id })
    });
    cargarEstado();
}

window.abrirPuerta = abrirPuerta;
