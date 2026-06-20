import { getEstado } from "./estado.js";
import { aplicarDescuento } from "./utilidades.js";

export async function comprarGenerador(tipo) {
    await fetch("/api/comprar_generador", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ tipo })
    });
}

export async function comprarMaxGenerador(tipo) {
    await fetch("/api/comprar_max_generador", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ tipo })
    });
}
