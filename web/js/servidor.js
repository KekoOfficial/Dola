// 📦 Variables globales
export let estado = {};
const CLAVE_ADMIN = "111";

// 🧮 Formateo de números grandes
export function formatearMonto(n) {
    if (typeof n !== 'number' || isNaN(n) || n < 0) return "$0.00";
    if (n >= 1e15) return `$${(n / 1e15).toFixed(2)}Q`;
    if (n >= 1e12) return `$${(n / 1e12).toFixed(2)}T`;
    if (n >= 1e9) return `$${(n / 1e9).toFixed(2)}B`;
    if (n >= 1e6) return `$${(n / 1e6).toFixed(2)}M`;
    if (n >= 1e3) return `$${(n / 1e3).toFixed(2)}K`;
    return `$${n.toFixed(2)}`;
}

// ⏱️ Formateo de tiempo
export function formatearTiempo(seg) {
    if (typeof seg !== 'number' || isNaN(seg) || seg < 0) return "0h 0m";
    const h = Math.floor(seg / 3600);
    const m = Math.floor((seg % 3600) / 60);
    const s = Math.floor(seg % 60);
    return h > 0 ? `${h}h ${m}m` : m > 0 ? `${m}m ${s}s` : `${s}s`;
}

// 📊 Cálculo de bonos totales
export function calcularBonoTotal() {
    const multGlobal = estado.multiplicador_global || 1.0;
    const bonoRenacimiento = estado.bono_renacimiento || 1.0;
    const bonoLogros = Object.values(estado.logros || {}).reduce((total, logro) => {
        return total * (logro.desbloqueado ? (logro.bono || 1.0) : 1.0);
    }, 1.0);
    return Number((multGlobal * bonoRenacimiento * bonoLogros).toFixed(4));
}

// 💰 Cálculo de ganancia por segundo
export function calcularGananciaPorSegundo() {
    let base = estado.ganancia_cpu || 0.0;
    for (const gen of Object.values(estado.generadores || {})) {
        const cantidad = gen.cantidad || 0;
        const ganancia = gen.ganancia || 0.0;
        base += cantidad * ganancia;
    }
    const total = base * calcularBonoTotal();
    return Number(total.toFixed(4));
}

// 📉 Aplicar descuento de mejoras pasivas
export function aplicarDescuento(monto) {
    const descuento = estado.mejoras_pasivas?.descuento?.efecto || 0.0;
    return Number((monto * (1 - descuento)).toFixed(2));
}

// 🔢 Calcular cuántos renacimientos se pueden hacer
export function calcularRenacimientosPosibles() {
    const nivelCpu = estado.nivel_cpu || 1;
    return Math.floor(nivelCpu / 5); // Cada 5 niveles = 1 renacimiento
}

// 🔄 Cargar estado desde el servidor
export async function cargarEstado() {
    try {
        const res = await fetch("/api/estado");
        if (!res.ok) throw new Error(`Error: ${res.status}`);
        estado = await res.json();
        actualizarInterfaz();
    } catch (e) {
        console.warn("⚠️ No se pudo cargar el estado:", e);
    }
}

// 📋 Actualizar todos los datos en pantalla
function actualizarInterfaz() {
    if (!estado || Object.keys(estado).length === 0) return;

    // Datos principales
    if (document.getElementById("dinero"))
        document.getElementById("dinero").textContent = formatearMonto(estado.dinero || 0);

    if (document.getElementById("multiplicador"))
        document.getElementById("multiplicador").textContent = `x${calcularBonoTotal().toFixed(2)}`;

    if (document.getElementById("nivel_cpu"))
        document.getElementById("nivel_cpu").textContent = estado.nivel_cpu || 1;

    if (document.getElementById("renacimientos"))
        document.getElementById("renacimientos").textContent = estado.renacimientos || 0;

    if (document.getElementById("bono_renacimiento"))
        document.getElementById("bono_renacimiento").textContent = `x${(estado.bono_renacimiento || 1.0).toFixed(2)}`;

    if (document.getElementById("ganancia_seg"))
        document.getElementById("ganancia_seg").textContent = `${formatearMonto(calcularGananciaPorSegundo())}/seg`;

    // Mejoras CPU y Multiplicador
    if (document.getElementById("costo_cpu"))
        document.getElementById("costo_cpu").textContent = formatearMonto(aplicarDescuento(estado.costo_cpu || 0));

    if (document.getElementById("costo_mult"))
        document.getElementById("costo_mult").textContent = formatearMonto(aplicarDescuento(100 * (estado.multiplicador_global || 1) * 1.9));

    // Generadores
    const gen = estado.generadores || {};
    for (const [tipo, datos] of Object.entries(gen)) {
        const costo = aplicarDescuento(datos.costo || 0);
        const idCosto = `costo_${tipo}`;
        const idCant = `cant_${tipo}`;
        if (document.getElementById(idCosto)) document.getElementById(idCosto).textContent = formatearMonto(costo);
        if (document.getElementById(idCant)) document.getElementById(idCant).textContent = datos.cantidad || 0;
    }

    // Renacimientos
    const posibles = calcularRenacimientosPosibles();
    if (document.getElementById("info_renacer")) {
        document.getElementById("info_renacer").textContent = posibles > 0 
            ? `Podés hacer ${posibles} renacimiento(s) (cada 5 niveles de CPU)` 
            : "Necesitás al menos nivel 5 de CPU";
    }
    if (document.getElementById("btn_renacer"))
        document.getElementById("btn_renacer").disabled = posibles < 1;

    // Puertas
    if (document.getElementById("lista_puertas")) {
        let html = "";
        for (const [id, p] of Object.entries(estado.puertas || {})) {
            const costo = aplicarDescuento(p.costo || 0);
            if (p.abierta) {
                html += `<div class="panel-mejora abierta"><h3>${p.nombre}</h3><p>✅ ABIERTA | Bono: +x${p.bono.toFixed(2)}</p></div>`;
            } else {
                html += `<div class="panel-mejora cerrada"><h3>${p.nombre}</h3>
                    <p>Costo: ${formatearMonto(costo)} | Bono: +x${p.bono.toFixed(2)}</p>
                    <button onclick="abrirPuerta('${id}')" ${estado.dinero < costo ? "disabled" : ""}>Abrir</button></div>`;
            }
        }
        document.getElementById("lista_puertas").innerHTML = html;
    }

    // Estadísticas
    if (document.getElementById("total_ganado")) {
        const s = estado.estadisticas || {};
        document.getElementById("total_ganado").textContent = formatearMonto(s.dinero_total_ganado || 0);
        document.getElementById("mejoras_cpu").textContent = s.mejoras_cpu || 0;
        document.getElementById("generadores_totales").textContent = s.generadores_comprados || 0;
        document.getElementById("puertas_totales").textContent = s.puertas_abiertas || 0;
        document.getElementById("tiempo_jugado").textContent = formatearTiempo(s.tiempo_jugado || 0);
        document.getElementById("ganancia_max").textContent = formatearMonto(s.ganancia_maxima || 0);
    }

    // Logros
    if (document.getElementById("lista_logros")) {
        let html = "";
        for (const l of Object.values(estado.logros || {})) {
            html += `<div class="logro ${l.desbloqueado ? 'desbloqueado' : 'bloqueado'}">
                <p>${l.desbloqueado ? '✅' : '❌'} ${l.descripcion}</p></div>`;
        }
        document.getElementById("lista_logros").innerHTML = html;
    }

    // Mejoras pasivas
    if (document.getElementById("nivel_ahorro")) {
        const mp = estado.mejoras_pasivas || {};
        document.getElementById("nivel_ahorro").textContent = mp.ahorro?.nivel || 0;
        document.getElementById("nivel_descuento").textContent = mp.descuento?.nivel || 0;
        document.getElementById("nivel_inicio").textContent = mp.inicio_mejorado?.nivel || 0;
    }
}

// ⚡ Acciones generales
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

export async function abrirPuerta(id) {
    await fetch("/api/abrir_puerta", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id })
    });
    cargarEstado();
}

// 🔄 Renacimiento con cantidad automática
export async function hacerRenacimiento() {
    const cantidad = calcularRenacimientosPosibles();
    if (cantidad < 1) return;
    if (!confirm(`¿Querés hacer ${cantidad} renacimiento(s)?\nSe reinicia progreso pero se mantienen logros y mejoras pasivas.`)) return;

    await fetch("/api/hacer_renacimiento", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ cantidad: cantidad })
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

// 👤 Administrador
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

// 🔁 Actualización automática cada segundo
setInterval(cargarEstado, 1000);
window.onload = cargarEstado;

// 📤 Hacer funciones accesibles desde el HTML
window.mejorarCPU = mejorarCPU;
window.comprarMultiplicador = comprarMultiplicador;
window.comprarGenerador = comprarGenerador;
window.comprarMaxGenerador = comprarMaxGenerador;
window.abrirPuerta = abrirPuerta;
window.hacerRenacimiento = hacerRenacimiento;
window.mejorarPasiva = mejorarPasiva;
