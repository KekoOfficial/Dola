import { estado, cargarEstado } from "./utilidades.js";

export function mostrarRenacimiento() {
    if (!estado) return;
    if (document.getElementById("bono_renacimiento")) {
        document.getElementById("bono_renacimiento").textContent = `x${(estado.bono_renacimiento || 1).toFixed(2)}`;
    }
    if (document.getElementById("btn_renacer")) {
        const puede = (estado.nivel_cpu || 0) >= 5;
        document.getElementById("btn_renacer").disabled = !puede;
        document.getElementById("info_renacer").textContent = puede ? "Listo para renacer" : "Necesitas nivel CPU ≥ 5";
    }
}

export async function hacerRenacimiento() {
    if (!confirm("¿Seguro que querés renacer? Se reinicia todo menos mejoras pasivas y logros")) return;
    await fetch("/api/hacer_renacimiento", { method: "POST" });
    cargarEstado();
}
