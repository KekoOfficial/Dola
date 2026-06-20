import { getEstado } from "./estado.js";
import { formatearMonto, formatearTiempo } from "./utilidades.js";
import { calcularMaxCPU, calcularCostoTotalCPU } from "./cpu.js";
import { calcularMaxMultiplicadores, calcularCostoTotalMultiplicadores } from "./multiplicadores.js";

export function calcularBonoTotal() {
    const estado = getEstado();
    const mult = estado.multiplicador_global || 1;
    const renac = estado.bono_renacimiento || 1;
    const logros = Object.values(estado.logros || {}).reduce((t, l) => t * (l.desbloqueado ? l.bono : 1), 1);
    return Number((mult * renac * logros).toFixed(2));
}

export function calcularGananciaPorSegundo() {
    const estado = getEstado();
    let base = estado.ganancia_cpu || 0;
    for (const g of Object.values(estado.generadores || {})) base += (g.cantidad || 0) * (g.ganancia || 0);
    return Number((base * calcularBonoTotal()).toFixed(4));
}

export function actualizarInterfaz() {
    const estado = getEstado();
    if (!estado) return;

    // Datos principales
    document.getElementById("dinero").textContent = formatearMonto(estado.dinero);
    document.getElementById("ganancia_seg").textContent = `${formatearMonto(calcularGananciaPorSegundo())}/seg`;
    document.getElementById("multiplicador").textContent = `x${calcularBonoTotal().toFixed(2)}`;
    document.getElementById("nivel_cpu").textContent = estado.nivel_cpu;
    document.getElementById("renacimientos").textContent = estado.renacimientos;

    // CPU
    document.getElementById("costo_cpu").textContent = formatearMonto(estado.costo_cpu);
    const maxCpu = calcularMaxCPU();
    document.getElementById("cant_max_cpu").textContent = maxCpu;
    document.getElementById("costo_total_cpu").textContent = formatearMonto(calcularCostoTotalCPU(maxCpu));

    // ✅ Multiplicadores
    const maxMult = calcularMaxMultiplicadores();
    document.getElementById("cant_max_mult").textContent = maxMult;
    document.getElementById("costo_total_mult").textContent = formatearMonto(calcularCostoTotalMultiplicadores(maxMult));
    document.getElementById("costo_mult").textContent = formatearMonto(100 * estado.multiplicador_global * 1.9 * (1 - estado.mejoras_pasivas.descuento.efecto));

    // ... resto de actualizaciones (generadores, puertas, etc.)
}
