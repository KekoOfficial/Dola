// 📊 estado.js
const estado = {
  activo: true, velocidad: 1.0, modo:"normal", admin:false, ultimaAct: new Date().toISOString()
};

export function cargarEstado() {
  const g = localStorage.getItem("estado");
  if(g) Object.assign(estado, JSON.parse(g));
  return estado;
}
export function guardarEstado() { localStorage.setItem("estado", JSON.stringify(estado)); }
export function modificarEstado(clave, valor) { if(clave in estado) { estado[clave]=valor; guardarEstado(); return true; } return false; }
