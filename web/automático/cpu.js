// 🧠 cpu.js - Gestión de Saldo
let saldo = BigInt(localStorage.getItem("saldo") || "0");

export function obtenerSaldo() { return saldo; }
export function formatearSaldo() { return saldo.toLocaleString("es-PY"); }

export function establecerSaldo(valor) {
  const nuevo = BigInt(valor.toString().replace(/\D/g, "") || "0");
  if (nuevo < 0) return {ok:false, error:"No negativo"};
  saldo = nuevo;
  localStorage.setItem("saldo", saldo.toString());
  return {ok:true, saldo};
}

export function agregarSaldo(monto) { return establecerSaldo(saldo + BigInt(monto)); }
export function restarSaldo(monto) {
  const m = BigInt(monto);
  return saldo >= m ? establecerSaldo(saldo - m) : {ok:false, error:"Insuficiente"};
}
