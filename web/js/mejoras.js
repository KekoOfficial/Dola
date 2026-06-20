import { estado, aplicarDescuento, formatearMonto, cargarEstado } from "./utilidades.js";

export function mostrarMejoras() {
    if (!estado) return;
    const costoCpu = aplicarDescuento(estado.costo_cpu || 0);
    const costoMult = aplicarDescuento(100 * (estado.multiplicador_global || 1) * 1.9);

    if (document.getElementById("costo_cpu")) {
        document.getElementById("costo_cpu").textContent = formatearMonto(costoCpu);
        document.getElementById("btn_mejorar_cpu").disabled = estado.dinero < costoCpu;
    }
    if (document.getElementById("costo_mult")) {
        document.getElementById("costo_mult").textContent = formatearMonto(costoMult);
        document.getElementById("btn_mult").disabled = estado.dinero < costoMult;
    }

    // Generadores
    const gen = estado.generadores || {};
    for (const [tipo, datos] of Object.entries(gen)) {
        const costo = aplicarDescuento(datos.costo || 0);
        const idCosto = `costo_${tipo}`;
        const idCant = `cant_${tipo}`;
        const idBtn = `btn_${tipo}`;
        if (document.getElementById(idCosto)) document.getElementById(idCosto).textContent = formatearMonto(costo);
        if (document.getElementById(idCant)) document.getElementById(idCant).textContent = datos.cantidad || 0;
        if (document.getElementById(idBtn)) document.getElementById(idBtn).disabled = estado.dinero < costo;
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
