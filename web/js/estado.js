let estado = {};

export function getEstado() {
    return estado;
}

export function setEstado(nuevoEstado) {
    estado = nuevoEstado;
}

export async function cargarEstado() {
    try {
        const res = await fetch("/api/estado");
        if (!res.ok) throw new Error("Error al cargar");
        setEstado(await res.json());
        return true;
    } catch (e) {
        console.warn("⚠️", e);
        return false;
    }
}
