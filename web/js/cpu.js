import { getEstado } from "./estado.js";
import { aplicarDescuento } from "./utilidades.js";

export function calcularMaxCPU() {
    const estado = getEstado();
    if (!estado || !estado.costo_cpu) return 0;
    let dinero = estado.dinero || 0;
    let costo = estado.costo_cpu;
    let cantidad = 0;
    while (dinero >= aplicarDescuento(costo, estado)) {
        dinero -= aplicarDescuento(costo, estado);
        costo *= 2;
        cantidad++;
    }
    return cantidad;
}

export function calcularCostoTotalCPU(cantidad) {
    const estado = getEstado();
    if (!estado || cantidad <= 0) return 0;
    let total = 0;
    let costo = estado.costo_cpu;
    for (let i = 0; i < cantidad; i++) {
        total += aplicarDescuento(costo, estado);
        costo *= 2;
    }
    return Number(total.toFixed(2));
}

export async function comprar1CPU() {
    await fetch("/api/mejorar_cpu", { method: "POST" });
}

export async function comprarMaxCPU() {
    const cantidad = calcularMaxCPU();
    if (cantidad < 1) return alert("❌ No tienes suficiente dinero");
    const costoTotal = calcularCostoTotalCPU(cantidad);
    if (!confirm(`¿Comprar ${cantidad} nivel(es) de CPU por ${costoTotal}?`)) return;
    await fetch("/api/comprar_max_cpu", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ cantidad })
    });
}
