"""
Sistema de Gestión de Productos - ABP3
Módulo principal que coordina todos los componentes del sistema
"""

import os
import sys
from datetime import datetime
from modules import usuarios, productos, inventario, auditoria, utils

def mostrar_menu_principal():
    """Muestra el menú principal del sistema"""
    print("\n" + "="*50)
    print("SISTEMA DE GESTIÓN DE PRODUCTOS - ABP3")
    print("="*50)
    print("1. Iniciar sesión")
    print("2. Registrarse (Solo administrador)")
    print("3. Salir")
    print("="*50)

def mostrar_menu_usuario(rol):
    """Muestra el menú según el rol del usuario"""
    print(f"\n{'='*40}")
    print(f"Menú {rol}")
    print(f"{'='*40}")
    
    if rol == "Administrador":
        print("1. Gestionar usuarios")
        print("2. Ingresar mercancía")
        print("3. Gestionar pedidos")
        print("4. Ver inventario")
        print("5. Ver reportes")
        print("6. Ver logs de auditoría")
        print("7. Cerrar sesión")
    
    elif rol == "Supervisor":
        print("1. Revisar stock crítico")
        print("2. Ver productos por caducar")
        print("3. Ver inventario")
        print("4. Ver reportes")
        print("5. Cerrar sesión")
    
    elif rol == "Digitador":
        print("1. Ingresar mercancía")
        print("2. Marcar egresos")
        print("3. Ver inventario")
        print("4. Cerrar sesión")
    
    elif rol == "Bodeguero":
        print("1. Ordenar mercancía")
        print("2. Revisar stock")
        print("3. Recibir mercancía")
        print("4. Procesar pedidos")
        print("5. Cerrar sesión")
    
    elif rol == "Usuario":
        print("1. Consultar producto en bodega")
        print("2. Cerrar sesión")
    
    else:
        print("Rol no reconocido")
    
    print(f"{'='*40}")

def menu_usuario(usuario, rol):
    """Maneja el menú específico para cada rol de usuario"""
    while True:
        mostrar_menu_usuario(rol)
        opcion = input("\nSeleccione una opción: ").strip()
        
        # Lógica para Administrador
        if rol == "Administrador":
            if opcion == "1":
                usuarios.gestionar_usuarios()
                auditoria.registrar_log(usuario, "GESTION_USUARIOS", "Accedió a gestión de usuarios")
            elif opcion == "2":
                productos.ingresar_mercancia(usuario)
            elif opcion == "3":
                inventario.procesar_pedido(usuario)
            elif opcion == "4":
                inventario.mostrar_inventario()
            elif opcion == "5":
                inventario.mostrar_reportes()
            elif opcion == "6":
                auditoria.mostrar_logs()
            elif opcion == "7":
                print(f"\nCerrando sesión de {usuario}...")
                auditoria.registrar_log(usuario, "CIERRE_SESION", "Sesión finalizada desde menú")
                break
            else:
                print("Opción no válida")
        
        # Lógica para Supervisor
        elif rol == "Supervisor":
            if opcion == "1":
                inventario.mostrar_stock_critico()
            elif opcion == "2":
                inventario.mostrar_productos_por_vencer()
            elif opcion == "3":
                inventario.mostrar_inventario()
            elif opcion == "4":
                inventario.mostrar_reportes()
            elif opcion == "5":
                print(f"\nCerrando sesión de {usuario}...")
                auditoria.registrar_log(usuario, "CIERRE_SESION", "Sesión finalizada desde menú")
                break
            else:
                print("Opción no válida")
        
        # Lógica para Digitador
        elif rol == "Digitador":
            if opcion == "1":
                productos.ingresar_mercancia(usuario)
            elif opcion == "2":
                productos.marcar_egreso(usuario)
            elif opcion == "3":
                inventario.mostrar_inventario()
            elif opcion == "4":
                print(f"\nCerrando sesión de {usuario}...")
                auditoria.registrar_log(usuario, "CIERRE_SESION", "Sesión finalizada desde menú")
                break
            else:
                print("Opción no válida")
        
        # Lógica para Bodeguero
        elif rol == "Bodeguero":
            if opcion == "1":
                inventario.ordenar_mercancia()
            elif opcion == "2":
                inventario.revisar_stock()
            elif opcion == "3":
                productos.recibir_mercancia(usuario)
            elif opcion == "4":
                inventario.procesar_pedido(usuario)
            elif opcion == "5":
                print(f"\nCerrando sesión de {usuario}...")
                auditoria.registrar_log(usuario, "CIERRE_SESION", "Sesión finalizada desde menú")
                break
            else:
                print("Opción no válida")
        
        # Lógica para Usuario
        elif rol == "Usuario":
            if opcion == "1":
                productos.consultar_producto()
            elif opcion == "2":
                print(f"\nCerrando sesión de {usuario}...")
                auditoria.registrar_log(usuario, "CIERRE_SESION", "Sesión finalizada desde menú")
                break
            else:
                print("Opción no válida")
        
        else:
            print("Rol no reconocido")
            break

def main():
    """Función principal del sistema"""
    utils.crear_estructura_carpetas()
    utils.mostrar_banner()
    
    # Usuarios de prueba para validación
    usuarios.crear_usuarios_prueba()
    
    usuario_actual = None
    rol_actual = None
    
    while True:
        mostrar_menu_principal()
        opcion = input("\nSeleccione una opción: ").strip()
        
        if opcion == "1":  # Iniciar sesión
            usuario_actual, rol_actual = usuarios.iniciar_sesion()
            if usuario_actual:
                auditoria.registrar_log(usuario_actual, "INICIO_SESION", f"Sesión iniciada como {rol_actual}")
                menu_usuario(usuario_actual, rol_actual)
        
        elif opcion == "2":  # Registrarse
            if usuario_actual and rol_actual == "Administrador":
                usuarios.registrar_usuario()
            else:
                print("ERROR: Solo los administradores pueden registrar nuevos usuarios")
        
        elif opcion == "3":  # Salir
            print("\n¡Gracias por usar el sistema!")
            if usuario_actual:
                auditoria.registrar_log(usuario_actual, "CIERRE_SESION", "Sesión finalizada desde menú principal")
            sys.exit(0)
        
        else:
            print("Opción no válida. Intente nuevamente.")

if __name__ == "__main__":
    main()