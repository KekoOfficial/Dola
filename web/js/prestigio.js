import { estado, cargarEstado } from "./utilidades.js";

export function mostrarPrestigio() {
    if (!estado || !estado.mejoras_pasivas) return;
    const mp = estado.mejoras_pasivas;
    if (document.getElementById("nivel_ahorro")) document.getElementById("nivel_ahorro").textContent = mp.ahorro.nivel || 0;
    if (document.getElementById("nivel_descuento")) document.getElementById("nivel_descuento").textContent = mp.descuento.nivel || 0;
    if (document.getElementById("nivel_inicio")) document.getElementById("nivel_inicio").textContent = mp.inicio_mejorado.nivel || 0;
}

export async function mejorarPasiva(tipo) {
    await fetch("/api/mejorar_pasiva", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ tipo })
    });
    cargarEstado();
}
