"""
Módulo de utilidades generales
Funciones auxiliares para el sistema
"""

import os
import sys

def crear_estructura_carpetas():
    """Crea la estructura de carpetas del proyecto"""
    carpetas = ["data", "logs", "modules"]
    
    print("Creando estructura de carpetas...")
    for carpeta in carpetas:
        try:
            os.makedirs(carpeta, exist_ok=True)
            print(f"  ✓ Carpeta '{carpeta}' creada/verificada")
        except Exception as e:
            print(f"  ✗ Error al crear carpeta '{carpeta}': {e}")
    
    print("\nEstructura de carpetas verificada\n")

def limpiar_pantalla():
    """Limpia la pantalla de la consola"""
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_banner():
    """Muestra un banner del sistema"""
    banner = """
    ╔═══════════════════════════════════════════════════════════════╗
    ║        SISTEMA DE GESTIÓN DE PRODUCTOS - ABP3                 ║
    ║         Sistema Modular y Auditable en Python                 ║
    ║         Versión: 1.0 | Fecha: 2026                            ║
    ╚═══════════════════════════════════════════════════════════════╝
    
    """
    print(banner)

def validar_numero(texto, tipo="entero"):
    """Valida que el texto sea un número"""
    try:
        if tipo == "entero":
            valor = int(texto)
            return True, valor
        elif tipo == "decimal":
            valor = float(texto)
            return True, valor
        else:
            return False, None
    except ValueError:
        return False, None

def validar_fecha(fecha_str, formato="%Y-%m-%d"):
    """Valida que la fecha tenga el formato correcto"""
    from datetime import datetime
    try:
        datetime.strptime(fecha_str, formato)
        return True
    except ValueError:
        return False

def formatear_fecha(fecha_str, formato_original="%Y-%m-%d", formato_salida="%d/%m/%Y"):
    """Formatea una fecha string a formato legible"""
    from datetime import datetime
    try:
        fecha = datetime.strptime(fecha_str, formato_original)
        return fecha.strftime(formato_salida)
    except:
        return fecha_str

def pausa(mensaje="\nPresione Enter para continuar..."):
    """Pausa la ejecución hasta que el usuario presione Enter"""
    input(mensaje)

def mostrar_mensaje_exito(mensaje):
    """Muestra un mensaje de éxito formateado"""
    print(f"\n✓ {mensaje}")

def mostrar_mensaje_error(mensaje):
    """Muestra un mensaje de error formateado"""
    print(f"\n✗ ERROR: {mensaje}")

def mostrar_mensaje_alerta(mensaje):
    """Muestra un mensaje de alerta formateado"""
    print(f"\n⚠ {mensaje}")

def separador(longitud=50):
    """Muestra un separador en pantalla"""
    print("\n" + "=" * longitud)

def salir_sistema():
    """Sale del sistema de forma controlada"""
    print("\n" + "="*50)
    print("Saliendo del sistema...")
    print("¡Gracias por usar el Sistema de Gestión de Productos!")
    print("="*50)
    sys.exit(0)