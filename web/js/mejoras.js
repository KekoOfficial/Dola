import { estado, aplicarDescuento, formatearMonto, cargarEstado } from "./utilidades.js";

export function mostrarMejoras() {
    if (!estado) return;
    document.getElementById("costo_cpu").textContent = formatearMonto(aplicarDescuento(estado.costo_cpu || 0));
    document.getElementById("costo_mult").textContent = formatearMonto(aplicarDescuento(100 * (estado.multiplicador_global || 1) * 1.9));

    const gen = estado.generadores || {};
    for (const [tipo, datos] of Object.entries(gen)) {
        document.getElementById(`costo_${tipo}`).textContent = formatearMonto(aplicarDescuento(datos.costo || 0));
        document.getElementById(`cant_${tipo}`).textContent = datos.cantidad || 0;
    }
}

export async function mejorarCPU() {
    await fetch("/api/mejorar_cpu", { method: "POST" });
    cargarEstado();
}

export async function comprarMultiplicador() {
    await fetch("/api/comprar_multiplicador", { method: "POST" });
    cargarEstado();
}

export async function comprarGenerador(tipo) {
    await fetch("/api/comprar_generador", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ tipo })
    });
    cargarEstado();
}

export async function comprarMaxGenerador(tipo) {
    await fetch("/api/comprar_max_generador", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ tipo })
    });
    cargarEstado();
}

window.mejorarCPU = mejorarCPU;
window.comprarMultiplicador = comprarMultiplicador;
window.comprarGenerador = comprarGenerador;
window.comprarMaxGenerador = comprarMaxGenerador;
