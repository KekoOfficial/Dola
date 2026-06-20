import { estado, formatearMonto, formatearTiempo } from "./utilidades.js";

export function mostrarEstadisticas() {
    if (!estado || !estado.estadisticas) return;
    const s = estado.estadisticas;
    if (document.getElementById("total_ganado")) document.getElementById("total_ganado").textContent = formatearMonto(s.dinero_total_ganado || 0);
    if (document.getElementById("mejoras_cpu")) document.getElementById("mejoras_cpu").textContent = s.mejoras_cpu || 0;
    if (document.getElementById("generadores_totales")) document.getElementById("generadores_totales").textContent = s.generadores_comprados || 0;
    if (document.getElementById("puertas_totales")) document.getElementById("puertas_totales").textContent = s.puertas_abiertas || 0;
    if (document.getElementById("tiempo_jugado")) document.getElementById("tiempo_jugado").textContent = formatearTiempo(s.tiempo_jugado || 0);
    if (document.getElementById("ganancia_max")) document.getElementById("ganancia_max").textContent = formatearMonto(s.ganancia_maxima || 0);
}
