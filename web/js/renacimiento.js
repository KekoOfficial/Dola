import { estado, cargarEstado } from "./utilidades.js";

// Calcula cuántos renacimientos podés hacer según nivel de CPU
export function calcularRenacimientosPosibles() {
    const nivelCpu = estado.nivel_cpu || 1;
    return Math.floor(nivelCpu / 5); // 5 niveles = 1 renacimiento
}

export function mostrarRenacimiento() {
    if (!estado) return;

    const totalPosibles = calcularRenacimientosPosibles();
    const bono = estado.bono_renacimiento || 1.0;

    document.getElementById("bono_renacimiento").textContent = `x${bono.toFixed(2)}`;
    document.getElementById("info_renacer").textContent = 
        totalPosibles > 0 
            ? `Podés hacer ${totalPosibles} renacimiento(s) (cada 5 niveles de CPU)` 
            : `Necesitás al menos nivel 5 de CPU para renacer`;

    document.getElementById("btn_renacer").disabled = totalPosibles < 1;
}

export async function hacerRenacimiento() {
    const total = calcularRenacimientosPosibles();
    if (total < 1) return;

    if (!confirm(`¿Querés hacer ${total} renacimiento(s)?\nSe reinicia progreso pero se mantienen logros y mejoras pasivas.`)) return;

    // Enviamos la cantidad al servidor
    await fetch("/api/hacer_renacimiento", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ cantidad: total })
    });

    cargarEstado();
}

window.hacerRenacimiento = hacerRenacimiento;
