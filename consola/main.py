import time
import sys
from core.estado import cargar_estado, guardar_estado
from core.tiempo import actualizar_ganancias
from core.interfaz import mostrar_menu_principal, limpiar_pantalla
from tienda.mejoras_cpu import mejorar_cpu
from tienda.multiplicadores import comprar_multiplicador
from tienda.generadores import comprar_generador
from puertas.logica_puertas import ver_puertas, abrir_puerta
from sistema.utilidades import esperar_entrada

def main():
    estado = cargar_estado()
    print("🎮 Juego: Multiplicadores de Dinero")
    print("⏳ Cargando...\n")
    time.sleep(1)

    while True:
        actualizar_ganancias(estado)
        limpiar_pantalla()
        mostrar_menu_principal(estado)
        opcion = esperar_entrada(1)
        if opcion == "1": mejorar_cpu(estado)
        elif opcion == "2": comprar_multiplicador(estado)
        elif opcion == "3": comprar_generador(estado)
        elif opcion == "4": ver_puertas(estado)
        elif opcion == "5": abrir_puerta(estado)
        elif opcion == "6":
            guardar_estado(estado)
            print("\n💾 Guardado. ¡Hasta luego!")
            sys.exit(0)

if __name__ == "__main__":
    main()
