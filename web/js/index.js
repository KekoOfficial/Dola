// ==============================================
// 🚀 INDEX.JS - PUNTO DE ENTRADA PRINCIPAL
// Conecta todos los módulos de la carpeta /js
// ==============================================

// 📦 IMPORTACIÓN DE TODOS LOS MÓDULOS
// (se cargan tal cual están en la carpeta)
import * as CPU from './cpu.js';
import * as Estado from './estado.js';
import * as Estadisticas from './estadisticas.js';
import * as Generadores from './generadores.js';
import * as Interfaz from './interfaz.js';
import * as Logica from './logica.js';
import * as Logros from './logros.js';
import * as Mejoras from './mejoras.js';
import * as Pasivas from './mejoras_pasivas.js';
import * as Multiplicadores from './multiplicadores.js';
import * as Perfil from './perfil.js';
import * as Prestigio from './prestigio.js';
import * as Puertas from './puertas.js';
import * as Renacimiento from './renacimiento.js';
import * as Servidor from './servidor.js';
import * as Utilidades from './utilidades.js';

// ==============================================
// ⚙️ INICIALIZACIÓN GENERAL
// ==============================================
export function iniciarSistema() {
  console.log("✅ Sistema iniciando...");

  // Cargar todos los datos guardados
  Estado.cargarEstado();
  Generadores.cargarGeneradores();
  Logros.cargarLogros();
  Perfil.cargarPerfil();
  Estadisticas.cargarStats();

  // Iniciar procesos automáticos
  Generadores.iniciar();
  setInterval(Pasivas.actualizar, 2000);
  setInterval(() => Logros.verificarLogros(CPU.obtenerSaldo()), 3000);
  setInterval(() => Puertas.verificarZonas(CPU.obtenerSaldo()), 4000);
  setInterval(Interfaz.actualizarTodo, 1000);

  console.log("✅ Sistema listo y funcionando");
}

// ==============================================
// 🎛️ FUNCIONES DE ACCESO GENERAL
// Para usarlas desde cualquier parte
// ==============================================
export const Sistema = {
  // Saldo y dinero
  getSaldo: CPU.obtenerSaldo,
  setSaldo: CPU.establecerSaldo,
  agregar: CPU.agregarSaldo,
  restar: CPU.restarSaldo,
  formatear: CPU.formatearSaldo,

  // Estado
  getEstado: Estado.cargarEstado,
  setEstado: Estado.modificarEstado,

  // Generadores
  agregarGenerador: Generadores.agregarGenerador,
  pausarGeneracion: Generadores.pausarGeneracion,

  // Mejoras
  comprarMejora: Mejoras.comprar,

  // Multiplicadores
  getMultiplicador: Multiplicadores.obtenerMultiplicadores,
  agregarBono: Multiplicadores.agregarMultiplicador,

  // Perfil / Admin
  verificarAdmin: Perfil.verificarAcceso,
  esAdmin: Estado.esAdministrador,

  // Prestigio / Renacimiento
  puedePrestigio: Prestigio.puedePrestigio,
  hacerPrestigio: Prestigio.hacerPrestigio,
  puedeRenacer: Renacimiento.puedeRenacer,
  hacerRenacer: Renacimiento.hacerRenacer,

  // Utilidades
  formato: Utilidades.formatoNumero,
  esperar: Utilidades.esperar
};

// Ejecutar automáticamente al cargar
iniciarSistema();
