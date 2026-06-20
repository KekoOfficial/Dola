import { getEstado } from "./estado.js";
import { aplicarDescuento, formatearMonto } from "./utilidades.js";

export function calcularMaxMultiplicadores() {
    const estado = getEstado();
    if (!estado || !estado.multiplicador_global) return 0;
    let dinero = estado.dinero || 0;
    let multActual = estado.multiplicador_global;
    let cantidad = 0;
    const base = 100;
    const factorCosto = 1.9;

    while (true) {
        const costo = aplicarDescuento(base * multActual * factorCosto, estado);
        if (dinero < costo) break;
        dinero -= costo;
        multActual *= 1.3;
        cantidad++;
    }
    return cantidad;
}

export function calcularCostoTotalMultiplicadores(cantidad) {
    const estado = getEstado();
    if (!estado || cantidad <= 0) return 0;
    let total = 0;
    let multActual = estado.multiplicador_global;
    const base = 100;
    const factorCosto = 1.9;

    for (let i = 0; i < cantidad; i++) {
        total += aplicarDescuento(base * multActual * factorCosto, estado);
        multActual *= 1.3;
    }
    return Number(total.toFixed(2));
}

export async function comprar1Multiplicador() {
    await fetch("/api/comprar_multiplicador", { method: "POST" });
}

export async function comprarMaxMultiplicadores() {
    const cant = calcularMaxMultiplicadores();
    if (cant < 1) return alert("❌ No alcanza el dinero");
    const total = calcularCostoTotalMultiplicadores(cant);
    if (!confirm(`¿Comprar ${cant} multiplicador(es) por ${formatearMonto(total)}?`)) return;
    await fetch("/api/comprar_max_multiplicador", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ cantidad: cant })
    });
}
