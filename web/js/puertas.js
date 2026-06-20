export async function abrirPuerta(id) {
    await fetch("/api/abrir_puerta", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id })
    });
}
