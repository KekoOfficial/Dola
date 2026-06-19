let estado = {};

function formatearMonto(n) {
    if (n >= 1e12) return `$${(n/1e12).toFixed(2)}T`;
    if (n >= 1e9) return `$${(n/1e9).toFixed(2)}B`;
    if (n >= 1e6) return `$${(n/1e6).toFixed(2)}M`;
    if (n >= 1e3) return `$${(n/1e3).toFixed(2)}K`;
    return `$${n.toFixed(2)}`;
}

function formatearTiempo(seg) {
    const h = Math.floor(seg / 3600);
    const m = Math.floor((seg % 3600) / 60);
    return `${h}h ${m}m`;
}

async function cargarEstado() {
    try {
        const res = await fetch("/api/estado");
        estado = await res.json();
        mostrarDatos();
    } catch (e) {
        console.log("Cargando...", e);
    }
}

function mostrarDatos() {
    if (document.getElementById("dinero"))
        document.getElementById("dinero").textContent = formatearMonto(estado.dinero);
    if (document.getElementById("multiplicador")) {
        const bonoLogros = Object.values(estado.logros).reduce((t, l) => t * (l.desbloqueado ? l.bono : 1), 1);
        document.getElementById("multiplicador").textContent = (estado.multiplicador_global * estado.bono_renacimiento * bonoLogros).toFixed(2);
    }
    if (document.getElementById("nivel_cpu")) document.getElementById("nivel_cpu").textContent = estado.nivel_cpu;
    if (document.getElementById("renacimientos")) document.getElementById("renacimientos").textContent = estado.renacimientos;
    if (document.getElementById("bono_renacimiento")) document.getElementById("bono_renacimiento").textContent = estado.bono_renacimiento.toFixed(2);
    if (document.getElementById("ganancia_seg")) {
        let base = estado.ganancia_cpu;
        for (const g of Object.values(estado.generadores)) base += g.cantidad * g.ganancia;
        const total = base * estado.multiplicador_global * estado.bono_renacimiento * Object.values(estado.logros).reduce((t,l)=>t*(l.desbloqueado?l.bono:1),1);
        document.getElementById("ganancia_seg").textContent = formatearMonto(total);
    }
    if (document.getElementById("costo_cpu")) document.getElementById("costo_cpu").textContent = formatearMonto(estado.costo_cpu * (1 - estado.mejoras_pasivas.descuento.efecto));
    if (document.getElementById("costo_mult")) document.getElementById("costo_mult").textContent = formatearMonto(100 * estado.multiplicador_global * 1.9 * (1 - estado.mejoras_pasivas.descuento.efecto));

    // Generadores
    const gen = estado.generadores;
    document.getElementById("costo_basico").textContent = formatearMonto(gen.basico.costo * (1 - estado.mejoras_pasivas.descuento.efecto));
    document.getElementById("cant_basico").textContent = gen.basico.cantidad;
    document.getElementById("costo_medio").textContent = formatearMonto(gen.medio.costo * (1 - estado.mejoras_pasivas.descuento.efecto));
    document.getElementById("cant_medio").textContent = gen.medio.cantidad;
    document.getElementById("costo_avanzado").textContent = formatearMonto(gen.avanzado.costo * (1 - estado.mejoras_pasivas.descuento.efecto));
    document.getElementById("cant_avanzado").textContent = gen.avanzado.cantidad;
    document.getElementById("costo_industrial").textContent = formatearMonto(gen.industrial.costo * (1 - estado.mejoras_pasivas.descuento.efecto));
    document.getElementById("cant_industrial").textContent = gen.industrial.cantidad;
    document.getElementById("costo_nuclear").textContent = formatearMonto(gen.nuclear.costo * (1 - estado.mejoras_pasivas.descuento.efecto));
    document.getElementById("cant_nuclear").textContent = gen.nuclear.cantidad;
    document.getElementById("costo_cuantico").textContent = formatearMonto(gen.cuantico.costo * (1 - estado.mejoras_pasivas.descuento.efecto));
    document.getElementById("cant_cuantico").textContent = gen.cuantico.cantidad;
    document.getElementById("costo_galactico").textContent = formatearMonto(gen.galactico.costo * (1 - estado.mejoras_pasivas.descuento.efecto));
    document.getElementById("cant_galactico").textContent = gen.galactico.cantidad;

    // Puertas
    if (document.getElementById("lista_puertas")) {
        let html = "";
        for (const [id, p] of Object.entries(estado.puertas)) {
            if (p.abierta) html += `<div class="panel-mejora"><h3>${p.nombre}</h3><p>✅ ABIERTA | Bono: +x${p.bono}</p></div>`;
            else html += `<div class="panel-mejora"><h3>${p.nombre}</h3><p>Costo: ${formatearMonto(p.costo * (1 - estado.mejoras_pasivas.descuento.efecto))} | Bono: +x${p.bono}</p><button onclick="abrirPuerta('${id}')" class="btn btn-accion">Abrir</button></div>`;
        }
        document.getElementById("lista_puertas").innerHTML = html;
    }

    // Estadísticas
    if (document.getElementById("total_ganado")) {
        const s = estado.estadisticas;
        document.getElementById("total_ganado").textContent = formatearMonto(s.dinero_total_ganado);
        document.getElementById("mejoras_cpu").textContent = s.mejoras_cpu;
        document.getElementById("generadores_totales").textContent = s.generadores_comprados;
        document.getElementById("puertas_totales").textContent = s.puertas_abiertas;
        document.getElementById("tiempo_jugado").textContent = formatearTiempo(s.tiempo_jugado);
        document.getElementById("ganancia_max").textContent = formatearMonto(s.ganancia_maxima);
    }

    // Logros
    if (document.getElementById("lista_logros")) {
        let html = "";
        for (const l of Object.values(estado.logros)) {
            html += `<div class="logro ${l.desbloqueado ? 'desbloqueado' : 'bloqueado'}">
                <p>${l.desbloqueado ? '✅' : '❌'} ${l.descripcion}</p>
            </div>`;
        }
        document.getElementById("lista_logros").innerHTML = html;
    }

    // Prestigio
    if (document.getElementById("nivel_ahorro")) {
        document.getElementById("nivel_ahorro").textContent = estado.mejoras_pasivas.ahorro.nivel;
        document.getElementById("nivel_descuento").textContent = estado.mejoras_pasivas.descuento.nivel;
        document.getElementById("nivel_inicio").textContent = estado.mejoras_pasivas.inicio_mejorado.nivel;
    }
}

async function accion(tipo) {
    await fetch(`/api/${tipo}`, { method: "POST" });
    cargarEstado();
}

async function comprarGenerador(tipo) {
    await fetch("/api/comprar_generador", { method: "POST", headers: {"Content-Type":"application/json"}, body: JSON.stringify({tipo}) });
    cargarEstado();
}

async function comprarMax(tipo) {
    await fetch("/api/comprar_max_generador", { method: "POST", headers: {"Content-Type":"application/json"}, body: JSON.stringify({tipo}) });
    cargarEstado();
}

async function abrirPuerta(id) {
    await fetch("/api/abrir_puerta", { method: "POST", headers: {"Content-Type":"application/json"}, body: JSON.stringify({id}) });
    cargarEstado();
}

async function mejorarPasiva(tipo) {
    await fetch("/api/mejorar_pasiva", { method: "POST", headers: {"Content-Type":"application/json"}, body: JSON.stringify({tipo}) });
    cargarEstado();
}

setInterval(cargarEstado, 1000);
window.onload = cargarEstado;
