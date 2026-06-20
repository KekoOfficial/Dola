import { getEstado } from "./estado.js";

export async function mejorarPasiva(tipo) {
    await fetch("/api/mejorar_pasiva", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ tipo })
    });
}
