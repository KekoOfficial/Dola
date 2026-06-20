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

export function aplicarDescuento(monto, estado) {
    const descuento = estado.mejoras_pasivas?.descuento?.efecto || 0;
    return Number((monto * (1 - descuento)).toFixed(4));
}
