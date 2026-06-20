let estado = {};

export function formatearMonto(n) {
    if (typeof n !== 'number' || isNaN(n) || n < 0) return "$0.00";
    if (n >= 1e15) return `$${(n / 1e15).toFixed(2)}Q`;
    if (n >= 1e12) return `$${(n / 1e12).toFixed(2)}T`;
    if (n >= 1e9) return `$${(n / 1e9).toFixed(2)}B`;
    if (n >= 1e6) return `$${(n / 1e6).toFixed(2)}M`;
    if (n >= 1e3) return `$${(n / 1e3).toFixed(2)}K`;
    return `$${n.toFixed(2)}`;
}

export function formatearTiempo(seg) {
    if (typeof seg !== 'number' || isNaN(seg) || seg < 0) return "0h 0m";
    const h = Math.floor(seg / 3600);
    const m = Math.floor((seg % 3600) / 60);
    const s = Math.floor(seg % 60);
    return h > 0 ? `${h}h ${m}m` : m > 0 ? `${m}m ${s}s` : `${s}s`;
}

export function calcularBonoTotal() {
    const mult = estado.multiplicador_global || 1;
    const renac = estado.bono_renacimiento || 1;
    const logros = Object.values(estado.logros || {}).reduce((t, l) => t * (l.desbloqueado ? l.bono : 1), 1);
    return Number((mult * renac * logros).toFixed(4));
}

export function aplicarDescuento(monto) {
    const desc = estado.mejoras_pasivas?.descuento?.efecto || 0;
    return Number((monto * (1 - desc)).toFixed(2));
}

export async function cargarEstado() {
    try {
        const res = await fetch("/api/estado");
        if (!res.ok) throw new Error("Error al cargar");
        estado = await res.json();
        actualizarTodo();
    } catch (e) {
        console.warn("Carga fallida:", e);
    }
}

function actualizarTodo() {
    if (document.getElementById("dinero")) document.getElementById("dinero").textContent = formatearMonto(estado.dinero || 0);
    if (document.getElementById("multiplicador")) document.getElementById("multiplicador").textContent = `x${calcularBonoTotal().toFixed(2)}`;
    if (document.getElementById("nivel_cpu")) document.getElementById("nivel_cpu").textContent = estado.nivel_cpu || 1;
    if (document.getElementById("renacimientos")) document.getElementById("renacimientos").textContent = estado.renacimientos || 0;
    if (document.getElementById("ganancia_seg")) document.getElementById("ganancia_seg").textContent = formatearMonto(calcularGanancia()) + "/seg";
}

function calcularGanancia() {
    let base = estado.ganancia_cpu || 0;
    for (const g of Object.values(estado.generadores || {})) base += (g.cantidad || 0) * (g.ganancia || 0);
    return base * calcularBonoTotal();
}

setInterval(cargarEstado, 1000);
window.onload = cargarEstado;
