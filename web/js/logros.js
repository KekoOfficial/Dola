import { estado } from "./utilidades.js";

export function mostrarLogros() {
    const cont = document.getElementById("lista_logros");
    if (!estado || !cont) return;
    let html = "";
    for (const l of Object.values(estado.logros || {})) {
        html += `<div class="logro ${l.desbloqueado ? 'desbloqueado' : 'bloqueado'}">
            <p>${l.desbloqueado ? "✅" : "❌"} ${l.descripcion}</p>
        </div>`;
    }
    cont.innerHTML = html;
}
