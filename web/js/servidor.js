export let estado = {};

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
    return Number((monto * (1 - desc)).toFixed(4));
}

export function calcularGananciaPorSegundo() {
    let base = estado.ganancia_cpu || 0;
    for (const g of Object.values(estado.generadores || {})) base += (g.cantidad || 0) * (g.ganancia || 0);
    return Number((base * calcularBonoTotal()).toFixed(4));
}

export function calcularMaxCPU() {
    if (!estado || !estado.costo_cpu) return 0;
    let dinero = estado.dinero || 0;
    let costo = estado.costo_cpu;
    let cant = 0;
    while (dinero >= aplicarDescuento(costo)) {
        dinero -= aplicarDescuento(costo);
        costo *= 2;
        cant++;
    }
    return cant;
}

export function calcularCostoTotalCPU(cantidad) {
    if (!estado || cantidad <= 0) return 0;
    let total = 0;
    let costo = estado.costo_cpu;
    for (let i = 0; i < cantidad; i++) {
        total += aplicarDescuento(costo);
        costo *= 2;
    }
    return Number(total.toFixed(2));
}

export function calcularRenacimientosPosibles() {
    return Math.floor((estado.nivel_cpu || 1) / 5);
}

export async function cargarEstado() {
    try {
        const res = await fetch("/api/estado");
        if (!res.ok) throw new Error("Error");
        estado = await res.json();
        actualizarInterfaz();
    } catch (e) {
        console.warn("⚠️", e);
    }
}

function actualizarInterfaz() {
    if (!estado) return;
    document.getElementById("dinero").textContent = formatearMonto(estado.dinero || 0);
    document.getElementById("ganancia_seg").textContent = `${formatearMonto(calcularGananciaPorSegundo())}/seg`;
    document.getElementById("multiplicador").textContent = `x${calcularBonoTotal().toFixed(2)}`;
    document.getElementById("nivel_cpu").textContent = estado.nivel_cpu || 1;
    document.getElementById("renacimientos").textContent = estado.renacimientos || 0;

    document.getElementById("costo_cpu").textContent = formatearMonto(aplicarDescuento(estado.costo_cpu || 0));
    const maxCpu = calcularMaxCPU();
    document.getElementById("cant_max_cpu").textContent = maxCpu;
    document.getElementById("costo_total_cpu").textContent = formatearMonto(calcularCostoTotalCPU(maxCpu));

    document.getElementById("costo_mult").textContent = formatearMonto(aplicarDescuento(100 * estado.multiplicador_global * 1.9));

    const gen = estado.generadores || {};
    for (const [tipo, d] of Object.entries(gen)) {
        document.getElementById(`cant_${tipo}`).textContent = d.cantidad || 0;
        document.getElementById(`costo_${tipo}`).textContent = formatearMonto(aplicarDescuento(d.costo || 0));
    }

    const renacPos = calcularRenacimientosPosibles();
    document.getElementById("info_renacer").textContent = renacPos ? `Podés hacer ${renacPos} renacimiento(s)` : "Necesitás nivel 5+";
    document.getElementById("btn_renacer").disabled = renacPos < 1;
    document.getElementById("bono_renacimiento").textContent = `x${(estado.bono_renacimiento || 1).toFixed(2)}`;

    let htmlPuertas = "";
    for (const [id, p] of Object.entries(estado.puertas || {})) {
        const costo = aplicarDescuento(p.costo);
        if (p.abierta) {
            htmlPuertas += `<div style="background:#064e3b;padding:10px;border-radius:6px;margin:5px 0;">✅ ${p.nombre} | Bono +x${p.bono.toFixed(2)}</div>`;
        } else {
            htmlPuertas += `<div style="background:#332a22;padding:10px;border-radius:6px;margin:5px 0;">
                ${p.nombre} | Costo: ${formatearMonto(costo)}
                <button onclick="abrirPuerta('${id}')" ${estado.dinero < costo ? "disabled" : ""}>Abrir</button>
            </div>`;
        }
    }
    document.getElementById("lista_puertas").innerHTML = htmlPuertas;

    const s = estado.estadisticas || {};
    document.getElementById("total_ganado").textContent = formatearMonto(s.dinero_total_ganado || 0);
    document.getElementById("mejoras_cpu").textContent = s.mejoras_cpu || 0;
    document.getElementById("generadores_totales").textContent = s.generadores_comprados || 0;
    document.getElementById("puertas_totales").textContent = s.puertas_abiertas || 0;
    document.getElementById("tiempo_jugado").textContent = formatearTiempo(s.tiempo_jugado || 0);
    document.getElementById("ganancia_max").textContent = formatearMonto(s.ganancia_maxima || 0);

    let htmlLogros = "";
    for (const l of Object.values(estado.logros || {})) {
        htmlLogros += `<div class="logro ${l.desbloqueado ? "desbloqueado" : "bloqueado"}">${l.desbloqueado ? "✅" : "❌"} ${l.descripcion}</div>`;
    }
    document.getElementById("lista_logros").innerHTML = htmlLogros;

    const mp = estado.mejoras_pasivas || {};
    document.getElementById("nivel_ahorro").textContent = mp.ahorro?.nivel || 0;
    document.getElementById("nivel_descuento").textContent = mp.descuento?.nivel || 0;
    document.getElementById("nivel_inicio").textContent = mp.inicio_mejorado?.nivel || 0;
}

export async function comprar1CPU() {
    await fetch("/api/mejorar_cpu", { method: "POST" });
    cargarEstado();
}

export async function comprarMaxCPU() {
    const cant = calcularMaxCPU();
    if (cant < 1) return alert("❌ No alcanza el dinero");
    if (!confirm(`¿Comprar ${cant} CPU por ${formatearMonto(calcularCostoTotalCPU(cant))}?`)) return;
    await fetch("/api/comprar_max_cpu", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ cantidad: cant })
    });
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

export async function abrirPuerta(id) {
    await fetch("/api/abrir_puerta", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id })
    });
    cargarEstado();
}

export async function hacerRenacimiento() {
    const cant = calcularRenacimientosPosibles();
    if (cant < 1) return;
    if (!confirm(`¿Renacer ${cant} vez/es?`)) return;
    await fetch("/api/hacer_renacimiento", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ cantidad: cant })
    });
    cargarEstado();
}

export async function mejorarPasiva(tipo) {
    await fetch("/api/mejorar_pasiva", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ tipo })
    });
    cargarEstado();
}

setInterval(cargarEstado, 1000);
window.onload = cargarEstado;

window.comprar1CPU = comprar1CPU;
window.comprarMaxCPU = comprarMaxCPU;
window.comprarMultiplicador = comprarMultiplicador;
window.comprarGenerador = comprarGenerador;
window.comprarMaxGenerador = comprarMaxGenerador;
window.abrirPuerta = abrirPuerta;
window.hacerRenacimiento = hacerRenacimiento;
window.mejorarPasiva = mejorarPasiva;
