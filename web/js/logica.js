let estado = {};

// 🧮 Formateo de números grandes
function formatearMonto(n) {
    if (typeof n !== 'number' || isNaN(n) || n < 0) return "$0.00";
    if (n >= 1e15) return `$${(n / 1e15).toFixed(2)}Q`;
    if (n >= 1e12) return `$${(n / 1e12).toFixed(2)}T`;
    if (n >= 1e9) return `$${(n / 1e9).toFixed(2)}B`;
    if (n >= 1e6) return `$${(n / 1e6).toFixed(2)}M`;
    if (n >= 1e3) return `$${(n / 1e3).toFixed(2)}K`;
    return `$${n.toFixed(2)}`;
}

// ⏱️ Formateo de tiempo
function formatearTiempo(seg) {
    if (typeof seg !== 'number' || isNaN(seg) || seg < 0) return "0h 0m";
    const h = Math.floor(seg / 3600);
    const m = Math.floor((seg % 3600) / 60);
    const s = Math.floor(seg % 60);
    if (h > 0) return `${h}h ${m}m`;
    if (m > 0) return `${m}m ${s}s`;
    return `${s}s`;
}

// 📊 Cálculo total de bonos combinados
function calcularBonoTotal() {
    const multGlobal = estado.multiplicador_global || 1.0;
    const bonoRenacimiento = estado.bono_renacimiento || 1.0;
    const bonoLogros = Object.values(estado.logros || {}).reduce((total, logro) => {
        return total * (logro.desbloqueado ? (logro.bono || 1.0) : 1.0);
    }, 1.0);
    return Number((multGlobal * bonoRenacimiento * bonoLogros).toFixed(4));
}

// 💰 Cálculo ganancia por segundo
function calcularGananciaPorSegundo() {
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
function aplicarDescuento(monto) {
    const descuento = estado.mejoras_pasivas?.descuento?.efecto || 0.0;
    return Number((monto * (1 - descuento)).toFixed(2));
}

// 🔄 Cargar estado desde servidor
async function cargarEstado() {
    try {
        const res = await fetch("/api/estado");
        if (!res.ok) throw new Error(`Error: ${res.status}`);
        estado = await res.json();
        mostrarDatos();
    } catch (e) {
        console.warn("No se pudo cargar el estado:", e);
    }
}

// 📋 Mostrar todos los datos en pantalla
function mostrarDatos() {
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

    // Costos con descuento aplicado
    if (document.getElementById("costo_cpu"))
        document.getElementById("costo_cpu").textContent = formatearMonto(aplicarDescuento(estado.costo_cpu || 0));

    if (document.getElementById("costo_mult"))
        document.getElementById("costo_mult").textContent = formatearMonto(aplicarDescuento(100 * (estado.multiplicador_global || 1) * 1.9));

    // Generadores
    const gen = estado.generadores || {};
    if (gen.basico) {
        document.getElementById("costo_basico").textContent = formatearMonto(aplicarDescuento(gen.basico.costo));
        document.getElementById("cant_basico").textContent = gen.basico.cantidad || 0;
    }
    if (gen.medio) {
        document.getElementById("costo_medio").textContent = formatearMonto(aplicarDescuento(gen.medio.costo));
        document.getElementById("cant_medio").textContent = gen.medio.cantidad || 0;
    }
    if (gen.avanzado) {
        document.getElementById("costo_avanzado").textContent = formatearMonto(aplicarDescuento(gen.avanzado.costo));
        document.getElementById("cant_avanzado").textContent = gen.avanzado.cantidad || 0;
    }
    if (gen.industrial) {
        document.getElementById("costo_industrial").textContent = formatearMonto(aplicarDescuento(gen.industrial.costo));
        document.getElementById("cant_industrial").textContent = gen.industrial.cantidad || 0;
    }
    if (gen.nuclear) {
        document.getElementById("costo_nuclear").textContent = formatearMonto(aplicarDescuento(gen.nuclear.costo));
        document.getElementById("cant_nuclear").textContent = gen.nuclear.cantidad || 0;
    }
    if (gen.cuantico) {
        document.getElementById("costo_cuantico").textContent = formatearMonto(aplicarDescuento(gen.cuantico.costo));
        document.getElementById("cant_cuantico").textContent = gen.cuantico.cantidad || 0;
    }
    if (gen.galactico) {
        document.getElementById("costo_galactico").textContent = formatearMonto(aplicarDescuento(gen.galactico.costo));
        document.getElementById("cant_galactico").textContent = gen.galactico.cantidad || 0;
    }

    // Puertas
    if (document.getElementById("lista_puertas")) {
        let html = "";
        for (const [id, p] of Object.entries(estado.puertas || {})) {
            const costo = aplicarDescuento(p.costo || 0);
            if (p.abierta) {
                html += `<div class="panel-mejora abierta">
                    <h3>${p.nombre || "Sin nombre"}</h3>
                    <p>✅ ABIERTA | Bono: +x${(p.bono || 1.0).toFixed(2)}</p>
                </div>`;
            } else {
                html += `<div class="panel-mejora cerrada">
                    <h3>${p.nombre || "Sin nombre"}</h3>
                    <p>Costo: ${formatearMonto(costo)} | Bono: +x${(p.bono || 1.0).toFixed(2)}</p>
                    <button onclick="abrirPuerta('${id}')" class="btn btn-accion" ${(estado.dinero || 0) < costo ? "disabled" : ""}>Abrir</button>
                </div>`;
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
                <p>${l.desbloqueado ? '✅' : '❌'} ${l.descripcion || "Sin descripción"}</p>
            </div>`;
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
async function accion(tipo) {
    try {
        await fetch(`/api/${tipo}`, { method: "POST" });
        cargarEstado();
    } catch (e) {
        console.error(`Error en acción ${tipo}:`, e);
    }
}

// 🛒 Comprar generador individual
async function comprarGenerador(tipo) {
    try {
        await fetch("/api/comprar_generador", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ tipo })
        });
        cargarEstado();
    } catch (e) {
        console.error(`Error al comprar ${tipo}:`, e);
    }
}

// 🚀 Comprar la cantidad máxima posible
async function comprarMax(tipo) {
    try {
        await fetch("/api/comprar_max_generador", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ tipo })
        });
        cargarEstado();
    } catch (e) {
        console.error(`Error al comprar máximo de ${tipo}:`, e);
    }
}

// 🚪 Abrir puerta
async function abrirPuerta(id) {
    try {
        await fetch("/api/abrir_puerta", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ id })
        });
        cargarEstado();
    } catch (e) {
        console.error(`Error al abrir puerta ${id}:`, e);
    }
}

// ⚙️ Mejorar habilidad pasiva
async function mejorarPasiva(tipo) {
    try {
        await fetch("/api/mejorar_pasiva", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ tipo })
        });
        cargarEstado();
    } catch (e) {
        console.error(`Error al mejorar pasiva ${tipo}:`, e);
    }
}

// 🔁 Actualización automática cada segundo
setInterval(cargarEstado, 1000);
window.onload = cargarEstado;
