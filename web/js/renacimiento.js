import { estado, cargarEstado } from "./utilidades.js";

export function mostrarRenacimiento() {
    if (!estado) return;
    document.getElementById("bono_renacimiento").textContent = `x${(estado.bono_renacimiento || 1).toFixed(2)}`;
    const puede = (estado.nivel_cpu || 0) >= 5;
    document.getElementById("info_renacer").textContent = puede ? "Listo para renacer" : "Necesitas nivel CPU ≥ 5";
    document.getElementById("btn_renacer").disabled = !puede;
}

export async function hacerRenacimiento() {
    if (!confirm("¿Renacer? Se reinicia todo menos logros y mejoras pasivas.")) return;
    await fetch("/api/hacer_renacimiento", { method: "POST" });
    cargarEstado();
}

window.hacerRenacimiento = hacerRenacimiento;