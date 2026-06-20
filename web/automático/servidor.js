// 🌐 servidor.js
export async function guardarEnNube(datos) {
  try {
    const res = await fetch("/api/guardar", {method:"POST", body:JSON.stringify(datos)});
    return res.ok;
  } catch { return false; }
}
