// 👤 perfil.js
let datos = { nombre:"", admin:false, ultimaSesion: new Date().toISOString() };

export function verificarAdmin(usuario, clave) {
  const ok = usuario==="admin" && clave==="tu_clave_segura";
  datos.admin = ok;
  return ok;
}
export function obtenerPerfil() { return datos; }
export function guardarPerfil() { localStorage.setItem("perfil", JSON.stringify(datos)); }
