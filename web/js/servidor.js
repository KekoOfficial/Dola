// 🔢 Calcular cuántos CPU se pueden comprar con el dinero actual
export function calcularMaxCPU() {
    if (!estado || !estado.costo_cpu) return 0;
    let dinero = estado.dinero || 0;
    let costoActual = estado.costo_cpu;
    let cantidad = 0;
    const tasaAumento = 2.0; // Igual que en el servidor

    while (dinero >= costoActual) {
        dinero -= costoActual;
        costoActual *= tasaAumento;
        cantidad++;
    }
    return cantidad;
}

// 📉 Calcular costo total para comprar N CPU
export function calcularCostoTotalCPU(cantidad) {
    if (!estado || !estado.costo_cpu || cantidad <= 0) return 0;
    let costo = 0;
    let costoActual = estado.costo_cpu;
    const tasaAumento = 2.0;

    for (let i = 0; i < cantidad; i++) {
        costo += costoActual;
        costoActual *= tasaAumento;
    }
    return aplicarDescuento(costo);
}

// 🖥️ Comprar 1 CPU
export async function comprar1CPU() {
    await fetch("/api/mejorar_cpu", { method: "POST" });
    cargarEstado();
}

// 🖥️ Comprar máximo de CPU posible
export async function comprarMaxCPU() {
    const cantidad = calcularMaxCPU();
    if (cantidad <= 0) {
        alert("❌ No tenés suficiente dinero para mejorar la CPU");
        return;
    }
    const costoTotal = calcularCostoTotalCPU(cantidad);
    if (!confirm(`¿Comprar ${cantidad} niveles de CPU por un total de ${formatearMonto(costoTotal)}?`)) return;

    await fetch("/api/comprar_max_cpu", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ cantidad: cantidad })
    });
    cargarEstado();
}

// Actualizar la interfaz para mostrar cantidades
function actualizarInterfaz() {
    // ... todo el código anterior ...

    // 🖥️ Datos de CPU
    const maxPosible = calcularMaxCPU();
    const costoTotal = calcularCostoTotalCPU(maxPosible);
    if (document.getElementById("cant_max_cpu"))
        document.getElementById("cant_max_cpu").textContent = maxPosible;
    if (document.getElementById("costo_total_cpu"))
        document.getElementById("costo_total_cpu").textContent = formatearMonto(costoTotal);

    // ... resto del código ...
}

// Hacer accesibles desde el HTML
window.comprar1CPU = comprar1CPU;
window.comprarMaxCPU = comprarMaxCPU;
