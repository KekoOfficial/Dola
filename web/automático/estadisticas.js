// 📈 estadisticas.js
const stats = { totalGanado:0, vecesMejorado:0, logros:0, tiempoJugado:0 };

export function cargarStats() {
  const g = localStorage.getItem("estadisticas");
  if(g) Object.assign(stats, JSON.parse(g));
  return stats;
}
export function guardarStats() { localStorage.setItem("estadisticas", JSON.stringify(stats)); }
export function actualizarGanancia(monto) { stats.totalGanado += Number(monto); guardarStats(); }
