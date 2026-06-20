import { getEstado } from "./estado.js";
import { formatearMonto, formatearTiempo, aplicarDescuento } from "./utilidades.js";
import { calcularMaxCPU, calcularCostoTotalCPU } from "./cpu.js";
import { calcularMaxMultiplicadores, calcularCostoTotalMultiplicadores } from "./multiplicadores.js";
import { calcularRenacimientosPosibles } from "./renacimiento.js";

export function calcularBonoTotal() {
    const estado = getEstado();
    const mult = estado.multiplicador_global || 1;
    const renac = estado.bono_renacimiento || 1;
    const logros = Object.values(estado.logros || {}).reduce((total, logro) => total * (logro.desbloqueado ? logro.bono : 1), 1);
    return Number((mult * renac * logros).toFixed(2));
}

export function calcularGananciaPorSegundo() {
    const estado = getEstado();
    let base = estado.ganancia_cpu || 0;
    for (const gen of Object.values(estado.generadores || {})) {
        base += (gen.cantidad || 0) * (gen.ganancia || 0);
    }
    return Number((base * calcularBonoTotal()).toFixed(4));
}

export function actualizarInterfaz() {
    const estado = getEstado();
    if (!estado) return;

    // Datos generales
    document.getElementById("dinero").textContent = formatearMonto(estado.dinero);
    document.getElementById("ganancia_seg").textContent = `${formatearMonto(calcularGananciaPorSegundo())}/seg`;
    document.getElementById("multiplicador").textContent = `x${calcularBonoTotal().toFixed(2)}`;
    document.getElementById("nivel_cpu").textContent = estado.nivel_cpu || 1;
    document.getElementById("renacimientos").textContent = estado.renacimientos || 0;
    document.getElementById("bono_renacimiento").textContent = `x${(estado.bono_renacimiento || 1).toFixed(2)}`;

    // 🖥️ CPU
    const costoCpu = aplicarDescuento(estado.costo_cpu || 0, estado);
    document.getElementById("costo_cpu").textContent = formatearMonto(costoCpu);
    const maxCpu = calcularMaxCPU();
    document.getElementById("cant_max_cpu").textContent = maxCpu;
    document.getElementById("costo_total_cpu").textContent = formatearMonto(calcularCostoTotalCPU(maxCpu));

    // ⚡ Multiplicadores
    const costoMult = aplicarDescuento(100 * estado.multiplicador_global * 1.9, estado);
    document.getElementById("costo_mult").textContent = formatearMonto(costoMult);
    const maxMult = calcularMaxMultiplicadores();
    document.getElementById("cant_max_mult").textContent = maxMult;
    document.getElementById("costo_total_mult").textContent = formatearMonto(calcularCostoTotalMultiplicadores(maxMult));

    // 🏭 Generadores
    const gen = estado.generadores || {};
    for (const tipo of ["basico", "medio", "avanzado", "industrial", "nuclear", "cuantico", "galactico"]) {
        if (gen[tipo]) {
            document.getElementById(`cant_${tipo}`).textContent = gen[tipo].cantidad || 0;
            document.getElementById(`costo_${tipo}`).textContent = formatearMonto(aplicarDescuento(gen[tipo].costo, estado));
        }
    }

    // 🔄 Renacimiento
    const renacPos = calcularRenacimientosPosibles();
    document.getElementById("info_renacer").textContent = renacPos > 0 
        ? `Podés renacer ${renacPos} vez(es)` 
        : "Necesitás nivel 5+ de CPU para renacer";
    document.getElementById("btn_renacer").disabled = renacPos < 1;

    // 🚪 Puertas
    let htmlPuertas = "";
    for (const [id, p] of Object.entries(estado.puertas || {})) {
        const costo = aplicarDescuento(p.costo, estado);
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

    // ⭐ Mejoras pasivas
    const mp = estado.mejoras_pasivas || {};
    document.getElementById("nivel_ahorro").textContent = mp.ahorro?.nivel || 0;
    document.getElementById("nivel_descuento").textContent = mp.descuento?.nivel || 0;
    document.getElementById("nivel_inicio").textContent = mp.inicio_mejorado?.nivel || 0;

    // 🏆 Logros
    let htmlLogros = "";
    for (const l of Object.values(estado.logros || {})) {
        htmlLogros += `<div class="logro ${l.desbloqueado ? "desbloqueado" : "bloqueado"}">${l.desbloqueado ? "✅" : "❌"} ${l.descripcion}</div>`;
    }
    document.getElementById("lista_logros").innerHTML = htmlLogros;

    // 📊 Estadísticas
    const est = estado.estadisticas || {};
    document.getElementById("total_ganado").textContent = formatearMonto(est.dinero_total_ganado || 0);
    document.getElementById("mejoras_cpu").textContent = est.mejoras_cpu || 0;
    document.getElementById("generadores_totales").textContent = est.generadores_comprados || 0;
    document.getElementById("puertas_totales").textContent = est.puertas_abiertas || 0;
    document.getElementById("tiempo_jugado").textContent = formatearTiempo(est.tiempo_jugado || 0);
    document.getElementById("ganancia_max").textContent = formatearMonto(est.ganancia_maxima || 0);
}
