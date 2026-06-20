import { estado } from "./utilidades.js";

export function mostrarLogros() {
    if (!estado || !document.getElementById("lista_logros")) return;
    let html = "";
    for (const l of Object.values(estado.logros || {})) {
        html += `<div class="logro ${l.desbloqueado ? "ok" : "bloqueado"}">
            <p>${l.desbloqueado ? "✅" : "❌"} ${l.descripcion}</p>
        </div>`;
    }
    document.getElementById("lista_logros").innerHTML = html;
}
