import { getEstado } from "./estado.js";

export function calcularRenacimientosPosibles() {
    const estado = getEstado();
    return Math.floor((estado.nivel_cpu || 1) / 5);
}

export async function hacerRenacimiento() {
    const cantidad = calcularRenacimientosPosibles();
    if (cantidad < 1) return alert("❌ Necesitas al menos nivel 5 de CPU para renacer");
    if (!confirm(`¿Renacer ${cantidad} vez/es? Perderás progreso pero obtendrás un bono permanente`)) return;
    await fetch("/api/hacer_renacimiento", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ cantidad })
    });
}
