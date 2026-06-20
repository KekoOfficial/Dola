import { cargarEstado } from "./utilidades.js";

const CLAVE_ADMIN = "111";

export async function verificarAdmin(clave) {
    const res = await fetch("/api/verificar-admin", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ clave })
    });
    return (await res.json()).ok;
}

export async function cambiarDineroAdmin(nuevoValor) {
    await fetch("/api/admin-cambiar-dinero", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ nuevo_valor: nuevoValor })
    });
    cargarEstado();
}
