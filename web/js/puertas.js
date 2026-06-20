import { estado, aplicarDescuento, formatearMonto, cargarEstado } from "./utilidades.js";

export function mostrarPuertas() {
    if (!estado || !document.getElementById("lista_puertas")) return;
    let html = "";
    for (const [id, p] of Object.entries(estado.puertas || {})) {
        const costo = aplicarDescuento(p.costo || 0);
        if (p.abierta) {
            html += `<div class="puerta abierta"><h3>${p.nombre}</h3><p>✅ Abierta | Bono: +x${p.bono.toFixed(2)}</p></div>`;
        } else {
            html += `<div class="puerta cerrada">
                <h3>${p.nombre}</h3>
                <p>Costo: ${formatearMonto(costo)} | Bono: +x${p.bono.toFixed(2)}</p>
                <button onclick="abrirPuerta('${id}')" ${estado.dinero < costo ? "disabled" : ""}>Abrir</button>
            </div>`;
        }
    }
    document.getElementById("lista_puertas").innerHTML = html;
}

export async function abrirPuerta(id) {
    await fetch("/api/abrir_puerta", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id })
    });
    cargarEstado();
}
