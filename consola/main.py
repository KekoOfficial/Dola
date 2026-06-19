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

# 🔑 Contraseña de administrador definida
CONTRASEÑA_ADMIN = "111"

def menu_perfil(estado):
    """Menú de Perfil y acceso a Administrador"""
    while True:
        limpiar_pantalla()
        print("👤 PERFIL")
        print("=" * 30)
        print("1. Acceder como Administrador")
        print("2. Volver al menú principal")
        print("=" * 30)
        opcion = esperar_entrada(1)

        if opcion == "1":
            print("\n🔑 Ingresar contraseña de administrador:")
            clave = input("> ").strip()
            if clave == CONTRASEÑA_ADMIN:
                print("\n✅ Acceso concedido. Entrando al panel...")
                time.sleep(0.8)
                panel_administrador(estado)
            else:
                print("\n❌ Contraseña incorrecta.")
                esperar_entrada(2)
        elif opcion == "2":
            break
        else:
            print("\n⚠️ Opción no válida.")
            esperar_entrada(1)

def panel_administrador(estado):
    """Panel para modificar SOLO la cantidad de dinero"""
    while True:
        limpiar_pantalla()
        print("⚙️ PANEL DE ADMINISTRADOR")
        print("=" * 40)
        print(f"💵 Dinero actual: ${estado['dinero']:.2f}")
        print("-" * 40)
        print("1. Establecer nueva cantidad de dinero")
        print("2. Guardar y salir")
        print("=" * 40)
        opcion = esperar_entrada(1)

        if opcion == "1":
            print("\nEscriba la nueva cantidad (ej: 0, 1, 1000000):")
            try:
                monto = float(input("> "))
                if monto >= 0:
                    estado["dinero"] = round(monto, 2)
                    print(f"\n✅ Dinero actualizado a: ${estado['dinero']:.2f}")
                else:
                    print("\n⚠️ No se permite cantidad negativa.")
            except ValueError:
                print("\n❌ Ingrese un número válido.")
            esperar_entrada(2)

        elif opcion == "2":
            guardar_estado(estado)
            print("\n✅ Cambios guardados. Volviendo...")
            time.sleep(1)
            break

        else:
            print("\n⚠️ Opción no válida.")
            esperar_entrada(1)

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

        if opcion == "1":
            mejorar_cpu(estado)
        elif opcion == "2":
            comprar_multiplicador(estado)
        elif opcion == "3":
            comprar_generador(estado)
        elif opcion == "4":
            ver_puertas(estado)
        elif opcion == "5":
            abrir_puerta(estado)
        elif opcion == "6":
            menu_perfil(estado)  # 🆕 Nueva opción Perfil
        elif opcion == "7":
            guardar_estado(estado)
            print("\n💾 Guardado. ¡Hasta luego!")
            sys.exit(0)

if __name__ == "__main__":
    main()
