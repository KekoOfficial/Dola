// 🔧 utilidades.js
export function formatoGrande(n) {
  return BigInt(n).toLocaleString("es-PY");
}
export function esperar(ms) { return new Promise(r=>setTimeout(r,ms)); }
export function numeroAleatorio(min,max) { return Math.floor(Math.random()*(max-min+1))+min; }
